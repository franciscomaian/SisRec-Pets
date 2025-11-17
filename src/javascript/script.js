const abrir_modal = document.getElementById("abrir-modal")
const modal = document.getElementById("modal-info")
const fechar_modal = document.getElementById("fechar-modal")


abrir_modal.addEventListener("click", () => {
    modal.style.display = "flex"
})

fechar_modal.addEventListener("click", () => {
    modal.style.display = "none"
})