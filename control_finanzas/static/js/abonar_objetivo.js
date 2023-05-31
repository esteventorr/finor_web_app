function openModal(event) {
  const goalId = $(event.target).attr("data-goal-id");
  $(`.modal.${goalId}`).css("display", "block");
}

function closeModal(event) {
  $(event.target).closest(".modal").css("display", "none");
}

function increaseProgress(event) {
  const modal = $(event.target).closest(".modal");
/*   let currentProgress = parseInt(progressElement.style.width) || 0;
  const increment = 10; // Cantidad que aumenta la barra de progreso

  if (currentProgress + increment <= 100) {
    currentProgress += increment;
    progressElement.style.width = currentProgress + "%";
  }
  closeModal(); */
}

const addButtons = $(".add-button");
const modal = document.querySelector(".modal");
const closeModalbutton = $(".close-modal");
const submitButton = $(".submit-button");
const progressElement = $(".progress");

addButtons.on("click", openModal);
closeModalbutton.on("click", closeModal);
submitButton.on("click", increaseProgress);

$(".value-form").on("submit", function (event) {
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
      $("#message").html("<p>Abono realizado con éxito.</p>");
      $("#message").css("color", "green");
      $(".modal").css("display", "none");
      window.location.href = location.origin + "/metas-ahorros/";
    },
    error: function () {
      $("#message").html("<p>Error al abonar al objetivo. Inténtalo de nuevo.</p>");
      $("#message").css("color", "red");
    },
  });
});
