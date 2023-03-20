$("#expenseForm").on("submit", function (event) {
  event.preventDefault();

  // Recoge los datos del formulario
  const formData = new FormData(this);
  const formURL = $(this).data("url");

  // Realiza la solicitud AJAX
  $.ajax({
    url: formURL,
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      // Muestra el mensaje de éxito
      console.warn(response);
      $("#message").html("<p>Gasto guardado con éxito.</p>");
      $("#message").css("color", "green");
      // navigate to the expense list
      window.location.href = location.origin + "/analisis-gastos/";
    },
    error: function () {
      // Muestra el mensaje de error
      $("#message").html(
        "<p>Error al guardar el gasto. Inténtalo de nuevo.</p>"
      );
      $("#message").css("color", "red");
    },
  });
});
