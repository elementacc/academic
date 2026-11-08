    (function () {
      var body = document.body;
      var dots = document.querySelectorAll('[data-theme]');
      function setTheme(t) {
        body.classList.remove('light', 'dark', 'mood');
        body.classList.add(t);
        dots.forEach(function (d) {
          var on = d.getAttribute('data-theme') === t;
          d.classList.toggle('is-active', on);
          d.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        try { localStorage.setItem('bs-lights', t); } catch (e) {}
      }
      var saved = 'light';
      try { saved = localStorage.getItem('bs-lights') || 'light'; } catch (e) {}
      setTheme(['light', 'dark', 'mood'].indexOf(saved) > -1 ? saved : 'light');
      dots.forEach(function (d) { d.addEventListener('click', function () { setTheme(d.getAttribute('data-theme')); }); });

      /* Thumbnails zoom the main stage to a detail; click again to reset */
      var stage = document.querySelector('#stage svg');
      var thumbs = document.querySelectorAll('.thumb');
      thumbs.forEach(function (t) {
        t.addEventListener('click', function () {
          var active = t.classList.contains('is-active');
          thumbs.forEach(function (o) { o.classList.remove('is-active'); });
          stage.style.opacity = 0;
          setTimeout(function () {
            stage.setAttribute('viewBox', active ? '0 0 400 400' : t.getAttribute('data-view'));
            stage.style.opacity = 1;
          }, 180);
          if (!active) t.classList.add('is-active');
        });
      });
    })();
