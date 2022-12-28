const bmiForm = document.getElementById("bmi-form");
const weight = document.getElementById("weight");
const height = document.getElementById("height");
const weightMs = document.getElementById("weight_ms");
const heightMs = document.getElementById("height_ms");

bmiForm.addEventListener('submit', e => {
    e.preventDefault();
    validateBmiForm(() => {
        e.target.submit();
    });
});

const validateBmiForm = (onValid) => {
    const weightValue = weight.value.trim();
    const heightValue = height.value.trim();
    const weightMsValue = weightMs.value.trim();
    const heightMsValue = heightMs.value.trim();

    if (weightValue === "") {
        setError(weight, "Please provide your weight.")
    } else if ((weightMsValue == "kg" & (weightValue < 40 || weightValue > 300)) || (weightMsValue == "lb" & (weightValue < 88 || weightValue > 661))) {
        setError(weight, "Please provide correct weight.")
    } else {
        setSuccess(weight)
    };

    if (heightValue === "") {
        setError(height, "Please provide your height.")
    } else if ((heightMsValue == "cm" & (heightValue < 140 || heightValue > 250)) || (heightMsValue == "in" & (heightValue < 55 || heightValue > 98))) {
        setError(height, "Please provide correct height.")
    } else {
        setSuccess(height)
    };

    if (bmiForm.querySelectorAll('.error:not(:empty)').length == 0) {
        onValid()
    }
};