// Node port of main.cpp for machines without Drift's prebuilt Skia: same CLI, same framing, rendered
// by Skottie from CanvasKit (Skia's WebAssembly build). tools/setup-cloud.sh installs it as
// build/skottie-render. CanvasKit exposes no Skottie logger, so --strict instead rejects the features
// Drift's rules forbid (text, images, fonts, expressions, 3D) and anything Skottie fails to parse.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

function usage() {
    process.stderr.write(
        'usage: skottie-render IN.json OUT.png [--size N] [--t FRACTION] [--sheet N]\n' +
        '                      [--bg none|checker|RRGGBB] [--pad FRACTION] [--region X,Y,W,H]\n' +
        '                      [--strict] [--frames DIR --height H --fps N]\n');
    process.exit(1);
}

// Drift-rule violations Skottie itself would render (or silently drop) without complaint.
function lint(doc) {
    const problems = [];
    if (doc.ddd) problems.push('3D composition');
    if ((doc.fonts && doc.fonts.list && doc.fonts.list.length) || (doc.chars && doc.chars.length))
        problems.push('fonts/chars');
    for (const a of doc.assets || []) if (a.p || a.u) problems.push(`image asset ${a.id}`);
    const walk = (node, where) => {
        if (Array.isArray(node)) { node.forEach((n) => walk(n, where)); return; }
        if (!node || typeof node !== 'object') return;
        if (typeof node.x === 'string' && ('k' in node || 'a' in node)) problems.push(`expression in ${where}`);
        for (const [k, v] of Object.entries(node)) if (v && typeof v === 'object') walk(v, where);
    };
    const layers = (list, where) => {
        for (const l of list || []) {
            const name = `${where}/${l.nm ?? l.ind}`;
            if (l.ty === 5) problems.push(`text layer ${name}`);
            if (l.ty === 2) problems.push(`image layer ${name}`);
            if (l.ddd) problems.push(`3D layer ${name}`);
            walk(l, name);
        }
    };
    layers(doc.layers, 'root');
    for (const a of doc.assets || []) layers(a.layers, `asset ${a.id}`);
    return problems;
}

function drawBackground(CK, canvas, r, bg) {
    if (bg === 'none') return;
    const paint = new CK.Paint();
    if (bg === 'checker') {
        paint.setColor(CK.Color(0x3a, 0x3a, 0x42));
        canvas.drawRect(r, paint);
        paint.setColor(CK.Color(0x2a, 0x2a, 0x30));
        const w = r[2] - r[0], cell = w / 16;
        for (let y = 0; y < 16; ++y)
            for (let x = y % 2; x < 16; x += 2)
                canvas.drawRect(CK.XYWHRect(r[0] + x * cell, r[1] + y * cell, cell, cell), paint);
    } else {
        const v = parseInt(bg, 16) || 0;
        paint.setColor(CK.Color((v >> 16) & 255, (v >> 8) & 255, v & 255));
        canvas.drawRect(r, paint);
    }
    paint.delete();
}

function drawFrame(CK, canvas, anim, t, cell, pad, bg, region) {
    drawBackground(CK, canvas, cell, bg);
    const [sw, sh] = anim.size();
    const r = region || [0, 0, sw, sh];
    const cw = cell[2] - cell[0], ch = cell[3] - cell[1];
    const inner = [cell[0] + cw * pad, cell[1] + ch * pad, cw * (1 - 2 * pad), ch * (1 - 2 * pad)];
    const scale = Math.min(inner[2] / r[2], inner[3] / r[3]);
    const ox = inner[0] + inner[2] / 2 - (r[0] + r[2] / 2) * scale;
    const oy = inner[1] + inner[3] / 2 - (r[1] + r[3] / 2) * scale;
    canvas.save();
    canvas.clipRect(cell, CK.ClipOp.Intersect, true);
    anim.seekFrame(t * anim.duration() * anim.fps());
    anim.render(canvas, CK.XYWHRect(ox, oy, sw * scale, sh * scale));
    canvas.restore();
}

function writePng(CK, surface, out) {
    const img = surface.makeImageSnapshot();
    const bytes = img.encodeToBytes(CK.ImageFormat.PNG, 100);
    img.delete();
    if (!bytes) throw new Error(`cannot encode ${out}`);
    fs.writeFileSync(out, bytes);
}

async function main() {
    const argv = process.argv.slice(2);
    if (argv.length < 2) usage();
    const [input, out] = argv;
    let size = 512, sheet = 0, height = 0, fps = 20, t = 0.5, pad = 0.06, strict = false;
    let bg = '1c1c22', framesDir = '', region = null;
    for (let i = 2; i < argv.length; ++i) {
        const a = argv[i];
        const next = () => { if (++i >= argv.length) usage(); return argv[i]; };
        if (a === '--size') size = parseInt(next(), 10);
        else if (a === '--t') t = parseFloat(next());
        else if (a === '--sheet') sheet = parseInt(next(), 10);
        else if (a === '--bg') bg = next();
        else if (a === '--pad') pad = parseFloat(next());
        else if (a === '--strict') strict = true;
        else if (a === '--frames') framesDir = next();
        else if (a === '--height') height = parseInt(next(), 10);
        else if (a === '--fps') fps = parseFloat(next());
        else if (a === '--region') {
            region = next().split(',').map(Number);
            if (region.length !== 4 || region.some(Number.isNaN)) usage();
        } else usage();
    }

    const text = fs.readFileSync(input, 'utf8');
    const doc = JSON.parse(text);
    const CanvasKitInit = require(path.join(HERE, 'node_modules/canvaskit-wasm/bin/full/canvaskit.js'));
    const CK = await CanvasKitInit({ locateFile: (f) => path.join(HERE, 'node_modules/canvaskit-wasm/bin/full', f) });
    const anim = CK.MakeManagedAnimation(text);
    if (!anim) {
        process.stderr.write(`error: Skottie could not parse ${input}\n`);
        return 1;
    }
    const [aw, ah] = anim.size();
    console.log(`size ${aw}x${ah}  fps ${anim.fps()}  duration ${anim.duration().toFixed(2)}s`);
    const slots = anim.getSlotInfo ? anim.getSlotInfo() : null;
    if (slots && slots.colorSlotIDs) console.log('slots: ' + slots.colorSlotIDs.map((s) => `${s}(color)`).join(' '));
    const problems = lint(doc);
    for (const p of problems) process.stderr.write(`warning: ${p}\n`);
    const status = strict && problems.length ? 2 : 0;

    if (framesDir) {
        const s = region ? [region[2], region[3]] : [aw, ah];
        const h = height > 0 ? height : 180;
        const aspect = Math.min(Math.max(s[0] / s[1], 1), 4);
        const w = Math.round((h * aspect) / 2) * 2;
        const surface = CK.MakeSurface(w, h);
        const canvas = surface.getCanvas();
        const count = Math.max(1, Math.round(anim.duration() * fps));
        fs.mkdirSync(framesDir, { recursive: true });
        for (let i = 0; i < count; ++i) {
            canvas.clear(CK.TRANSPARENT);
            drawFrame(CK, canvas, anim, i / count, CK.LTRBRect(0, 0, w, h), pad, bg, region);
            writePng(CK, surface, path.join(framesDir, String(i).padStart(4, '0') + '.png'));
        }
        canvas.clear(CK.TRANSPARENT);
        drawFrame(CK, canvas, anim, t, CK.LTRBRect(0, 0, w, h), pad, bg, region);
        writePng(CK, surface, out);
        console.log(`frames ${count} at ${w}x${h}`);
        return status;
    }

    const surface = CK.MakeSurface(size, size);
    const canvas = surface.getCanvas();
    canvas.clear(CK.TRANSPARENT);
    if (sheet > 0) {
        const cell = size / sheet;
        for (let i = 0; i < sheet * sheet; ++i) {
            const ft = (i / (sheet * sheet - 1)) * 0.999;
            const x = (i % sheet) * cell, y = Math.floor(i / sheet) * cell;
            drawFrame(CK, canvas, anim, ft, CK.LTRBRect(x + 1, y + 1, x + cell - 1, y + cell - 1), pad, bg, region);
        }
    } else {
        drawFrame(CK, canvas, anim, t, CK.LTRBRect(0, 0, size, size), pad, bg, region);
    }
    writePng(CK, surface, out);
    return status;
}

main().then((code) => process.exit(code), (err) => {
    process.stderr.write(`error: ${err.stack || err}\n`);
    process.exit(1);
});
