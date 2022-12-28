const registrationForm = document.getElementById('registration-form');
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password2 = document.getElementById('confirmation');

registrationForm.addEventListener('submit', e => {
    e.preventDefault();
    validateInputsRegistration(() => {
        e.target.submit();
    });
});

const validateInputsRegistration = (onValid) => {

    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const password2Value = password2.value.trim();
    const userQueryPromise = userExistsPromise(emailValue);

    userQueryPromise.then((userExists) => {
        if (userExists) {
            setError(email, 'Such user already exists. Try to login instead.');
            return ;
        }
        if(usernameValue === '') {
            setError(username, 'Username is required');
        } else {
            setSuccess(username);
        }
    
        if(emailValue === '') {
            setError(email, 'Email is required');
        } else if (!isValidEmail(emailValue)) {
            setError(email, 'Provide a valid email address');
        } else {
            setSuccess(email);
        }
    
        if(passwordValue === '') {
            setError(password, 'Password is required');
        } else if (!isValidPassword(passwordValue)) {
            setError(password, 'Password must be at least 8 characters, including one lowercase, one uppercase, digit and symbol.')
        } else {
            setSuccess(password);
        }
    
        if(password2Value === '') {
            setError(password2, 'Please confirm your password');
        } else if (password2Value !== passwordValue) {
            setError(password2, "Passwords doesn't match");
        } else if (!isValidPassword(password2Value)) {
            setError(password2, 'Password is invalid.')
        } else {
            setSuccess(password2);
        }

        //console.log((registrationForm.querySelectorAll('.error')));
        if (registrationForm.querySelectorAll('.error:not(:empty)').length == 0) {
            onValid();
        }
    }).catch(message => {
        setError(email, message);
    });

};
    