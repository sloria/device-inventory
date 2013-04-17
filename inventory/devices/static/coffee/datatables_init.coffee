

initialize_table = () ->
    $('#id_devices_table').dataTable({
        "sDom": "<'row-fluid'<'span6'T><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
        "oTableTools": {
            "sSwfPath": '/static/libs/datatables/extras/TableTools/media/swf/copy_csv_xls.swf',
            'sRowSelect': 'single',
            "aButtons": [
                # Check out
                {
                    'sExtends': 'text',
                    'sButtonClass': 'btn btn-large btn-primary btn-checkout',
                    'sButtonText': '<i class="icon-signout"></i> Check OUT'
                    'fnClick': (nButton, oConfig, oFlash) ->
                        ret = prompt("Enter the lendee's name or subject ID: ", "")
                        if (ret)
                            checkout_selected(ret)

                },
                # Check in
                {
                    'sExtends': 'text',
                    'sButtonClass': 'btn btn-large btn-warning btn-checkin',
                    'sButtonText': '<i class="icon-signin"></i> Check IN'

                },
                # Edit
                {
                    'sExtends': 'text',
                    'sButtonClass': 'btn btn-large btn-info btn-edit',
                    'sButtonText': '<i class="icon-pencil"></i> Edit device'
                }
                # Export csv
                {
                    'sExtends': 'csv',
                    'sButtonClass': 'btn btn-large btn-default btn-export'
                    'sButtonText': '<i class="icon-file"></i> Export'
                },

            ]
        }
    })

$( () ->
    window.oTable = initialize_table()
    window.oTT = TableTools.fnGetInstance('id_devices_table')
)

checkout_selected = (subject_id) ->
    selected = oTT.fnGetSelected(oTable)
    console.log get_selected_id(selected)

get_selected_id = (selected) ->
    ###
    Returns the id of a selected device as an integer.
    ###
    $(selected).data('id')

get_selected_ids = (selected) ->
    ###
    Returns an array of ids for the selected devices.
    ###
    $.map(selected, (element) -> $(element).data('id'))
