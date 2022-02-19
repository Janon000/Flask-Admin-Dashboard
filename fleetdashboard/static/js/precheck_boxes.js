$(document).ready(function(){

    //execute after modal is shown
    $('#editcostModal').on('shown.bs.modal', function (e) {
       check_paid_boxes()
    });

    //Set checkbox value based on click
    $(document).on("click", ".paid_box", function(){
        if(this.checked) {
            $(this).val("Paid");
        }
        else {
            $(this).val("Unpaid");
        }
    });

    //function to check the checkboxes based on database value
    function check_paid_boxes(){
        setTimeout(function(){
            $('.paid_box').each(function(){
                if ($(this).val() == "Paid"){
                ($(this).prop('checked', true));
                }
            })
        }, 50);
    }

 });