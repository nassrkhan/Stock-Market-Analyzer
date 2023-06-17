// Sub-Menu (Nav-Bar)
const liClick = document.getElementById("click-li");

liClick.addEventListener("click", function () {
  const li = document.getElementById("plus-sub");
  const subMenu = document.getElementById("S-sub-menu");
  li.classList.toggle("add-menu");
  subMenu.classList.toggle("subMenutoggle");
});

// hamburger
const hamburgerOne = document.getElementById("hambergurOne");
const sidebar = document.querySelector(".S-Sidebar-left");
const navfull = document.querySelector("section.S-navbar-section");

const scrn = window.innerWidth;
var bodyClick = document.querySelector(".bodyClick");

hamburgerOne.addEventListener("click", function () {
  hamburgerOne.classList.toggle("active_hamburgerOne");
  sidebar.classList.toggle("sm-sidebar");
  navfull.classList.toggle("nav-full");
  bodyClick.classList.toggle("bClick_hide");
  toggleDiv.classList.remove("toggle");
});
 
 
 // profile-click
 var profClick = document.querySelector(".prof-cntnt-btn");
 const toggleDiv = document.getElementById("click-content-two");
 profClick.addEventListener("click", function () {
     toggleDiv.classList.toggle("toggle");
     notif[0].classList.remove("notif_toggle");
     notif[1].classList.remove("notif_toggle");
     notif[2].classList.remove("notif_toggle");
     notif[3].classList.remove("notif_toggle");
     notif_sm[0].classList.remove("notif_toggle");
     notif_sm[1].classList.remove("notif_toggle");
     notif_sm[2].classList.remove("notif_toggle");
     notif_sm[3].classList.remove("notif_toggle");
 });

// Historic Form Dates

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    } 
    
today = yyyy + '-' + mm + '-' + dd;
document.getElementById("endDatePicker").setAttribute("max", today);


// Java Script for Spinner
var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 1000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("loader_heading").style.display = "none";
  document.getElementById("absolute_div").classList.remove("newDiv")
}