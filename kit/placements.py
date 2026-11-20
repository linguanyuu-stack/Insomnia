# (plate id, unique anchor string in original.html, 'before' | 'after')
# Plates sharing an anchor with 'before' keep list order.
T = '<h3><span class="tag">%s</span>'
PLACEMENTS = [
    # ch1 physiology
    ('pl-adenosine',      T % 'PROCESS C', 'before'),
    ('pl-scn',            T % 'ALLOSTATIC DRIVE', 'before'),
    ('pl-hpa',            T % 'THE FLIP-FLOP SWITCH', 'before'),
    ('pl-brain',          '<figure id="fig-switch">', 'before'),
    ('pl-orexin',         T % 'THE STRESS PICTURE', 'before'),
    ('pl-eeg',            '<div class="widget" id="w-hypno">', 'before'),
    # ch2
    ('pl-psg',            '<div class="box say"><div class="bt">在診間怎麼用</div>', 'before'),
    # ch3
    ('pl-patterns',       T % 'AXIS 4–5 · RESEARCH', 'before'),
    ('pl-osa',            '<div class="widget tree" id="w-tree">', 'before'),
    ('pl-rls-rbd',        '<div class="widget tree" id="w-tree">', 'before'),
    # ch4
    ('pl-hyperarousal',   T % 'CONDITIONING', 'before'),
    ('pl-conditioning',   T % 'REM INSTABILITY', 'before'),
    # ch7
    ('pl-molecules',      '<h3><span class="tag">CLASS BY CLASS</span>各類藥物一覽</h3>', 'after'),
    ('pl-gabaa',          '<h4>BZRA：為什麼「藥效差不多，選擇看半衰期」</h4>', 'after'),
    ('pl-orexin-receptor','<h4>兩個關鍵試驗</h4>', 'before'),
    ('pl-melatonin',      '<div class="box say"><div class="bt">跟病人怎麼說</div>', 'before'),
    ('pl-histamine',      '<div class="box say"><div class="bt">跟病人怎麼說</div>', 'before'),
    # ch8
    ('pl-synapse',        T % 'THE KEY STUDY', 'before'),
    # ch9
    ('pl-banxia',         T % 'READING 2', 'before'),
    ('pl-weiqi',          T % 'READING 3', 'before'),
    ('pl-stomach',        T % 'READING 4', 'before'),
    # ch10
    ('pl-herbs',          T % 'BETWEEN THE LINES', 'before'),
    # ch11
    ('pl-tongue',         T % 'QUICK SORT', 'before'),
    # ch12
    ('pl-elderly',        T % 'HARD CASE 4', 'before'),
    ('pl-hotflash',       T % 'HARD CASE 5', 'before'),
    # ch13
    ('pl-acupoints',      '<div class="box warn"><div class="bt">一個數字的警訊</div>', 'before'),
]
