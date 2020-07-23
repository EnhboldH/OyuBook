$(document).ready(function() {
  var up = "<i class='fas fa-angle-up' type='button'></i>";
  var down = "<i class='fas fa-angle-down' type='button'></i>";

  $("#activeCollapse").on("hide.bs.collapse", function() {
    $(".angleSwitchActive").html(up);
  });
  $("#activeCollapse").on("show.bs.collapse", function() {
    $(".angleSwitchActive").html(down);
  });
  $("#learnMore").on("hide.bs.collapse", function() {
    $(".angleSwitchLearn").html(up);
  });
  $("#learnMore").on("show.bs.collapse", function() {
    $(".angleSwitchLearn").html(down);
  });
  $("#problembsCollapse").on("hide.bs.collapse", function() {
    $(".angleSwitchProblems").html(up);
  });
  $("#problembsCollapse").on("show.bs.collapse", function() {
    $(".angleSwitchProblems").html(down);
  });
  $("#news").on("hide.bs.collapse", function() {
    $(".angleSwitchNews").html(up);
  });
  $("#news").on("show.bs.collapse", function() {
    $(".angleSwitchNews").html(down);
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