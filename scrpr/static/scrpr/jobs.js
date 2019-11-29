var filtersList = document.getElementById('filters_list');

xList = [
  window.matchMedia("(max-width: 639px)"),
  window.matchMedia("(min-width: 1024px)")
];

function adjustCityButton(x) {
  var filtersTab = document.getElementsByClassName('filters_tab')[0];
  var filtersChild = document.getElementById('filters_list');
  var searchTab = document.getElementsByClassName('search_tab')[0];
  var searchChild = document.getElementsByClassName('search_button')[0];
  var elem = document.getElementsByClassName('city_filter')[0];
  var parentNode = elem.parentNode;

  if (xList[0].matches || xList[1].matches) {
    if (elem !== undefined) {
      parentNode.removeChild(elem);
    }
    filtersTab.insertBefore(elem, filtersChild);
    elem.classList.remove("city_inline");
    elem.classList.toggle("city_separate");
  }

  if (!xList[0].matches && !xList[1].matches) {
    if (elem !== undefined) {
      parentNode.removeChild(elem);
    }
    searchTab.insertBefore(elem, searchChild);
    elem.classList.remove("city_separate");
    elem.classList.toggle("city_inline");
  }
}

if (document.getElementsByClassName('city_filter')[0] !== undefined) {
  for (var i = 0; i < xList.length; i++) {
    adjustCityButton(xList[i]);
    xList[i].addListener(adjustCityButton);
  }
}
