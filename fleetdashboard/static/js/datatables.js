$(document).ready(function () {
    var today = new Date();
    var utc = today.toUTCString();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();


    moment.updateLocale(moment.locale(), { invalidDate: "" });
    $.fn.dataTable.moment( 'DD/MM/YYYY' );

   //Vehicle details datatable
   $('#data').DataTable({
        dom: '<"row"lfB>rtip',
        //Button
        buttons: [
            {
                text: 'New',
                action: function ( e, dt, node, config ) {
                    $('#newvehicleModal').modal('show')
                },
                attr:  {
                    id: 'new-vehicle',
                    class: 'new-btn '

                }
            }
        ],
        // Datatable definitions
        ajax: '/details/data',

        columnDefs: [
            {
                "targets": [0],
                className: 't-numba'
            },
            {
                "targets": [4,5,6,7,8],
                render:function(data){
                return moment(data).format('DD/MM/YYYY');
                }
            },
            {
                "targets": [4,5,6,7,8],
                "createdCell": function (td, cellData, rowData, row, col) {
                  if ( cellData != null && Date.parse(cellData) < today ) {
                    $(td).css('color', 'white')
                    $(td).css('background', 'red')
                  } else if
                    ( cellData != null && (Date.parse(cellData) - today)/(1000 * 3600 * 24) < 14 ) {

                    $(td).css('color', 'white')
                    $(td).css('background', 'orange')
                  }
            }
          },
          {
            "targets": [-1],
            "data": null,
            "defaultContent": '<span class="edit_btn"><a id="edit_pencil"><i class="fas fa-pencil-alt"></i></a></span>'
          }
        ],
        columns: [
          {data: 'T_Number'},
          {data: 'department'},
          {data: 'driver_name'},
          {data: 'ownership_type'},
          {data: 'service_date'},
          {data: 'registration_exp'},
          {data: 'fitness_exp'},
          {data: 'carrier_exp'},
          {data: 'insurance_exp'},
          {data: null},
        ],

       initComplete: function () {

        //Select filters for vehicle details table
        $('div.dataTables_filter').prepend('<select id="ownership1" name="ownership" class="form-control-sm filter_dropdowns"><option value="">All</option><option value="Personal">Personal</option><option value="Own Vehicle">Own Vehicle</option><option value="TELiCON">TELiCON</option></select>')
        $('div.dataTables_filter').prepend('<select id="department1" name="department1" class="form-control-sm filter_dropdowns"><option value="">All</option><option value="Personal">Personal</option><option value="Installation">Installation</option><option value="Construction">Construction</option><option value="Fibre">Fibre</option></select>')

           this.api().columns([1]).every( function () {
                var that = this;

                $('#department1').on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                });
           });

           this.api().columns([4]).every( function () {
                var that = this;

                $('#ownership1').on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                });
           });

       }

   });



    //Expense datatable
    var  exp_table = $('#expense-table-main').DataTable({

        responsive: true,
        ajax: '/expense/data',
        columnDefs: [
          { className: "deek", "targets": [0] },

          {
            "targets": [-1],
            "data": null,
            "defaultContent": '<span class="expense_edit_btn"><a class="edit_cost" data-bs-toggle="modal" data-bs-target="#editcostModal" data-bs-dismiss="modal" data-id="" data-tn=""><i class="fas fa-pencil-alt"></i></a></span>'
          }
        ],
        columns: [
          {data: 'T_Number'},
          {data: 'cost_description', searchable: false},
          {data: 'cost', orderable: false, searchable: false, render: $.fn.dataTable.render.number(',', '.', 2, '$')},
          {data: 'expense_status', orderable: false, searchable: false},
          {data: 'repair_id', visible: false},
          {data: null}
        ],
        initComplete: function () {

            $('.edit_cost').each(function() {
                $row = $(this).closest("tr");
                t = $row.find(".deek").html()
                $(this).attr('data-tn', t)

                var row_data = $('#expense-table-main').DataTable().row($row).data();
                $(this).attr('data-id', row_data['repair_id'])
            });
        }
      });



    //Garage Datatable
    $('#garage-table').DataTable({
        responsive: true,
        ajax: '/garage/data',
        columnDefs: [

        {"targets": [0], className: "table-t-num"},
         {
                "targets": [1],
                render:function(data){
                return moment(data).format('DD/MM/YYYY');
                }
          },
          {
                "targets": [3],
                render:function(data){
                return moment(data).format('DD/MM/YYYY');
                }
          },
          {
            "targets": [-1],
            "data": null,
            "defaultContent": '<span class="edit_btn"><a class="option_btn" data-bs-toggle="modal" data-bs-target="#optionModal" id="option_link" data-id="" name="GARAGE"><i class="fas fa-pencil-alt"></i></a></span>'+
                                '<span class="history" data-bs-toggle="modal" data-bs-target="#historyModal" name="GARAGE"><a><i class="fas fa-file-alt"></i></a><span>'
          }
        ],
        columns: [
          {data: 'T_Number'},
          {data: 'date_garage'},
          {data: 'garage_reason'},
          {data: 'repair_expense_sum', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
          {data: null}
        ],
      });

    //Parked Datatable
    $('#parked-table').DataTable({
        responsive: true,
        ajax: '/parked/data',
        columnDefs: [

        {"targets": [0], className: "table-t-num"},
         {
                "targets": [1],
                render:function(data){
                return moment(data).format('DD/MM/YYYY');
                }
          },
          {
                "targets": [3],
                render:function(data){
                return moment(data).format('DD/MM/YYYY');
                }
          },
          {
            "targets": [-1],
            "data": null,
            "defaultContent": '<span class="edit_btn"><a class="option_btn" data-bs-toggle="modal" data-bs-target="#optionModal" id="option_link" data-id="" name="PARKED"><i class="fas fa-pencil-alt"></i></a></span>'+
                              '<span class="history" data-bs-toggle="modal" data-bs-target="#historyModal" name="PARKED"><a><i class="fas fa-file-alt"></i></a><span>'
          }
        ],
        columns: [
          {data: 'T_Number'},
          {data: 'date_parked'},
          {data: 'park_reason'},
          {data: 'repair_expense_sum', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
          {data: null}
        ],
      });

      //Parked Datatable
    $('#active-table').DataTable({
        responsive: true,
        ajax: '/active/data',
        columnDefs: [

        {"targets": [0], className: "table-t-num"},
         {
                "targets": [1],
                render:function(data){
                return moment(data).format('DD/MM/YYYY');
                }
          },
          {
            "targets": [-1],
            "data": null,
            "defaultContent": '<span class="edit_btn"><a class="option_btn" data-bs-toggle="modal" data-bs-target="#optionModal" id="option_link" data-id="" name="ACTIVE"><i class="fas fa-pencil-alt"></i></a></span>'
          }
        ],
        columns: [
          {data: 'T_Number'},
          {data: 'date_active'},
          {data: 'active_notes'},
          {data: null}
        ],
      });

});