$(document).ready(function() {
  $('i').click(function(){
    $(this).toggleClass('fa-angle-up fa-angle-down');
  });
  $("#solveproblem").mouseover(function() {
    $("#challenge-icon").addClass("text-info");
  });
  $("#solveproblem").mouseleave(function() {
    $("#challenge-icon").removeClass("text-info");
  });
  $("#addchallenge").mouseover(function() {
    $("#addchallenge-icon").addClass("text-success");
  });
  $("#addchallenge").mouseleave(function() {
    $("#addchallenge-icon").removeClass("text-success");
  });
});