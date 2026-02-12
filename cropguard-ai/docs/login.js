const API = "https://aid103-jyothi-ch-tech.onrender.com"
let mode = "login"

const btnLoginTab = document.getElementById("btnLoginTab")
const btnRegisterTab = document.getElementById("btnRegisterTab")
const rowName = document.getElementById("rowName")
const nameEl = document.getElementById("name")
const emailEl = document.getElementById("email")
const passwordEl = document.getElementById("password")
const authError = document.getElementById("authError")
const btnAuth = document.getElementById("btnAuth")
const statusEl = document.getElementById("status")

function setMode(m) {
  mode = m
  btnLoginTab.classList.toggle("active", m === "login")
  btnRegisterTab.classList.toggle("active", m === "register")
  rowName.style.display = m === "register" ? "block" : "none"
  authError.style.display = "none"
}

btnLoginTab.onclick = () => setMode("login")
btnRegisterTab.onclick = () => setMode("register")

function setAuthError(msg) {
  authError.style.display = msg ? "block" : "none"
  authError.textContent = msg || ""
}

btnAuth.onclick = async () => {
  setAuthError("")
  const email = emailEl.value.trim()
  const password = passwordEl.value.trim()
  const name = nameEl.value.trim()

  if (!email || !password) {
    setAuthError("Email and password required")
    return
  }

  if (mode === "register" && !name) {
    setAuthError("Name required for registration")
    return
  }

  btnAuth.disabled = true
  btnAuth.textContent = "Loading..."

  try {
    const r = await fetch(API + "/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, email, password, name })
    })
    const j = await r.json()

    if (!r.ok) {
      setAuthError(j.error || "Error")
      btnAuth.disabled = false
      btnAuth.textContent = "Submit"
      return
    }

    localStorage.setItem("email", email)
    localStorage.setItem("loggedIn", "true")
    localStorage.setItem("authToken", j.token || "verified_" + Date.now())
    window.location.href = "./main.html"
  } catch (e) {
    setAuthError("Network error")
    btnAuth.disabled = false
    btnAuth.textContent = "Submit"
  }
}

// Check if already logged in
if (localStorage.getItem("loggedIn") && localStorage.getItem("email") && localStorage.getItem("authToken")) {
  window.location.href = "./main.html"
}
