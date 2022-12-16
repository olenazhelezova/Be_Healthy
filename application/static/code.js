$(document).ready(function () {
    $('#datepicker').datepicker({
        autoclose: true,
        format: "dd.mm.yyyy",
        weekStart: 1,
        immediateUpdates: true,
        todayBtn: true,
        todayBtn: "linked",
        todayHighlight: true
    }).datepicker("setDate", "0");

    $('#query-main').autoComplete({
        resolverSettings: {
            url: '/autocomplete'
        }
    });

    // const input = document.querySelector('#query-main');
    // input.addEventListener('keyup', function(event) {
    //     let results = "";
    //     if (this.value) {
    //         const req = new XMLHttpRequest();
    //         req.open("GET", '/autocomplete');
    //         req.send();
    //         req.onerror = function() { console.log('This shit is broken!'); }
    //         req.onloadend = function() { 
    //             const response = JSON.parse(req.responseText);
    //             for (const option of response) {
    //                 if (option.startsWith(input.value)) {
    //                     results +=`<li>${option}</li>`;
    //                 }
    //             }
    //             document.querySelector('footer').innerHTML = results;
    //         } 
    //     }
    // });
});


  