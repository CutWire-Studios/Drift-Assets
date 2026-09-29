# Asset spec

Every asset lives in its own directory together with a square thumbnail and a small metadata file.
Everything is generated from scripts under `tools/`, so assets can be tweaked and rebuilt.

```
lottie/<category>/<id>/<id>.json      Lottie animation
                       thumbnail.png  512x512
                       asset.json
face-props/<id>/<id>.glb              3D prop worn on a tracked face
                thumbnail.png
                prop.json
objects/<id>/<id>.glb                 standalone animated 3D object
             thumbnail.png
             asset.json
tools/lottie/lottie_kit.py            Lottie authoring helpers
tools/lottie/<category>/<id>.py       one generator per Lottie asset
tools/blender/drift3d.py              Blender helpers (materials, export, head space, thumbnails)
tools/blender/{face-props,objects}/<id>.py
tools/lottie/drift_lottie.py          Variant/Build output step shared by new Lottie generators
tools/skottie-render/                 renders Lottie with Skottie (the renderer Drift uses)
tools/check-assets.py                 lints every asset (CI runs it)
tools/build-readme.py                 regenerates the README asset tables
```

`<id>` is kebab-case and unique across the repo. Thumbnails are 512x512 PNG.

## Setup

```sh
python3 -m venv .venv                       # Python tooling runs from this venv
cmake -S tools/skottie-render -B tools/skottie-render/build -DCMAKE_BUILD_TYPE=Release
cmake --build tools/skottie-render/build    # links Drift's prebuilt Skia (see its CMakeLists.txt)
```

Blender 5.2 (flatpak `org.blender.Blender`) builds the 3D assets headless.

Without Drift's prebuilt Skia or the flatpak (CI runners, cloud dev boxes on Ubuntu), run
`tools/setup-cloud.sh` instead. It installs ffmpeg and Blender 5.2 from blender.org, creates the
venv, and installs `build/skottie-render` as a launcher for `skottie-render.mjs`: the same CLI,
rendered by Skottie from CanvasKit (Skia's WebAssembly build) in Node. Its `--strict` rejects the
content rules below instead of Skottie log warnings, which CanvasKit does not expose. Then run
Blender as `$DRIFT_BLENDER` (printed by the script) wherever this guide says `flatpak run
org.blender.Blender`; `tools/build-previews.py` honours `DRIFT_BLENDER` too.

## Variants

An asset can ship several designs, e.g. a follow button as a solid pill, an outline, a glass card
and an icon-only pop. Variants must differ in **shape, style or motion**, never only in colour
(colour slots already cover recolouring). One generator script builds all of an asset's variants.

The first variant is the default: it keeps the plain file names and the metadata's top-level
fields describe it, so clients that ignore variants still work. Variant `<v>` adds
`<id>--<v>.json|.glb`, `thumbnail--<v>.png`, `preview--<v>.webp` (and `poster--<v>.png` for
Lottie). The metadata lists every variant, the default included:

```json
"variants": [
  {"id": "classic", "name": "Classic Pill", "file": "follow-button-instagram.json",
   "thumbnail": "thumbnail.png", "preview": "preview.webp", "poster": "poster.png",
   "width": 680, "height": 290, "duration": 4.0, "playback": "intro-hold-outro",
   "slots": {"primary": "#0095F6", "secondary": "#363636"}, "textArea": [230, 88, 398, 72]},
  {"id": "outline", "name": "Outline", "file": "follow-button-instagram--outline.json", ...}
]
```

Face-prop variants carry `model`, `thumbnail`, `preview` and their own `params`; object variants
carry `file`, `thumbnail`, `preview` and `animation`. Any variant may add a `description` and
`tags`. The builders write all of this:

- Lottie: `drift_lottie.build_asset(category, id, name, description, tags, [Variant(...), ...])`
  (see `tools/lottie/call-to-action/follow-button-instagram.py`). It also renders the previews.
- Objects: `drift3d.build_object_variants(id, name, description, tags, [(vid, name, opts)], build)`
  where `build(opts)` returns `(objects, action_name, frames)` (see `tools/blender/objects/heart.py`).
- Face props: `drift3d.build_prop_variants(id, name, description, tags, [(vid, name, opts)], build)`
  where `build(opts)` returns the prop meshes (see `tools/blender/face-props/party-hat.py`).

The 3D builders render their own previews (so `render-previews.py` skips them). All builders take
`--no-preview` and `--only=a,b` after the script (`-- --only=a,b` for Blender); the Lottie
builder also takes `--sheet` to write contact sheets to `.preview-frames/sheets/`.

Before committing, run `python3 tools/check-assets.py` and `python3 tools/build-readme.py`.

## Previews and release

Each asset also ships the animated preview Drift's marketplace plays on hover:

- `preview.webp`: a looping animated WebP. For Lottie it has the canvas's own aspect (1:1 to 4:1)
  and is 180 px tall; 3D assets are 256 px square. Objects play their loop and face props turn
  the head.
- `poster.png`: Lottie only. A still at the same size as the preview.

`.venv/bin/python tools/build-previews.py [--skip-3d] [ID ...]` rebuilds them. It needs ffmpeg
with libwebp and the skottie-render build, plus the Blender flatpak for 3D. Run it after changing
an asset and commit the results.

`python3 tools/build-index.py dist` writes `dist/index.json` (categories in shelf order, plus each
asset's metadata with the sha256 of every file) and `dist/drift-assets.tar.gz`. CI runs it on
every push, and pushing a `v*` tag publishes both as a GitHub release, which the marketplace
syncs from. Categories and their order live in `CATEGORIES` in that script. A new Lottie category
must be added there.

## Lottie

Build: `.venv/bin/python tools/lottie/<category>/<id>.py` writes `lottie/<category>/<id>/<id>.json`,
renders the thumbnail and writes `asset.json`.

Rules (Drift plays Lottie through Skia's Skottie):

- **No text layers and no baked-in words.** Users add text with Drift's text tool; leave room for it.
- **No expressions, no images, no fonts, no 3D layers.** Shapes only; everything keyframed.
- **Tight canvas**: the canvas is the element's own bounds plus a little margin for overshoot,
  not a full 1920x1080 frame. Pick sizes that suit an element placed on a 1080p video
  (a lower third bar ~1000-1400 px wide, a button ~400-700 px).
- **30 fps.** Keep durations short: pops/stamps 1-2 s, lower thirds 4-6 s.
- **Colour slots**: every main colour the user may want to change is a colour slot
  (`comp.slot("primary", ...)`, `fill(slot="primary")`). Use consistent ids: `primary`,
  `secondary`, `accent`, `background`, `icon`, `outline`. Brand-logo colours stay fixed (no slot);
  gradients cannot be slotted.
- **Timing structure**, recorded in `asset.json` as `"playback"`:
  - `loop` - seamless; first and last frames match.
  - `intro-hold` - animates in, then the last frame holds (Drift's default "hold" loop mode).
  - `intro-hold-outro` - add markers `intro` (0 → end of intro) and `outro` (start → end) with
    `comp.marker()`, so the hold can later be stretched.
- Must render with `tools/skottie-render/build/skottie-render <json> <png> --strict` exiting 0.
- Thumbnail: `skottie-render <json> thumbnail.png --size 512 --t <fraction of the most
  representative frame>`; default background `1c1c22`, use `--bg e8e8ee` if the asset is mostly
  dark. For very wide or sparse assets, frame a readable close-up with `--region x,y,w,h`
  (canvas pixels). Check your animation with `--sheet 4` and look at the result.

`asset.json` for Lottie:

```json
{
  "schema": 1, "id": "like-thumb-pop", "name": "Like Thumb Pop", "type": "lottie",
  "category": "call-to-action", "file": "like-thumb-pop.json", "thumbnail": "thumbnail.png",
  "license": "CC-BY-NC-SA-4.0", "description": "...", "tags": ["like", "youtube"],
  "width": 400, "height": 400, "fps": 30, "duration": 2.0,
  "playback": "intro-hold", "slots": {"primary": "#FF0000", "icon": "#FFFFFF"},
  "textArea": null
}
```

`textArea` is `[x, y, w, h]` in canvas pixels where the user is meant to put their text
(e.g. the inside of a lower-third bar), or `null`. Assets with several text regions keep the
main one in `textArea` and add all of them by name, e.g.
`"textAreas": {"headline": [56, 106, 1288, 66], "subtitle": [56, 187, 1288, 28]}`.

## 3D (face props and objects)

Build: `flatpak run org.blender.Blender -b --factory-startup --python-exit-code 1 --python
"$PWD/tools/blender/<kind>/<id>.py"` (absolute path; the flatpak's cwd is not the repo).

Drift loads `.glb` only and shades with a simple Blinn-Phong model. It reads: base colour factor
or a base-colour texture on UV0, metallic factor, roughness factor, emissive factor, alpha mode,
double-sided. It ignores normal/occlusion/roughness maps and Blender procedural nodes, and rejects
Draco/meshopt compression. So model detail in geometry and use flat Principled materials
(`drift3d.material()`). Budget: under 50k vertices, textures at most 1024 px if any.

### Face props

- Model in **head space** with `drift3d.reference_head()` for fitting (never export it):
  1 unit = 1 head-width, origin between the eyes, +X image-right, +Z up (forehead),
  -Y toward the camera. Proportions are in `drift3d.HEAD_REF`.
- Static mesh only; Drift does not play animations on face props.
- Drift occludes whatever is behind the head ellipsoid, so hats and ear pieces can wrap around.
- `drift3d.write_prop_json()` writes the Drift face-model params (`scale`, `offsetX/Y/Z`) that
  undo Drift's auto-centring, so the prop sits exactly where it was modelled.
- Thumbnail: `drift3d.render_prop_thumbnail(path, props, head, region="face"|"head")` - the
  prop on the mannequin (eyes and mouth added for the render only), front three-quarter view;
  `face` framing for glasses/nose/mouth props, `head` for hats, ears and halos.

### Objects

- Centred at the origin, about 1 unit across, resting pose facing -Y (the camera).
- One seamless looping animation (node transforms only: rotate/bob/pulse; 2-4 s at 30 fps,
  last frame == first frame, linear interpolation on continuous spins). Drift plays glTF node
  animations with loop mode on by default.
- `asset.json` with `"type": "object"`, plus `"animation": {"name", "duration", "loop": true}`.
- Thumbnail: three-quarter hero view on the default background.
