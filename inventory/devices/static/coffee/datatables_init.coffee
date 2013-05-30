$( () ->
    window.oTable = initialize_table()
    window.oTT = TableTools.fnGetInstance('id_devices_table')
    # Enable column filtering
    oTable.yadcf([
        # Make the Status column filter-able
        {column_number: 1, filter_default_label: "Status"}
        # Make the Condition column filter-able
        {column_number: 5, filter_default_label: "Condition"}
    ])
)

initialize_table = () ->
    ###
    Initialize jQuery Datatables
    ###
    updated_at_idx = get_col_idx('Updated at')
    $('#id_devices_table').dataTable({
        "sDom": "<'row-fluid'<'span6'T><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
        "aoColumnDefs": [
        ],
        # Initially sort by 'updated at' date
        "aaSorting": [[updated_at_idx, "desc"]],
        # Initially show up to 50 devices
        "iDisplayLength": 50,
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
                        selected = oTT.fnGetSelected(oTable)
                        pk = get_selected_id(selected)
                        if selected.length < 1
                            # Check if device has been reset
                            alert('Please select a device')
                        else if is_in("NOT READY", get_td("Status", parseInt(pk)))
                            alert("Cannot check out this device. Device has not been reset.")
                        else
                            ret = prompt("Check OUT - Enter a subject ID or user's e-mail address: ", "")
                            if (ret)
                                checkout_selected(ret)
                },
                # Check in
                {
                    'sExtends': 'text',
                    'sButtonClass': 'btn btn-large btn-warning btn-checkin',
                    'sButtonText': '<i class="icon-signin"></i> Check IN',
                    "fnClick": (nButton, oConfig, oFlash) ->
                        selected = oTT.fnGetSelected(oTable)
                        pk = get_selected_id(selected)
                        # if user hasn't selected a device
                        if selected.length < 1
                            # show an alert
                            alert('Please select a device')
                        # else if the device is already checked in
                        else if is_in("Checked in", get_td("Status", parseInt(pk)))
                            alert("Device is already checked in")
                        else
                            checkin_selected()
                },
                # View details
                {
                    'sExtends': 'text',
                    'sButtonClass': 'btn btn-large btn-info btn-detail',
                    'sButtonText': '<i class="icon-info-sign"></i> View details',
                    'fnClick': (nButton, oConfig, oFlash) ->
                        # On click, go to the detail page for the selected device
                        selected = oTT.fnGetSelected(oTable)
                        if selected.length < 1
                            alert('Please select a device')
                        else
                            pk = get_selected_id(selected)
                            device_class = get_selected_class(selected)
                            window.location = "#{window.base_url}#{device_class}/#{pk}/"
                },
                # Edit
                {
                    'sExtends': 'text',
                    'sButtonClass': 'btn btn-large btn-default btn-edit-device',
                    'sButtonText': '<i class="icon-pencil"></i> Edit device'
                    'fnClick': (nButton, oConfig, oFlash) ->
                            selected = oTT.fnGetSelected(oTable)
                            if selected.length < 1
                                alert("Please select a device.")
                            else
                                # redirect to device edit page
                                pk = get_selected_id(selected)
                                device_class = get_selected_class(selected)
                                window.location = "#{window.base_url}#{device_class}/#{pk}/edit/"
                },
                # # Export csv
                # {
                #     'sExtends': 'csv',
                #     'sButtonClass': 'btn btn-large btn-default btn-export'
                #     'sButtonText': '<i class="icon-file"></i> Export'
                # },

            ]
        }
    })

checkout_selected = (lendee) ->
    selected = oTT.fnGetSelected(oTable)
    pk = get_selected_id(selected)
    device_type = get_selected_class(selected)
    $.ajax(
        url: "#{window.base_url}#{device_type}/#{pk}/checkout/"
        type: 'POST',
        data: {
            "lendee": lendee,
        },
        success: (data) ->
            if data.error
                alert(data.error)
            else
                # Show confirmation dialog
                confirmed = confirm("Confirm check out to #{data.name}?")
                if confirmed
                    $.ajax(
                        url: "#{window.base_url}#{device_type}/#{pk}/checkout/confirm/",
                        type: 'POST',
                        data: {
                            'lendee': lendee,
                            'device_type': device_type
                        },
                        success: (data) ->
                            # Refresh the page
                            window.location = "#{window.base_url}#{device_type}/"
                    )
    )

checkin_selected = () ->
    selected = oTT.fnGetSelected(oTable)
    pk = get_selected_id(selected)
    device_type = get_selected_class(selected)
    window.location = "#{window.base_url}#{device_type}/#{pk}/checkin"


# Add click handler for device delete button
$("#id_delete_btn").click( (e) ->
    e.preventDefault()
    selected = oTT.fnGetSelected(oTable)
    if selected.length < 1
        alert("No device selected.")
    else
        confirmed = confirm("Are you sure you want to delete this device?\n
WARNING: This action is irreversible.")
        pk = get_selected_id(selected)
        if confirmed
            $.ajax(
                url: "#{window.base_url}#{pk}/delete/",
                type: "POST",
                data: {
                    'pk': pk,
                    'device_type': get_selected_class(selected)
                    }
                success: (data) ->
                    # Refresh the page
                    window.location = "#{window.base_url}"
            )
)

change_td = (column_name, pk, new_text) ->
    ###
    Changes the text of the cell at the column that contains
    text column_name and the row of the device with a given pk.
    ###
    col_idx = $("th:contains('#{column_name}')").index()
    $("tr[data-id='#{pk}']")
                .find('td')
                .eq(col_idx)
                .html(new_text)

get_td = (column_name, pk) ->
    ###
    Get the text of a table cell at the column that contains the
    text column_name and the row of the device with a given pk.
    ###
    col_idx = $("th:contains('#{column_name}')").index()
    $("tr[data-id='#{pk}']")
                .find('td')
                .eq(col_idx)
                .text()

get_col_idx = (column_name) ->
    ###
    Return the index of the table column that contains the text
    column_name.
    ###
    return $("th:contains('#{column_name}')").index()

get_selected_id = (selected) ->
    ###
    Returns the id of a selected device as an integer.
    ###
    $(selected).data('id')

get_selected_class = (selected) ->
    ###
    Returns the device class of a selected device as an integer.
    ###
    $(selected).data('type')

get_selected_ids = (selected) ->
    ###
    Returns an array of ids for the selected devices.
    ###
    $.map(selected, (element) -> $(element).data('id'))

is_in = (sub, whole) ->
    return whole.indexOf(sub) isnt -1

