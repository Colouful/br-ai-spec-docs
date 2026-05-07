#!/usr/bin/env python3
import argparse, json, re, subprocess
from pathlib import Path
EXT={".vue",".ts",".tsx",".js",".jsx"}
BAD={"koi_import":re.compile(r"@koi-design/[\w\-\/]+"),"old_component_name":re.compile(r"\b(DynamicsFilter|DynamicsForm|EditDrawer|ColumnsSetting|ViewContent|OneLineText|UModal)\b"),"u_tag":re.compile(r"<\/?(u-[a-zA-Z0-9\-]+)")}
PRO=re.compile(r"<ProActions\b([\s\S]*?)(?:\/>|>)"); MAX2=re.compile(r"(:?max-visible-count|:maxVisibleCount|maxVisibleCount)\s*=\s*[\"'](?:2|\{?2\}?)[\"']")
PM=re.compile(r"<ProModalForm\b([\s\S]*?)(?:\/>|>)"); MODAL_PROPS=re.compile(r"(modal-props|modalProps)[\s\S]{0,240}titleAlign\s*:\s*[\"']start[\"']"); DRAWER=re.compile(r"type\s*=\s*[\"']drawer[\"']")
AM=re.compile(r"<a-modal\b([\s\S]*?)(?:\/>|>)"); TA=re.compile(r"(title-align\s*=\s*[\"']start[\"']|titleAlign\s*:\s*[\"']start[\"'])")
def main():
 p=argparse.ArgumentParser(); p.add_argument('--page2',required=True); p.add_argument('--original'); p.add_argument('--allow-u-tags',default=''); p.add_argument('--json-output'); a=p.parse_args()
 root=Path(a.page2); allow={x.strip() for x in a.allow_u_tags.split(',') if x.strip()}; errors=[]; warnings=[]
 if not root.exists(): errors.append({'kind':'missing_page2','message':str(root)})
 else:
  for path in sorted(root.rglob('*')):
   if path.is_file() and path.suffix in EXT:
    txt=path.read_text(encoding='utf-8',errors='replace')
    for i,line in enumerate(txt.splitlines(),1):
     for kind,pat in BAD.items():
      for m in pat.finditer(line):
       val=m.group(1) if kind=='u_tag' else m.group(0)
       if kind=='u_tag' and val in allow: continue
       errors.append({'kind':kind,'file':str(path),'line':i,'match':val,'text':line.strip()[:300]})
    for m in PRO.finditer(txt):
     if not MAX2.search(m.group(0)): warnings.append({'kind':'proactions_missing_max_visible_count_2','file':str(path),'line':txt[:m.start()].count('\n')+1})
    for m in PM.finditer(txt):
     b=m.group(0)
     if not DRAWER.search(b) and not MODAL_PROPS.search(b): warnings.append({'kind':'promodalform_modal_missing_modal_props_title_align_start','file':str(path),'line':txt[:m.start()].count('\n')+1})
    for m in AM.finditer(txt):
     if not TA.search(m.group(0)): warnings.append({'kind':'arco_modal_missing_title_align_start','file':str(path),'line':txt[:m.start()].count('\n')+1})
 orig={'checked':False,'pass':None}
 if a.original:
  proc=subprocess.run(['git','diff','--',a.original],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  diff=proc.stdout.strip(); orig={'checked':True,'pass':proc.returncode==0 and diff=='','diff_preview':diff[:4000],'stderr':proc.stderr[:1000]}
 passed=(not errors) and (orig['pass'] in (True,None))
 res={'page2':a.page2,'original':a.original,'pass':passed,'page2_error_count':len(errors),'page2_errors':errors,'warning_count':len(warnings),'warnings':warnings,'original_diff':orig}
 out=json.dumps(res,ensure_ascii=False,indent=2); print(out)
 if a.json_output: Path(a.json_output).write_text(out,encoding='utf-8')
 if not passed: raise SystemExit(2)
if __name__=='__main__': main()
