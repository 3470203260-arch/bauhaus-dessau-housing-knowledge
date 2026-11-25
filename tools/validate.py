from pathlib import Path
import json,collections
root=Path(__file__).resolve().parents[1]
def read(n):return json.loads((root/'data'/f'{n}.json').read_text(encoding='utf-8'))
s,e,k,r=[read(n) for n in ['sources','entities','knowledge_units','relations']]
errors=[]
for name,data in [('sources',s),('entities',e),('knowledge_units',k),('relations',r)]:
 if len({x['id'] for x in data})!=len(data):errors.append(name+' duplicate IDs')
sid={x['id'] for x in s};eid={x['id'] for x in e};kid={x['id'] for x in k}
for x in k:
 if not set(x['source_ids'].split(';'))<=sid:errors.append(x['id']+' invalid source')
 if not x['locator'] or not x['statement']:errors.append(x['id']+' missing evidence locator')
for x in r:
 if x['subject_id'] not in eid or x['object_id'] not in eid or x['knowledge_id'] not in kid:errors.append(x['id']+' invalid endpoint')
if len({(x['subject'],x['predicate'],x['object']) for x in k})!=len(k):errors.append('duplicate proposition triple')
if len(r)!=len(k) or {x['knowledge_id'] for x in r}!=kid:errors.append('mapping is not one-to-one')
facts=sum(x['epistemic_status']=='来源明示' for x in k);analysis=sum(x['epistemic_status']=='本文分析' for x in k)
stats=read('statistics')
for key,value in [('sources',len(s)),('entities',len(e)),('knowledge_units',len(k)),('relations',len(r)),('explicit',facts),('interpretive',analysis)]:
 if stats[key]!=value:errors.append('incorrect statistic '+key)
result={'ok':not errors,'errors':errors,'sources':len(s),'entities_and_values':len(e),'knowledge_units':len(k),'relations':len(r),'explicit':facts,'interpretive':analysis,'human_verified':0,'note':'Structure validation does not establish historical truth.'}
(root/'data'/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(bool(errors))
