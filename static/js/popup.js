function infoPopUp_orgname() {hide_protname();hide_header();hide_seq();
    var popup = document.getElementById("infopopup_orgname");
    popup.classList.toggle("show");}

function infoPopUp_protname() {hide_orgname();hide_header();hide_seq();
    var popup = document.getElementById("infopopup_protname");
    popup.classList.toggle("show");}

function infoPopUp_header() {hide_orgname();hide_protname();hide_seq();
    var popup = document.getElementById("infopopup_header");
    popup.classList.toggle("show");}

function infoPopUp_seq() {hide_orgname();hide_protname();hide_header();
    var popup = document.getElementById("infopopup_seq");
    popup.classList.toggle("show");}

function hide_orgname() {var popup = document.getElementById("infopopup_orgname");
    popup.classList.remove("show");}

function hide_protname() {var popup = document.getElementById("infopopup_protname");
    popup.classList.remove("show");}
function hide_header() {var popup = document.getElementById("infopopup_header");
    popup.classList.remove("show");}
function hide_seq() {var popup = document.getElementById("infopopup_seq");
    popup.classList.remove("show");}