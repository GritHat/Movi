// Genera uno stato per fotogramma (finto registro di simulatore): node genera_stati.mjs <uscita.json> <uscita.js> <secondi> <fps>
import { writeFileSync } from "node:fs";
const [out, outJs, sec = "6", fps = "30"] = process.argv.slice(2);
const n = Math.round(+sec * +fps), frames = [];
for (let i = 0; i < n; i++) {
  const t = i / +fps, objs = [];
  for (let k = 0; k < 3; k++) {
    const cx = 80 + 90 * t * (1 + 0.3 * k) + 40 * k, cy = 90 + 110 * k + 25 * Math.sin(t * 1.3 + k), a = 0.2 * Math.sin(t + k);
    const w = 70, h = 34, c = Math.cos(a), s = Math.sin(a);
    const poly = [[-w/2,-h/2],[w/2,-h/2],[w/2,h/2],[-w/2,h/2]].map(([x,y]) => [+(cx + x*c - y*s).toFixed(2), +(cy + x*s + y*c).toFixed(2)]);
    objs.push({ id: k + 1, x: +cx.toFixed(2), y: +cy.toFixed(2), poly, label: `T${k + 1} ${(8 + 3 * k + Math.sin(t)).toFixed(1)} m/s` });
  }
  frames.push({ f: i, t: +t.toFixed(4), objs });
}
const doc = { fps: +fps, n, frames };
writeFileSync(out, JSON.stringify(doc));
writeFileSync(outJs, "window.__STATI = " + JSON.stringify(doc) + ";\n");
console.log(n, "fotogrammi");
