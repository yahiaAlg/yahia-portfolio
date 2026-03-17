/* ── NAVBAR SCROLL ──────────────────────────────────────── */
const nav = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 50);
});

/* ── REVEAL ON SCROLL ───────────────────────────────────── */
const revealEls = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); } });
}, { threshold: 0.12 });
revealEls.forEach(el => revealObs.observe(el));

/* ── PROJECT FILTER ─────────────────────────────────────── */
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('.project-item').forEach(item => {
      const show = filter === 'all' || item.dataset.cat === filter;
      item.classList.toggle('hidden', !show);
    });
    lucide.createIcons();
  });
});

/* ── SMOOTH ACTIVE NAV ──────────────────────────────────── */
const sections = document.querySelectorAll('section[id]');
const navLinks  = document.querySelectorAll('.nav-link');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) current = s.id;
  });
  navLinks.forEach(l => {
    l.classList.toggle('active', l.getAttribute('href') === `#${current}`);
  });
}, { passive: true });

/* ── RE-INIT LUCIDE AFTER FILTER ────────────────────────── */
document.addEventListener('DOMContentLoaded', () => lucide.createIcons());


/* ── THEME TOGGLE ───────────────────────────────────────── */
(function () {
  const root    = document.documentElement;
  const btn     = document.getElementById('themeToggle');
  const STORAGE = 'portfolio-theme';

  // Apply saved or system preference on load
  const saved = localStorage.getItem(STORAGE);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = saved || (prefersDark ? 'dark' : 'light');
  applyTheme(initial);

  btn && btn.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    applyTheme(next);
    localStorage.setItem(STORAGE, next);
  });

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    // Bootstrap uses data-bs-theme for some components
    root.setAttribute('data-bs-theme', theme);
    lucide && lucide.createIcons();
  }
})();

/* ── THEME TOGGLE ───────────────────────────────────────── */
(function () {
  const root    = document.documentElement;
  const btn     = document.getElementById('themeToggle');
  const DARK    = 'dark';
  const LIGHT   = 'light';
  const KEY     = 'portfolio-theme';

  // Icon visibility helpers
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    root.setAttribute('data-bs-theme', theme);
    localStorage.setItem(KEY, theme);
    if (btn) {
      btn.querySelector('.icon-sun').style.display  = theme === LIGHT ? 'none'  : 'block';
      btn.querySelector('.icon-moon').style.display = theme === LIGHT ? 'block' : 'none';
      btn.title = theme === LIGHT ? 'Switch to Dark Mode' : 'Switch to Light Mode';
    }
  }

  // Load saved preference, fall back to OS preference
  const saved = localStorage.getItem(KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? DARK : LIGHT));

  // Toggle on click
  if (btn) {
    btn.addEventListener('click', () => {
      applyTheme(root.getAttribute('data-theme') === DARK ? LIGHT : DARK);
      lucide.createIcons();
    });
  }

  // Sync with OS changes when no saved preference
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem(KEY)) applyTheme(e.matches ? DARK : LIGHT);
  });
})();


/* ── THEME TOGGLE ───────────────────────────────────────── */
(function () {
  const root    = document.documentElement;
  const btn     = document.getElementById('themeToggle');
  const STORAGE = 'portfolio-theme';

  // Apply saved or system preference on load
  const saved   = localStorage.getItem(STORAGE);
  const prefers = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  const initial = saved || prefers;
  root.setAttribute('data-theme', initial);
  // Remove Bootstrap's data-bs-theme so our CSS variables take over
  root.removeAttribute('data-bs-theme');

  if (btn) {
    btn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem(STORAGE, next);
      // Re-init icons so sun/moon swap renders
      lucide.createIcons();
    });
  }
})();


/* ── CERT LIGHTBOX ──────────────────────────────────────── */
(function () {
  const lightbox   = document.getElementById('certLightbox');
  if (!lightbox) return;

  const img        = document.getElementById('certLightboxImg');
  const title      = document.getElementById('certLightboxTitle');
  const issuer     = document.getElementById('certLightboxIssuer');
  const download   = document.getElementById('certLightboxDownload');
  const closeBtn   = document.getElementById('certLightboxClose');
  const backdrop   = lightbox.querySelector('.cert-lightbox-backdrop');

  function open(src, t, i) {
    img.src          = src;
    img.alt          = t;
    title.textContent  = t;
    issuer.textContent = i;
    download.href    = src;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
    lucide.createIcons();
  }

  function close() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => { img.src = ''; }, 260);
  }

  // Attach to all view buttons (works after filter too)
  document.addEventListener('click', e => {
    const btn = e.target.closest('.cert-btn-view');
    if (btn) {
      open(
        btn.dataset.lightboxSrc,
        btn.dataset.lightboxTitle,
        btn.dataset.lightboxIssuer
      );
    }
  });

  closeBtn.addEventListener('click', close);
  backdrop.addEventListener('click', close);

  // Close on Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && lightbox.classList.contains('open')) close();
  });
})();
