"""Validate auxiliary reading records; does not certify historical truth or visual quality."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
def read(name):return json.loads((root/'data'/f'{name}.json').read_text(encoding='utf-8'))
p,t,v,c,k,s=[read(n) for n in ['presentation_profile','presentation_task','presentation_review','case_comparisons','knowledge_units','sources']]
kd={x['id']:x for x in k};sid={x['id'] for x in s};rules={x['rule_id'] for x in p['rules']}
assert p['id']==t['profile_id']==v['profile_id']
assert t['id']==v['task_id'] and p['version']==t['version']==v['version']
assert p['method_reference']['historical_evidence'] is False
assert p['method_reference']['id'] not in sid
assert len(rules)==len(p['rules'])
for rule in p['rules']:
 assert rule['priority'] in ['must','should','may']
 assert rule['change_class'] in ['core','project_locked','conditional','free']
 assert all(rule.get(field) for field in ['condition','verification','method_locator'])
for case in c:
 assert set(case['rule_ids'])<=rules and set(case['source_ids'])<=sid
 for field,status in [('evidence_ids','来源明示'),('interpretation_ids','本文分析')]:
  for ref in case[field]:assert kd[ref]['epistemic_status']==status
 for ref in case['evidence_ids']+case['interpretation_ids']+case['method_ids']:
  assert set(kd[ref]['source_ids'].split(';'))<=set(case['source_ids'])
 assert case['unknown'] and case['interface']
assert all(x['status'] in ['pass','pending','unknown','fail'] for x in v['checks'])
print('PASS: auxiliary case/rule/task/review references. Historical counts unchanged; no human acceptance implied.')
