// js script to listen for button click on sidebar button
let sidebarToggle = document.querySelector(".sidebarToggle");
sidebarToggle.addEventListener("click", function(){
    document.querySelector(".page").classList.toggle("active");
    document.getElementById("sidebarToggle").classList.toggle("active");
});
