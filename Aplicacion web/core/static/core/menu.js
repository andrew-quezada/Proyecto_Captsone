// JavaScript para abrir y cerrar el menú del empleado
function openMenu() {
    document.getElementById("sideMenu").style.width = "250px";
    document.querySelector(".contenedor").style.marginLeft = "250px"; /* Desplaza el contenido */
}

function closeMenu() {
    document.getElementById("sideMenu").style.width = "0";
    document.querySelector(".contenedor").style.marginLeft = "0"; /* Restaura el contenido */
}