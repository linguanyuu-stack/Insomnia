# Addendum: plates for the PUBLIC edition 《重新認識失眠・民眾版》

Read `kit/BRIEF.md` first — format, kit, quality bar and the render/verify loop are identical.
Differences for this edition:

- Audience: Taiwanese patients and the general public (not doctors). It is also the pre-production
  research for a future animated explainer video, so each plate should feel like a strong, clear
  storyboard frame: one idea, instantly readable, with a friendly metaphor — but still richly drawn in
  the same engraved / hand-tinted style (hatching, stippling, real proportions; NO stick figures, no
  cartoon emoji look). Warm tints welcome.
- Fewer, larger labels (12–20 per plate max), plain words first, the technical term second, e.g.
  `生理時鐘總司令 <tspan class="le">視交叉上核 SCN</tspan>`. Label font sizes may go up to 14–15px.
- Save to `/home/user/Insomnia/figs_public/<id>.html` (+ png). ids start with `pp-`. Plate numbers in
  the `pn` span use the form `圖 1·A`. Every internal SVG id must be prefixed with the plate id.
- Real historical people: draw them as generic period figures (clothing, setting, props), never an
  attempt at a likeness; caption says 「人物為示意，非肖像」. Never draw the actual Nobel medal design
  with a real person's face — a generic gold medal with laurel and the text "2017" is fine.
- Captions (figcaption): 1–3 friendly sentences in Traditional Chinese explaining what to notice.
- Verify: `node kit/render_fig.js figs_public/<id>.html` until no OVERLAP/CLIPPED, then Read the PNG and
  critique; iterate ≥2×. Keep each plate under ~150 KB (prefer patterns over thousands of dots).
- Put any generator script in `figs_public/_gen/`. Don't edit kit/*, figs/*, or other agents' files. No git.
