import sys; sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from clk_lib import write
from clk_mimosa_lib import plant
body = plant(190, 300, 1.0, False) + plant(560, 300, 1.0, True)
write('pp-mimosa', '圖 1·A', 'test', 'test', 360, body, 'x', 'x')
