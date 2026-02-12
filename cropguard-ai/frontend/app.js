const API = "http://127.0.0.1:5000"
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
const fileEl = document.getElementById("file")
const previewEl = document.getElementById("preview")
const cropTypeEl = document.getElementById("cropType")
const locationEl = document.getElementById("location")
const btnPredict = document.getElementById("btnPredict")
const predictError = document.getElementById("predictError")
const resultEl = document.getElementById("result")
function setMode(m){mode=m;btnLoginTab.classList.toggle("active",m==="login");btnRegisterTab.classList.toggle("active",m==="register");rowName.style.display=m==="register"?"block":"none"}
btnLoginTab.onclick=()=>setMode("login")
btnRegisterTab.onclick=()=>setMode("register")
function setStatus(text){statusEl.textContent=text}
function setAuthError(msg){authError.style.display=msg?"block":"none";authError.textContent=msg||""}
function setPredictError(msg){predictError.style.display=msg?"block":"none";predictError.textContent=msg||""}
btnAuth.onclick=async()=>{setAuthError("");const email=emailEl.value.trim();const password=passwordEl.value.trim();const name=nameEl.value.trim();if(!email||!password){setAuthError("Email and password required");return}try{const r=await fetch(API+"/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({mode,email,password,name})});const j=await r.json();if(!r.ok){setAuthError(j.error||"Error");return}localStorage.setItem("email",email);setStatus("Logged in as "+email)}catch(e){setAuthError("Network error")}}
fileEl.onchange=()=>{const f=fileEl.files[0];if(!f){previewEl.style.display="none";return}const url=URL.createObjectURL(f);previewEl.src=url;previewEl.style.display="block"}
btnPredict.onclick=async()=>{setPredictError("");resultEl.textContent="";const email=localStorage.getItem("email")||emailEl.value.trim();if(!email){setPredictError("Login first");return}const f=fileEl.files[0];if(!f){setPredictError("Choose an image");return}const fd=new FormData();fd.append("email",email);fd.append("crop_type",cropTypeEl.value.trim());fd.append("location",locationEl.value.trim());fd.append("image",f);try{const r=await fetch(API+"/predict",{method:"POST",body:fd});const j=await r.json();if(!r.ok){setPredictError(j.error||"Error");return}resultEl.innerHTML=`<div class="section-card"><div class="section-title">${j.disease}</div><div>Confidence: ${j.confidence}%</div><div>Severity: ${j.severity}</div><div style="margin-top:8px"><div class="section-title" style="margin-bottom:6px">Recommendation</div><div class="muted">${j.recommendation}</div></div><div style="margin-top:8px"><div class="section-title" style="margin-bottom:6px">Explanation</div><div class="muted">${j.explanation}</div></div></div>`}catch(e){setPredictError("Network error")}}
const initEmail=localStorage.getItem("email");if(initEmail){setStatus("Logged in as "+initEmail);emailEl.value=initEmail}
