"""python tools/rapido.py arquivo print quando post 'Y json' 'R json' 'chk json' 'dias' 'zx' [fator]"""
import json, sys, subprocess
a = sys.argv
Y = json.loads(a[5]); R = json.loads(a[6]); chk = json.loads(a[7])
dias = a[8].split(','); zx = [float(v) for v in a[9].split(',')]; f = float(a[10]) if len(a) > 10 else 1.4507
Yp = [[y, p] for y, p in Y]
d = {"arquivo": a[1], "print": a[2], "quando": a[3], "post": a[4], "y": Yp, "checks": [[y, p] for y, p in chk],
     "xz_fator": f, "xz": [[z, dd] for z, dd in zip(zx, dias)],
     "linhas": {n: {"cor": v[6] if len(v) > 6 else "", "estilo": v[7] if len(v) > 7 else "", "nota": v[8] if len(v) > 8 else "",
                    "m": v[0], "c": v[1], "res": v[2], "x0": v[3], "x1": v[4]} for n, v in R.items()}}
json.dump(d, open('/tmp/s.json', 'w'), ensure_ascii=False)
print(subprocess.run(['python3', 'tools/salva_print.py', '/tmp/s.json'], capture_output=True, text=True).stdout)
