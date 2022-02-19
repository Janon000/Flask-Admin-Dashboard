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

    //Get the repair id and show the related expense info
	$(document).on("click", ".edit_cost", function(){
	       event.preventDefault();

	       var repair_id = $(this).attr("data-id");
	       console.log(repair_id)
	       var t_num = $(this).attr("data-tn");

           $.ajax({
			data : {repair_id : repair_id, t_num : t_num},
			type : 'POST',
			url : '/get_expense'
		})
		.done(function(data) {
			if (data.error) {
			    alert('Error occurred with ajax post request');
			}
			else {
                $('#expense-table').html(data);
                $('#expense-table').append(data.htmlresponse);

			}
		});
      });

});