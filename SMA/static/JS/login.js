const togglePassword = document.querySelector("#togglePassword");
const password = document.querySelector("#id_password");

// Login Page
try {
  togglePassword.addEventListener("click", function (e) {
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    this.classList.toggle("fa-eye-slash");
  });
}
// Sign up Page
catch {
  const toggleReg = document.querySelector("#toggleReg");
  const toggleReg1 = document.querySelector("#toggleReg1");
  const pass = document.querySelector("#id_reg");
  const pass1 = document.querySelector("#id_reg1");

  toggleReg.addEventListener("click", function (e) {
    const type = pass.getAttribute("type") === "password" ? "text" : "password";
    pass.setAttribute("type", type);
    this.classList.toggle("fa-eye-slash");
  });

  toggleReg1.addEventListener("click", function (e) {
    const type = pass1.getAttribute("type") === "password" ? "text" : "password";
    pass1.setAttribute("type", type);
    this.classList.toggle("fa-eye-slash");
  });
}