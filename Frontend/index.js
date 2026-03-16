const API = "http://localhost:8000"

let token = null


// ============================
// TOAST
// ============================

function showToast(message, type = "error") {

const toast = document.getElementById("toast")

toast.textContent = message
toast.classList.remove("hidden")

if (type === "error") {

toast.className = "fixed top-6 right-6 bg-red-600 px-6 py-3 rounded-lg shadow-lg text-white"

} else {

toast.className = "fixed top-6 right-6 bg-green-600 px-6 py-3 rounded-lg shadow-lg text-white"

}

setTimeout(() => {
toast.classList.add("hidden")
}, 3000)

}



// ============================
// LOGIN
// ============================

async function login() {

const btn = document.getElementById("login-btn")
const spinner = document.getElementById("login-spinner")
const text = document.getElementById("login-text")

const username = document.getElementById("username").value
const password = document.getElementById("password").value


spinner.classList.remove("hidden")
text.textContent = "Validando..."
btn.disabled = true


try {

const res = await fetch(API + "/auth/login", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({ username, password })

})

if (!res.ok) {

if (res.status === 401) {
showToast("Credenciales incorrectas")
}

else if (res.status === 429) {
showToast("Demasiados intentos. Intenta en 1 minuto.")
}

else {
showToast("Error en login")
}

spinner.classList.add("hidden")
text.textContent = "Login"
btn.disabled = false

return

}

const data = await res.json()

token = data.access_token

if (!token) {

showToast("Error de autenticación")

spinner.classList.add("hidden")
text.textContent = "Login"
btn.disabled = false

return

}

showToast("Login exitoso", "success")

initApp()

}

catch {

showToast("Error de conexión")

spinner.classList.add("hidden")
text.textContent = "Login"
btn.disabled = false

}

}



// ============================
// JWT
// ============================

function parseJwt(token) {

try {

const base64 = token.split('.')[1]
const json = atob(base64)

return JSON.parse(json)

}

catch {

return null

}

}



// ============================
// INIT APP
// ============================

function initApp() {

document.getElementById("login-section").style.display = "none"

document.getElementById("app").classList.remove("hidden")

const payload = parseJwt(token)

if (payload && payload.role === "admin") {

document
.getElementById("admin-panel")
.classList.remove("hidden")

}

loadHeroes()

}



// ============================
// CREATE HERO
// ============================

async function createHero() {

const hero = {

name: document.getElementById("name").value,
real_name: document.getElementById("real_name").value,
team: document.getElementById("team").value,
power_level: Number(document.getElementById("power_level").value),
image_url: document.getElementById("image_url").value

}

const res = await fetch(API + "/heroes", {

method: "POST",

headers: {
"Content-Type": "application/json",
"Authorization": "Bearer " + token
},

body: JSON.stringify(hero)

})

if (!res.ok) {
showToast("Error creando héroe")
return
}

showToast("Héroe creado", "success")

clearForm()

loadHeroes()

}



// ============================
// CLEAR FORM
// ============================

function clearForm() {

document.getElementById("name").value = ""
document.getElementById("real_name").value = ""
document.getElementById("team").value = ""
document.getElementById("power_level").value = ""
document.getElementById("image_url").value = ""

}



// ============================
// LOAD HEROES
// ============================

async function loadHeroes() {

const res = await fetch(API + "/heroes")

const heroes = await res.json()

const container = document.getElementById("heroes-container")

container.innerHTML = ""

heroes.forEach(hero => {

container.innerHTML += `

<div class="hero-card fade-in bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">

<img src="${hero.image_url}" 
class="w-full h-64 object-cover object-top">

<div class="p-4">

<h2 class="text-xl font-bold text-red-400">
${hero.name}
</h2>

<p class="text-gray-400 text-sm">
${hero.real_name}
</p>

<p class="text-gray-500 text-xs mt-1">
${hero.team}
</p>

</div>

</div>

`

})

}



// ============================
// SEARCH
// ============================

document.addEventListener("input", (e) => {

if (e.target.id === "search") {

const value = e.target.value.toLowerCase()

const cards = document.querySelectorAll(".hero-card")

cards.forEach(card => {

if (card.innerText.toLowerCase().includes(value)) {
card.style.display = "block"
} else {
card.style.display = "none"
}

})

}

})


// ocultar app al iniciar
document.getElementById("app").classList.add("hidden")