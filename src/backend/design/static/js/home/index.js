$(document).ready(function() {
  var up = "<i class='fas fa-angle-up' type='button'></i>";
  var down = "<i class='fas fa-angle-down' type='button'></i>";

  $("#acCollapse1").on("hide.bs.collapse", function() {
    $(".angleSwitch1").html(up);
  });
  $("#acCollapse1").on("show.bs.collapse", function() {
    $(".angleSwitch1").html(down);
  });
  $("#acCollapse2").on("hide.bs.collapse", function() {
    $(".angleSwitch2").html(up);
  });
  $("#acCollapse2").on("show.bs.collapse", function() {
    $(".angleSwitch2").html(down);
  });
  $("#acCollapse3").on("hide.bs.collapse", function() {
    $(".angleSwitch3").html(up);
  });
  $("#acCollapse3").on("show.bs.collapse", function() {
    $(".angleSwitch3").html(down);
  });
  $("#acCollapse4").on("hide.bs.collapse", function() {
    $(".angleSwitch4").html(up);
  });
  $("#acCollapse4").on("show.bs.collapse", function() {
    $(".angleSwitch4").html(down);
  });
});