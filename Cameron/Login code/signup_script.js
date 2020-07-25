$(document).ready(function() {
  $("form").submit(function(event) {
    event.preventDefault();
    var firstName = $(#inputFirstName).val();
    var surname = $(#inputSurname).val();
    var email = $(#inputEmail).val();
    var pwd = $(#inputPwd).val();
    var pwdConfirm = $(#inputPwdConfirm).val();

    $(".submit-feedback").load("submit.inc.php", {
      firstName: firstName,
      surname: surname,
      email: email,
      pwd: pwd,
      pwdConfirm: pwdConfirm
    })
  })
})
