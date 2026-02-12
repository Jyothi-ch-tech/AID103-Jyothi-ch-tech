const API = "https://aid103-jyothi-ch-tech-5.onrender.com"
const userEmailEl = document.getElementById("userEmail")
const btnLogout = document.getElementById("btnLogout")
const fileEl = document.getElementById("file")
const previewEl = document.getElementById("preview")
const cropTypeEl = document.getElementById("cropType")
const locationEl = document.getElementById("location")
const btnPredict = document.getElementById("btnPredict")
const predictError = document.getElementById("predictError")
const resultEl = document.getElementById("result")

// Check authentication
const email = localStorage.getItem("email")
const userName = localStorage.getItem("userName")

if (!email) {
    window.location.href = "index.html"
}

// Display user info
userEmailEl.textContent = userName || email

// Logout functionality
btnLogout.onclick = () => {
    localStorage.removeItem("email")
    localStorage.removeItem("userName")
    window.location.href = "index.html"
}

// File preview
fileEl.onchange = () => {
    const f = fileEl.files[0]
    if (!f) {
        previewEl.style.display = "none"
        return
    }
    const url = URL.createObjectURL(f)
    previewEl.src = url
    previewEl.style.display = "block"
}

// Prediction
function setPredictError(msg) {
    predictError.style.display = msg ? "block" : "none"
    predictError.textContent = msg || ""
}

btnPredict.onclick = async () => {
    setPredictError("")
    resultEl.textContent = ""

    const f = fileEl.files[0]
    if (!f) {
        setPredictError("Please choose an image")
        return
    }

    const fd = new FormData()
    fd.append("email", email)
    fd.append("crop_type", cropTypeEl.value.trim())
    fd.append("location", locationEl.value.trim())
    fd.append("image", f)

    // Show loading state
    btnPredict.disabled = true
    btnPredict.innerHTML = '<span>Analyzing...</span><span class="btn-icon">⏳</span>'

    try {
        const r = await fetch(API + "/api/predict", {
            method: "POST",
            body: fd
        })
        const j = await r.json()

        if (!r.ok) {
            setPredictError(j.error || "Error analyzing image")
            return
        }

        // Display results
        resultEl.innerHTML = `
            <div class="result-card">
                <div class="result-header">
                    <h3>Analysis Results</h3>
                </div>
                <div class="result-body">
                    <div class="result-item">
                        <span class="result-label">Disease Detected:</span>
                        <span class="result-value disease">${j.disease}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Confidence:</span>
                        <span class="result-value">${j.confidence}%</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Severity:</span>
                        <span class="result-value severity-${j.severity.toLowerCase()}">${j.severity}</span>
                    </div>
                    <div class="result-section">
                        <h4>💡 Recommendation</h4>
                        <p>${j.recommendation}</p>
                    </div>
                    <div class="result-section">
                        <h4>📋 Explanation</h4>
                        <p>${j.explanation}</p>
                    </div>
                </div>
            </div>
        `
    } catch (e) {
        setPredictError("Network error. Please check if the backend is running.")
    } finally {
        btnPredict.disabled = false
        btnPredict.innerHTML = '<span>Analyze Crop</span><span class="btn-icon">→</span>'
    }
}
