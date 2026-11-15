(function(){
 const L = d3.formatLocale({decimal: '.', thousands: ',', grouping: [3], currency: ['RD$', '']});
 const TN = {Manana: 'Mañana', Tarde: 'Tarde', Noche: 'Noche'};
 const ORD = ['Manana', 'Tarde', 'Noche'];
 const T = {
  int: L.format(',.0f'), num1: L.format(',.1f'), dec2: L.format(',.2f'), pct: L.format('.1%'), pct2: L.format('.2%'),
  turno: v => TN[v] || String(v),
  combo: v => String(v).replace(/Planta /g, '').replace(/Manana/g, 'Mañana')
 };
 const C = i => (dash.colors || [])[i] || (dash.colors || [])[0];
 window.icTpMetric = window.icTpMetric || 'cumplimiento';

 function agg(produccion, keyf){
  const m = {};
  produccion.forEach(r => {
   const k = keyf(r);
   const o = m[k.id] || (m[k.id] = {...k.cols, lotes: 0, producidas: 0, planificadas: 0, defectuosas: 0, costo: 0, lotes_ok: 0});
   const p = +r.UnidadesProducidas || 0, pl = +r.UnidadesPlanificadas || 0;
   o.lotes += 1; o.producidas += p; o.planificadas += pl; o.defectuosas += +r.UnidadesDefectuosas || 0; o.costo += +r.CostoProduccion_DOP || 0;
   if (p >= pl) o.lotes_ok += 1;
  });
  const tot = Object.values(m).reduce((s, o) => s + o.producidas, 0);
  return Object.values(m).map(o => ({...o, costo: Math.round(o.costo * 100) / 100, buenas: o.producidas - o.defectuosas, share: o.producidas / tot,
   cumplimiento: o.producidas / o.planificadas, pct_defect: o.defectuosas / o.producidas, por_lote: o.producidas / o.lotes,
   pct_lotes_ok: o.lotes_ok / o.lotes}));
 }

 dash.calc('turno', {inputs: ['produccion'], title: 'Producción por turno', description: 'Por turno: lotes, unidades producidas, planificadas y defectuosas, y sus proporciones.',
  fn: (produccion) => agg(produccion, r => ({id: r.Turno, cols: {Turno: r.Turno}})).sort((a, b) => b.producidas - a.producidas)});

 dash.calc('turno_planta', {inputs: ['produccion'], title: 'Producción por planta y turno', description: 'Las mismas medidas por turno, separadas por planta.',
  fn: (produccion) => agg(produccion, r => ({id: r.Planta + '|' + r.Turno, cols: {Planta: r.Planta, Turno: r.Turno}}))});

 dash.calc('turno_dest', {inputs: ['turno', 'turno_planta'], title: 'Turnos destacados', description: 'Turno líder en volumen, cumplimiento, calidad y unidades por lote, y la mejor y peor combinación planta-turno.',
  fn: (turno, turno_planta) => {
   if (!turno || !turno.length || !turno_planta || !turno_planta.length) return [];
   const by = (a, k, dir) => a.reduce((b, r) => (dir * (r[k] - b[k]) > 0 ? r : b));
   const v = by(turno, 'producidas', 1), c = by(turno, 'cumplimiento', 1), cw = by(turno, 'cumplimiento', -1);
   const d = by(turno, 'pct_defect', -1), l = by(turno, 'por_lote', 1);
   const pb = by(turno_planta, 'cumplimiento', 1), pw = by(turno_planta, 'cumplimiento', -1);
   return [{mayor_vol: v.Turno, vol: v.producidas, share_vol: v.share, lotes_vol: v.lotes, lotes_prom: d3.mean(turno, r => r.lotes),
    mejor_cump: c.Turno, cump_mejor: c.cumplimiento, peor_cump: cw.Turno, cump_peor: cw.cumplimiento, dif_cump_pp: (c.cumplimiento - cw.cumplimiento) * 100,
    menor_def: d.Turno, def_menor: d.pct_defect, mejor_lote: l.Turno, lote_mejor: l.por_lote,
    combo_mejor: pb.Planta + ' · ' + pb.Turno, combo_cump: pb.cumplimiento, combo_peor: pw.Planta + ' · ' + pw.Turno, combo_peor_cump: pw.cumplimiento}];
  }});

 dash.draw('tnum', el => {
  const d = dash.data(el.dataset.source);
  const w = el.dataset.where;
  const match = r => w.split('&').every(p => { const [k, v] = p.split('=').map(decodeURIComponent); return String(r[k]) === v; });
  const row = d.status === 'ok' && Array.isArray(d.data) ? (w ? d.data.find(match) : d.data[+el.dataset.row || 0]) : null;
  const v = row ? row[el.dataset.field] : null;
  el.classList.toggle('dash-skeleton', d.status === 'loading');
  el.textContent = v == null || v === '' ? '—' : (T[el.dataset.fmt] || String)(v);
 });

 function mount(el){
  const box = document.createElement('div'); box.style.position = 'relative';
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('width', '100%'); svg.setAttribute('role', 'img');
  const tip = document.createElement('div'); tip.className = 'ic-tip'; tip.hidden = true;
  box.append(svg, tip); el.appendChild(box);
  return {box, svg: d3.select(svg), tip};
 }
 function textW(svg, labels){
  const g = svg.append('g'); let w = 0;
  labels.forEach(l => { const t = g.append('text').attr('class', 'ic-vl').text(l); w = Math.max(w, t.node().getComputedTextLength()); });
  g.remove(); return w;
 }
 function tip(made, head, items, x, y){
  const t = made.tip, W = made.box.clientWidth;
  const h = document.createElement('div'); h.className = 'ic-tip-h'; h.textContent = head;
  t.replaceChildren(h, ...items.map(([lab, val]) => { const d = document.createElement('div'); const s = document.createElement('span'); s.className = 'ic-tip-s'; s.textContent = lab + ': '; d.append(s, document.createTextNode(val)); return d; }));
  t.hidden = false;
  t.style.left = Math.max(0, Math.min(W - t.offsetWidth, x - t.offsetWidth / 2)) + 'px';
  t.style.top = Math.max(0, y - t.offsetHeight - 12) + 'px';
 }
 function empty(made, d){
  made.svg.selectAll('*').remove(); made.tip.hidden = true;
  if (d.status === 'ok' && Array.isArray(d.data) && d.data.length) return false;
  made.svg.attr('viewBox', '0 0 300 60').attr('height', 60);
  made.svg.append('text').attr('class', 'ic-vl').attr('x', 0).attr('y', 30).text(d.status === 'error' ? 'No se pudo cargar' : '—');
  return true;
 }
 function grid(svg, x, H, mT, mB, ticks, fmt){
  svg.append('g').attr('transform', `translate(0,${H - mB})`).call(d3.axisBottom(x).ticks(ticks).tickFormat(fmt).tickSize(-(H - mB - mT)))
   .call(g => g.select('.domain').remove()).call(g => g.selectAll('.tick line').attr('stroke', 'var(--cds-chart-grid)'));
 }

 dash.draw('tvol', {mount, update(el, made){
  const d = dash.data('turno');
  if (empty(made, d)) return;
  const rows = d.data, W = made.box.clientWidth || 500, rowH = 50, mT = 6, mB = 26, H = mT + mB + rows.length * rowH;
  made.svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H).attr('aria-label', 'Unidades producidas y planificadas por turno');
  const mL = Math.ceil(textW(made.svg, rows.map(r => T.turno(r.Turno)))) + 12;
  const endW = Math.ceil(textW(made.svg, rows.map(r => T.int(r.producidas)))) + 10;
  const x = d3.scaleLinear().domain([0, d3.max(rows, r => Math.max(r.producidas, r.planificadas))]).nice().range([mL, W - endW]);
  const y = d3.scaleBand().domain(rows.map(r => r.Turno)).range([mT, H - mB]).padding(0.25);
  grid(made.svg, x, H, mT, mB, W < 420 ? 3 : 4, v => v >= 1e3 ? T.int(v / 1e3) + ' mil' : T.int(v));
  const s = made.svg;
  s.append('g').selectAll('text').data(rows).join('text').attr('class', 'ic-vl').attr('x', mL - 8).attr('y', r => y(r.Turno) + y.bandwidth() / 2).attr('dy', '0.35em').attr('text-anchor', 'end').text(r => T.turno(r.Turno));
  s.append('g').selectAll('rect').data(rows).join('rect').attr('x', mL).attr('y', r => y(r.Turno)).attr('height', y.bandwidth()).attr('width', r => x(r.planificadas) - mL).attr('rx', 2).style('fill', 'var(--cds-chart-muted)');
  const inner = y.bandwidth() * 0.56;
  s.append('g').selectAll('rect').data(rows).join('rect').attr('x', mL).attr('y', r => y(r.Turno) + (y.bandwidth() - inner) / 2).attr('height', inner).attr('width', r => x(r.producidas) - mL).attr('rx', 2).style('fill', C(0));
  s.append('g').selectAll('text').data(rows).join('text').attr('class', 'ic-vl').attr('x', r => x(Math.max(r.producidas, r.planificadas)) + 4).attr('y', r => y(r.Turno) + y.bandwidth() / 2).attr('dy', '0.35em').text(r => T.int(r.producidas));
  s.append('g').selectAll('rect').data(rows).join('rect').attr('x', 0).attr('width', W).attr('y', r => y(r.Turno) - y.step() * y.paddingInner() / 2).attr('height', y.step()).attr('fill', 'transparent')
   .on('pointerenter pointermove', (ev, r) => { const [px, py] = d3.pointer(ev, made.box); tip(made, 'Turno ' + T.turno(r.Turno), [['Producidas', T.int(r.producidas)], ['Planificadas', T.int(r.planificadas)], ['Cumplimiento', T.pct(r.cumplimiento)], ['Lotes', T.int(r.lotes)]], px, py); })
   .on('pointerleave', () => { made.tip.hidden = true; });
 }});

 dash.draw('tplanta', {mount, update(el, made){
  const d = dash.data('turno_planta');
  if (empty(made, d)) return;
  const M = {cumplimiento: ['Cumplimiento del plan', T.pct], pct_defect: ['% defectuosas', T.pct2], por_lote: ['Unidades por lote', T.num1], producidas: ['Unidades producidas', T.int]};
  const k = M[window.icTpMetric] ? window.icTpMetric : 'cumplimiento';
  const [mlab, mf] = M[k];
  const rows = d.data, plantas = [...new Set(rows.map(r => r.Planta))].sort();
  const turnos = ORD.filter(t => rows.some(r => r.Turno === t)).concat([...new Set(rows.map(r => r.Turno))].filter(t => !ORD.includes(t)));
  const W = made.box.clientWidth || 500, rowH = 64, mT = 8, mB = 26, H = mT + mB + turnos.length * rowH;
  made.svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H).attr('aria-label', mlab + ' por planta y turno');
  const half = Math.ceil(textW(made.svg, rows.map(r => mf(r[k]))) / 2) + 4;
  const mL = Math.ceil(textW(made.svg, turnos.map(T.turno))) + 12 + half, mR = half + 4;
  const vals = rows.map(r => r[k]); let lo = d3.min(vals), hi = d3.max(vals);
  const pad = (hi - lo) * 0.2 || Math.abs(hi) * 0.05 || 1;
  const x = d3.scaleLinear().domain([lo - pad, hi + pad]).nice().range([mL, W - mR]);
  const y = d3.scaleBand().domain(turnos).range([mT, H - mB]).padding(0.1);
  grid(made.svg, x, H, mT, mB, W < 420 ? 3 : 4, mf);
  const s = made.svg, cy = t => y(t) + y.bandwidth() / 2;
  s.append('g').selectAll('text').data(turnos).join('text').attr('class', 'ic-vl').attr('x', mL - 8 - half).attr('y', cy).attr('dy', '0.35em').attr('text-anchor', 'end').text(T.turno);
  turnos.forEach(t => {
   const rs = rows.filter(r => r.Turno === t);
   if (rs.length > 1) s.append('line').attr('x1', x(d3.min(rs, r => r[k]))).attr('x2', x(d3.max(rs, r => r[k]))).attr('y1', cy(t)).attr('y2', cy(t)).style('stroke', 'var(--cds-chart-muted)').attr('stroke-width', 3);
   rs.forEach(r => {
    const i = plantas.indexOf(r.Planta);
    s.append('circle').attr('cx', x(r[k])).attr('cy', cy(t)).attr('r', 6).style('fill', C(i));
    s.append('text').attr('class', 'ic-vl').attr('text-anchor', 'middle').attr('x', x(r[k])).attr('y', cy(t) + (i % 2 ? 20 : -11)).attr('dy', i % 2 ? '0.35em' : 0).text(mf(r[k]));
   });
  });
  s.append('g').selectAll('rect').data(turnos).join('rect').attr('x', 0).attr('width', W).attr('y', t => y(t)).attr('height', y.bandwidth()).attr('fill', 'transparent')
   .on('pointerenter pointermove', (ev, t) => { const [px, py] = d3.pointer(ev, made.box); tip(made, 'Turno ' + T.turno(t) + ' · ' + mlab, rows.filter(r => r.Turno === t).sort((a, b) => a.Planta < b.Planta ? -1 : 1).map(r => [T.combo(r.Planta), mf(r[k])]), px, py); })
   .on('pointerleave', () => { made.tip.hidden = true; });
 }});

 dash.draw('ttabla', tb => {
  const d = dash.data('turno');
  const rows = d.status === 'ok' && Array.isArray(d.data) ? d.data : [];
  const cols = [['Turno', T.turno], ['lotes', T.int], ['producidas', T.int], ['share', T.pct], ['planificadas', T.int], ['cumplimiento', T.pct], ['pct_defect', T.pct2], ['buenas', T.int], ['por_lote', T.num1], ['pct_lotes_ok', T.pct]];
  tb.replaceChildren(...rows.map(r => {
   const tr = document.createElement('tr'); tr.dataset.key = encodeURIComponent(r.Turno);
   cols.forEach(([k, f]) => { const td = document.createElement('td'); td.textContent = r[k] == null ? '—' : f(r[k]); tr.appendChild(td); });
   return tr;
  }));
 });

 document.querySelectorAll('#tp-metric').forEach(sel => sel.addEventListener('change', () => { window.icTpMetric = sel.value; dash.draw('tplanta'); }));
})();
