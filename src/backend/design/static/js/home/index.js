!(function($) {
  $('.collapse').on('show.bs.collapse', function () {
    $('.collapse.show').each(function(){
      $(this).collapse('hide');
    });
  });
})(jQuery);