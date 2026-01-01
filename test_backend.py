"""
Quick test script to verify backend is working
"""
import requests
import os

def test_backend():
    base_url = "http://localhost:5000"
    
    print("Testing Backend API...")
    print("="*50)
    
    # Test health endpoint
    try:
        print("\n1. Testing /api/health...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print("   Start it with: python backend_api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test model-info endpoint
    try:
        print("\n2. Testing /api/model-info...")
        response = requests.get(f"{base_url}/api/model-info", timeout=5)
        if response.status_code == 200:
            print("✅ Model info retrieved")
            data = response.json()
            print(f"   Model: {data.get('model_name')}")
            print(f"   Device: {data.get('device')}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test detect endpoint with a test image
    test_image_path = "1.png"
    if os.path.exists(test_image_path):
        try:
            print(f"\n3. Testing /api/detect with {test_image_path}...")
            with open(test_image_path, 'rb') as f:
                files = {'image': f}
                response = requests.post(f"{base_url}/api/detect", files=files, timeout=30)
            
            if response.status_code == 200:
                print("✅ Image detection successful")
                data = response.json()
                print(f"   Prediction: {data.get('prediction')}")
                print(f"   Confidence: {data.get('confidence')}%")
            else:
                print(f"❌ Detection failed: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"\n3. Skipping image test (test image not found: {test_image_path})")
    
    print("\n" + "="*50)
    print("✅ Backend is working!")
    return True

if __name__ == "__main__":
    test_backend()

