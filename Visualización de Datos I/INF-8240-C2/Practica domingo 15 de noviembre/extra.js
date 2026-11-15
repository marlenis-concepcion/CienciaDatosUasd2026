(function(){
 const L = d3.formatLocale({decimal: '.', thousands: ',', grouping: [3], currency: ['RD$', '']});
 const MES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
 const MESL = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
 const f0 = L.format(',.0f'), f1 = L.format(',.1f'), f2 = L.format(',.2f');
 const T = {
  int: v => f0(v), num1: v => f1(v), pct: L.format('.1%'), pct2: L.format('.2%'), rd2: v => 'RD$' + f2(v),
  money: v => 'RD$' + f2(v / 1e6) + ' M',
  short: v => Math.abs(v) >= 1e6 ? f1(v / 1e6) + ' M' : Math.abs(v) >= 1e3 ? f0(v / 1e3) + ' mil' : f0(v),
  mes: s => MESL[+String(s).slice(5, 7) - 1] || String(s),
  mesc: s => MES[+String(s).slice(5, 7) - 1] || String(s)
 };
 const C = i => (dash.colors || [])[i] || (dash.colors || [])[0];
 const r2 = v => Math.round(v * 100) / 100;
 const mesOf = r => String(r.Fecha).slice(0, 7);

 function ventasPor(ventas, key){
  const m = new Map();
  ventas.forEach(r => { const k = r[key]; if (!m.has(k)) m.set(k, []); m.get(k).push(r); });
  const tot = d3.sum(ventas, r => +r.IngresoNeto_DOP || 0);
  return Array.from(m, ([k, rs]) => {
   const ing = d3.sum(rs, r => +r.IngresoNeto_DOP || 0);
   return {[key]: k, ingreso: r2(ing), vendidas: d3.sum(rs, r => +r.Unidades || 0), transacciones: rs.length, share: ing / tot, ticket: ing / rs.length};
  }).sort((a, b) => b.ingreso - a.ingreso);
 }

 dash.calc('ex_region', {inputs: ['ventas'], title: 'Ventas por región', description: 'Ingreso neto, unidades y transacciones por región.',
  fn: (ventas) => ventasPor(ventas, 'Region')});
 dash.calc('ex_canal', {inputs: ['ventas'], title: 'Ventas por canal', description: 'Ingreso neto, unidades y transacciones por canal de venta.',
  fn: (ventas) => ventasPor(ventas, 'Canal')});
 dash.calc('ex_desc', {inputs: ['ventas'], title: 'Ventas por nivel de descuento', description: 'Ingreso neto, unidades y ticket promedio según el descuento aplicado.',
  fn: (ventas) => ventasPor(ventas, 'DescuentoPct').map(r => ({...r, Descuento: Math.round(+r.DescuentoPct * 100) + '%'})).sort((a, b) => +a.DescuentoPct - +b.DescuentoPct)});

 dash.calc('ex_prod_mes', {inputs: ['ventas'], title: 'Unidades vendidas por producto y mes', description: 'Suma de unidades vendidas e ingreso neto por producto y mes.',
  fn: (ventas) => {
   const m = new Map();
   ventas.forEach(r => {
    const k = r.Producto + '|' + mesOf(r);
    const o = m.get(k) || {Producto: r.Producto, mes: mesOf(r), vendidas: 0, ingreso: 0};
    o.vendidas += +r.Unidades || 0; o.ingreso += +r.IngresoNeto_DOP || 0; m.set(k, o);
   });
   return [...m.values()].map(o => ({...o, ingreso: r2(o.ingreso)})).sort((a, b) => a.Producto < b.Producto ? -1 : a.Producto > b.Producto ? 1 : (a.mes < b.mes ? -1 : 1));
  }});

 dash.calc('ex_turno_mes', {inputs: ['produccion'], title: 'Unidades producidas por mes y turno', description: 'Suma de unidades producidas por mes en cada turno.',
  fn: (produccion) => {
   const m = new Map();
   produccion.forEach(r => {
    const k = mesOf(r);
    const o = m.get(k) || {mes: k, Manana: 0, Tarde: 0, Noche: 0};
    o[r.Turno] = (o[r.Turno] || 0) + (+r.UnidadesProducidas || 0); m.set(k, o);
   });
   return [...m.values()].sort((a, b) => a.mes < b.mes ? -1 : 1);
  }});

 dash.calc('ex_planta_mes', {inputs: ['produccion'], title: 'Cumplimiento del plan por mes y planta', description: 'Unidades producidas ÷ planificadas por mes en cada planta.',
  fn: (produccion) => {
   const m = new Map();
   produccion.forEach(r => {
    const k = mesOf(r), p = /Santiago/.test(r.Planta) ? 'santiago' : 'santo_domingo';
    const o = m.get(k) || {mes: k, santiago_p: 0, santiago_pl: 0, santo_domingo_p: 0, santo_domingo_pl: 0};
    o[p + '_p'] += +r.UnidadesProducidas || 0; o[p + '_pl'] += +r.UnidadesPlanificadas || 0; m.set(k, o);
   });
   return [...m.values()].map(o => ({mes: o.mes, santiago: o.santiago_p / o.santiago_pl, santo_domingo: o.santo_domingo_p / o.santo_domingo_pl})).sort((a, b) => a.mes < b.mes ? -1 : 1);
  }});

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
 const gridLines = g => { g.select('.domain').remove(); g.selectAll('.tick line').attr('stroke', 'var(--cds-chart-grid)'); };

 // Barras horizontales: una barra por categoría, valor al final.
 function hbar(id, src, o){
  dash.draw(id, {mount, update(el, made){
   const d = dash.data(src);
   if (empty(made, d)) return;
   let rows = d.data.slice(); if (o.sort) rows.sort(o.sort);
   const W = made.box.clientWidth || 400, rowH = 36, mT = 4, mB = 24, H = mT + mB + rows.length * rowH;
   made.svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H).attr('aria-label', o.aria);
   const mL = Math.ceil(textW(made.svg, rows.map(r => r[o.label]))) + 12;
   const endW = Math.ceil(textW(made.svg, rows.map(r => o.vfmt(r[o.key])))) + 10;
   const x = d3.scaleLinear().domain([0, d3.max(rows, r => r[o.key])]).nice().range([mL, W - endW]);
   const y = d3.scaleBand().domain(rows.map(r => r[o.label])).range([mT, H - mB]).padding(0.25);
   made.svg.append('g').attr('transform', `translate(0,${H - mB})`).call(d3.axisBottom(x).ticks(W < 420 ? 3 : 4).tickFormat(o.axfmt).tickSize(-(H - mB - mT))).call(gridLines);
   const s = made.svg;
   s.append('g').selectAll('text').data(rows).join('text').attr('class', 'ic-vl').attr('x', mL - 8).attr('y', r => y(r[o.label]) + y.bandwidth() / 2).attr('dy', '0.35em').attr('text-anchor', 'end').text(r => r[o.label]);
   s.append('g').selectAll('rect').data(rows).join('rect').attr('x', mL).attr('y', r => y(r[o.label])).attr('height', y.bandwidth()).attr('width', r => Math.max(0, x(r[o.key]) - mL)).attr('rx', 2).style('fill', o.color());
   s.append('g').selectAll('text').data(rows).join('text').attr('class', 'ic-vl').attr('x', r => x(r[o.key]) + 4).attr('y', r => y(r[o.label]) + y.bandwidth() / 2).attr('dy', '0.35em').text(r => o.vfmt(r[o.key]));
   s.append('g').selectAll('rect').data(rows).join('rect').attr('x', 0).attr('width', W).attr('y', r => y(r[o.label]) - y.step() * y.paddingInner() / 2).attr('height', y.step()).attr('fill', 'transparent')
    .on('pointerenter pointermove', (ev, r) => { const [px, py] = d3.pointer(ev, made.box); tip(made, r[o.label], o.tip(r), px, py); })
    .on('pointerleave', () => { made.tip.hidden = true; });
  }});
 }

 // Líneas mensuales: varias series sobre los 12 meses.
 function lines(id, src, o){
  dash.draw(id, {mount, update(el, made){
   const d = dash.data(src);
   if (empty(made, d)) return;
   const rows = d.data, series = o.series();
   const W = made.box.clientWidth || 400, H = Math.max(200, Math.min(300, Math.round(W * 0.55)));
   made.svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H).attr('aria-label', o.aria);
   const vals = rows.flatMap(r => series.map(s => r[s.key]));
   let lo = o.zero ? 0 : d3.min(vals), hi = d3.max(vals);
   if (!o.zero) { const pad = (hi - lo) * 0.15 || hi * 0.02; lo -= pad; hi += pad; }
   const y = d3.scaleLinear().domain([lo, hi]).nice();
   const g0 = made.svg.append('g').call(d3.axisLeft(y).ticks(4).tickFormat(o.yfmt));
   let yw = 0; g0.selectAll('text').each(function(){ yw = Math.max(yw, this.getComputedTextLength()); }); g0.remove();
   const mL = Math.ceil(yw) + 10, mR = 10, mT = 10, mB = 24;
   const x = d3.scalePoint().domain(rows.map(r => r.mes)).range([mL + 6, W - mR - 6]);
   y.range([H - mB, mT]);
   const s = made.svg;
   s.append('g').attr('transform', `translate(${mL},0)`).call(d3.axisLeft(y).ticks(4).tickFormat(o.yfmt).tickSize(-(W - mL - mR))).call(gridLines);
   const step = W < 420 ? 2 : 1;
   s.append('g').attr('transform', `translate(0,${H - mB})`).call(d3.axisBottom(x).tickSizeOuter(0).tickFormat((m, i) => i % step ? '' : T.mesc(m)));
   series.forEach(se => {
    s.append('path').datum(rows).attr('d', d3.line().x(r => x(r.mes)).y(r => y(r[se.key]))).attr('fill', 'none').style('stroke', se.color).attr('stroke-width', 2.25);
    s.append('g').selectAll('circle').data(rows).join('circle').attr('cx', r => x(r.mes)).attr('cy', r => y(r[se.key])).attr('r', 3).style('fill', se.color);
   });
   const hl = s.append('line').attr('y1', mT).attr('y2', H - mB).style('stroke', 'var(--cds-chart-reference)').attr('opacity', 0);
   const bw = x.step();
   s.append('g').selectAll('rect').data(rows).join('rect').attr('x', r => x(r.mes) - bw / 2).attr('width', bw).attr('y', mT).attr('height', H - mB - mT).attr('fill', 'transparent')
    .on('pointerenter pointermove', (ev, r) => {
     hl.attr('x1', x(r.mes)).attr('x2', x(r.mes)).attr('opacity', 1);
     const [px] = d3.pointer(ev, made.box);
     tip(made, T.mes(r.mes) + ' 2025', series.map(se => [se.label, o.tfmt(r[se.key])]), px, y(d3.max(series, se => r[se.key])));
    })
    .on('pointerleave', () => { hl.attr('opacity', 0); made.tip.hidden = true; });
  }});
 }

 hbar('ex_region', 'ex_region', {label: 'Region', key: 'ingreso', color: () => C(0), vfmt: T.money, axfmt: T.short, aria: 'Ingreso neto por región',
  tip: r => [['Ingreso neto', T.money(r.ingreso)], ['% del ingreso', T.pct(r.share)], ['Unidades', T.int(r.vendidas)], ['Transacciones', T.int(r.transacciones)]]});
 hbar('ex_canal', 'ex_canal', {label: 'Canal', key: 'ingreso', color: () => C(1), vfmt: T.money, axfmt: T.short, aria: 'Ingreso neto por canal',
  tip: r => [['Ingreso neto', T.money(r.ingreso)], ['% del ingreso', T.pct(r.share)], ['Unidades', T.int(r.vendidas)], ['Ticket promedio', T.rd2(r.ticket)]]});
 hbar('ex_desc', 'ex_desc', {label: 'Descuento', key: 'ingreso', color: () => C(2), vfmt: T.money, axfmt: T.short, aria: 'Ingreso neto por nivel de descuento',
  tip: r => [['Ingreso neto', T.money(r.ingreso)], ['% del ingreso', T.pct(r.share)], ['Transacciones', T.int(r.transacciones)], ['Ticket promedio', T.rd2(r.ticket)]]});
 hbar('ex_defect', 'producto', {label: 'Producto', key: 'pct_defect', color: () => 'var(--cds-chart-status-critical)', vfmt: T.pct2, axfmt: L.format('.1%'), aria: 'Porcentaje de unidades defectuosas por producto',
  sort: (a, b) => b.pct_defect - a.pct_defect,
  tip: r => [['% defectuosas', T.pct2(r.pct_defect)], ['Defectuosas', T.int(r.defectuosas)], ['Producidas', T.int(r.producidas)]]});

 lines('ex_turno_mes', 'ex_turno_mes', {aria: 'Unidades producidas por mes y turno', zero: false, yfmt: T.short, tfmt: T.int,
  series: () => [{key: 'Manana', label: 'Mañana', color: C(0)}, {key: 'Tarde', label: 'Tarde', color: C(1)}, {key: 'Noche', label: 'Noche', color: C(2)}]});
 lines('ex_planta_mes', 'ex_planta_mes', {aria: 'Cumplimiento del plan por mes y planta', zero: false, yfmt: L.format('.0%'), tfmt: T.pct,
  series: () => [{key: 'santiago', label: 'Planta Santiago', color: C(0)}, {key: 'santo_domingo', label: 'Planta Santo Domingo', color: C(1)}]});
 lines('ex_ing_costo', 'mensual', {aria: 'Ingreso neto y costo de producción por mes', zero: true, yfmt: T.short, tfmt: T.money,
  series: () => [{key: 'ingreso', label: 'Ingreso neto', color: C(1)}, {key: 'costo', label: 'Costo de producción', color: C(0)}]});

 // Mapa de calor: productos × meses, intensidad = unidades vendidas.
 dash.draw('ex_heat', {mount, update(el, made){
  const d = dash.data('ex_prod_mes');
  if (empty(made, d)) return;
  const rows = d.data;
  const tot = d3.rollup(rows, v => d3.sum(v, r => r.vendidas), r => r.Producto);
  const prods = [...tot.keys()].sort((a, b) => tot.get(b) - tot.get(a));
  const meses = [...new Set(rows.map(r => r.mes))].sort();
  const W = made.box.clientWidth || 600;
  const mL = Math.ceil(textW(made.svg, prods)) + 12, mT = 22, cellH = 32;
  const H = mT + prods.length * cellH + 4;
  made.svg.attr('viewBox', `0 0 ${W} ${H}`).attr('height', H).attr('aria-label', 'Unidades vendidas por producto y mes');
  const x = d3.scaleBand().domain(meses).range([mL, W]).padding(0.06);
  const y = d3.scaleBand().domain(prods).range([mT, H - 4]).padding(0.06);
  const ext = d3.extent(rows, r => r.vendidas);
  const op = d3.scaleLinear().domain(ext).range([0.12, 1]);
  const s = made.svg, showVals = x.bandwidth() >= 40;
  const step = x.bandwidth() < 24 ? 2 : 1;
  s.append('g').selectAll('text').data(meses).join('text').attr('class', 'ic-vl').attr('x', m => x(m) + x.bandwidth() / 2).attr('y', 12).attr('text-anchor', 'middle').style('fill', 'var(--cds-text-secondary)').text((m, i) => i % step ? '' : T.mesc(m));
  s.append('g').selectAll('text').data(prods).join('text').attr('class', 'ic-vl').attr('x', mL - 8).attr('y', p => y(p) + y.bandwidth() / 2).attr('dy', '0.35em').attr('text-anchor', 'end').text(p => p);
  const cells = s.append('g').selectAll('g').data(rows).join('g');
  cells.append('rect').attr('x', r => x(r.mes)).attr('y', r => y(r.Producto)).attr('width', x.bandwidth()).attr('height', y.bandwidth()).attr('rx', 2).style('fill', C(0)).attr('fill-opacity', r => op(r.vendidas));
  if (showVals) cells.append('text').attr('class', 'ic-vl').attr('x', r => x(r.mes) + x.bandwidth() / 2).attr('y', r => y(r.Producto) + y.bandwidth() / 2).attr('dy', '0.35em').attr('text-anchor', 'middle')
   .style('fill', r => op(r.vendidas) > 0.6 ? 'var(--color-bg)' : 'var(--color-fg)').text(r => T.int(r.vendidas));
  cells.on('pointerenter pointermove', (ev, r) => { const [px, py] = d3.pointer(ev, made.box); tip(made, r.Producto + ' · ' + T.mes(r.mes), [['Unidades vendidas', T.int(r.vendidas)], ['Ingreso neto', T.rd2(r.ingreso)]], px, py); })
   .on('pointerleave', () => { made.tip.hidden = true; });
 }});
})();
