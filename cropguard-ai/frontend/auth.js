const API = "https://aid103-jyothi-ch-tech-5.onrender.com"
let mode = "login"
const btnLoginTab = document.getElementById("btnLoginTab")
const btnRegisterTab = document.getElementById("btnRegisterTab")
const rowName = document.getElementById("rowName")
const nameEl = document.getElementById("name")
const emailEl = document.getElementById("email")
const passwordEl = document.getElementById("password")
const authError = document.getElementById("authError")
const btnAuth = document.getElementById("btnAuth")

function setMode(m) {
    mode = m
    btnLoginTab.classList.toggle("active", m === "login")
    btnRegisterTab.classList.toggle("active", m === "register")
    rowName.style.display = m === "register" ? "block" : "none"
    btnAuth.textContent = m === "login" ? "Login" : "Register"
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
        setAuthError("Name is required for registration")
        return
    }

    try {
        const r = await fetch(API + "/api/user/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mode, email, password, name })
        })
        const j = await r.json()

        if (!r.ok) {
            setAuthError(j.error || "Error")
            return
        }

        // Store user info and redirect to dashboard
        localStorage.setItem("email", email)
        localStorage.setItem("userName", name || email.split("@")[0])
        window.location.href = "dashboard.html"
    } catch (e) {
        setAuthError("Network error. Please check if the backend is running.")
    }
}

// Check if already logged in
const existingEmail = localStorage.getItem("email")
if (existingEmail) {
    window.location.href = "dashboard.html"
}
