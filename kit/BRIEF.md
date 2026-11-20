# Illustration brief — 《重新認識失眠：給中醫師的由淺入深讀本》

The book is `/home/user/Insomnia/original.html` (Traditional Chinese, for a TCM doctor self-studying insomnia).
The reader asked for **hand-drawn-style illustrations for every chapter/section**, so they can SEE the
thing behind each name (e.g. where the suprachiasmatic nucleus physically sits, what a GABA-A receptor
looks like, what the tongue of 陰虛火旺 looks like, what 半夏 the plant looks like) instead of memorising a word.
Their words: references are *Gray's Anatomy plates* and *Shutterstock medical outline illustrations*.
"不要太簡陋，別用簡單的 stickman"; colour is allowed where it helps; labels and drawings must NEVER overlap;
terms bilingual (中文 + English/Latin).

## Deliverable per plate
One file `figs/<id>.html` containing exactly one snippet:

```html
<figure class="plate" id="pl-xxx">
  <div class="pt"><span class="pn">Plate 1·B</span><span class="ptt">中文標題</span><span class="pte">English title</span></div>
  <svg viewBox="0 0 760 H" role="img" aria-label="中文描述">
    ... drawing ...
  </svg>
  <figcaption><b>圖 1-B　短標題。</b>1–3 sentences: what to notice, why it matters for the text. Note "示意圖，依解剖教科書重繪" or similar honesty about schematic simplifications.</figcaption>
</figure>
```
- viewBox width is ALWAYS 760 (column width ≈ 742px, so 1 unit ≈ 1 px). Height as needed (typically 360–620).
- Every id you define inside the SVG (gradients, clipPaths, patterns, symbols) MUST be prefixed with the plate id, e.g. `pl-scn-clip1`. Never define ids without the prefix.
- Shared defs already exist in the page (kit/defs.svg) — reuse them: `url(#ink-hatch)`, `#ink-hatch-l` (light), `#ink-hatch-d` (dense), `#ink-hatch-r` (other diagonal), `#ink-hatch-h`, `#ink-cross`, `#ink-stipple`, `#ink-stipple-l`, `#ink-stipple-d`, `#ink-membrane` (lipid bilayer, 34 tall), gradients `#ink-vol`, `#ink-vol-red`, `#ink-vol-blue`, `#ink-vol-yel`, `#ink-vol-flesh`, filter `#ink-rough` (wobbly inked line; apply to drawing `<g>` only, NEVER to text), markers `#ink-dot` (leader end), `#ink-arrow`, `#ink-arrow-red`, `#ink-arrow-blue`, `#ink-tee` (inhibition bar).
- CSS classes available inside plates (kit/plate.css): text `.lb` (13px bold zh label), `.le` (italic English, 11.5px), `.ls` (11px small note), `.lt` (15px heading), `.halo` (paper-coloured outline behind text — put on every label that sits near lines), lines `.ld` (leader line .7), `.ink` (1.1 outline), `.ink2` (0.6 detail), `.ink3` (1.8 bold contour), `.panel` (dashed panel frame).
  Typical label: `<text x=".." y=".." class="lb halo">視交叉上核 <tspan class="le">Suprachiasmatic nucleus (SCN)</tspan></text>` or put the English on a second line with another `<text>` 14px lower.
- Palette: ink #2a2018, paper #fbf6ea, Gray's-plate tints — red #b5473a / soft #f0c4b8, blue #3f6fa6 / soft #cfdcef, yellow #d9b53c / soft #f6e7b0, flesh #f3d9c6 / shade #dcae93, nerve yellow #e8cf7a, bone #efe6d2. Book accent colours: TCM red #a8412c, Western blue #2c5d9c, gold #c9962e.
- Molecules: `python3 kit/mol.py "<SMILES>" W H` prints an accurate RDKit skeletal formula as a `<g>`; embed it with `<g transform="translate(x,y) scale(k)">…</g>`. Use this for any chemical structure (never hand-draw rings). Remove the leading HTML comment line if you like.

## Quality bar (the reader explicitly complained earlier figures were too crude)
- Draw like an engraved anatomical plate: confident contour lines (`.ink3` outer contour, `.ink` inner structures, `.ink2` fine detail), **hatching / stippling to model volume** (layer a soft tint fill, then a hatch-pattern fill on the shadow side via a second path or clipPath), gyri/sulci squiggles on brains, muscle-fibre striations, vessel branching, cell organelles, etc. Many paths, real shapes — not boxes and circles.
- Anatomy must be **topologically and proportionally correct** (e.g. SCN sits just dorsal to the optic chiasm on either side of the 3rd ventricle; pineal sits above the superior colliculi behind the 3rd ventricle; LC is in the dorsal pons at the floor of the 4th ventricle; TMN in the posterior hypothalamus near mammillary bodies; tongue regions etc.). When simplifying, say so in the caption.
- Humans: realistic proportions and contours (head ≈ 1/7.5 body, a real face profile with nose/lips/chin, ears, hair mass, hands with fingers, fabric folds on blankets drawn with hatching). Medical-outline style like Shutterstock medical vectors is fine. **No stick figures.**
- Labels sit **outside or at the edge of the drawing**, aligned in tidy columns on the left/right margins, connected by thin leader lines `.ld` ending in `marker-start/end="url(#ink-dot)"` on the structure. Leaders must not cross each other where avoidable. Keep ≥ 4px gap between any two text boxes. Text never sits on top of hatching without `.halo`.
- Bilingual: 中文名稱 + English (and abbreviation). Use Taiwanese terms (e.g. 視交叉上核、松果體、藍斑核、結節乳頭核、腦下垂體、腎上腺、褪黑激素、受體、會厭).
- Make each plate teach: add 1–2 small inset panels / callouts / arrows showing the mechanism mentioned in the text (e.g. day vs night, normal vs disease), numbered steps ①②③ if there's a pathway.

## Verify every plate (mandatory)
`node kit/render_fig.js figs/<id>.html` → writes `figs/<id>.png` (2x) and prints any `OVERLAP:` / `CLIPPED:` text. Fix until there are none, then **open the PNG with the Read tool and look at it critically** (does it look like a real anatomical plate? is anything misplaced, ugly, cramped, cut off? are leader lines pointing at the right structure?). Iterate at least twice per plate. Delete nothing outside your own figs files. Do not edit original.html or kit/*. Do not git commit.

## Report back
For each plate: id, one-line content summary, suggested insertion point (chapter + the h3/h4 heading text it should follow, and whether before/after a given paragraph), and any caveats. Keep the report short.
