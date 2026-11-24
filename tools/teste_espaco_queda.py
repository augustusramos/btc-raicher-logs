import json,re,sys,datetime as d,pandas as pd,numpy as np
sys.path.insert(0,'.')
from raicher.indicators import rsi, stoch_rsi, sma
L={ # rótulo manual da conclusão dele: Q = espera mais queda/continuação; R = espera reversão/fundo perto/beartrap
'2025-12-26 21:07':'R','2025-12-29 14:16':'R','2025-12-29 21:15':'R','2025-12-31 14:30':'Q','2026-01-29 08:33':'Q',
'2026-02-10 08:37':'Q','2026-02-17 08:39':'R','2026-02-18 21:43':'R','2026-02-27 22:43':'R','2026-02-27 22:45':'R',
'2026-02-28 08:34':'R','2026-03-01 21:24':'Q','2026-03-01 21:27':'Q','2026-03-07 21:13':'R','2026-03-08 21:40':'R',
'2026-03-21 21:14':'R','2026-03-22 14:51':'R','2026-03-22 22:11':'R','2026-06-01 21:10':'R','2026-06-09 21:16':'Q',
'2026-06-18 21:05':'R','2026-06-21 21:42':'R','2026-06-23 08:32':'R','2026-07-13 19:54':'Q','2026-07-31 14:13':'Q',
'2026-07-31 23:31':'Q','2026-08-01 10:02':'R','2026-08-11 21:08':'Q','2026-08-12 19:57':'Q','2026-08-14 08:30':'Q',
'2026-11-12 21:31':'Q','2026-11-16 08:31':'Q','2026-11-24 08:30':'Q'}
casos=json.load(open('calibracao/espaco_queda_casos.json')); txt={t:b for t,b in casos}
D={}
for tf,mins in (('343m',343),('686m',686)):
    df=pd.read_csv(f'/tmp/{tf}.csv',index_col=0,parse_dates=True)
    r=rsi(df.close); k,dd=stoch_rsi(r); ra=sma(r,14)
    f=pd.DataFrame({'close':df.close,'rsi':r,'rsima':ra,'k':k,'d':dd})
    f['kmax6']=k.rolling(6).max(); f['rsimin20']=r.rolling(20).min()
    f['lowmin20']=df.low.rolling(20).min()
    f.index=f.index+pd.Timedelta(minutes=mins)  # horário de fechamento (UTC)
    D[tf]=f
rows=[]
for t,lab in L.items():
    b=txt.get(t,'686' if False else '343')
    tf='686m' if re.match(r'\s*686',b) and not b.strip().startswith('686 e') else '343m'
    T=pd.Timestamp(t,tz='America/Sao_Paulo').tz_convert('UTC')
    f=D[tf]; f=f[f.index<=T]; x=f.iloc[-1]; prev=f.iloc[-2]
    div = (x.close<=f.close.iloc[-20:].min()*1.003) and (x.rsi>x.rsimin20+3)
    rows.append(dict(quando=t,tf=tf[:3],lab=lab,k=round(x.k),d=round(x.d),kmax6=round(x.kmax6),rsi=round(x.rsi,1),rsima=round(x.rsima,1),div=div))
R=pd.DataFrame(rows); pd.set_option('display.width',200); print(R.to_string())
R.to_csv('/tmp/R.csv',index=False)
