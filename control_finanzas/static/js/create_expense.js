$("#expenseForm").on("submit", function (event) {
  event.preventDefault();

  const valueInput = $("#value-input");
  const floatValue = unformatCurrency(valueInput.val());
  console.log("floatValue ------------------------------------------------------------------------")
  console.log(floatValue)
  valueInput.val(floatValue);

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
      $("#message").html("<p>Gasto guardado con éxito.</p>");
      $("#message").css("color", "green");
      window.location.href = location.origin + "/analisis-gastos/";
    },
    error: function () {
      $("#message").html(
        "<p>Error al guardar el gasto. Inténtalo de nuevo.</p>"
      );
      $("#message").css("color", "red");
    },
  });
});
