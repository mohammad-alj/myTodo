        
        password = document.querySelector('.password');
        let hidden = false;
        
        const password_content = password.innerHTML
        let dots = ''
        for (let i = 0; i < password_content.length; i++) {
            dots += '&bull;'
        }
        
        changeApperance()
        
        function changeApperance() {
            if (hidden === true) {
                password.innerHTML = password_content;
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