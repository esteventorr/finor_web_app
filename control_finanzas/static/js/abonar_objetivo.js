const addButton = document.querySelector('.add-button');
const modal = document.querySelector('.modal');
const closeModalbutton = document.querySelector('.close-modal');
const submitButton = document.querySelector('submit-button');
const progressElement = document.querySelector('.progress');

addButton.addEventListener('click', openModal);
closeModalbutton.addEventListener('click', closeModal);
submitButton.addEventListener('click', increaseProgress);

function openModal() {
    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

function increaseProgress() {
    let currentProgress = parseInt(progressElement.style.width) || 0;
    const increment = 10; // Cantidad que aumenta la barra de progreso

    if (currentProgress + increment <= 100) {
        currentProgress += increment;
        progressElement.style.width = currentProgress + '%';
    }
    closeModal();
}

$("#value-form").on("submit", function (event) {
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
          $("#message").html("<p>Abono realizado con éxito.</p>");
          $("#message").css("color", "green");
          window.location.href = location.origin + "/metas-ahorros/";
        },
        error: function () {
          $("#message").html(
            "<p>Error al abonar al objetivo. Inténtalo de nuevo.</p>"
          );
          $("#message").css("color", "red");
        },
      });
    });