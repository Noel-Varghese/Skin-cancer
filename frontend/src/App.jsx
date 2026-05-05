import { useState } from 'react'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    setSelectedFile(file)
    setPreview(URL.createObjectURL(file))
    setResult(null)
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return
    setLoading(true)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      // Send the file to your local FastAPI PyTorch server
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData,
      })
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error("Error communicating with AI engine:", error)
      setResult({ diagnosis: "Connection Error", confidence: 0 })
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 flex flex-col items-center justify-center font-sans">
      <div className="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl p-8 border border-gray-700">
        <h1 className="text-3xl font-bold mb-2 text-blue-400">DermAI Scanner</h1>
        <p className="text-gray-400 mb-8 text-sm">Local GPU-Accelerated Diagnosis</p>

        {/* Upload Area */}
        <div className="mb-6">
          <label className="flex flex-col items-center px-4 py-6 bg-gray-700 text-blue-400 rounded-lg shadow-lg tracking-wide uppercase border border-blue-400 cursor-pointer hover:bg-blue-500 hover:text-white transition duration-300">
            <span className="mt-2 text-base leading-normal">Select Image or Video</span>
            <input type='file' className="hidden" onChange={handleFileChange} accept="image/*,video/*,.gif" />
          </label>
        </div>

        {/* Preview */}
        {preview && (
          <div className="mb-6 flex justify-center">
            <img src={preview} alt="Preview" className="max-h-48 rounded shadow-md border border-gray-600 object-contain" />
          </div>
        )}

        {/* Action Button */}
        <button 
          onClick={handleAnalyze} 
          disabled={!selectedFile || loading}
          className={`w-full font-bold py-3 px-4 rounded ${loading ? 'bg-gray-600 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'} transition duration-300`}
        >
          {loading ? 'Analyzing on RTX 4050...' : 'Run Analysis'}
        </button>

        {/* Results */}
        {result && (
          <div className="mt-8 p-4 bg-gray-900 rounded-lg border border-gray-700 text-center">
            <h2 className="text-sm text-gray-400 uppercase tracking-wider mb-1">Diagnosis</h2>
            <p className={`text-2xl font-bold ${result.diagnosis.includes('DANGER') ? 'text-red-500' : 'text-green-400'}`}>
              {result.diagnosis}
            </p>
            <div className="mt-4 bg-gray-800 rounded-full h-2.5 overflow-hidden">
              <div className="bg-blue-500 h-2.5 rounded-full transition-all duration-1000 ease-out" style={{ width: `${result.confidence}%` }}></div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Confidence: {parseFloat(result.confidence).toFixed(2)}%</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App