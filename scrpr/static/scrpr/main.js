var burger = document.getElementById('burger_touch');
var burger2 = document.getElementById('burger_click');
var filtersList = document.getElementById('filters_list');
burger.addEventListener('touchend', toggleClassOnTouch);
burger2.addEventListener('click', toggleClassOnClick);

xList = [
  window.matchMedia("(max-width: 639px)"),
  window.matchMedia("(min-width: 1024px)")
];


function toggleClassOnTouch() {
  this.classList.toggle("change");
}

function toggleClassOnClick() {
  this.classList.toggle("change");
}

function openFilters() {
  filtersList.classList.toggle("filters_open")
}

function openForm(itemClass) {
  var item = document.getElementsByClassName(itemClass)[0];
  item.classList.toggle("open");
}
