// Cenas das etapas desenhadas em SVG (viewBox 780 x 390).
// O balão de pergunta cobre aprox. x 113–503 / y 10–172 no desktop,
// por isso os elementos principais ficam abaixo ou à direita dessa área.

const Cenas = (() => {
  const L = 780, A = 390, CHAO = 330;
  let nSeta = 0;

  const defs = `
    <defs>
      <linearGradient id="g-torre" x1="0" x2="1">
        <stop offset="0" stop-color="#8a8a8a"/><stop offset=".35" stop-color="#f6f6f6"/><stop offset="1" stop-color="#7a7a7a"/>
      </linearGradient>
      <linearGradient id="g-duto" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#a5a5a5"/><stop offset=".35" stop-color="#fff"/><stop offset="1" stop-color="#8a8a8a"/>
      </linearGradient>
      <linearGradient id="g-metal" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#f3f3f3"/><stop offset="1" stop-color="#a3a3a3"/>
      </linearGradient>
      <linearGradient id="g-capsula" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#d9d9d9"/><stop offset=".3" stop-color="#fff"/><stop offset="1" stop-color="#b5b5b5"/>
      </linearGradient>
      <radialGradient id="g-fogo" cx=".5" cy="1" r="1">
        <stop offset="0" stop-color="#fff3a0"/><stop offset=".45" stop-color="#ffb52e"/><stop offset="1" stop-color="#d9480f"/>
      </radialGradient>
      <linearGradient id="g-mar" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#6fb2dc"/><stop offset="1" stop-color="#3f86b5"/>
      </linearGradient>
    </defs>`;

  // ---------- peças ----------

  function fundo() {
    // silhueta da refinaria ao fundo
    const predios = [
      [20, 40, 200], [70, 18, 150], [95, 60, 230], [170, 14, 120], [190, 50, 210],
      [255, 22, 170], [290, 70, 240], [380, 16, 110], [400, 44, 190], [455, 26, 150],
      [500, 60, 225], [575, 18, 130], [600, 40, 180], [650, 14, 100], [670, 56, 215],
      [735, 20, 140], [755, 40, 200]
    ];
    const s = predios.map(([x, w, t]) => `<rect x="${x}" y="${t}" width="${w}" height="${CHAO - t}"/>`).join("");
    return `
      <g fill="#dedede">${s}</g>
      <g fill="#e6e6e6">
        <rect x="0" y="260" width="${L}" height="${CHAO - 260}"/>
      </g>
      <rect x="0" y="${CHAO}" width="${L}" height="${A - CHAO}" fill="#e3e3e3"/>
      <g stroke="#cdcdcd" stroke-width="1.5">
        <line x1="0" x2="${L}" y1="${CHAO + 4}" y2="${CHAO + 4}"/>
        <line x1="0" x2="${L}" y1="${CHAO + 22}" y2="${CHAO + 22}"/>
        <line x1="0" x2="${L}" y1="${CHAO + 44}" y2="${CHAO + 44}"/>
      </g>`;
  }

  function duto(x1, x2, y, h = 14) {
    return `<rect x="${x1}" y="${y}" width="${x2 - x1}" height="${h}" fill="url(#g-duto)" stroke="#999" stroke-width=".6"/>`;
  }

  // símbolo BR da Petrobras, com a mesma geometria de images/petrobras.svg;
  // ocupa a mesma caixa do desenho antigo (w de largura x 0,8w de altura), centralizado
  function logoBR(x, y, w = 30) {
    const h = w * 0.8, s = h / 63.7, dx = (w - 63.9 * s) / 2;
    return `<g transform="translate(${x + dx} ${y}) scale(${s})">
      <path fill="#f7bf21" d="M0,15.5L63.9,15.5L63.9,0L0,0Z"/>
      <path fill="#007d4f" d="M0,63.7L63.9,63.7L63.9,23.2L0,23.2Z"/>
      <path fill="#ffffff" fill-rule="evenodd" d="M63.9,23.2L63.9,15.5L0,15.5L0,23.2L12.3,23.2L5.5,46.8L19.4,46.8C25.5,46.8 26.5,45.4 27.8,44.3C29.4,43 30.3,39.7 29.5,37.4C29,35.8 27.5,34.8 27.3,34.8C29.2,33.9 30.3,32 30.4,31.7C31.1,30.2 31.7,27.6 29.9,25.5C28.5,23.7 25.7,23.2 23.6,23.2L38.6,23.2L31.7,46.8L38.6,46.8L41.2,37.9L45.1,37.9C48,37.9 47.7,39.6 47.8,40.4L48,47L54.5,47C54.5,47 54.2,39.6 54.1,39.1C54.1,37.2 52.8,36.3 51.7,36.3C53.8,35.8 55.6,33.9 56.3,32.7C57.1,31.3 57.7,29.1 56.9,26.9C55.7,23.8 52.7,23.2 50.6,23.2ZZM43.9,28L49,28C51.4,28 51.5,29.6 51.5,30C51.5,31.1 50.5,33.2 47.6,33.2L42.5,33.2C42.5,33.2 43.9,28.1 43.9,28ZM15.2,36.8L19.8,36.8C22.1,36.8 22.2,37.4 22.5,38C22.8,38.5 22.7,39.6 22.5,40C22.2,40.4 21.8,41.9 18.9,41.9L13.8,41.9C13.8,41.9 15.2,36.8 15.2,36.8ZM17.8,27.9L23.1,27.9C24.1,27.9 25.1,28.6 25.1,29.7C25.1,31.2 23.9,32.3 22.2,32.3L16.5,32.3Z"/></g>`;
  }

  function titulo(x, y, texto) {
    const linhas = texto.split("\n").map((t, i) => `<tspan x="${x}" dy="${i ? 24 : 0}">${t}</tspan>`).join("");
    return `<text x="${x}" y="${y}" font-size="22" fill="#4a4a4a" class="titulo-cena">${linhas}</text>`;
  }

  // seta horizontal com rótulo; entra animada em sequência
  function seta(x, y, w, rotulo, cor) {
    const id = `gs${nSeta}`, atraso = (0.3 + nSeta * 0.22).toFixed(2);
    nSeta++;
    const linhas = rotulo.split("\n");
    const h = 10 + 12 * linhas.length, ponta = 16;
    const pts = [
      [x, y], [x + w - ponta, y], [x + w - ponta, y - 5], [x + w, y + h / 2],
      [x + w - ponta, y + h + 5], [x + w - ponta, y + h], [x, y + h]
    ].map(p => p.join(",")).join(" ");
    const texto = linhas.map((t, i) =>
      `<tspan x="${x + 8}" dy="${i ? 12 : 0}">${t}</tspan>`).join("");
    return `<g class="seta" style="animation-delay:${atraso}s">
      <linearGradient id="${id}"><stop offset="0" stop-color="${cor}" stop-opacity="0"/><stop offset=".45" stop-color="${cor}" stop-opacity=".55"/><stop offset="1" stop-color="${cor}"/></linearGradient>
      <polygon points="${pts}" fill="url(#${id})"/>
      <text x="${x + 8}" y="${y + 15}" class="rotulo-seta">${texto}</text>
    </g>`;
  }

  // seta vertical (para baixo) com rótulo acima
  function setaBaixo(cx, y1, y2, rotulo, cor) {
    const id = `gs${nSeta}`, atraso = (0.3 + nSeta * 0.22).toFixed(2);
    nSeta++;
    const w = 34, ponta = 16;
    const pts = [
      [cx - w / 2, y1], [cx + w / 2, y1], [cx + w / 2, y2 - ponta], [cx + w / 2 + 6, y2 - ponta],
      [cx, y2], [cx - w / 2 - 6, y2 - ponta], [cx - w / 2, y2 - ponta]
    ].map(p => p.join(",")).join(" ");
    const texto = rotulo.split("\n").map((t, i) =>
      `<tspan x="${cx}" dy="${i ? 12 : 0}">${t}</tspan>`).join("");
    return `<g class="seta seta-baixo" style="animation-delay:${atraso}s">
      <linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${cor}" stop-opacity="0"/><stop offset="1" stop-color="${cor}"/></linearGradient>
      <polygon points="${pts}" fill="url(#${id})"/>
      <text x="${cx}" y="${y1 - 18}" text-anchor="middle" class="rotulo-seta">${texto}</text>
      <text x="${cx}" y="${y1 + 30}" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">+</text>
    </g>`;
  }

  // tanque de teto em cúpula
  function tanque(cx, base, w) {
    const h = w * 0.38, x = cx - w / 2, topo = base - h, pico = topo - w * 0.22;
    let linhas = "";
    for (let i = 1; i < 14; i++) linhas += `<line x1="${x + i * w / 14}" x2="${x + i * w / 14}" y1="${topo}" y2="${base}"/>`;
    let cupula = "";
    for (let i = 1; i < 6; i++) {
      const xi = x + i * w / 6;
      cupula += `<path d="M${xi},${topo} Q${(xi + cx) / 2},${pico - 4} ${cx},${pico}" fill="none"/>`;
    }
    cupula += `<path d="M${x + w * .12},${topo - w * .08} Q${cx},${pico - w * .06} ${x + w * .88},${topo - w * .08}" fill="none"/>`;
    return `<g stroke="#7a7a7a" stroke-width=".8">
      <rect x="${x}" y="${topo}" width="${w}" height="${h}" fill="#fafafa"/>
      <g stroke="#b3b3b3">${linhas}
        <line x1="${x}" x2="${x + w}" y1="${topo + h / 3}" y2="${topo + h / 3}"/>
        <line x1="${x}" x2="${x + w}" y1="${topo + 2 * h / 3}" y2="${topo + 2 * h / 3}"/>
      </g>
      <path d="M${x},${topo} Q${cx},${topo - w * 0.44} ${x + w},${topo} Z" fill="#fff"/>
      <g stroke="#b3b3b3">${cupula}</g>
    </g>`;
  }

  // tanque horizontal (cápsula) com logo
  function capsula(x, base, w, h = 58) {
    return `<g>
      <rect x="${x + 14}" y="${base - 12}" width="${w - 28}" height="12" fill="#333"/>
      <rect x="${x}" y="${base - 12 - h}" width="${w}" height="${h}" rx="${h / 2}" fill="url(#g-capsula)" stroke="#888"/>
      ${logoBR(x + w / 2 - 14, base - 12 - h / 2 - 12, 28)}
    </g>`;
  }

  function forno(cx, base) {
    return `<g>
      <rect x="${cx - 18}" y="${base - 175}" width="36" height="40" fill="url(#g-torre)" stroke="#888"/>
      <g fill="none" stroke="#999"><line x1="${cx - 18}" x2="${cx + 18}" y1="${base - 165}" y2="${base - 165}"/>
        <line x1="${cx - 18}" x2="${cx + 18}" y1="${base - 152}" y2="${base - 152}"/></g>
      <path d="M${cx - 26},${base - 135} H${cx + 26} L${cx + 46},${base - 110} H${cx - 46} Z" fill="url(#g-torre)" stroke="#888"/>
      <rect x="${cx - 52}" y="${base - 110}" width="104" height="${110}" fill="url(#g-torre)" stroke="#888"/>
      <rect x="${cx - 40}" y="${base - 90}" width="80" height="62" rx="7" fill="#5a3418" stroke="#444" stroke-width="2"/>
      <rect x="${cx - 36}" y="${base - 86}" width="72" height="54" rx="5" fill="url(#g-fogo)"/>
      <g fill="#ffd34d">
        ${[-26, -12, 2, 16, 28].map((d, i) =>
          `<path class="chama" style="animation-delay:${i * 0.13}s" d="M${cx + d - 7},${base - 32} Q${cx + d - 6},${base - 58} ${cx + d},${base - 72} Q${cx + d + 3},${base - 52} ${cx + d + 7},${base - 32} Z"/>`).join("")}
      </g>
    </g>`;
  }

  // torre de fracionamento com anéis verdes
  function torre(cx, base, h, w = 46) {
    const topo = base - h;
    const aneis = [0, 1, 2, 3].map(i => {
      const y = topo + 12 + i * 22;
      return `<rect x="${cx - w / 2 - 5}" y="${y}" width="${w + 10}" height="11" rx="5" fill="#3b6b34"/>
              <rect x="${cx - w / 2 - 5}" y="${y}" width="${w + 10}" height="3" rx="1.5" fill="#6f9c63"/>`;
    }).join("");
    let degraus = "";
    for (let y = topo + 20; y < base; y += 9) degraus += `<line x1="${cx + w / 2 + 3}" x2="${cx + w / 2 + 11}" y1="${y}" y2="${y}"/>`;
    return `<g>
      <rect x="${cx - w / 2}" y="${topo}" width="${w}" height="${h}" fill="url(#g-torre)" stroke="#888"/>
      <ellipse cx="${cx}" cy="${topo}" rx="${w / 2}" ry="5" fill="#ddd" stroke="#888"/>
      ${aneis}
      <g stroke="#777" stroke-width="1.2">
        <line x1="${cx + w / 2 + 3}" x2="${cx + w / 2 + 3}" y1="${topo + 14}" y2="${base}"/>
        <line x1="${cx + w / 2 + 11}" x2="${cx + w / 2 + 11}" y1="${topo + 14}" y2="${base}"/>
        ${degraus}
      </g>
      <rect x="${cx - w / 2 - 8}" y="${base - 6}" width="${w + 16}" height="6" fill="#999"/>
    </g>`;
  }

  // reator da unidade de craqueamento
  function reator(cx, base) {
    return `<g>
      <rect x="${cx - 46}" y="${base - 145}" width="16" height="105" rx="3" fill="#2b2b2b"/>
      <rect x="${cx - 46}" y="${base - 145}" width="70" height="10" fill="#2b2b2b"/>
      <rect x="${cx - 46}" y="${base - 55}" width="70" height="8" fill="#2b2b2b"/>
      <rect x="${cx - 24}" y="${base - 155}" width="52" height="125" rx="26" fill="url(#g-torre)" stroke="#333" stroke-width="2.5"/>
      <rect x="${cx - 8}" y="${base - 138}" width="20" height="88" rx="10" fill="#666" opacity=".55"/>
      <line x1="${cx + 2}" x2="${cx + 2}" y1="${base - 30}" y2="${base}" stroke="#444" stroke-width="5"/>
    </g>`;
  }

  function esfera(cx, cy, r) {
    const pernas = [-0.85, -0.45, 0, 0.45, 0.85].map(f =>
      `<rect x="${cx + f * r - 3}" y="${cy}" width="6" height="${CHAO - cy}" fill="#2b2b2b"/>`).join("");
    const lat = [-0.6, -0.3, 0.3, 0.6].map(f => {
      const y = cy + f * r, rx = r * Math.sqrt(1 - f * f);
      return `<ellipse cx="${cx}" cy="${y}" rx="${rx}" ry="${rx * 0.12}" fill="none"/>`;
    }).join("");
    return `<g>
      ${pernas}
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="#fafafa" stroke="#444" stroke-width="2"/>
      <g stroke="#666" stroke-width="1.1">
        <ellipse cx="${cx}" cy="${cy}" rx="${r * 0.35}" ry="${r}" fill="none"/>
        <ellipse cx="${cx}" cy="${cy}" rx="${r * 0.75}" ry="${r}" fill="none"/>
        <line x1="${cx - r}" x2="${cx + r}" y1="${cy}" y2="${cy}"/>
        ${lat}
      </g>
      <g stroke="#555" stroke-width="2" fill="none">
        <path d="M${cx - r * 0.2},${cy - r} L${cx - r * 0.2},${cy + r * 0.2}" stroke-dasharray="3 3"/>
      </g>
      ${logoBR(cx - 22, cy - r * 0.62, 44)}
    </g>`;
  }

  function roda(x, y, r = 13) {
    return `<circle cx="${x}" cy="${y}" r="${r}" fill="#1e1e1e"/><circle cx="${x}" cy="${y}" r="${r * 0.42}" fill="#ccc"/>`;
  }

  // caminhão: carga "botijoes" ou "tanque"; cabine à direita
  function caminhao(x, base, carga) {
    const comp = 230;
    let corpo;
    if (carga === "botijoes") {
      let b = "";
      for (let fila = 0; fila < 2; fila++)
        for (let i = 0; i < 9; i++) {
          const bx = x + 10 + i * 23 + fila * 6, by = base - 62 + fila * 16;
          b += `<rect x="${bx}" y="${by}" width="18" height="24" rx="7" fill="url(#g-capsula)" stroke="#777"/>`;
        }
      corpo = `${b}<rect x="${x}" y="${base - 36}" width="${comp}" height="10" fill="#2b2b2b"/>`;
    } else {
      corpo = `<rect x="${x}" y="${base - 92}" width="${comp}" height="60" rx="26" fill="url(#g-capsula)" stroke="#888"/>
        ${logoBR(x + comp / 2 - 15, base - 75, 30)}
        <rect x="${x}" y="${base - 36}" width="${comp}" height="10" fill="#2b2b2b"/>`;
    }
    const cx = x + comp + 6;
    return `<g>
      ${corpo}
      <path d="M${cx},${base - 26} V${base - 86} H${cx + 42} L${cx + 62},${base - 56} V${base - 26} Z" fill="#7d8b99" stroke="#4b5560"/>
      <path d="M${cx + 8},${base - 80} H${cx + 38} L${cx + 52},${base - 58} H${cx + 8} Z" fill="#cfe2ef"/>
      ${roda(x + 30, base - 16)}${roda(x + 60, base - 16)}${roda(x + comp - 30, base - 16)}${roda(cx + 42, base - 16)}
    </g>`;
  }

  function posto(x, base, w) {
    const topo = base - 140;
    return `<g>
      <rect x="${x + 50}" y="${topo + 26}" width="10" height="${base - topo - 26}" fill="#5e5e5e"/>
      <rect x="${x + w - 70}" y="${topo + 26}" width="10" height="${base - topo - 26}" fill="#5e5e5e"/>
      <polygon points="${x},${topo + 10} ${x + w},${topo} ${x + w},${topo + 20} ${x},${topo + 28}" fill="#008542"/>
      <polygon points="${x},${topo + 28} ${x + w},${topo + 20} ${x + w},${topo + 27} ${x},${topo + 34}" fill="#fdc82f"/>
      <polygon points="${x - 14},${topo + 12} ${x},${topo + 10} ${x},${topo + 34} ${x - 14},${topo + 32}" fill="#00602f"/>
      ${logoBR(x + 6, topo + 13, 18)}
    </g>`;
  }

  function carro(x, base) {
    return `<g>
      <path d="M${x},${base - 18} Q${x},${base - 40} ${x + 30},${base - 42} L${x + 60},${base - 64}
        Q${x + 100},${base - 72} ${x + 135},${base - 62} L${x + 165},${base - 42} Q${x + 190},${base - 40} ${x + 192},${base - 22}
        L${x + 192},${base - 14} H${x} Z" fill="#e6e6e6" stroke="#666" stroke-width="1.5"/>
      <path d="M${x + 66},${base - 60} Q${x + 100},${base - 67} ${x + 128},${base - 58} L${x + 150},${base - 42} H${x + 52} Z" fill="#cfe2ef" stroke="#888"/>
      <line x1="${x + 100}" x2="${x + 100}" y1="${base - 64}" y2="${base - 18}" stroke="#999"/>
      ${roda(x + 40, base - 12, 15)}${roda(x + 152, base - 12, 15)}
    </g>`;
  }

  function fabrica(x, base) {
    const chamines = [0, 1, 2].map(i => {
      const cx = x + 30 + i * 45;
      let faixas = "";
      for (let y = base - 175; y < base - 70; y += 12) faixas += `<line x1="${cx}" x2="${cx + 24}" y1="${y}" y2="${y}"/>`;
      return `<rect x="${cx}" y="${base - 185}" width="24" height="125" fill="#a33b2c"/>
        <rect x="${cx - 2}" y="${base - 190}" width="28" height="8" fill="#5a1d14"/>
        <g stroke="#7e2a1e" stroke-width="2">${faixas}</g>`;
    }).join("");
    return `<g>
      ${chamines}
      <rect x="${x - 10}" y="${base - 66}" width="190" height="12" fill="#1e1e1e"/>
      <rect x="${x}" y="${base - 56}" width="170" height="56" fill="#4a3a30"/>
      <g fill="#7a6555">${[0, 1, 2, 3, 4, 5].map(i => `<rect x="${x + 12 + i * 26}" y="${base - 42}" width="16" height="6"/>`).join("")}</g>
    </g>`;
  }

  function aviao(x, y) {
    return `<g>
      <path d="M${x},${y + 38} Q${x + 10},${y + 22} ${x + 40},${y + 20} H${x + 190} L${x + 230},${y - 22} H${x + 245}
        L${x + 228},${y + 22} Q${x + 248},${y + 26} ${x + 245},${y + 38} Q${x + 240},${y + 50} ${x + 220},${y + 52} H${x + 30}
        Q${x + 6},${y + 50} ${x},${y + 38} Z" fill="#fafafa" stroke="#666" stroke-width="1.5"/>
      <path d="M${x + 95},${y + 44} L${x + 150},${y + 82} H${x + 170} L${x + 140},${y + 44} Z" fill="#e6e6e6" stroke="#666"/>
      <g fill="#9bb7cc">${[0, 1, 2, 3, 4, 5, 6, 7].map(i => `<rect x="${x + 50 + i * 16}" y="${y + 28}" width="7" height="8" rx="2"/>`).join("")}</g>
      <path d="M${x + 6},${y + 34} Q${x + 14},${y + 25} ${x + 26},${y + 25} V${y + 34} Z" fill="#9bb7cc"/>
      <rect x="${x + 120}" y="${y + 58}" width="36" height="16" rx="8" fill="#ddd" stroke="#666"/>
      ${roda(x + 40, y + 62, 6)}${roda(x + 180, y + 62, 6)}
    </g>`;
  }

  function mar(y) {
    let crista = "", crista2 = "";
    for (let x = -60; x < L + 60; x += 60) {
      crista += `Q${x + 15},${y - 14} ${x + 30},${y} Q${x + 45},${y - 14} ${x + 60},${y} `;
      crista2 += `Q${x + 15},${y + 2} ${x + 30},${y + 14} Q${x + 45},${y + 2} ${x + 60},${y + 14} `;
    }
    return `<g>
      <rect x="0" y="${y}" width="${L}" height="${A - y}" fill="url(#g-mar)"/>
      <path class="onda" d="M-60,${y} ${crista} V${A} H-60 Z" fill="#8cc6e6"/>
      <path class="onda lenta" d="M-60,${y + 14} ${crista2} V${A} H-60 Z" fill="#5d9fcb"/>
    </g>`;
  }

  function sinal(x, y, ang = 0) {
    return `<g transform="translate(${x},${y}) rotate(${ang})" fill="none" stroke-linecap="round">
      <path class="sinal" d="M-28,0 A30,30 0 0 0 28,0" stroke="#3a7fd0" stroke-width="7"/>
      <path class="sinal s2" d="M-48,6 A52,52 0 0 0 48,6" stroke="#a9d3cf" stroke-width="7"/>
    </g>`;
  }

  function satelite(x, y) {
    const painel = (px) => `<g transform="translate(${px},0)">
        <rect x="0" y="-9" width="44" height="18" fill="#555" stroke="#222"/>
        <g stroke="#999">${[11, 22, 33].map(i => `<line x1="${i}" x2="${i}" y1="-9" y2="9"/>`).join("")}<line x1="0" x2="44" y1="0" y2="0"/></g>
      </g>`;
    return `<g transform="translate(${x},${y}) rotate(12)">
      ${painel(-62)}${painel(18)}
      <rect x="-18" y="-3" width="36" height="6" fill="#888"/>
      <circle r="15" fill="#666" stroke="#222" stroke-width="2"/>
      <circle r="6" fill="#999"/>
    </g>`;
  }

  // ---------- cenas ----------

  const desenhos = {
    1: () => `
      ${sinal(40, 250, 205)}
      ${satelite(660, 70)}
      ${sinal(600, 140, 15)}
      ${duto(270, 540, 268, 16)}
      <ellipse cx="500" cy="276" rx="16" ry="6" fill="#333"/>
      <rect x="520" y="248" width="${L - 520}" height="70" fill="url(#g-metal)" stroke="#777"/>
      ${tanque(640, 250, 150)}
      ${mar(300)}
      <polygon points="0,262 185,262 158,330 0,330" fill="#111"/>
      <rect x="0" y="256" width="150" height="8" fill="#5a2c16"/>
      <rect x="200" y="262" width="62" height="70" fill="#111"/>
      <path d="M150,262 Q200,200 238,262" fill="none" stroke="#a8322a" stroke-width="12" stroke-dasharray="4 2"/>
      <text x="40" y="250" class="rotulo-seta">Petroleiro</text>
      <text x="231" y="356" class="rotulo-seta" text-anchor="middle" style="fill:#fff">Monobóia</text>
      <text x="330" y="262" class="rotulo-seta">Oleoduto</text>
      <text x="650" y="292" class="rotulo-seta" text-anchor="middle">Tanque de petróleo</text>`,

    2: () => `
      ${duto(0, 560, 296)}
      ${tanque(190, CHAO, 180)}
      ${forno(390, CHAO)}
      ${torre(570, CHAO, 235)}
      ${titulo(530, 46, "Unidade de\nDestilação")}
      ${seta(608, 98, 160, "GLP", "#4a90d9")}
      ${seta(608, 136, 160, "Nafta leve", "#35c49a")}
      ${seta(608, 174, 160, "Nafta pesada", "#8c8a5a")}
      ${seta(608, 212, 160, "Querosene", "#a07a70")}
      ${seta(608, 250, 160, "Diesel", "#c9b46a")}
      ${seta(608, 288, 160, "RAT", "#6f7f8f")}`,

    3: () => `
      ${duto(260, 560, 296)}
      ${seta(30, 230, 250, "Resíduo atmosférico", "#8c8c8c")}
      ${forno(400, CHAO)}
      ${torre(570, CHAO, 235)}
      ${titulo(530, 46, "Unidade a\nVácuo")}
      ${seta(608, 180, 160, "Diesel pesado", "#8c8a5a")}
      ${seta(608, 225, 160, "Gasóleo", "#a07a70")}
      ${seta(608, 270, 160, "RV", "#5f7f99")}`,

    4: () => `
      ${duto(250, 560, 296)}
      ${seta(80, 230, 200, "Gasóleo", "#8c8c8c")}
      ${reator(380, CHAO)}
      ${torre(570, CHAO, 235)}
      ${titulo(530, 46, "Unidade de\nCraqueamento")}
      ${seta(608, 160, 160, "GLP (2)", "#35c49a")}
      ${seta(608, 205, 160, "Nafta craqueada", "#8c8a5a")}
      ${seta(608, 250, 160, "Diluente para\nóleo combustível", "#a07a70")}`,

    5: () => `
      ${duto(0, 780, 300)}
      ${seta(10, 200, 200, "GLP (destilação)", "#35b5c4")}
      ${seta(10, 246, 200, "GLP (craqueamento)", "#4a90d9")}
      ${esfera(330, 210, 95)}
      ${caminhao(490, CHAO + 10, "botijoes")}
      ${titulo(560, 205, "Distribuidora")}`,

    6: () => `
      ${duto(0, 780, 300)}
      ${titulo(40, 205, "Unidade de\nDesasfaltação")}
      ${seta(10, 262, 190, "Resíduo de vácuo", "#7a9a3c")}
      ${torre(250, CHAO, 200)}
      ${setaBaixo(440, 200, 248, "Diluente para óleo\ncombustível (craqueamento)", "#4a90d9")}
      ${seta(290, 252, 130, "Resíduo\nasfáltico", "#a0624a")}
      ${seta(425, 252, 160, "Matéria-prima", "#a0624a")}
      ${fabrica(600, CHAO)}
      ${titulo(610, 128, "Fosfértil")}`,

    7: () => `
      ${duto(0, 470, 300)}
      ${seta(10, 210, 210, "Nafta leve (destilação)", "#e0883a")}
      ${seta(10, 258, 210, "Nafta craqueada", "#7d93a3")}
      ${capsula(240, CHAO + 4, 170)}
      ${posto(470, CHAO, 300)}
      ${carro(560, CHAO + 14)}
      ${titulo(250, 228, "Gasolina A")}`,

    8: () => `
      ${duto(0, 780, 300)}
      ${seta(10, 248, 150, "Diesel pesado", "#7a9a3c")}
      ${torre(205, CHAO, 190)}
      ${seta(240, 195, 130, "Diesel leve", "#35c49a")}
      ${seta(240, 235, 130, "Nafta pesada", "#8c8a5a")}
      ${seta(240, 275, 130, "Querosene", "#a07a70")}
      <path d="M380,192 V302" stroke="#555" stroke-width="2" stroke-dasharray="3 3"/>
      <text x="388" y="200" class="rotulo-seta" font-weight="700">Mistura</text>
      ${seta(388, 210, 200, "Diesel para uso em motores", "#c9b46a")}
      ${posto(610, CHAO, 160)}
      ${caminhao(420, CHAO + 12, "tanque")}`,

    9: () => `
      ${duto(0, 560, 300)}
      ${seta(10, 252, 190, "Querosene (destilação)", "#d06a4a")}
      ${torre(230, CHAO, 190)}
      ${seta(264, 252, 120, "QAV-1", "#c9935a")}
      ${capsula(390, CHAO + 4, 140)}
      ${aviao(535, 228)}
      ${titulo(560, 200, "Para uso em aeronaves")}`,

    10: () => `
      ${duto(0, 780, 300)}
      ${seta(10, 258, 230, "Nafta leve (destilação)", "#e0883a")}
      ${torre(280, CHAO, 210)}
      ${seta(318, 210, 190, "Nafta peróxida", "#3a4a5a")}
      ${seta(318, 258, 190, "Solvente de borracha", "#d98a3a")}
      ${tanque(640, CHAO, 170)}
      ${titulo(560, 186, "Unidade de\nSolvente")}`
  };

  function desenhar(etapa) {
    nSeta = 0;
    return `<svg viewBox="0 0 ${L} ${A}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
      ${defs}${fundo()}${desenhos[etapa]()}
    </svg>`;
  }

  // técnico da refinaria que "apresenta" o jogo: chapéu marrom, headset vermelho com microfone,
  // camisa social cinza-azulada com crachá, mão direita apontando para cima.
  // cada cópia do personagem usa IDs próprios: um SVG oculto com o mesmo ID quebraria os gradientes do outro
  let nPersonagem = 0;
  function personagem() {
    const id = `pers${++nPersonagem}`;
    return `<svg viewBox="0 0 300 450" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="${id}-camisa" x1="0" x2="1">
          <stop offset="0" stop-color="#a3aed3"/><stop offset=".6" stop-color="#97a3cb"/><stop offset="1" stop-color="#8391bc"/>
        </linearGradient>
        <linearGradient id="${id}-chapeu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#9a6438"/><stop offset="1" stop-color="#7d4c28"/>
        </linearGradient>
      </defs>

      <g stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
        <!-- calça e cinto -->
        <path d="M54,398 H208 L214,450 H48 Z" fill="#232323"/>
        <path d="M74,412 Q90,420 96,440 M188,412 Q172,420 166,440" fill="none" stroke="#444" stroke-width="2"/>

        <!-- braço esquerdo (caído ao lado do corpo) -->
        <path d="M44,222 Q20,232 16,276 L8,424 Q28,432 54,428 L58,300 Z" fill="url(#${id}-camisa)"/>
        <path d="M8,422 L54,426 L52,448 L6,446 Z" fill="#8f9bc4"/>
        <circle cx="14" cy="437" r="3" fill="#fff" stroke="none"/>
        <path d="M30,270 Q28,330 30,400" fill="none" stroke="#7f8bb5" stroke-width="2.5"/>

        <!-- tronco -->
        <path d="M44,222 Q72,210 98,200 L121,224 L146,200 Q176,208 200,216 Q210,240 208,300 L206,390 H56 L54,300 Q50,250 44,222 Z"
              fill="url(#${id}-camisa)"/>
        <path d="M121,224 V390" fill="none" stroke-width="2.4"/>
        <g fill="#fff" stroke="none">
          <circle cx="127" cy="242" r="3.5"/><circle cx="127" cy="282" r="3.5"/>
          <circle cx="127" cy="322" r="3.5"/><circle cx="127" cy="362" r="3.5"/>
        </g>
        <path d="M74,250 Q70,320 76,388" fill="none" stroke="#8391bc" stroke-width="2"/>

        <!-- crachá com prendedor -->
        <rect x="158" y="240" width="10" height="14" rx="2" fill="#f2f2f2" stroke-width="2"/>
        <rect x="145" y="253" width="40" height="28" rx="3" fill="#fff"/>
        <path d="M147,255 H183 V266 H147 Z" fill="#4caf50" stroke="none"/>

        <!-- cinto -->
        <rect x="54" y="386" width="154" height="16" rx="2" fill="#141414"/>
        <rect x="113" y="385" width="30" height="18" rx="2" fill="#f5c518"/>

        <!-- pescoço e gola -->
        <path d="M100,150 V198 L121,224 L144,198 V150 Z" fill="#e3ad85"/>
        <path d="M100,186 Q121,200 144,186" fill="none" stroke="#c98f68" stroke-width="2"/>
        <path d="M98,194 L82,210 L94,236 L121,224 Z" fill="#a9b3d8"/>
        <path d="M146,194 L162,210 L150,236 L121,224 Z" fill="#a9b3d8"/>

        <!-- braço direito: sobe do cotovelo até a mão apontando -->
        <path d="M196,208 Q222,214 225,240 L234,307 L245,278 L271,288 L239,370 Q228,382 212,368 L192,250 Q190,226 196,208 Z"
              fill="url(#${id}-camisa)"/>
        <path d="M210,250 Q214,300 222,350" fill="none" stroke="#7f8bb5" stroke-width="2.2"/>
        <path d="M245,278 L271,288 L267,300 L241,290 Z" fill="#8f9bc4"/>
        <circle cx="262" cy="293" r="2.6" fill="#fff" stroke="none"/>
      </g>

      <!-- mão (balança no pulso) -->
      <g class="mao" stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
        <path d="M246,280 Q234,262 244,246 Q250,236 264,236 L281,202 Q287,190 295,195 Q301,201 295,211 L281,240
                 Q293,247 291,263 Q289,282 271,289 Z" fill="#f2c29a"/>
        <path d="M262,250 Q272,246 279,252 M260,262 Q270,258 281,264 M262,273 Q270,271 277,277" fill="none" stroke-width="2.4"/>
        <path d="M247,252 Q256,245 266,252" fill="none" stroke-width="2.4"/>
      </g>

      <!-- cabeça -->
      <g stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
        <ellipse cx="66" cy="116" rx="10" ry="15" fill="#e8b48c"/>
        <ellipse cx="178" cy="116" rx="10" ry="15" fill="#e8b48c"/>
        <path d="M74,66 Q70,150 98,168 Q122,182 146,168 Q174,150 170,66 Z" fill="#f2c29a"/>
      </g>
      <!-- cabelo nas laterais -->
      <path d="M72,64 Q66,96 76,120 L82,86 Z M172,64 Q178,96 168,120 L162,86 Z" fill="#5a3a22"/>
      <!-- sobrancelhas e olhos -->
      <path d="M90,86 Q103,77 117,83 M128,83 Q142,77 155,86" fill="none" stroke="#3b2416" stroke-width="5.5" stroke-linecap="round"/>
      <g stroke="#1a1a1a" stroke-width="2.5">
        <ellipse cx="105" cy="105" rx="13" ry="14" fill="#fff"/>
        <ellipse cx="142" cy="105" rx="13" ry="14" fill="#fff"/>
      </g>
      <circle class="olho" cx="109" cy="104" r="6" fill="#111"/>
      <circle class="olho" cx="145" cy="104" r="6" fill="#111"/>
      <circle cx="111" cy="101.5" r="1.8" fill="#fff"/><circle cx="147" cy="101.5" r="1.8" fill="#fff"/>
      <!-- nariz -->
      <path d="M124,110 Q119,124 117,130 Q123,137 132,131" fill="none" stroke="#c98f68" stroke-width="2.6" stroke-linecap="round"/>
      <!-- sorriso aberto -->
      <path d="M99,142 Q122,148 148,140 Q145,166 122,168 Q102,166 99,142 Z" fill="#8b1e1e" stroke="#1a1a1a" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M102,144 Q122,149 145,142 L143,150 Q122,155 104,151 Z" fill="#fff"/>
      <path d="M110,160 Q122,153 136,159 Q129,166 122,166 Q114,166 110,160 Z" fill="#e57373"/>

      <!-- headset vermelho com microfone -->
      <g fill="none" stroke-linecap="round">
        <path d="M68,124 Q70,160 96,176" stroke="#1a1a1a" stroke-width="6.5"/>
        <path d="M68,124 Q70,160 96,176" stroke="#e01b1b" stroke-width="3.5"/>
        <path d="M176,124 Q174,160 150,174" stroke="#1a1a1a" stroke-width="6.5"/>
        <path d="M176,124 Q174,160 150,174" stroke="#e01b1b" stroke-width="3.5"/>
        <path d="M94,176 L117,181" stroke="#222" stroke-width="4"/>
      </g>
      <g stroke="#1a1a1a" stroke-width="2">
        <rect x="62" y="108" width="10" height="16" rx="3" fill="#e01b1b"/>
        <rect x="172" y="108" width="10" height="16" rx="3" fill="#e01b1b"/>
        <ellipse cx="120" cy="181.5" rx="6" ry="4" fill="#2a2a2a"/>
      </g>

      <!-- chapéu -->
      <g stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round">
        <path d="M26,76 Q34,54 92,51 Q122,49 152,51 Q210,54 218,76 Q206,80 176,72 Q122,63 68,72 Q38,80 26,76 Z" fill="url(#${id}-chapeu)"/>
        <path d="M70,60 Q70,22 98,11 Q122,2 148,11 Q174,22 174,60 Q122,68 70,60 Z" fill="url(#${id}-chapeu)"/>
        <path d="M70,50 Q122,58 174,50 L174,60 Q122,68 70,60 Z" fill="#5e3a20"/>
      </g>
      <path d="M100,16 Q122,26 144,16" fill="none" stroke="#6a4024" stroke-width="3" stroke-linecap="round"/>
      <path d="M84,40 Q88,22 104,14" fill="none" stroke="#b47a4c" stroke-width="3" stroke-linecap="round" opacity=".7"/>
    </svg>`;
  }

  return { desenhar, personagem };
})();
