"""Validate the published knowledge repository using the Python standard library.

Structural checks cannot certify historical truth or stand in for personal review.
"""
from pathlib import Path
import argparse,collections,csv,json,re,sqlite3,struct

def validate(root):
 errors=[]
 def fail(message):errors.append(message)
 def read(name):
  return json.loads((root/'data'/f'{name}.json').read_text(encoding='utf-8'))
 def csvread(name):
  with (root/'data'/f'{name}.csv').open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
 core={n:read(n) for n in ['sources','entities','knowledge_units','relations']}
 for name,rows in core.items():
  ids=[r.get('id','') for r in rows]
  if not all(ids) or len(set(ids))!=len(ids):fail(name+': empty/duplicate identifier')
  if csvread(name)!=rows:fail(name+': CSV/JSON mismatch')
 s,e,k,r=[core[n] for n in ['sources','entities','knowledge_units','relations']]
 sid={x['id'] for x in s};labels={x['id']:x['label'] for x in e};kid={x['id']:x for x in k}
 for x in s:
  if any(not x.get(f,'').strip() for f in ['author','title','category','url','locator','reference','access_scope','accessed']):fail(x['id']+': incomplete source metadata')
  if not x['url'].startswith('https://'):fail(x['id']+': invalid source URL')
 if len({x['label'] for x in e})!=len(e):fail('duplicate entity label')
 alias_owner={}
 for x in e:
  for name in [x['label'],*filter(None,x['aliases'].split(';'))]:
   normalized=re.sub(r'[\s·._-]','',name).casefold()
   if normalized in alias_owner and alias_owner[normalized]!=x['id']:fail('alias collision: '+name)
   alias_owner[normalized]=x['id']
 for x in k:
  if not set(x['source_ids'].split(';'))<=sid:fail(x['id']+': unknown source')
  if any(not x.get(f,'').strip() for f in ['subject','predicate','object','statement','locator','review_status']):fail(x['id']+': missing proposition/evidence field')
  if x['epistemic_status'] not in ['来源明示','本文分析']:fail(x['id']+': unknown epistemic status')
 if len({(x['subject'],x['predicate'],x['object']) for x in k})!=len(k):fail('duplicate proposition triple')
 for x in r:
  if x['subject_id'] not in labels or x['object_id'] not in labels or x['knowledge_id'] not in kid:
   fail(x['id']+': invalid relation endpoint');continue
  u=kid[x['knowledge_id']]
  if labels[x['subject_id']]!=u['subject'] or labels[x['object_id']]!=u['object']:fail(x['id']+': endpoint label/proposition mismatch')
  for f in ['predicate','source_ids','epistemic_status']:
   if x[f]!=u[f]:fail(x['id']+': relation/proposition mismatch '+f)
 if len(r)!=len(k) or collections.Counter(x['knowledge_id'] for x in r)!=collections.Counter(x['id'] for x in k):fail('relation/knowledge mapping not one-to-one')
 # Read-only connection avoids accidental changes during verification.
 with sqlite3.connect((root/'knowledge.sqlite').resolve().as_uri()+'?mode=ro',uri=True) as con:
  con.row_factory=sqlite3.Row
  if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok':fail('SQLite integrity check failed')
  for name,rows in core.items():
   actual=[dict(x) for x in con.execute('SELECT * FROM '+name+' ORDER BY id')]
   if actual!=sorted(rows,key=lambda x:x['id']):fail(name+': SQLite mismatch')
  queries=[q.strip() for q in re.sub(r'--[^\n]*','',(root/'docs/queries.sql').read_text(encoding='utf-8')).split(';') if q.strip()]
  if len(queries)!=3:fail('expected three evaluation queries')
  expected=[{x['id'] for x in k if x['subject'] in ['大师住宅','托尔滕排屋','外廊住宅'] and x['epistemic_status']=='来源明示'},{x['id'] for x in k if x['subject']=='梅耶设计方法' or x['predicate'] in ['设计实施','设计领导']},{x['id'] for x in k if x['epistemic_status']=='本文分析'}]
  for i,q in enumerate(queries):
   actual={x['id'] for x in con.execute(q)}
   if i>=len(expected) or actual!=expected[i]:fail('evaluation SQL differs from stated scope: '+str(i+1))
 html=(root/'index.html').read_text(encoding='utf-8');marker='<script id="payload" type="application/json">';start=html.index(marker)+len(marker);payload=json.loads(html[start:html.index('</script>',start)])
 for name,rows in core.items():
  if payload[name]!=rows:fail('HTML embedded mismatch: '+name)
 for g in payload['graphs']:
  if not set(g['nodes'])<=set(labels.values()) or set(g['nodes'])!=set(g['positions']):fail(g['id']+': graph node/layout mismatch')
  if any(not(0<=p[0]<=1200 and 0<=p[1]<=640) for p in g['positions'].values()):fail(g['id']+': graph position out of view')
 for i in [1,2,3]:
  raw=(root/'figures'/f'screenshot{i}.png').read_bytes()
  if raw[:8]!=b'\x89PNG\r\n\x1a\n':fail('invalid screenshot PNG '+str(i));continue
  width,height=struct.unpack('>II',raw[16:24])
  if width<1200 or height<600:fail('low resolution screenshot '+str(i))
 for name in ['source_roles','relation_dictionary','argument_checks']:
  if read(name)!=csvread(name):fail(name+': CSV/JSON mismatch')
 # Case CSV is an intentional reading projection; list fields use semicolons.
 cases=csvread('case_comparisons');case_json=read('case_comparisons')
 projected=[{f:';'.join(x[f]) if isinstance(x[f],list) else x[f] for f in cases[0]} for x in case_json] if cases else []
 if cases!=projected:fail('case comparison CSV projection mismatch')
 roles=read('source_roles')
 if collections.Counter(x['source_id'] for x in roles)!=collections.Counter(sid):fail('source roles do not cover each source once')
 for x in roles:
  source=next((y for y in s if y['id']==x['source_id']),None)
  if source and (x['actual_scope']!=source['access_scope'] or x['source_url']!=source['url']):fail(x['source_id']+': source role metadata mismatch')
 dictionary=read('relation_dictionary');counts=collections.Counter(x['predicate'] for x in k)
 if collections.Counter(x['predicate'] for x in dictionary)!=collections.Counter(counts.keys()):fail('relation dictionary incomplete or duplicate')
 for d in dictionary:
  actual=[x for x in k if x['predicate']==d['predicate']]
  if str(len(actual))!=d['actual_count'] or set(d['knowledge_ids'].split(';'))!={x['id'] for x in actual}:fail(d['predicate']+': dictionary count/knowledge IDs mismatch')
  if not d['definition'].strip() or any(x['epistemic_status']!=d['epistemic_status'] for x in actual):fail(d['predicate']+': dictionary definition/evidence mismatch')
 for x in read('argument_checks'):
  u=kid.get(x['knowledge_id'])
  if not u or u['epistemic_status']!='本文分析':fail(x['id']+': argument must reference an analysis');continue
  if any(x[f]!=u[f] for f in ['statement','source_ids','locator']):fail(x['id']+': argument evidence mismatch')
  if not x['inference_limit'] or not x['revision_condition']:fail(x['id']+': missing inference boundary')
 human=csvread('human_review');reviewed=[]
 if collections.Counter(x['knowledge_id'] for x in human)!=collections.Counter(kid.keys()):fail('human review template incomplete/duplicate')
 for x in human:
  u=kid.get(x['knowledge_id'])
  if u and (x['source_ids']!=u['source_ids'] or x['locator']!=u['locator']):fail(x['knowledge_id']+': review locator mismatch')
  pending=x['result'] in ['待本人核验','未核验','']
  if not pending:
   if x['result'] not in ['支持','部分支持','不支持','无法判定']:fail(x['knowledge_id']+': unrecognized human judgment')
   if not x['reviewer'] or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',x['date']) or not x['correction']:fail(x['knowledge_id']+': incomplete actual review record')
   reviewed.append(x)
  elif x['reviewer'] or x['date']:fail(x['knowledge_id']+': pending review has signature/date')
 stats=read('statistics');computed=dict(sources=len(s),entities=len(e),knowledge_units=len(k),relations=len(r),explicit=sum(x['epistemic_status']=='来源明示' for x in k),interpretive=sum(x['epistemic_status']=='本文分析' for x in k),human_verified=len(reviewed))
 for f,value in computed.items():
  if stats[f]!=value:fail('statistic mismatch '+f)
 if stats['relations_by_type']!=dict(counts):fail('predicate statistics mismatch')
 if stats['source_categories']!=dict(collections.Counter(x['category'] for x in s)):fail('source category statistics mismatch')
 if payload['statistics']!=stats:fail('HTML statistics mismatch')
 return dict(ok=not errors,errors=errors,sources=len(s),entities_and_values=len(e),knowledge_units=len(k),relations=len(r),explicit=computed['explicit'],interpretive=computed['interpretive'],human_verified=len(reviewed),predicate_types=len(counts),query_rows=[len(x) for x in expected],note='Structure validation does not establish historical truth or personal review.')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--no-write',action='store_true');args=parser.parse_args()
 try:result=validate(args.root)
 except (OSError,ValueError,KeyError,TypeError,sqlite3.Error) as exc:result={'ok':False,'errors':[type(exc).__name__+': '+str(exc)],'note':'Validation stopped on invalid or unreadable input.'}
 if not args.no_write:(args.root/'data/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=True));raise SystemExit(0 if result['ok'] else 1)
