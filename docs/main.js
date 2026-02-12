const API = "https://aid103-jyothi-ch-tech.onrender.com"

const fileEl = document.getElementById("file")
const previewEl = document.getElementById("preview")
const cropTypeEl = document.getElementById("cropType")
const locationEl = document.getElementById("location")
const btnPredict = document.getElementById("btnPredict")
const predictError = document.getElementById("predictError")
const resultEl = document.getElementById("result")
const userEmailEl = document.getElementById("userEmail")
const btnLogout = document.getElementById("btnLogout")
const recentResultsEl = document.getElementById("recentResults")

// Check authentication - STRICT CHECK
const email = localStorage.getItem("email")
const loggedIn = localStorage.getItem("loggedIn")
const token = localStorage.getItem("authToken")

// Must have ALL three to be logged in
if (!loggedIn || !email || !token) {
  localStorage.clear()
  window.location.href = "./login.html"
}

userEmailEl.textContent = email

btnLogout.onclick = () => {
  localStorage.clear()
  window.location.href = "./login.html"
}

function setPredictError(msg) {
  predictError.style.display = msg ? "block" : "none"
  predictError.textContent = msg || ""
}

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

btnPredict.onclick = async () => {
  setPredictError("")
  resultEl.textContent = ""

  const f = fileEl.files[0]
  if (!f) {
    setPredictError("Choose an image")
    return
  }

  btnPredict.disabled = true
  btnPredict.textContent = "Analyzing..."

  const fd = new FormData()
  fd.append("email", email)
  fd.append("crop_type", cropTypeEl.value.trim())
  fd.append("location", locationEl.value.trim())
  fd.append("image", f)

  try {
    const r = await fetch(API + "/predict", {
      method: "POST",
      body: fd
    })
    const j = await r.json()

    if (!r.ok) {
      setPredictError(j.error || "Error")
      btnPredict.disabled = false
      btnPredict.textContent = "Submit"
      return
    }

    resultEl.innerHTML = `
      <div class="section-card">
        <div class="section-title">${j.disease}</div>
        <div><strong>Confidence:</strong> ${j.confidence}%</div>
        <div><strong>Severity:</strong> ${j.severity}</div>
        <div style="margin-top:12px;">
          <div class="section-title" style="margin-bottom:6px;">Recommendation</div>
          <div class="muted">${j.recommendation}</div>
        </div>
        <div style="margin-top:12px;">
          <div class="section-title" style="margin-bottom:6px;">Explanation</div>
          <div class="muted">${j.explanation}</div>
        </div>
      </div>
    `

    // Add to recent results
    const recentHTML = `
      <div style="padding:12px;border:1px solid #e5e7eb;border-radius:8px;margin-bottom:8px;">
        <div><strong>${j.disease}</strong></div>
        <div class="muted" style="margin-top:4px;">${new Date().toLocaleString()}</div>
      </div>
    `
    recentResultsEl.innerHTML = recentHTML + recentResultsEl.innerHTML
    btnPredict.disabled = false
    btnPredict.textContent = "Submit"
  } catch (e) {
    setPredictError("Network error")
    btnPredict.disabled = false
    btnPredict.textContent = "Submit"
  }
}
