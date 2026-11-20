import sys; sys.path.insert(0,'.')
from lib import *
b = head(100,100,2,0,'open','short') + head(280,100,2,0,'closed','long') + head(460,100,2,0,'wide','grey',age='old',sweat=True) + hand(560,100,2.5) + head(650,140,1.2,-90,'open','short')
write('_t1', fig('pl-t','T','t','t',230,'t',b,'t'))
