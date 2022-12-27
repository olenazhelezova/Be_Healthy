const bmiForm = document.getElementById("bmi-form");
const weight = document.getElementById("weight");
const height = document.getElementById("height");

console.log(bmiForm);
console.log(weight);
console.log(height);

bmiForm.addEventListener('submit', e => {
    e.preventDefault();
    validateBmiForm(() => {
        e.target.submit();
    });
});

const validateBmiForm = (onValid) => {
    const weightValue = weight.value.trim();
    const heightValue = height.value.trim();

    if (weightValue === "") {
        setError(weight, "Please provide your weight.")
    } else if (weightValue <= 35) {
        setError(weight, "Please provide correct weight.")
    } else {
        setSuccess(weight)
    };

    if (heightValue === "") {
        setError(height, "Please provide your height.")
    } else if (heightValue <= 50) {
        setError(height, "Please provide correct height.")
    } else {
        setSuccess(height)
    };

    if (bmiForm.querySelectorAll('.error:not(:empty)').length == 0) {
        onValid()
    }
};