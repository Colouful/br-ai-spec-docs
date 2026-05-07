#!/usr/bin/env python3
"""Read previous component-refactor bugfix memory and print prevention rules."""
import argparse, json, re
from pathlib import Path
DEFAULT_PROJECT_ROOT='/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html'
ISSUE_RE=re.compile(r'## .*? - (?P<issue>[a-z0-9\-]+)')
def read(p): return p.read_text(encoding='utf-8',errors='replace') if p.exists() and p.is_file() else ''
def preventions(text):
    out=[]; lines=text.splitlines()
    for i,line in enumerate(lines):
        low=line.lower()
        if 'how to avoid next time' in low or '下次如何避免' in line or line.strip() in {'## Prevention','### Prevention'}:
            buf=[]
            for nxt in lines[i+1:i+14]:
                if nxt.startswith('## ') or nxt.startswith('---'): break
                if nxt.strip(): buf.append(nxt.strip())
            if buf: out.append('\n'.join(buf))
    return out
def issues(text): return sorted(set(m.group('issue') for m in ISSUE_RE.finditer(text)))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',default=DEFAULT_PROJECT_ROOT); ap.add_argument('--page2'); ap.add_argument('--json-output')
    a=ap.parse_args(); root=Path(a.project_root).expanduser().resolve()
    srcs=[root/'docs/component-refactor/bugfix-log.md', root/'docs/component-refactor/known-issues-prevention.md']
    if a.page2:
        p=Path(a.page2); page2=p if p.is_absolute() else root/p; srcs.append(page2/'__migration__/bugfix-log.md')
    records=[]; all_issues=set(); all_prev=[]
    for s in srcs:
        txt=read(s); its=issues(txt); prs=preventions(txt); all_issues.update(its); all_prev.extend(prs)
        records.append({'source':str(s),'exists':bool(txt),'issue_types':its,'prevention_count':len(prs),'preventions':prs})
    res={'project_root':str(root),'sources':records,'known_issue_types':sorted(all_issues),'preventions':all_prev,'message':'Apply these prevention rules as constraints before editing.' if all_prev else 'No prior prevention rules found.'}
    payload=json.dumps(res,ensure_ascii=False,indent=2)
    if a.json_output: Path(a.json_output).write_text(payload,encoding='utf-8')
    print(payload)
if __name__=='__main__': main()
