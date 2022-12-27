const loginForm = document.getElementById('login-form');
const email = document.getElementById('email');
const password = document.getElementById('password');

loginForm.addEventListener('submit', e => {
    e.preventDefault();
    validateInputsLogin(() => {
        e.target.submit();
    });
});

const userPasswordPromise = (email, password) => {
    return new Promise(function(resolve, reject) {
        axios.post("/validate-password", {
            email: email,
            password: password
        }).then(response => {
            resolve(response.data.user_password == "true");
        }).catch(error => {
            reject("Couldn't verify user password.");
        });
    });
}

const validateInputsLogin = (onValid) => {
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const userQueryPromise = userExistsPromise(emailValue);
    const userValidPassword = userPasswordPromise(emailValue, passwordValue)

    userQueryPromise.then((userExists) => {
        if (!userExists & emailValue != '') {
            setError(email, 'This user is not registered. Try to register instead.');
            return;
        }
        if(emailValue === '') {
            setError(email, 'Email is required');
        } else if (!isValidEmail(emailValue)) {
            setError(email, 'Provide a valid email address');
        } else {
            setSuccess(email);
        };
        
        userValidPassword.then((passwordIsOk) => {
            if (!passwordIsOk & passwordValue == "") {
                setError(password, 'Password is required');
            } else if (!passwordIsOk) {
                setError(password, "Password doesn't match");
            } else {
                setSuccess(password);
            }

            if (loginForm.querySelectorAll('.error:not(:empty)').length == 0) {
                onValid()
            };
        }).catch(message => {
            setError(password, message);
        });
    }).catch(message => {
        setError(email, message);
    });


};