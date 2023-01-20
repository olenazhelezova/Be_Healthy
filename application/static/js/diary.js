// Set datapicker
$('#datepicker').datepicker({
    autoclose: true,
    format: "dd.mm.yyyy",
    weekStart: 1,
    immediateUpdates: true,
    todayBtn: true,
    todayBtn: "linked",
    todayHighlight: true
    }).datepicker("setDate", diary_date);

const addMealButton = document.querySelectorAll(".add-meal-button");

const contentAddMealButton = `
        <div class="input-group mb-3 w-50 m-auto">
            <input autocomplete="off" autofocus class="input form-control text-center mx-auto autocomplete-food"
            placeholder="search for food" type="text"
            {% if query %}value="{{query}}"{% endif %}/>
            <button class="btn btn-success input-group-append" type="submit"><i class="fa fa-search"></i></button>
        </div>`
        
const contentTable = `
        <table class="table table-responsive table-hover text-nowrap text-success">
            <thead>
                <tr>
                    <th>Name</th><th>Serving size</th><th>Calories</th>
                </tr>
            </thead>
            <tbody>
                
            </tbody>
        </table>`;

const getDate = function() {
    let dateTime = $( "#datepicker" ).datepicker("getDate");
    var date = dateTime.getDate() + "." + (dateTime.getMonth()+1) + "." + dateTime.getFullYear();
    return date
}


$('#datepicker').datepicker()
.on('changeDate', function(e) {
    document.location.href = '/diary?date=' + getDate();
});

addMealButton.forEach(function(element) {
    element.addEventListener('click', () => {
        const targetMeal = element.parentElement;
        const classes = targetMeal.querySelector(".add-item").classList;
        const captionValue = targetMeal.querySelector(".caption");
        if (targetMeal.querySelectorAll(".food-search").length == 0) {
            captionValue.innerHTML = `Close`;
            const result = classes.replace("fa-plus", "fa-minus");
            classes.textContent = result ? classes : 'token not replaced successfully';
            let addFoodSearch = document.createElement("form");
            addFoodSearch.setAttribute("class", "food-search");
            addFoodSearch.setAttribute("method", "get");
            addFoodSearch.setAttribute("action", "/food-search-diary");
            addFoodSearch.innerHTML = contentAddMealButton;
            $(addFoodSearch.querySelector('.autocomplete-food')).autoComplete({
                resolverSettings: {
                    url: '/autocomplete'
                }
            });
            targetMeal.append(addFoodSearch);

            const submitButton = targetMeal.querySelector(".food-search");
            submitButton.addEventListener("submit", (e) => {
                e.preventDefault();
                if (targetMeal.querySelectorAll(".content-table").length != 0) {
                    targetMeal.querySelectorAll(".content-table")[0].remove();
                }
                let foodTable = document.createElement("div");
                foodTable.setAttribute("class", "content-table");
                foodTable.innerHTML = contentTable;
                targetMeal.append(foodTable);
                foodTable.hidden = true;

                const query = targetMeal.querySelector(".input").value.trim();

                axios.get("/food-search-diary?query=" + query
                ).then(response => {
                    const bodyTable = targetMeal.querySelector(".content-table tbody");
                    if (response.data.length == 0) {
                        targetMeal.querySelector(".input").value = "";
                        return ;
                    }
                    response.data.forEach((element, index) => {
                        foodTable.hidden = false;
                        const row = document.createElement("tr");
                        row.setAttribute("id", index);
                        row.innerHTML = `
                            <td class="food-name">${response.data[index]["name"]}</td>
                            <td class="serving-size">${response.data[index]["serving_size_g"]} g</td>
                            <td class="calories">${response.data[index]["calories"]}</td>
                            <td><button class="add-btn btn btn-outline-success m-0 p-0 px-1"><i class="fa fa-plus"></i></button></td>`;
                        bodyTable.append(row);

                        const addBtn = targetMeal.querySelectorAll(".add-btn");
                        addBtn.forEach(function(element) {
                            element.addEventListener("click", e => {
                                let index = element.parentNode.parentNode.id;
                                let data = response.data[index];
                                let date = getDate();
                                let meal = targetMeal.className;
                                axios.post("/add-food", {
                                    data: data,
                                    date: date,
                                    meal: meal
                                }).then(response => {
                                    if (response.data.food_added) {
                                        location.reload()
                                    }
                                }).catch(error => {
                                    $('#myModal').modal("show");
                                });
                            })});
                    })}).catch(error => {
                        $('#myModal').modal("show");
                    });

            });
        } else {
            const result = classes.replace("fa-minus", "fa-plus");
            captionValue.innerHTML = `Add item`;
            classes.textContent = result ? classes : 'token not replaced successfully';
            targetMeal.querySelector(".food-search").remove();
            if (targetMeal.querySelector(".content-table")) {
                targetMeal.querySelector(".content-table").remove();
            };
        };    
    })});
;






























// const date = document.getElementById("date").value.trim();
