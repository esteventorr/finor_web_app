$("#loginForm").on("submit", function (event) {
  event.preventDefault();

  var email = document.getElementById("emailL").value;
  var password = document.getElementById("passwordL").value;

  console.log(email)
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential;
      console.log("Inicio de sesión exitoso.", user);
      $("#message").html("<p>Inicio de sesión exitoso.</p>");
      $("#message").css("color", "green");
      //...
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.error("Error al iniciar sesión: " + errorMessage);
      $("#message").html("<p>Error al iniciar sesión. Inténtalo de nuevo.</p>");
      $("#message").css("color", "red");
    });
});