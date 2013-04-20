

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
                        if oTT.fnGetSelected(oTable).length == 0
                            alert('Please select a device')
                        else
                            ret = prompt("Check OUT - Enter a subject ID or user's e-mail address: ", "")
                            if (ret)
                                checkout_selected(ret)
                    'sucess'

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

checkout_selected = (lendee) ->
    selected = oTT.fnGetSelected(oTable)
    pk = get_selected_id(selected)
    $.ajax(
        url: "/devices/#{pk}/checkout/"
        type: 'POST',
        data: {
            "lendee": lendee,
        },
        success: (data) -> 
            if data.error
                alert(data.error)
            else
                confirmed = confirm("Confirm check out to #{data.full_name}?")
    )

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
