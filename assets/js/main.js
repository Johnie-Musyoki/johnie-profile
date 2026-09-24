// Profile site behaviour: footer year, smooth anchor offset, active nav state.
(function () {
  'use strict';

  // Keep the copyright year current without a build step.
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Sticky header overlaps anchors, so scroll the target into view manually.
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = link.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.pageYOffset - 68;
      window.scrollTo({ top: top, behavior: 'smooth' });
      history.replaceState(null, '', id);
    });
  });

  // Highlight the section currently in view.
  var sections = Array.prototype.slice.call(
    document.querySelectorAll('main section[id]')
  );
  var links = {};
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    links[a.getAttribute('href').slice(1)] = a;
  });

  function onScroll() {
    var pos = window.pageYOffset + 100;
    var current = null;
    sections.forEach(function (s) {
      if (s.offsetTop <= pos) current = s.id;
    });
    Object.keys(links).forEach(function (id) {
      links[id].style.background = '';
      links[id].style.color = '';
    });
    if (current && links[current]) {
      links[current].style.background = 'var(--accent-soft)';
      links[current].style.color = 'var(--accent)';
    }
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      onScroll();
      ticking = false;
    });
  }, { passive: true });

  onScroll();
})();
