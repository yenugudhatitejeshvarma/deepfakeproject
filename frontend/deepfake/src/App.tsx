import { useState } from 'react'
import './App.css'

interface AnalysisResult {
  success: boolean
  prediction: string
  confidence: number
  probabilities: {
    fake: number
    real: number
  }
  model_info: {
    model_name: string
    model_type: string
    device: string
    framework: string
  }
  analysis: {
    image_size: [number, number]
    inference_time: number
    preprocessing_time: number
    total_time: number
    timestamp: string
  }
  interpretation: string
  visualization?: {
    available: boolean
    original_image?: string
    heatmap_overlay?: string
    visualization_time?: number
    message?: string
  }
  error?: string
}

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedImage(file)
      setResult(null)
      setError(null)
      
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select an image first')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('image', selectedImage)

      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
      const response = await fetch(`${apiUrl}/api/detect`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `Server error: ${response.status}`)
      }

      const data = await response.json()

      if (data.success !== false) {
        setResult(data)
        setError(null)
      } else {
        setError(data.error || 'Failed to analyze image')
      }
    } catch (err) {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
      const errorMessage = err instanceof Error 
        ? err.message 
        : `Failed to connect to server. Make sure the backend is running on ${apiUrl}`
      setError(errorMessage)
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setSelectedImage(null)
    setPreview(null)
    setResult(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Deepfake Detector</h1>
        <p>Upload an image to detect if it's real or a deepfake</p>
      </header>

      <main className="main-content">
        <div className="upload-section">
          <div className="upload-area">
            {!preview ? (
              <div className="upload-placeholder">
                <p className="upload-text">Drop an image here or click to browse</p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  className="file-input"
                  id="image-upload"
                />
                <label htmlFor="image-upload" className="upload-button">
                  Select Image
                </label>
              </div>
            ) : (
              <div className="image-preview">
                <img src={preview} alt="Preview" />
                <button onClick={handleClear} className="clear-button">
                  Clear
                </button>
              </div>
            )}
      </div>

          {selectedImage && (
            <div className="actions">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="analyze-button"
              >
                {loading ? 'Analyzing...' : 'Analyze Image'}
        </button>
            </div>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="results-section">
            <h2>Analysis Results</h2>
            
            <div className={`prediction-card ${result.prediction.toLowerCase()}`}>
              <div className="prediction-header">
                <span className="prediction-label">Prediction:</span>
                <span className="prediction-value">{result.prediction}</span>
              </div>
              <div className="confidence-bar">
                <div className="confidence-fill" style={{ width: `${result.confidence}%` }}></div>
                <span className="confidence-text">{result.confidence}% confidence</span>
              </div>
            </div>

            <div className="probabilities">
              <div className="prob-item fake">
                <span className="prob-label">Fake</span>
                <div className="prob-bar">
                  <div className="prob-fill fake" style={{ width: `${result.probabilities.fake}%` }}></div>
                </div>
                <span className="prob-value">{result.probabilities.fake}%</span>
              </div>
              <div className="prob-item real">
                <span className="prob-label">Real</span>
                <div className="prob-bar">
                  <div className="prob-fill real" style={{ width: `${result.probabilities.real}%` }}></div>
                </div>
                <span className="prob-value">{result.probabilities.real}%</span>
              </div>
            </div>

            <div className="interpretation">
              <h3>Interpretation</h3>
              <p>{result.interpretation}</p>
            </div>

            <div className="model-info">
              <h3>Model Information</h3>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Model:</span>
                  <span className="info-value">trainingmodel</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Type:</span>
                  <span className="info-value">{result.model_info.model_type}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Device:</span>
                  <span className="info-value">{result.model_info.device.toUpperCase()}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Framework:</span>
                  <span className="info-value">{result.model_info.framework}</span>
                </div>
              </div>
            </div>

            <div className="analysis-details">
              <h3>Analysis Details</h3>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Image Size:</span>
                  <span className="info-value">{result.analysis.image_size[0]} × {result.analysis.image_size[1]} px</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Inference Time:</span>
                  <span className="info-value">{result.analysis.inference_time} ms</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Preprocessing:</span>
                  <span className="info-value">{result.analysis.preprocessing_time} ms</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Total Time:</span>
                  <span className="info-value">{result.analysis.total_time} ms</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Timestamp:</span>
                  <span className="info-value">{new Date(result.analysis.timestamp).toLocaleString()}</span>
                </div>
              </div>
            </div>

            {result.visualization && result.visualization.available && (
              <div className="visualization-section">
                <h3>Forensic Analysis - Suspicious Regions</h3>
                <p className="visualization-description">
                  {result.prediction === "FAKE" 
                    ? "The model has detected manipulated regions in this image. Red patches indicate high-intensity fake regions, while yellow patches indicate medium-high intensity suspicious areas. These distinct color patches highlight exactly where manipulation was detected."
                    : "The model analyzed this image and found it to be authentic. The heatmap shows regions the model focused on during analysis using green color only, indicating normal attention patterns."}
                </p>
                <div className="visualization-grid">
                  <div className="visualization-item">
                    <h4>Original Image</h4>
                    {result.visualization.original_image && (
                      <img 
                        src={result.visualization.original_image} 
                        alt="Original" 
                        className="visualization-image"
                      />
                    )}
                  </div>
                  <div className="visualization-item">
                    <h4>
                      {result.prediction === "FAKE" 
                        ? "Detected Fake Regions (Red & Yellow Patches)" 
                        : "Authentic Regions (Green Only)"}
                    </h4>
                    {result.visualization.heatmap_overlay && (
                      <div className="heatmap-container">
                        <img 
                          src={result.visualization.heatmap_overlay} 
                          alt="Forensic Heatmap" 
                          className="visualization-image"
                        />
                        {result.prediction === "FAKE" && (
                          <div className="fake-regions-label">
                            Red patches = High manipulation | Yellow patches = Medium manipulation
                          </div>
                        )}
                        {result.prediction === "REAL" && (
                          <div className="real-regions-label">
                            Green indicates authentic regions analyzed by the model
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
                {result.visualization.visualization_time && (
                  <div className="visualization-time">
                    Forensic analysis generated in {result.visualization.visualization_time} ms
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Powered by SigLIP Deepfake Detection Model</p>
      </footer>
      </div>
  )
}

export default App
