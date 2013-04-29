$("#id-comment_delete").click( (e) ->
    confirmed = confirm('Are you sure you want to delete this comment?')
    if confirmed
        # Get the pk of the comment from the data-id attribute of the <li> tag
        pk = $(this).parent().data('id')
        console.log "TODO: send ajax request to delete comment"
        $.ajax(
            url: "comment/#{pk}/delete/",
            type: "POST",
            data: {'pk': pk},
            success: (data) -> document.location.reload(true)  # Refresh on success
        )
    else
        console.log "rejected!"
)