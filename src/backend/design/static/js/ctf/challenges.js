!(function($) {
  window.setTimeout(function() {
    $(".alert").fadeTo(300, 0).slideUp(300, function(){
    });
  }, 4000);
  $('#challenges .collapse').on('show.bs.collapse', function () {
    $('#challenges .collapse.show').each(function(){
      $(this).collapse('hide');
    });
  });
  // $.ajax({
  //   url : "http://localhost:8000/api/ctf/challenges",
  //   dataType: "json",
  //   success : function (data) {
  //     console.log(data);
  //   }
  // });
})(jQuery);

