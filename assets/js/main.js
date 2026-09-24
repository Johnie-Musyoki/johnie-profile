// Profile behaviour: smooth anchor scrolling, active sidebar state, and
// reveal-on-scroll for the fade-up sections.
(function () {
  'use strict';

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Sidebar is fixed on desktop and a bottom bar on mobile, so offset the
  // scroll target to clear it.
  function headerOffset() {
    if (window.matchMedia('(max-width: 900px)').matches) return 76;
    return 24;
  }

  document.querySelectorAll('a.scroller').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var href = link.getAttribute('href');
      if (!href || href.charAt(0) !== '#') return;
      var target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.pageYOffset - headerOffset();
      window.scrollTo({ top: top, behavior: 'smooth' });
      history.replaceState(null, '', href);
    });
  });

  // Highlight the section currently in view.
  var sections = Array.prototype.slice.call(document.querySelectorAll('section[id]'));
  var navLinks = {};
  document.querySelectorAll('#sidebar nav a').forEach(function (a) {
    navLinks[a.getAttribute('href').slice(1)] = a;
  });

  function update() {
    var pos = window.pageYOffset + window.innerHeight * 0.35;
    var current = null;
    sections.forEach(function (s) { if (s.offsetTop <= pos) current = s.id; });
    Object.keys(navLinks).forEach(function (id) {
      navLinks[id].classList.remove('active');
    });
    if (current && navLinks[current]) navLinks[current].classList.add('active');
  }

  // Reveal fade-up sections as they enter the viewport.
  var fades = document.querySelectorAll('.fade-up');
  // Only hide content once we know we can reveal it again.
  if ('IntersectionObserver' in window && fades.length) {
    Array.prototype.forEach.call(fades, function (el) { el.classList.add('js-reveal'); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    Array.prototype.forEach.call(fades, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(fades, function (el) { el.classList.add('in'); });
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { update(); ticking = false; });
  }, { passive: true });

  update();
})();
