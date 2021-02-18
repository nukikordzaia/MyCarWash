document.addEventListener('DOMContentLoaded', function () {
    var sideNav = M.Sidenav.init(document.querySelectorAll('.sidenav'), {});
    var collapsible = M.Collapsible.init(document.querySelectorAll('.collapsible'), {});
    var formSelect = M.FormSelect.init(document.querySelectorAll('select'), {});
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
});
