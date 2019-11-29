function toggleClassOnTouch() {
  this.classList.toggle("change");
}

function toggleClassOnClick() {
  this.classList.toggle("change");
}

var burger = document.getElementById('burger_touch');
var burger2 = document.getElementById('burger_click');
var filtersList = document.getElementById('filters_list');
burger.addEventListener('touchend', toggleClassOnTouch);
burger2.addEventListener('click', toggleClassOnClick);
