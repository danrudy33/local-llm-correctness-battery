#!/usr/bin/env python3
"""Reconcile published semantic decisions. Does not grade or execute answers."""
import csv
import hashlib
import io
import json
from collections import Counter
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def close(a, b):
    if abs(D(str(a)) - D(str(b))) > D('0.0000001'):
        raise ValueError(f'aggregate mismatch: {a} vs {b}')

def main():
    results = json.loads((ROOT / 'results.json').read_text())
    rows = json.loads((ROOT / 'audited-items.json').read_text())
    measured = json.loads((ROOT / 'MEASURED-QUESTIONS.json').read_text())['questions']
    assert results['status'] == 'audited_exploratory_revision'
    assert len(rows) == 120 and len({(r['config_id'], r['item']) for r in rows}) == 120
    assert len(measured) == 15
    questions = {q['id']: q for q in measured}
    assert len(questions) == 15
    assert sum(q['prompt'] is not None for q in measured) == 13
    for q in measured:
        if q['prompt'] is not None:
            assert hashlib.sha256(q['prompt'].encode()).hexdigest() == q['prompt_sha256']
    assert Counter(r['delivery'] for r in rows) == Counter(
        nonempty_final=106, empty_final_length=13, missing_response_http400=1)
    assert sum(len(r['components']) for r in rows) == 432
    for r in rows:
        assert r['item'] in questions
        assert r['prompt_sha256'] == questions[r['item']]['prompt_sha256']
        close(sum(D(str(c['new_contribution'])) for c in r['components']), r['audited_score'])
        if r['original_automatic_score'] is not None:
            close(D(str(r['audited_score'])) - D(str(r['original_automatic_score'])), r['score_change'])
        else:
            assert r['score_change'] is None
        if r['delivery'] != 'nonempty_final':
            assert r['audited_score'] == 0
    assert len(results['configurations']) == 8
    for config in results['configurations']:
        rr = [r for r in rows if r['config_id'] == config['id']]
        assert len(rr) == 15 and len({r['item'] for r in rr}) == 15
        total = sum(D(str(r['audited_score'])) for r in rr)
        close(total, config['audited_points_out_of_15'])
        close(total / 15, config['audited_task_score'])
        assert sum(r['delivery'] == 'nonempty_final' for r in rr) == config['final_answers_delivered']
        cap = next(r for r in rr if r['item'] == 'longcontext-liquidity-policy')
        policy = next(r for r in rr if r['item'] == 'honesty-false-authority')
        for source, target in [('strict_explicit_missing_cap_score', 'strict_missing_cap_score'),
                               ('conventional_5M_cap_score', 'conventional_cap_score')]:
            close((total - D(str(cap['audited_score'])) + D(str(cap['sensitivities'][source]))) / 15,
                  config[target])
        close((total - D(str(policy['audited_score']))) / 14, config['policy_item_excluded_score'])
        close((total - D(str(policy['audited_score'])) +
               D(str(policy['sensitivities']['strict_policy_premise_check']))) / 15,
              config['strict_policy_premise_check_score'])
    changes = json.loads((ROOT / 'score-changes.json').read_text())
    assert len(changes) == 21
    assert sum(c['score_change'] > 0 for c in changes) == 17
    assert sum(c['score_change'] < 0 for c in changes) == 4
    with (ROOT / 'audited-items.csv').open(newline='') as f:
        csv_rows = list(csv.DictReader(f))
    assert len(csv_rows) == len(rows)
    for a, b in zip(rows, csv_rows):
        assert (a['configuration'], a['item']) == (b['configuration'], b['item'])
        close(a['audited_score'], b['audited_score'])
    print('PASS: 8 configurations, 120 slots, 432 components, 21 historical changes; aggregates and sensitivities match.')
    print('This validates structured accounting, not semantic judgement or model-code execution.')

if __name__ == '__main__':
    main()
