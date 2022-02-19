$(document).ready(function(){



    $(document).on("click", ".add-cost-btn", function(){
        var new_id = getlastID()+1;
        console.log(new_id);
        $(this).attr("disabled", "disabled");
        var repair_id = $(this).attr("data-id");
        var t_num = $(this).attr("data-tn");
        var index = $("#expense-table").find("tr").last().index();
        var rowCount = $('.expense-table tr').length;
        $(".cost-body").append(addNewRow(repair_id,new_id,t_num));
        $(".expense-table tr").eq(rowCount).find(".add-cost, .edit-cost, .delete-cost").toggle();

    });

    function getlastID(){
        var id =0;

        $.ajax({
            'url':'/add_expense',
            'type':'GET',
            'async':false,
            'success':function(data){
                         id = data;
             }
       });

       return id;
    }

    function addNewRow(repair_id, new_id, t_num){
        var tr = '<tr>'+
                '<td style="display:none;"><input type="text" class="id_hidden" value="'+new_id+'"</td>'+
                '<td style="display:none;"><input type="text" class="repair_id_hidden" value="'+repair_id+'"></td>'+
                '<td style="display:none;"><input type="text" class="t_num_hidden" value="'+t_num+'"></td>'+
                '<td><input type="text" name="cost-description" class="cost_description"></td>'+
                '<td><input type="text" name="cost-amount" class="cost_amount"></td>'+
                '<td><input class="paid_box" type="checkbox" value="Unpaid" name="paid_box"></td>'+
                '<td>'+
                '<a class="add-cost"><i class="fas fa-plus-square"></i></a>'+
                '<a class="edit-cost"><i class="fas fa-pencil-alt"></i></a>'+
                '<a class="delete-cost"><i class="fas fa-trash-alt"></i></a>'+
                '</td>'+
                '</tr>'
        return tr;
    }


 });