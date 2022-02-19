$(document).ready(function () {
     $(document).on("click", "#edit_pencil", function(){
        var $row = $(this).closest("tr");
        var t_num = $row.find(".t-numba").html();

        var Url = '/update/'+t_num

        $.ajax(Url)
            .done(function(data) {
            window.location.href =Url;
        })
     });
});