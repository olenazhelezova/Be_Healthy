const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const isValidEmail = email => {
    const re = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;
    return re.test(String(email).toLowerCase());
};

const isValidPassword = password => {
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,16}$/;
    return re.test(String(password));
};

const userExistsPromise = email => {
    return new Promise(function(resolve, reject) {
        axios.post("/validate-email", {
            email: email
        }).then(response => {
            resolve(response.data.user_exists == "true");
        }).catch(error => {
            reject("Couldn't verify email isn't already in use.");
        });
    });
};