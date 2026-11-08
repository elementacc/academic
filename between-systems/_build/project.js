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

      /* Thumbnails: zoom the stage drawing (svg) or swap the stage image; click again to reset */
      var stageSvg = document.querySelector('#stage svg');
      var stageImg = document.querySelector('#stage img');
      var stageCap = document.querySelector('.stage__caption');
      var orig = stageImg ? { src: stageImg.getAttribute('src'), cap: stageCap.textContent } : null;
      var thumbs = document.querySelectorAll('.thumb');
      thumbs.forEach(function (t) {
        t.addEventListener('click', function () {
          var active = t.classList.contains('is-active');
          thumbs.forEach(function (o) { o.classList.remove('is-active'); });
          var el = stageImg || stageSvg;
          el.style.opacity = 0;
          setTimeout(function () {
            if (stageImg) {
              stageImg.setAttribute('src', active ? orig.src : t.getAttribute('data-src'));
              stageCap.textContent = active ? orig.cap : t.getAttribute('data-alt');
            } else {
              stageSvg.setAttribute('viewBox', active ? '0 0 400 400' : t.getAttribute('data-view'));
            }
            el.style.opacity = 1;
          }, 180);
          if (!active) t.classList.add('is-active');
        });
      });
    })();
