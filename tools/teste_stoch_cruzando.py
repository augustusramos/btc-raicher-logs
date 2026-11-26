"""Quando o Dollynho/Raicher escreve 'Stoch cruzando/cruzou', o cruzamento K x D já estava confirmado no fechamento?"""
import json, re, sys, datetime as dt
import numpy as np, pandas as pd
sys.path.insert(0, '.')
from raicher.indicators import rsi, stoch_rsi

def prep(path, dur_min=None, daily=False):
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    if daily: df['end'] = df.index + pd.Timedelta(days=1)
    else:
        day = df.index.floor('D')
        df['end'] = np.minimum(df.index + pd.Timedelta(minutes=dur_min), day + pd.Timedelta(days=1))
    k, d = stoch_rsi(rsi(df.close)); df['k'] = k; df['d'] = d
    return df

TF = {'343': prep('/tmp/h343.csv', 343), '686': prep('/tmp/h686.csv', 686), '1D': prep('/tmp/1D.csv', daily=True)}

def tf_do_post(txt):
    s = txt.strip().lower()
    if re.match(r'(em resposta a @\w+ / )?(686\b(?! e))', s): return '686'
    if re.search(r'^(em resposta a @\w+ / )?(log|di[áa]rio)', s): return '1D'
    return '343'

def frases(txt):
    out = []
    for m in re.finditer(r'(?i)stoch\w*[^/.;!\n]{0,80}?(cruz\w*|ensai\w*[^/.;!\n]{0,20}cruz\w*)[^/.;!\n]{0,40}', txt):
        f = m.group(0).lower()
        if re.search(r'cruz\w* (a |o |d[ao] )?(resist|suport|regi|linha|n[íi]vel|m[ée]dia|50|80|20)', f): continue  # cruzando um NÍVEL, não K x D
        modo = 'futuro' if re.search(r'ensai|prest|vai cruzar|pode cruzar|tentando|querendo|amea[çc]|poss[íi]vel|chegada', f) else ('passado' if re.search(r'cruzou|confirmou', f) else 'presente')
        m2 = re.search(r'cruz\w*\s+(\w+\s+){0,2}?(bear\w*|bull\w*|para baixo|para cima|de baixo|de cima)', f)
        dire = '?' if not m2 else ('baixa' if re.search(r'bear|baixo$|para baixo|de cima', m2.group(0)) else 'alta')
        out.append((modo, dire, f[:90]))
    return out

def avalia(arquivo, tf_fixo=None):
    rows = json.load(open(arquivo)); res = []
    for pid, ts, body, imgs in rows:
        fs = frases(body)
        if not fs: continue
        tf = tf_fixo or tf_do_post(body); df = TF[tf]
        T = pd.Timestamp(ts, unit='ms', tz='UTC')
        fech = df[df.end <= T]
        if len(fech) < 3 or (T - fech.end.iloc[-1]) > pd.Timedelta(hours=2): continue
        k, d = fech.k.values, fech.d.values
        for modo, dire, f in fs:
            if dire == '?': continue
            sg = 1 if dire == 'alta' else -1
            ja = np.sign(k[-1] - d[-1]) == sg            # no fechamento, K já está do lado novo
            agora = ja and np.sign(k[-2] - d[-2]) != sg  # cruzou exatamente nesse fechamento
            virando = (np.sign(k[-1] - k[-2]) == sg)      # K apontando na direção, mesmo sem cruzar
            res.append(dict(quando=(T - pd.Timedelta(hours=3)).strftime('%Y-%m-%d %H:%M'), tf=tf, modo=modo, dir=dire,
                            confirmado=bool(ja), cruzou_neste=bool(agora), so_virando=bool(virando and not ja), k=round(k[-1], 1), d=round(d[-1], 1), frase=f))
    return res

if __name__ == '__main__':
    out = {}
    for nome, arq in (('dollynho', 'calibracao/historico/dollynho_posts.json'), ('raicher', 'calibracao/historico/raicher_posts.json')):
        r = avalia(arq); out[nome] = r
        df = pd.DataFrame(r)
        if df.empty: print(nome, 'nada'); continue
        print(f'== {nome}: {len(df)} frases')
        print(df.groupby(['modo']).agg(n=('confirmado', 'size'), confirmado=('confirmado', 'mean'), cruzou_neste=('cruzou_neste', 'mean'), so_virando=('so_virando', 'mean')).round(2))
        print(df.groupby(['tf']).confirmado.agg(['size', 'mean']).round(2))
    json.dump(out, open('calibracao/teste_stoch_cruzando.json', 'w'), ensure_ascii=False, indent=1)
