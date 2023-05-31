function openModal(event) {
  const goalId = $(event.target).attr("data-goal-id");
  $(`.modal.${goalId}`).css("display", "block");
}

function closeModal(event) {
  $(event.target).closest(".modal").css("display", "none");
}

function increaseProgress(event) {
  const goalId = $(event.target).attr("data-goal-id");
  const goalValue = $(`.goal-objective-value[data-goal-id="${goalId}"]`).text().trim();
  console.log("goal value: " + goalValue);

  const totalExpenses = $(`.goal-objective-value[data-goal-id="${goalId}"]`).siblings(".goal-value");
  const totalExpensesValue = totalExpenses.text().trim();
  console.log("total expenses: " + totalExpensesValue);

  const progressPercentage = (parseFloat(totalExpensesValue) / parseFloat(goalValue)) * 100;
  console.log("percentage: " + progressPercentage);

  $(event.target).closest(".progress-bar").find(".progress").css("width", progressPercentage + "%");
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
