$(document).ready(function(){

    //Function to get data from route
    function notification(){
       $.ajax({
			type : 'POST',
			url : '/notification'
       })
       .done(function(data) {
            if (data != null){
                var count = 0;
                for(let i =0; i<data.length; i++){
                    if (data[i].read == 'No'){
                    count++;
                    }
                }
                if(count !=0){
                    $('.badge').html(count)
                }
            }
            if(data.length == 0){
                $('.dropdown-menu').html('<li><a class="see-all" href="/details">See all dates</a></li>')
            } else {
                for (let i = 0; i < data.length; i++){
                    $('.dropdown-menu').prepend('<li><a class="dropdown-item" href="#" data-id="'+data[i].id+'">'+data[i].notification+'</a></li>')
                }
                $('.dropdown-menu').append('<li><hr class="dropdown-divider"></li>')
                $('.dropdown-menu').append('<li><a class="see-all" href="/details">See all dates</a></li>')
            }
		});
    }

    window.onload = function() {
        notification();
    };


    $(document).on("click", "#dropdownMenuLink", function(){
        $('.badge').empty()
        arr = [];
        var id_list = document.querySelector(".dropdown-menu").querySelectorAll('.dropdown-item')
        for (var i=0; i<id_list.length; i++){
            arr.push(id_list[i].getAttribute('data-id'))
        }

        var ids = JSON.stringify(arr);

        $.ajax({
			type : 'POST',
			url : '/notification-read',
			data : {ids : ids}
       })
       .done(function(data) {
            console.log(data)
       });
    });




});