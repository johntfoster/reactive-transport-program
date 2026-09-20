#!/usr/bin/env python3
"""Audit registered papers read-only; build a snapshot-based program dashboard."""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text())


def audit(program=ROOT, papers=None):
    registry=read(program/'portfolio.json');results=[];seen=set()
    for entry in registry['projects']:
        name=entry['id']
        if name in seen:raise ValueError('duplicate project: '+name)
        seen.add(name)
        record={'id':name,'repository':entry['repository'],'observation':'committed-snapshot','errors':[]}
        snapshot=(program/entry['manifest']).resolve()
        if not snapshot.is_relative_to(program.resolve()):raise ValueError('snapshot escapes program')
        m=read(snapshot)
        if papers:
            checkout=(papers/entry['directory']).resolve()
            if checkout.parent!=papers.resolve():raise ValueError('checkout escapes explicit paper parent')
            record['observation']='live-local'
            if not (checkout/'research-project.yml').is_file():
                record['errors'].append('checkout or project manifest unavailable')
            else:
                m=read(checkout/'research-project.yml')
                r=subprocess.run(['git','--no-optional-locks','-C',str(checkout),'status','--porcelain=v1','-uall'],text=True,capture_output=True)
                if r.returncode:record['errors'].append('Git status unavailable')
                else:record['dirty_paths']=r.stdout.splitlines()
                r=subprocess.run(['git','--no-optional-locks','-C',str(checkout),'rev-parse','HEAD'],text=True,capture_output=True)
                record['head']=r.stdout.strip() if r.returncode==0 else None
        if m.get('id')!=name or m.get('repository')!=entry['repository']:record['errors'].append('registry/manifest identity mismatch')
        for k in ['status','workflow','publication','verification','next_milestone']:
            record[k]=m.get(k)
            if k not in m:record['errors'].append('missing '+k)
        results.append(record)
    return {'schema_version':1,'projects':results,'errors':sum(len(x['errors']) for x in results),'paper_repositories_modified':False}


def build(output):
    p=output if output.is_absolute() else ROOT/output;p=p.resolve()
    if not p.is_relative_to((ROOT/'.agent-runtime').resolve()):raise ValueError('output must be below .agent-runtime/')
    report=audit();p.mkdir(parents=True,exist_ok=True)
    cards=[];e=html.escape
    for item in report['projects']:
        pub=item['publication'];site=pub['site'].get('url');code=pub['codespace']['url']
        links=f'<a href="{e(item["repository"],quote=True)}">Source</a> · <a href="{e(code,quote=True)}">Codespace</a>'
        if site:links+=f' · <a href="{e(site,quote=True)}">Companion site</a>'
        release=pub.get('release',{}).get('url')
        if release:links+=f' · <a href="{e(release,quote=True)}">Release</a>'
        verification=''.join(f'<li>{e(k.replace("_"," "))}: {e(v)}</li>' for k,v in item['verification'].items())
        cards.append(f'<article><h2>{e(item["id"])}</h2><p>{links}</p><p>{e(item["status"])} · workflow {e(item["workflow"]["release"])}</p><p>{e(item["next_milestone"])}</p><ul>{verification}</ul></article>')
    document='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reactive transport research program</title><style>body{font:17px/1.6 system-ui;background:#f4f7fa;color:#1c3447;max-width:1120px;margin:3rem auto;padding:0 1.5rem}h1{font-size:2.6rem;line-height:1.15}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:1.2rem}article{padding:1.5rem;background:white;border:1px solid #cbd7df;border-radius:8px}h2{overflow-wrap:anywhere;font-size:1.3rem}a{color:#006b80}li{font-size:.9rem}</style></head><body><p>Independent papers · versioned workflows</p><h1>Reactive transport research program</h1><p>Four active publication repositories. This coordination layer reports recorded evidence; each paper retains scientific authority. Launch links and tooling checks do not establish scientific validation.</p><p><a href="https://github.com/johntfoster/reactive-transport-program">Program source and decisions</a> · <a href="status.json">Machine-readable status</a></p><div class="grid">'''+''.join(cards)+'''</div><h2>Archived work</h2><p>Inactive projects are preserved separately. Archival status reflects current work scope, not a scientific judgment.</p></body></html>'''
    (p/'index.html').write_text(document+'\n');(p/'status.json').write_text(json.dumps(report,indent=2)+'\n')
    return p


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    a=sub.add_parser('audit');a.add_argument('--root',type=Path)
    b=sub.add_parser('build');b.add_argument('--output',type=Path,default=Path('.agent-runtime/site'))
    args=p.parse_args()
    try:
        if args.action=='audit':
            result=audit(papers=args.root);print(json.dumps(result,indent=2));return bool(result['errors'])
        print(build(args.output));return 0
    except (OSError,ValueError,KeyError) as e:print('portfolio: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
