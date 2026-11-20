from rdkit import Chem
from rdkit.Chem import rdMolDescriptors as D
S={
'GABA':('NCCCC(=O)O','C4H9NO2'),
'diazepam':('CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc21','C16H13ClN2O'),
'triazolam':('Cc1nnc2n1-c1ccc(Cl)cc1C(c1ccccc1Cl)=NC2','C17H12Cl2N4'),
'zolpidem':('Cc1ccc(-c2nc3ccc(C)cn3c2CC(=O)N(C)C)cc1','C19H21N3O'),
'eszopiclone':('CN1CCN(CC1)C(=O)O[C@@H]1c2nccnc2C(=O)N1c1ccc(Cl)cn1','C17H17ClN6O3'),
'suvorexant':('Cc1ccc(-n2nccn2)c(c1)C(=O)N1CCN(c3nc4cc(Cl)ccc4o3)CC[C@H]1C','C23H23ClN6O2'),
'lemborexant':('Cc1ncc(OC[C@]2(c3cccc(F)c3)C[C@H]2C(=O)Nc2ccc(F)cn2)c(C)n1','C22H20F2N4O2'),
'doxepin':('CN(C)CCC=C1c2ccccc2COc2ccccc21','C19H21NO'),
'trazodone':('O=c1n(CCCN2CCN(c3cccc(Cl)c3)CC2)nc2ccccn12','C19H22ClN5O'),
'melatonin':('COc1ccc2[nH]cc(CCNC(C)=O)c2c1','C13H16N2O2'),
'ramelteon':('CCC(=O)NCC[C@@H]1CCc2ccc3OCCc3c21','C16H21NO2'),
'diphenhydramine':('CN(C)CCOC(c1ccccc1)c1ccccc1','C17H21NO'),
'tryptophan':('N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O','C11H12N2O2'),
'5HTP':('N[C@@H](Cc1c[nH]c2ccc(O)cc12)C(=O)O','C11H12N2O3'),
'serotonin':('NCCc1c[nH]c2ccc(O)cc12','C10H12N2O'),
'NAS':('CC(=O)NCCc1c[nH]c2ccc(O)cc12','C12H14N2O2'),
'histamine':('NCCc1cnc[nH]1','C5H9N3'),
}
for k,(s,f) in S.items():
    m=Chem.MolFromSmiles(s); g=D.CalcMolFormula(m); print(k,g,f,'OK' if g==f else 'MISMATCH')
