$(document).ready(function() {
  const lockModal = $("#lock-modal");
  const loadingCircle = $("#loading-circle");
  const form = $("#my-form");


  form.on('submit', function(e) {
    lockModal.css("display", "block");
    loadingCircle.css("display", "block");

  });

});
