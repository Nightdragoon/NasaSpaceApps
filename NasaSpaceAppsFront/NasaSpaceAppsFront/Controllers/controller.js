// assets/js/controller.js
document.addEventListener('DOMContentLoaded', () => {

  const ROUTES = {
    results:  'results.html',   // o '/Search' si usas MVC
    login:    'login.cshtml',   // o '/Account/Login'
    register: 'signup.cshtml'   // o '/Account/Register'
  };

  
  const DATA_URL = '../model/data.json';

  // ========= REFERENCIAS =========
  const $searchBtn = document.getElementById('searchBtn');     // botón Buscar
  const $searchInp = document.getElementById('searchInput');   // input
  const $searchForm = document.getElementById('searchForm');   // form (si existe)
  const $results = document.getElementById('results');         // contenedor resultados (si quieres render inline)

  const $btnLoginNav    = document.getElementById('btnLoginNav');
  const $btnRegisterNav = document.getElementById('btnRegisterNav');
  const $btnLoginMain   = document.getElementById('btnLogin');     // por si tienes ids en el main
  const $btnRegisterMain= document.getElementById('btnRegister');

  // ========= NAV: LOGIN / REGISTER =========
  function navTo(url) { window.location.href = url; }

  [$btnLoginNav, $btnLoginMain].forEach(btn => {
    if (btn) btn.addEventListener('click', (e) => {
      // Si ya tienes href, puedes omitir preventDefault
      // e.preventDefault();
      navTo(ROUTES.login);
    });
  });

  [$btnRegisterNav, $btnRegisterMain].forEach(btn => {
    if (btn) btn.addEventListener('click', (e) => {
      // e.preventDefault();
      navTo(ROUTES.register);
    });
  });

  // ========= ATAJOS: "/" enfoca, "Esc" limpia =========
  window.addEventListener('keydown', (e) => {
    if (e.key === '/') {
      // Evita que se escriba "/" si no está enfocado
      if (document.activeElement !== $searchInp) e.preventDefault();
      $searchInp?.focus(); $searchInp?.select();
    }
    if (e.key === 'Escape') { if ($searchInp) $searchInp.value = ''; }
  });

  // ========= BÚSQUEDA (click en botón) =========
  if ($searchBtn) {
    $searchBtn.addEventListener('click', (e) => {
      // Si el botón está dentro de un form con type="submit", el submit también disparará
      e.preventDefault();
      doSearch();
    });
  }

  // ========= BÚSQUEDA (Enter en el form) =========
  if ($searchForm) {
    $searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      doSearch();
    });
  }

  // ========= LÓGICA PRINCIPAL DE BÚSQUEDA =========
  async function doSearch() {
    const query = ($searchInp?.value || '').trim();
    if (!query) {
      alert('Please enter a search term.');
      $searchInp?.focus();
      return;
    }

    // 1) Carga datos del modelo
    let data = [];
    try {
      const res = await fetch(DATA_URL, { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      data = await res.json();
    } catch (err) {
      console.error('Error al cargar el modelo:', err);
      alert('Error al cargar datos. Revisa la ruta de data.json y usa un servidor local (Live Server).');
      return;
    }

    // 2) Filtra resultados (title/snippet)
    const results = data.filter(item => {
      const t = (item.title || '').toLowerCase();
      const s = (item.snippet || '').toLowerCase();
      const q = query.toLowerCase();
      return t.includes(q) || s.includes(q);
    });

    // 3) Modo A: si existe #results, render en la misma página
    if ($results) {
      renderInline(results, query);
      return;
    }

    // 4) Modo B: si NO hay #results, navega a results.html y pasa datos
    sessionStorage.setItem('lastQuery', query);
    sessionStorage.setItem('lastResults', JSON.stringify(results));
    window.location.href = `${ROUTES.results}?q=${encodeURIComponent(query)}`;
  }

  // ========= RENDER INLINE (tarjetas Bootstrap) =========
  function renderInline(list, q) {
    // si tienes un spinner, podrías quitarlo aquí
    if (!$results) return;
    $results.innerHTML = '';

    if (!list.length) {
      $results.innerHTML = `
        <div class="col-12">
          <div class="alert alert-secondary" role="alert">
            No results for “${escapeHtml(q)}”.
          </div>
        </div>`;
      return;
    }

    const frag = document.createDocumentFragment();
    list.forEach(item => {
      const col = document.createElement('div');
      col.className = 'col-12 col-md-6 col-lg-4';
      col.innerHTML = `
        <a class="card h-100 text-decoration-none" href="${item.url || '#'}" target="_blank" rel="noopener">
          <div class="card-body">
            <div class="text-muted small mb-1">${escapeHtml(item.type || '')}</div>
            <h5 class="card-title text-primary mb-2">${escapeHtml(item.title || 'Untitled')}</h5>
            <p class="card-text text-body">${escapeHtml(item.snippet || '')}</p>
          </div>
        </a>`;
      frag.appendChild(col);
    });
    $results.appendChild(frag);
  }

  // ========= UTIL: escape HTML =========
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, m => ({
      '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
    }[m]));
  }
});
