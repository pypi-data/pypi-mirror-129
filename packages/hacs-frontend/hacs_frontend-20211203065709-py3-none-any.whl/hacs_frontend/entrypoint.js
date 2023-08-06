
try {
  new Function("import('/hacsfiles/frontend/main-4fe0750e.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-4fe0750e.js';
  document.body.appendChild(el);
}
  