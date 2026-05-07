#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
PATTERNS={"koi_import":re.compile(r"@koi-design/[\w\-\/]+"),"old_component_name":re.compile(r"\b(DynamicsFilter|DynamicsForm|EditDrawer|ColumnsSetting|ViewContent|OneLineText|UModal)\b"),"u_tag":re.compile(r"<\/?u-[a-zA-Z0-9\-]+")}
EXT={".vue",".ts",".tsx",".js",".jsx"}
def main():
 p=argparse.ArgumentParser(); p.add_argument('--target',required=True); p.add_argument('--json-output'); a=p.parse_args(); t=Path(a.target); f=[]
 if not t.exists(): raise SystemExit(f"missing target: {t}")
 for path in sorted(t.rglob('*')):
  if path.is_file() and path.suffix in EXT:
   txt=path.read_text(encoding='utf-8',errors='replace')
   for i,line in enumerate(txt.splitlines(),1):
    for kind,pat in PATTERNS.items():
     for m in pat.finditer(line): f.append({'file':str(path),'kind':kind,'line':i,'match':m.group(0),'text':line.strip()[:300]})
 res={'target':a.target,'finding_count':len(f),'findings':f,'pass':len(f)==0}; out=json.dumps(res,ensure_ascii=False,indent=2); print(out)
 if a.json_output: Path(a.json_output).write_text(out,encoding='utf-8')
 if f: raise SystemExit(2)
if __name__=='__main__': main()
