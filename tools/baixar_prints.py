"""Baixa os prints do Dollynho listados em calibracao/historico/*.json.
Escolhe, para cada dia, o último post de 343 (ou "686 e 343") e o último Diário/Log, e baixa as imagens em tamanho medium.
Uso (no GitHub Actions): python tools/baixar_prints.py saida/
"""
import json, sys, glob, datetime as dt, urllib.request, pathlib, re, time
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rows = []
for f in sorted(glob.glob('calibracao/historico/dollynho_posts_*.json')):
    rows += json.load(open(f))
seen = {}
for pid, ts, body, imgs in sorted(rows, key=lambda r: r[1]):
    t = dt.datetime.utcfromtimestamp(ts / 1000) - dt.timedelta(hours=3)
    b = body.strip()
    if re.match(r'^(343|686 e 343|686 & 343)', b): kind = '343'
    elif re.match(r'^(Log ?\d+|DI[ÁA]RIO)', b): kind = '1D'
    else: continue
    seen[(t.date(), kind)] = (pid, t, imgs)
idx = []
for (d, kind), (pid, t, imgs) in sorted(seen.items()):
    for k, fn in enumerate(imgs):
        name = f"{t:%Y-%m-%d_%H%M}_{kind}_{pid}_{k}.{fn.split('.')[-1]}"
        p = out / name
        if not p.exists():
            base, ext = fn.rsplit('.', 1)
            url = f"https://pbs.twimg.com/media/{base}?format={ext}&name=medium"
            try:
                p.write_bytes(urllib.request.urlopen(url, timeout=30).read())
            except Exception as e:
                print('falhou', url, e); continue
            time.sleep(0.2)
        idx.append({'arquivo': name, 'post': pid, 'quando': f"{t:%Y-%m-%d %H:%M}", 'tf': kind})
(out / 'index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=0))
print(len(idx), 'imagens')
