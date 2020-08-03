!(function($) {
  $('i').click(function(){
    $(this).toggleClass('fa-angle-up fa-angle-down');
  });
  window.setTimeout(function() {
    $(".alert").fadeTo(300, 0).slideUp(300, function(){
    });
  }, 4000);
})(jQuery);

