$(document).ready(function () {

    // Set datapicker
    $('#datepicker').datepicker({
        autoclose: true,
        format: "dd.mm.yyyy",
        weekStart: 1,
        immediateUpdates: true,
        todayBtn: true,
        todayBtn: "linked",
        todayHighlight: true
    }).datepicker("setDate", "0");

    // Autocomplete
    $('#query-main').autoComplete({
        resolverSettings: {
            url: '/autocomplete'
        }
    });
});




  