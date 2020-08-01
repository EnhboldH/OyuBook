!(function($) {
  window.setTimeout(function() {
    $(".alert").fadeTo(300, 0).slideUp(300, function(){
      $(this).remove();
    });
  }, 2000);
  $("#alertClose").click(function(){
    $(".alert").fadeTo(300, 0).slideUp(300, function(){
      $(this).remove(); 
    });
  });
})(jQuery);