function setMinWindowSize() {
  var minWidth = 800;
  var minHeight = 500;
  if (window.innerWidth < minWidth) {
    window.resizeTo(minWidth, window.innerHeight);
  }
  if (window.innerHeight < minHeight) {
    window.resizeTo(window.innerWidth, minHeight);
  }
}

window.addEventListener('resize', setMinWindowSize);
