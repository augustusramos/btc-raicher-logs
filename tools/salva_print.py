"""Uso: python tools/salva_print.py spec.json  -> grava .medidas.json e .json em calibracao/linhas_prints e confere linhas repetidas."""
import json, sys, math, glob, datetime as dt, subprocess
spec = json.load(open(sys.argv[1]))
if 'xz' in spec:
    f = spec.pop('xz_fator'); spec['x'] = [[round(z * f, 1), d] for z, d in spec.pop('xz')]
nome = spec['arquivo']; base = f'calibracao/linhas_prints/{nome}'
json.dump(spec, open(base + '.medidas.json', 'w'), ensure_ascii=False)
print(subprocess.run(['python3', 'tools/linhas_print.py', base + '.medidas.json', base + '.json'], capture_output=True, text=True).stdout)
def val(L, t):
    (a, pa), (b, pb) = L['p1'], L['p2']; ta, tb, tt = [dt.datetime.fromisoformat(x).timestamp() for x in (a, b, t)]
    return round(pa * math.exp(math.log(pb / pa) * (tt - ta) / (tb - ta)))
novo = json.load(open(base + '.json'))
t = novo['linhas'][next(iter(novo['linhas']))]['p1'][0][:10] + ' 12:00'
for n, L in novo['linhas'].items():
    out = []
    for f in sorted(glob.glob('calibracao/linhas_prints/2*_343.json')):
        if f.endswith(nome + '.json') or f.endswith('.medidas.json'): continue
        o = json.load(open(f))['linhas'].get(n)
        if o: out.append((f.split('/')[-1][:16], val(o, t)))
    if out: print('  conf', n, t, 'novo', val(L, t), 'antes', out[-3:])
