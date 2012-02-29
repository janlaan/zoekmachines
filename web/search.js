$(document).ready(function() {
  $(".advanced").hide();
  $("#show_advanced").click(function() {
    $(".advanced").toggle();
    return false;
  });
});