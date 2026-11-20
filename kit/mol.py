#!/usr/bin/env python3
"""Skeletal formula -> inline SVG <g> for embedding in a plate.
Usage: python3 kit/mol.py "SMILES" WIDTH HEIGHT [--id name]
Prints a <g> element (no XML header, transparent background, ink-coloured bonds,
heteroatoms keep muted colours). Put it inside a plate SVG with x/y/width/height attributes,
e.g. <svg x="40" y="60" width="200" height="150" viewBox=...> (the output already has viewBox)."""
import sys, re
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
smi, w, h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
m = Chem.MolFromSmiles(smi)
AllChem.Compute2DCoords(m)
d = rdMolDraw2D.MolDraw2DSVG(w, h)
o = d.drawOptions()
o.clearBackground = False
o.bondLineWidth = 1.6
o.fixedFontSize = 13
o.padding = 0.08
o.updateAtomPalette({6: (0.165, 0.125, 0.094), 7: (0.17, 0.36, 0.61), 8: (0.66, 0.25, 0.17),
                     9: (0.3, 0.5, 0.3), 17: (0.3, 0.5, 0.3), 16: (0.6, 0.5, 0.1), 1: (0.165, 0.125, 0.094)})
d.DrawMolecule(m)
d.FinishDrawing()
s = d.GetDrawingText()
s = re.sub(r'<\?xml[^>]*\?>\s*', '', s)
s = re.sub(r"<rect style='opacity:1.0;fill:#FFFFFF[^>]*>\s*</rect>", '', s)
s = re.sub(r"<!-- END OF HEADER -->", '', s)
s = re.sub(r'<svg[^>]*>', '', s, count=1).replace('</svg>', '')
s = re.sub(r"class='[^']*'\s*", '', s)
print("<!-- molecule %dx%d: wrap with transform=translate(x,y) scale(k) -->" % (w, h))
print('<g class="mol">' + s.strip() + '</g>')
