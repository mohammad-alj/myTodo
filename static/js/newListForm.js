document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('create-list-btn')
    const formContainer = document.getElementById('list-form-container')
    const hideForm = document.getElementById('hide-form-btn')
    formContainer.style.display = 'none'
    btn.onclick = () => {
        formContainer.style.display = 'flex'
    }
    hideForm.onclick = () => formContainer.style.display = 'none'
}, false);
