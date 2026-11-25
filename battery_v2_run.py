#!/usr/bin/python3
"""Run Battery v2 against a served model. Usage: battery_v2_run.py <label> <base_url> <model> [max_tokens]"""
import json, sys, time, datetime, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = json.loads((ROOT / 'CASES-v2.json').read_text())
SYSTEM = ("You are a precise, honest assistant. Work through each problem carefully and show your reasoning "
          "and final answers. For numeric answers give exact values. For code, provide a complete working "
          "function in a python code block. If a question cannot be answered from the given facts, or rests "
          "on a false premise, say so plainly rather than inventing an answer.")


def post(base, model, prompt, max_tokens, api_key=None):
    body = {'model': model, 'messages': [{'role': 'system', 'content': SYSTEM},
                                          {'role': 'user', 'content': prompt}],
            'temperature': 0, 'max_tokens': max_tokens, 'stream': False}
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = 'Bearer ' + api_key
    req = urllib.request.Request(base + '/v1/chat/completions',
                                 data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())


def main():
    label = sys.argv[1]; base = sys.argv[2]; model = sys.argv[3]
    max_tokens = int(sys.argv[4]) if len(sys.argv) > 4 else 16000
    api_key = sys.argv[5] if len(sys.argv) > 5 else None
    run = ROOT / 'runs' / (label + '-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    rows = []
    for item in CASES['items']:
        d = run / item['id']; d.mkdir(parents=True, exist_ok=True)
        (d / 'prompt.txt').write_text(item['prompt'])
        t0 = time.time()
        try:
            resp = post(base, model, item['prompt'], max_tokens, api_key)
            (d / 'response.json').write_text(json.dumps(resp, ensure_ascii=False))
            dt = time.time() - t0
            u = resp.get('usage', {})
            fin = resp['choices'][0].get('finish_reason')
            content = resp['choices'][0]['message'].get('content') or ''
            row = {'case_id': item['id'], 'axis': item['axis'], 'seconds': round(dt, 1), 'finish': fin,
                   'usage': u, 'content_len': len(content)}
        except Exception as e:
            (d / 'error.txt').write_text(str(e)); dt = time.time() - t0
            row = {'case_id': item['id'], 'axis': item['axis'], 'seconds': round(dt, 1), 'error': str(e)[:120]}
        rows.append(row)
        print(item['id'], row.get('finish', row.get('error')), str(row['seconds']) + 's', flush=True)
    summary = {'label': label, 'base': base, 'model': model, 'max_tokens': max_tokens,
               'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'rows': rows}
    (run / 'summary.json').write_text(json.dumps(summary, indent=1))
    print('RUN_DIR', run)


if __name__ == '__main__':
    main()