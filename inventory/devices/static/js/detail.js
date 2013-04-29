// Generated by CoffeeScript 1.4.0
(function() {

  $("#id-comment_delete").click(function(e) {
    var confirmed, pk;
    confirmed = confirm('Are you sure you want to delete this comment?');
    if (confirmed) {
      pk = $(this).parent().data('id');
      console.log("TODO: send ajax request to delete comment");
      return $.ajax({
        url: "comment/" + pk + "/delete/",
        type: "POST",
        data: {
          'pk': pk
        },
        success: function(data) {
          return document.location.reload(true);
        }
      });
    } else {
      return console.log("rejected!");
    }
  });

}).call(this);