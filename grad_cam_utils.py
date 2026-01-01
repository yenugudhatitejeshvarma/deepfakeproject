"""
Grad-CAM visualization utilities for SigLIP deepfake detection model.
Generates heatmaps highlighting manipulated regions in images.
"""
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import io
import base64

# Try to import cv2, fallback to PIL if not available
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Try to import matplotlib for colormap fallback
try:
    from matplotlib.cm import get_cmap
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GradCAM:
    """Grad-CAM implementation for SigLIP vision encoder."""
    
    def __init__(self, model, processor, device):
        """
        Initialize Grad-CAM.
        
        Args:
            model: The SiglipForImageClassification model
            processor: The AutoImageProcessor
            device: Device to run on ('cuda' or 'cpu')
        """
        self.model = model
        self.processor = processor
        self.device = device
        self.gradients = None
        self.activations = None
        
        # Register hooks to capture gradients and activations
        self._register_hooks()
    
    def _register_hooks(self):
        """Register forward and backward hooks on the vision encoder."""
        # SigLIP models have a vision_model attribute
        if hasattr(self.model, 'siglip'):
            vision_model = self.model.siglip.vision_model
        elif hasattr(self.model, 'vision_model'):
            vision_model = self.model.vision_model
        else:
            # Try to find the vision encoder in the model structure
            vision_model = None
            for name, module in self.model.named_modules():
                if 'vision' in name.lower() or 'encoder' in name.lower():
                    vision_model = module
                    break
        
        if vision_model is None:
            raise ValueError("Could not find vision encoder in model")
        
        # Find the last convolutional layer (usually in the encoder layers)
        self.target_layer = None
        for name, module in vision_model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                self.target_layer = module
                self.target_layer_name = name
        
        if self.target_layer is None:
            # Fallback: use the last encoder layer
            if hasattr(vision_model, 'encoder'):
                encoder = vision_model.encoder
                if hasattr(encoder, 'layers'):
                    self.target_layer = encoder.layers[-1]
                else:
                    self.target_layer = encoder
            else:
                self.target_layer = vision_model
        
        # Register hooks
        self.target_layer.register_forward_hook(self._forward_hook)
        self.target_layer.register_full_backward_hook(self._backward_hook)
    
    def _forward_hook(self, module, input, output):
        """Capture activations during forward pass."""
        self.activations = output
    
    def _backward_hook(self, module, grad_input, grad_output):
        """Capture gradients during backward pass."""
        self.gradients = grad_output[0]
    
    def generate_cam(self, input_image: Image.Image, target_class: Optional[int] = None, is_fake: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate Grad-CAM heatmap for the input image.
        
        Args:
            input_image: PIL Image to analyze
            target_class: Class index to generate CAM for (None = use predicted class)
            is_fake: Whether the image is detected as fake (True) or real (False)
        
        Returns:
            Tuple of (heatmap, overlay_image) as numpy arrays
        """
        # Preprocess image
        inputs = self.processor(images=input_image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Forward pass
        self.model.eval()
        self.gradients = None
        self.activations = None
        
        # Get prediction first
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)
        
        if target_class is None:
            target_class = torch.argmax(probs, dim=1).item()
        
        # Backward pass with gradients enabled
        self.model.zero_grad()
        inputs['pixel_values'].requires_grad = True
        
        outputs = self.model(**inputs)
        logits = outputs.logits
        
        # Backward pass for target class
        target = logits[0, target_class]
        target.backward()
        
        # Get gradients and activations
        if self.gradients is None or self.activations is None:
            # Fallback: use simpler attention method
            return self._generate_attention_fallback(input_image, target_class, is_fake=is_fake)
        
        # Process gradients and activations
        gradients = self.gradients[0].cpu().data.numpy()
        activations = self.activations[0].cpu().data.numpy()
        
        # Handle different activation shapes
        if len(activations.shape) == 4:  # [batch, channels, height, width]
            activations = activations[0]
        if len(gradients.shape) == 4:
            gradients = gradients[0]
        
        # Compute weights (global average pooling of gradients)
        if len(gradients.shape) == 3:  # [channels, height, width]
            weights = np.mean(gradients, axis=(1, 2), keepdims=True)
        else:
            weights = np.mean(gradients, axis=0, keepdims=True)
        
        # Generate CAM
        if len(activations.shape) == 3:  # [channels, height, width]
            cam = np.sum(weights * activations, axis=0)
        else:
            cam = np.sum(weights * activations, axis=0)
        
        cam = np.maximum(cam, 0)  # ReLU
        if cam.max() > 0:
            cam = cam / cam.max()  # Normalize
        
        # Apply threshold to only highlight significant regions (forensic approach)
        # Only show top 30% of attention values
        threshold = np.percentile(cam, 70)
        cam_thresholded = np.where(cam >= threshold, cam, 0)
        
        # Normalize thresholded CAM
        if cam_thresholded.max() > 0:
            cam_thresholded = cam_thresholded / cam_thresholded.max()
        else:
            cam_thresholded = cam
        
        # Resize thresholded CAM to original image size
        original_size = input_image.size
        
        if CV2_AVAILABLE:
            cam_resized = cv2.resize(cam_thresholded, original_size, interpolation=cv2.INTER_LINEAR)
            # For fake: red/yellow patches, For real: green only
            if is_fake:
                # Create patched red/yellow colormap (not smooth gradient)
                heatmap = self._apply_colormap_jet(cam_resized)
            else:
                # For real images, use only green color
                heatmap = self._apply_green_colormap(cam_resized)
                heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        else:
            # PIL fallback
            cam_pil = Image.fromarray((cam_thresholded * 255).astype(np.uint8))
            cam_resized = np.array(cam_pil.resize(original_size, Image.Resampling.LANCZOS)) / 255.0
            if is_fake:
                heatmap = self._apply_colormap_jet(cam_resized)
            else:
                heatmap = self._apply_green_colormap(cam_resized)
        
        # Overlay on original image with selective blending
        original_array = np.array(input_image)
        overlay = self._overlay_heatmap_forensic(original_array, heatmap, cam_resized, alpha=0.5)
        
        return heatmap, overlay
    
    def _apply_colormap_jet(self, cam: np.ndarray) -> np.ndarray:
        """
        Apply patched red/yellow colormap for fake regions.
        Creates distinct patches of red and yellow, not a smooth gradient.
        Matches the reference image style.
        
        Args:
            cam: CAM array (2D, normalized 0-1, already thresholded)
        
        Returns:
            Colormapped image (3D RGB array) - red and yellow patches
        """
        # Create distinct patches: red for high intensity, yellow for medium-high
        heatmap = np.zeros((cam.shape[0], cam.shape[1], 3), dtype=np.uint8)
        
        # More lenient thresholds to ensure patches are visible
        # High intensity (top 50%): RED patches
        if cam.max() > 0:
            red_threshold = np.percentile(cam[cam > 0], 50) if np.any(cam > 0) else cam.max() * 0.7
        else:
            red_threshold = 0.7
        
        # Medium-high intensity (20-50%): YELLOW patches
        if cam.max() > 0:
            yellow_threshold = np.percentile(cam[cam > 0], 20) if np.any(cam > 0) else cam.max() * 0.3
        else:
            yellow_threshold = 0.3
        
        # Ensure we have some patches even if thresholds are high
        if red_threshold > cam.max() * 0.9:
            red_threshold = cam.max() * 0.6
        if yellow_threshold > cam.max() * 0.8:
            yellow_threshold = cam.max() * 0.3
        
        # Create red patches (high intensity regions)
        red_mask = cam >= red_threshold
        heatmap[red_mask, 0] = 255  # Red channel
        heatmap[red_mask, 1] = 0    # Green channel
        heatmap[red_mask, 2] = 0    # Blue channel
        
        # Create yellow patches (medium-high intensity regions)
        yellow_mask = (cam >= yellow_threshold) & (cam < red_threshold) & (cam > 0)
        heatmap[yellow_mask, 0] = 255  # Red channel
        heatmap[yellow_mask, 1] = 255  # Green channel (red + green = yellow)
        heatmap[yellow_mask, 2] = 0    # Blue channel
        
        # If no patches found, create some based on top values
        if not np.any(red_mask) and not np.any(yellow_mask) and cam.max() > 0:
            # Use top 30% for red, next 20% for yellow
            sorted_values = np.sort(cam.flatten())
            if len(sorted_values) > 0:
                red_val = sorted_values[int(len(sorted_values) * 0.7)]
                yellow_val = sorted_values[int(len(sorted_values) * 0.5)]
                red_mask = cam >= red_val
                yellow_mask = (cam >= yellow_val) & (cam < red_val)
                heatmap[red_mask, 0] = 255
                heatmap[red_mask, 1] = 0
                heatmap[red_mask, 2] = 0
                heatmap[yellow_mask, 0] = 255
                heatmap[yellow_mask, 1] = 255
                heatmap[yellow_mask, 2] = 0
        
        return heatmap
    
    def _apply_green_colormap(self, cam: np.ndarray) -> np.ndarray:
        """
        Apply green-only colormap for real/authentic images.
        
        Args:
            cam: CAM array (2D, normalized 0-1, already thresholded)
        
        Returns:
            Colormapped image (3D RGB array) - green gradient only
        """
        # Normalize to 0-255
        cam_uint8 = np.uint8(255 * cam)
        
        # Create green-only heatmap
        heatmap = np.zeros((cam.shape[0], cam.shape[1], 3), dtype=np.uint8)
        
        # Green channel: full intensity based on CAM value
        heatmap[:, :, 1] = cam_uint8  # Green channel
        # Red and Blue channels remain 0
        
        return heatmap
    
    def _overlay_heatmap_forensic(self, original: np.ndarray, heatmap: np.ndarray, cam_mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """
        Overlay heatmap on original image with selective blending.
        Only overlays where CAM values are significant (forensic approach).
        
        Args:
            original: Original image as numpy array
            heatmap: Heatmap as numpy array (red/yellow)
            cam_mask: CAM mask (2D array, 0-1) indicating significant regions
            alpha: Transparency factor for heatmap
        
        Returns:
            Overlayed image as numpy array
        """
        # Ensure same size
        if original.shape[:2] != heatmap.shape[:2]:
            if CV2_AVAILABLE:
                heatmap = cv2.resize(heatmap, (original.shape[1], original.shape[0]))
            else:
                heatmap_pil = Image.fromarray(heatmap)
                heatmap_pil = heatmap_pil.resize((original.shape[1], original.shape[0]), Image.Resampling.LANCZOS)
                heatmap = np.array(heatmap_pil)
        
        # Resize cam_mask to match image size
        if original.shape[:2] != cam_mask.shape[:2]:
            if CV2_AVAILABLE:
                cam_mask = cv2.resize(cam_mask, (original.shape[1], original.shape[0]), interpolation=cv2.INTER_LINEAR)
            else:
                cam_mask_pil = Image.fromarray((cam_mask * 255).astype(np.uint8))
                cam_mask_pil = cam_mask_pil.resize((original.shape[1], original.shape[0]), Image.Resampling.LANCZOS)
                cam_mask = np.array(cam_mask_pil) / 255.0
        
        # Create 3D mask from 2D CAM mask
        if len(cam_mask.shape) == 2:
            cam_mask_3d = np.stack([cam_mask, cam_mask, cam_mask], axis=2)
        else:
            cam_mask_3d = cam_mask
        
        # Selective blending: only overlay where CAM values are significant
        # Use the mask to control where heatmap is applied
        overlay = original.astype(np.float32) * (1 - cam_mask_3d * alpha) + heatmap.astype(np.float32) * (cam_mask_3d * alpha)
        overlay = np.clip(overlay, 0, 255).astype(np.uint8)
        
        return overlay
    
    def _overlay_heatmap(self, original: np.ndarray, heatmap: np.ndarray, alpha: float = 0.4) -> np.ndarray:
        """
        Overlay heatmap on original image (fallback method).
        
        Args:
            original: Original image as numpy array
            heatmap: Heatmap as numpy array
            alpha: Transparency factor for heatmap
        
        Returns:
            Overlayed image as numpy array
        """
        # Ensure same size
        if original.shape[:2] != heatmap.shape[:2]:
            if CV2_AVAILABLE:
                heatmap = cv2.resize(heatmap, (original.shape[1], original.shape[0]))
            else:
                heatmap_pil = Image.fromarray(heatmap)
                heatmap_pil = heatmap_pil.resize((original.shape[1], original.shape[0]), Image.Resampling.LANCZOS)
                heatmap = np.array(heatmap_pil)
        
        # Blend images
        if CV2_AVAILABLE:
            overlay = cv2.addWeighted(original, 1 - alpha, heatmap, alpha, 0)
        else:
            overlay = (original.astype(np.float32) * (1 - alpha) + heatmap.astype(np.float32) * alpha).astype(np.uint8)
        return overlay
    
    def _generate_attention_fallback(self, input_image: Image.Image, target_class: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fallback method using model attention weights if Grad-CAM fails.
        """
        # Simple attention visualization based on model features
        inputs = self.processor(images=input_image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            # Get intermediate features
            if hasattr(self.model, 'siglip'):
                vision_outputs = self.model.siglip.vision_model(**inputs)
            elif hasattr(self.model, 'vision_model'):
                vision_outputs = self.model.vision_model(**inputs)
            else:
                # Use a simpler approach: create a uniform attention map
                original_size = input_image.size
                attention_map = np.ones((original_size[1], original_size[0])) * 0.5
                if CV2_AVAILABLE:
                    heatmap = cv2.applyColorMap(np.uint8(255 * attention_map), cv2.COLORMAP_HOT)
                    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
                else:
                    heatmap = self._apply_colormap_forensic(attention_map)
                original_array = np.array(input_image)
                overlay = self._overlay_heatmap_forensic(original_array, heatmap, attention_map, alpha=0.3)
                return heatmap, overlay
            
            # Extract features from last hidden state
            if hasattr(vision_outputs, 'last_hidden_state'):
                features = vision_outputs.last_hidden_state
            elif hasattr(vision_outputs, 'pooler_output'):
                features = vision_outputs.pooler_output
            else:
                features = vision_outputs[0] if isinstance(vision_outputs, tuple) else vision_outputs
            
            # Compute attention weights (simplified)
            if len(features.shape) == 3:  # [batch, seq_len, hidden_dim]
                # Average over sequence dimension
                attention_weights = torch.mean(torch.abs(features), dim=-1).squeeze().cpu().numpy()
            else:
                attention_weights = torch.mean(torch.abs(features), dim=-1).squeeze().cpu().numpy()
        
        # Reshape to spatial dimensions (approximate)
        original_size = input_image.size
        if len(attention_weights.shape) == 1:
            # Reshape to approximate spatial dimensions
            seq_len = attention_weights.shape[0]
            # Assume square patches (common in vision transformers)
            patch_size = int(np.sqrt(seq_len))
            if patch_size * patch_size == seq_len:
                attention_2d = attention_weights.reshape(patch_size, patch_size)
            else:
                # Fallback to uniform
                attention_2d = np.ones((original_size[1] // 16, original_size[0] // 16)) * 0.5
        else:
            attention_2d = attention_weights
        
        # Resize to original image size
        if CV2_AVAILABLE:
            attention_2d = cv2.resize(attention_2d, original_size, interpolation=cv2.INTER_LINEAR)
        else:
            attention_pil = Image.fromarray((attention_2d * 255).astype(np.uint8))
            attention_pil = attention_pil.resize(original_size, Image.Resampling.LANCZOS)
            attention_2d = np.array(attention_pil) / 255.0
        
        attention_2d = (attention_2d - attention_2d.min()) / (attention_2d.max() - attention_2d.min() + 1e-8)
        
        # Apply threshold for forensic visualization
        threshold = np.percentile(attention_2d, 70)
        attention_thresholded = np.where(attention_2d >= threshold, attention_2d, 0)
        if attention_thresholded.max() > 0:
            attention_thresholded = attention_thresholded / attention_thresholded.max()
        else:
            attention_thresholded = attention_2d
        
        # Convert to heatmap: JET for fake, GREEN for real
        if CV2_AVAILABLE:
            if is_fake:
                heatmap = cv2.applyColorMap(np.uint8(255 * attention_thresholded), cv2.COLORMAP_JET)
            else:
                heatmap = self._apply_green_colormap(attention_thresholded)
            heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        else:
            if is_fake:
                heatmap = self._apply_colormap_jet(attention_thresholded)
            else:
                heatmap = self._apply_green_colormap(attention_thresholded)
        
        # Overlay on original image
        original_array = np.array(input_image)
        overlay = self._overlay_heatmap(original_array, heatmap, alpha=0.4)
        
        return heatmap, overlay
    
    def image_to_base64(self, image_array: np.ndarray) -> str:
        """
        Convert numpy image array to base64 encoded string.
        
        Args:
            image_array: Image as numpy array (RGB)
        
        Returns:
            Base64 encoded string
        """
        # Convert to PIL Image
        if image_array.dtype != np.uint8:
            image_array = (image_array * 255).astype(np.uint8)
        
        pil_image = Image.fromarray(image_array)
        
        # Convert to base64
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return img_str


def generate_gradcam_visualization(
    model, 
    processor, 
    device, 
    image: Image.Image, 
    target_class: Optional[int] = None
) -> Tuple[str, str]:
    """
    Generate Grad-CAM visualization for an image.
    
    Args:
        model: The SiglipForImageClassification model
        processor: The AutoImageProcessor
        device: Device to run on
        image: PIL Image to analyze
        target_class: Class index (None = use predicted class)
    
    Returns:
        Tuple of (original_image_base64, heatmap_overlay_base64)
    """
    try:
        # Initialize Grad-CAM
        gradcam = GradCAM(model, processor, device)
        
        # Generate heatmap and overlay
        heatmap, overlay = gradcam.generate_cam(image, target_class)
        
        # Convert original image to base64
        original_base64 = gradcam.image_to_base64(np.array(image))
        
        # Convert overlay to base64
        overlay_base64 = gradcam.image_to_base64(overlay)
        
        return original_base64, overlay_base64
    
    except Exception as e:
        print(f"[WARNING] Grad-CAM visualization failed: {e}")
        import traceback
        traceback.print_exc()
        print("Falling back to returning original image only...")
        
        # Fallback: return original image twice
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return img_str, img_str
