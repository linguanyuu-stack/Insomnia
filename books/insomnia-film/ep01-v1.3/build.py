import json,re,base64
U='/root/.claude/uploads/28acec4b-5990-570f-ab59-cad4e02ba9a8/8cb1aa6f-Insomnia_EP01_V1.2______01-27.html'
t=open(U,encoding='utf-8').read()
shots=json.loads(re.search(r'id="shots">(.*?)</script>',t,re.S).group(1))
def m(x):
    if x<44.20: return x
    if x<56.55: return x-0.582
    return x-2.306
cutsB=[0,1.8,7.8,14.4,21.7,28.3,37.5,41.7,46.7,55.3,61.3,65.1,68.6,70.1,77.2,82.3,85.3,88.9,92.4,98.2,101.7,112,119.2,124.7,129.3,138.1,145.7]
cuts=[round(m(c),2) for c in cutsB]; cuts[9]=54.10
END=148.74
shots[7]['narration']='為了回答這個問題，我們得回到 1729 年的法國。'
shots[9]['narration']='法國天文學家德梅朗，注意到了一個有趣的現象。'
# camera: (cx,cy,z) from -> to ; fx list
CAM={
'01':((340,224,1.0),(310,232,1.08)),'02':((310,224,1.04),(335,224,1.10)),'03':((340,224,1.0),(340,224,1.05)),
'04':((340,224,1.06),(300,240,1.12)),'05':((340,224,1.0),(385,292,1.3)),'06':((340,224,1.0),(340,224,1.05)),
'07':((340,224,1.0),(340,205,1.1)),'08':((420,224,1.18),(380,224,1.0)),'09':((210,224,1.16),(470,224,1.16)),
'10':((300,224,1.0),(280,250,1.2)),'11':((340,224,1.0),(345,212,1.06)),'12':((345,212,1.06),(345,200,1.1)),
'13':((220,224,1.08),(210,215,1.12)),'14':((340,224,1.0),(340,224,1.06)),'15':((300,205,1.05),(470,245,1.14)),
'16':((210,200,1.1),(185,175,1.28)),'17':((250,224,1.0),(430,224,1.1)),'18':((210,224,1.12),(520,224,1.12)),
'19':((400,224,1.0),(470,230,1.16)),'20':((340,224,1.0),(340,224,1.07)),'21':((300,224,1.0),(345,224,1.05)),
'22':((230,230,1.0),(205,205,1.14)),'23':((340,224,1.0),(340,238,1.1)),'24':((300,260,1.1),(430,260,1.1)),
'25':((340,224,1.0),(390,224,1.06)),'26':((340,224,1.0),(320,224,1.08)),'27':((340,224,1.0),(300,205,1.25)),
}
XF={'12':0.9,'21':0.6,'20':0.5,'23':0.6,'27':0.5}
data=[]
for i,s in enumerate(shots):
    st=cuts[i]; en=cuts[i+1] if i+1<len(cuts) else END
    a,b=CAM[s['id']]
    data.append({"id":s['id'],"title":s['title'],"t0":st,"t1":en,"img":i,"from":a,"to":b,"xf":XF.get(s['id'],0.3),"say":s['narration']})
imgs=[s['image'] for s in shots]
audio='data:audio/mpeg;base64,'+base64.b64encode(open('film/voice.mp3','rb').read()).decode()
html=open('film/template.html',encoding='utf-8').read()
html=html.replace('/*SHOTS*/',json.dumps(data,ensure_ascii=False)).replace('/*IMGS*/',json.dumps(imgs)).replace('__AUDIO__',audio).replace('/*END*/',str(END))
open('/home/user/Insomnia/books/insomnia-film/ep01-v1.3/index.html','w',encoding='utf-8').write(html)
print('ok',len(html), cuts)
