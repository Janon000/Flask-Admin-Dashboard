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

    // Sumbit new row on add button click
    $(document).on("click", ".add-cost", function(){
        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');
        var $row = $(this).closest("tr");

        input.each(function(){
            if(!$(this).val()){
                $(this).addClass("input-error");
                empty = true;
            } else{
                $(this).removeClass("input-error");
            }
        });

        var id = $row.find(".id_hidden").val();
        var repair_id = $row.find(".repair_id_hidden").val();
        var description = $row.find(".cost_description").val();
        var amount = $row.find(".cost_amount").val();
        var paid = $row.find(".paid_box").val();
        var t_num = $row.find(".t_num_hidden").val();
        console.log(t_num)


        $.post("/add_expense", { id: id, repair_id: repair_id, description: description, amount: amount, paid: paid, t_num: t_num}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show().fadeOut(5000);

        });

        $(this).parents("tr").find(".error").first().focus();
        if(!empty){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });
            $(this).closest("tr").find(".add-cost, .edit-cost, .delete-cost").toggle();
            $(".add-cost-btn").removeAttr("disabled");
            $row.find(".paid_box").attr("disabled","disabled");
        }
    });

    // Delete row on delete button click
    $(document).on("click", ".delete-cost", function(){
        var $row = $(this).closest("tr");
        var id = $row.find("td").eq(0).html();

        $row.remove();
        $(".add-new").removeAttr("disabled");

        $.post("/delete_expense", {id: id}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show().fadeOut(5000);
        });
    });



    // Edit row on edit button click
    $(document).on("click", ".edit-cost", function(){
        var $row = $(this).closest("tr");
        $row.find("td:not(:last-child)").each(function(i){
            if (i=='0'){
                $(this).replaceWith('<td style="display:none;"><input type="hidden" class="id_hidden" value="' + $(this).text() + '"></td>');
            }else if (i=='1'){
                $(this).replaceWith('<td style="display:none;"><input type="hidden" class="repair_id_hidden" value="' + $(this).text() + '"></td>');
            }else if (i=='2'){
                $(this).replaceWith('<td style="display:none;"><input type="hidden" class="t_num_hidden" value="' + $(this).text() + '"></td>');
            }else if (i=='3'){
                $(this).replaceWith('<td><input type="text" name="cost-description" class="cost_description" value="' + $(this).text() + '"></td>');
            }else if (i=='4'){
                $(this).replaceWith('<td><input type="text" name="cost-amount" class="cost_amount" value="' + $(this).text() + '"></td>');
            }else if (i=='5'){
                if ($row.find(".paid_box").val()=="Paid"){
                $(this).replaceWith('<td><input class="paid_box" type="checkbox" name="paid_box" value="' + $row.find(".paid_box").val() + '"></td>');
                $row.find(".paid_box").prop('checked', true);
                }else{$(this).replaceWith('<td><input class="paid_box" type="checkbox" name="paid_box" value="' + $row.find(".paid_box").val() + '"></td>');}
            }else{}
        });

        $row.find(".add-cost, .edit-cost").toggle();
        $("#cost-cancel").toggle();
        $(".add-cost-btn").attr("disabled", "disabled");
        $row.find(".add-cost").removeClass("add-cost").addClass("update-cost");
    });


    // update record row on add button click
    $(document).on("click", ".update-cost", function(){
        var empty = false;
        var $row = $(this).closest("tr");
        var input = $(this).parents("tr").find('input[type="text"]');

        input.each(function(){
            if(!$(this).val()){
                $("#displaymessage").html("Please fill all fields");

                $(this).addClass("input-error");

                empty = true;
            } else{
                $(this).removeClass("input-error");

            }
        });

        var id = $row.find(".id_hidden").val();
        var repair_id = $row.find(".repair_id_hidden").val();
        var description = $row.find(".cost_description").val();
        var amount = $row.find(".cost_amount").val();
        var paid = $row.find(".paid_box").val();

        $.post("/update_expense", { id: id, repair_id: repair_id, description: description, amount: amount, paid: paid}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show().fadeOut(5000);
        });

        $(this).parents("tr").find(".input-error").first().focus();
        if(!empty){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });
            $row.find(".update-cost").removeClass("update-cost").addClass("add-cost");
            $(this).closest("tr").find(".add-cost, .edit-cost").toggle();
            $(".add-cost-btn").removeAttr("disabled");
            $row.find(".paid_box").attr("disabled","disabled");
        }

    });


});