
document.addEventListener('DOMContentLoaded', () => {
    // INFO SECTION
    password = document.querySelector('.password');
    let hidden = false;

    const passwordContent = password.innerHTML
    let dots = ''
    for (let i = 0; i < passwordContent.length; i++) {
        dots += '&bull;'
    }

    changeApperance()

    function changeApperance() {
        if (hidden === true) {
            password.innerHTML = passwordContent;
            hidden = false
        } else {
            password.innerHTML = dots
            hidden = true
        }
    }

    btn = document.getElementById('show')
    btn.onclick = () => {
        changeApperance()
        if (hidden === true) {
            btn.innerHTML = 'show password'
        } else {
            btn.innerHTML = 'hide password'
        }
    }

    // CHANGE INFO SECTION
    const changeUsernameBtn = document.getElementById('change-username')
    const changeUsernameForm = document.getElementById('change-username-form')

    const changePasswordBtn = document.getElementById('change-password')
    const changePasswordForm = document.getElementById('change-password-form')

    changeUsernameForm.style.display = 'none'
    changePasswordForm.style.display = 'none'

    const hideForms = document.getElementById('hide-forms')

    changeUsernameBtn.onclick = () => {
        changeUsernameForm.style.display = 'flex'
        changeUsernameBtn.setAttribute('hidden', '')
        hideForms.removeAttribute('hidden')
    }

    changePasswordBtn.onclick = () => {
        changePasswordForm.style.display = 'flex'
        changePasswordBtn.setAttribute('hidden', '')
        hideForms.removeAttribute('hidden')
    }

    hideForms.onclick = () => {
        hideForms.setAttribute('hidden', '')
        changeUsernameBtn.removeAttribute('hidden')
        changePasswordBtn.removeAttribute('hidden')
        changeUsernameForm.style.display = 'none'
        changePasswordForm.style.display = 'none'
    }

}, false);
