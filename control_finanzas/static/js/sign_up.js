$("#signupForm").on("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const formURL = $(this).data("url");

  $.ajax({
    url: formURL,
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      console.warn(response);
      $("#message").html("<p>Objetivo guardado con éxito.</p>");
      $("#message").css("color", "green");
      window.location.href = "/loginpage";
    },
    error: function () {
      $("#message").html("<p>Error al guardar el objetivo. Inténtalo de nuevo.</p>");
      $("#message").css("color", "red");
    },
  });
});
