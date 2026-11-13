"""Select only t-new candidates; report t-repro and frozen A8 as controls."""
import argparse
import json
from pathlib import Path

import yaml

from desk.attestation import sha256
from desk.lora import dump
from desk.select import denominators, select
from .common import BASE_REVISION, rows, system_hashes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__);ap.add_argument('--params', default='params.yaml');a = ap.parse_args(argv)
    cfg = yaml.safe_load(Path(a.params).read_text())['todo']['select']
    candidates = [f't-new-R16-e{e}' for e in (1,2,3)]
    if cfg['candidate_arms'] != candidates or cfg['rule'] != 'protocol-v1-section-6' or cfg['tolerance'] != .01:
        raise SystemExit('todo selection pool or rule differs from protocol')
    val = Path('data/todo/t-new/val.jsonl');directory = val.parent / 'validation-runs'
    paths = [directory / 'reference.json'] + [directory / (arm + '.json') for arm in candidates]
    inputs = [json.loads(p.read_text()) for p in paths]
    if [r['arm_id'] for r in inputs[1:]] != candidates:
        raise SystemExit('todo candidate metric arm IDs differ from frozen t-new pool')
    for epoch, obj in enumerate(inputs[1:], 1):
        if obj['rank'] != 16 or obj['epochs'] != epoch or obj.get('role') != 'candidate':
            raise SystemExit('todo candidate rank/epoch/role mismatch')
    for obj in inputs:
        if obj.get('pool') != 't-new' or obj.get('system_sha256s') != system_hashes():raise SystemExit('candidate pool or frozen A8 scorer mismatch')
    result = select(inputs[1:], inputs[0], 'todo', sha256(val), denominators(rows(val), 'todo'))
    controls = []
    for epoch in (1,2,3):
        path = Path(f'data/todo/t-repro/validation-runs/t-repro-R16-e{epoch}.json');obj = json.loads(path.read_text())
        if obj['arm_id'] != f't-repro-R16-e{epoch}' or obj.get('pool') != 't-repro' or obj['validation_sha256'] != sha256('data/todo/t-repro/val.jsonl') or obj['system_sha256s'] != system_hashes():
            raise SystemExit('reproduction control provenance mismatch')
        controls.append(obj);paths.append(path)
    for path in (Path('data/todo/t-repro/validation-runs/reference.json'), Path('data/todo/t-new/controls/t-a8.json')):
        obj = json.loads(path.read_text())
        expected_pool = 't-new' if obj['arm_id'] == 't-a8' else 't-repro'
        expected_arm = 't-a8' if path.name == 't-a8.json' else 't-base'
        if obj['arm_id'] != expected_arm or obj['pool'] != expected_pool or obj['validation_sha256'] != sha256(f'data/todo/{expected_pool}/val.jsonl') or obj['system_sha256s'] != system_hashes():
            raise SystemExit('todo reference/A8 control provenance mismatch')
        controls.append(obj);paths.append(path)
    winner = next((r for r in inputs[1:] if r['arm_id'] == result['selected_arm']), None)
    if winner:
        artifact = winner['artifact'];path = Path(artifact['path'])
        if artifact.get('base_revision') != BASE_REVISION:
            raise SystemExit('selected artifact base revision differs')
        if artifact['sha256s'] != {f.name:sha256(f) for f in path.iterdir() if f.is_file()}:
            raise SystemExit('selected artifact differs from per-run validation receipt')
        result['selected_artifact'] = artifact
    result.update(controls=controls, controls_label='descriptive only; t-repro and frozen t-a8 never candidates; t-a8 validation on t-new contains A8 training requests and is optimistic',
                  input_sha256s={str(p):sha256(p) for p in paths},params_sha256=sha256(a.params),
                  claim='H3 paired non-inferiority, margin -2 pp; held-out evaluator only',
                  contrast='bundled pipeline contrast; no superiority claim')
    dump('data/todo/selected.json', result);print(result['status'], result['selected_arm'])


if __name__ == '__main__':main()
