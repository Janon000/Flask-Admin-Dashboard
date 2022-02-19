$(document).ready(function(){

    //Handle csrf token during on post requests
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });

    // get the vehicle number and show status form info
   $(document).on("click", ".option_btn", function(){
        event.preventDefault();

        var t_num = $(this).closest("tr").find(".table-t-num").html();
        var page_name = $(this).attr("name");

		$.ajax({
			data : {t_num : t_num, page_name : page_name },
			type : 'POST',
			url : '/process_status'
		})
		.done(function(data) {
			if (data.error) {
			    alert('Error occurred with ajax post request');
			}
			else {
				$('.modal-body-update').html(data);
                $('.modal-body-update').replaceWith(data.htmlresponse);
			}
		});

		$('#park').attr('data-id', t_num);
		$('#active').attr('data-id', t_num);
		$('#garage').attr('data-id', t_num);

	});

    // get the status option and return the appropriate form
    $('.change-options').click(function(event){
        event.preventDefault();

        if($(this).attr('id')=='park'){
        var page_name = "PARKED"

        } else if ($(this).attr('id')=='active') {
        var page_name = "ACTIVE"

        }else if ($(this).attr('id')=='garage') {
        var page_name = "GARAGE"

        }

        var t_num = $(this).attr("data-id");
        var new_record = true;

		$.ajax({
			data : {t_num : t_num, page_name : page_name, new_record: new_record},
			type : 'POST',
			url : '/process_status'
		})
		.done(function(data) {
			if (data.error) {
			    alert('Error occurred with ajax post request');
			}
			else {
				$('.modal-body-update').html(data);
                $('.modal-body-update').replaceWith(data.htmlresponse);
                $('#page_name_hidden').attr('value',page_name);

			}
		});
	});

	 // get the vehicle number and show status form info
   $(document).on("click", ".history", function(){
        event.preventDefault();

        var t_num = $(this).closest("tr").find(".table-t-num").html();
        var page_name = $(this).attr("name");
        console.log(t_num)

		$.ajax({
			data : {t_num : t_num, page_name : page_name },
			type : 'POST',
			url : '/process_history'
		})
		.done(function(data) {
			if (data.error) {
			    alert('Error occurred with ajax post request');
			}
			else {

                $('.modal-body-history').html(data.htmlresponse);
			}
		});

    });





});