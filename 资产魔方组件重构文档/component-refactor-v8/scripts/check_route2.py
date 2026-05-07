#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--route2',required=True); p.add_argument('--router-index',required=True); p.add_argument('--expected-route-fragment',required=True); p.add_argument('--expected-component-fragment'); p.add_argument('--json-output'); a=p.parse_args()
 errors=[]; warnings=[]; r=Path(a.route2); idx=Path(a.router_index); rt=''; it=''
 if not r.exists(): errors.append({'kind':'missing_route2_file','message':str(r)})
 else: rt=r.read_text(encoding='utf-8',errors='replace')
 if not idx.exists(): errors.append({'kind':'missing_router_index','message':str(idx)})
 else: it=idx.read_text(encoding='utf-8',errors='replace')
 if rt and a.expected_route_fragment not in rt: errors.append({'kind':'route2_missing_expected_route_fragment','message':a.expected_route_fragment})
 if a.expected_component_fragment and rt and a.expected_component_fragment not in rt: errors.append({'kind':'route2_missing_expected_component_fragment','message':a.expected_component_fragment})
 if it and r.stem not in it and r.name not in it: warnings.append({'kind':'router_index_registration_not_obvious','message':r.stem})
 res={'route2':a.route2,'router_index':a.router_index,'expected_route_fragment':a.expected_route_fragment,'expected_component_fragment':a.expected_component_fragment,'pass':len(errors)==0,'errors':errors,'warnings':warnings}
 out=json.dumps(res,ensure_ascii=False,indent=2); print(out)
 if a.json_output: Path(a.json_output).write_text(out,encoding='utf-8')
 if errors: raise SystemExit(2)
if __name__=='__main__': main()
