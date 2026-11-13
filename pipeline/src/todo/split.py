"""Preserve A8 reproduction data and re-split non-test requests by whole groups."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
import shutil

from desk.attestation import sha256
from desk.leakcheck import fingerprint, near_pairs, note_hash
from desk.lora import dump
from .common import lines, rows
from .import_a8 import ARM, verify as verify_import


def memberships(requests, seed=7311):
    if seed != 7311:
        raise ValueError('protocol requires split seed 7311')
    ids = [r['id'] for r in requests]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError('request IDs must be unique and nonempty')
    parent = list(range(len(requests)))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]];i = parent[i]
        return i
    def union(a, b):
        a, b = root(a), root(b)
        parent[max(a, b)] = min(a, b)
    seen = {}
    for i, r in enumerate(requests):
        for field in ('family', 'template'):
            if not isinstance(r.get(field), str) or not r[field]:
                raise ValueError('every request requires recorded family and template IDs')
            key = (field, r[field])
            if key in seen:union(seen[key], i)
            seen[key] = i
        key = ('exact', note_hash(r['query']))
        if key in seen:union(seen[key], i)
        seen[key] = i
    for a, b, _ in near_pairs([fingerprint(r['query']) for r in requests]):
        union(a, b)
    groups = defaultdict(list)
    for i, r in enumerate(requests):groups[root(i)].append(r['id'])
    keys = sorted(groups, key=lambda k: min(groups[k]))
    if len(keys) < 2:
        raise ValueError('corpus has fewer than two independent groups')
    random.Random(seed).shuffle(keys)
    nval = max(1, round(len(keys) * .1))
    validation = set(keys[:nval])
    return [{'request_id': r['id'], 'family': r['family'], 'template': r['template'],
             'group_id': min(groups[root(i)]), 'split': 'validation' if root(i) in validation else 'train'}
            for i, r in enumerate(requests)]


def map_training_rows(requests, training_rows):
    """A8 rows have no ID; join by original split/query and refuse ambiguous sides."""
    lookup = defaultdict(list)
    for r in requests:lookup[(r['split'], r['query'])].append(r['id'])
    result = []
    for split, values in training_rows.items():
        for row in values:
            ids = lookup[(split, row['query'])]
            if not ids:raise ValueError('training row has no source request')
            result.append((row, ids))
    return result


def verify(pool):
    data = Path('data/todo') / pool
    receipt = json.loads((data / 'split-receipt.json').read_text())
    if receipt['sha256s'] != {n: sha256(data / n) for n in receipt['sha256s']}:
        raise SystemExit('todo split receipt is stale')
    if receipt['source_sha256s'] != {n: sha256(ARM / 'inputs/data' / n) for n in receipt['source_sha256s']}:
        raise SystemExit('todo split source differs from frozen A8')
    membership = json.loads((data / 'split-membership.json').read_text())
    if pool == 't-new':
        source_train = {r['id'] for r in rows(ARM / 'inputs/data/requests.jsonl') if r['split'] == 'train'}
        if len(source_train) != 6278 or {r['request_id'] for r in membership} != source_train:
            raise SystemExit('t-new must cover exactly A8 arm-1 training requests')
        if any(r.get('original_split') != 'train' for r in rows(data / 'requests.jsonl')):
            raise SystemExit('A8 validation entered t-new')
        for field in ('family', 'template', 'group_id'):
            sides = defaultdict(set)
            for r in membership:sides[r[field]].add(r['split'])
            if any(len(v) != 1 for v in sides.values()):raise SystemExit('todo grouping crosses partitions')
    else:
        for source, target in (('train.jsonl', 'train.jsonl'), ('validation.jsonl', 'validation-rows.jsonl')):
            if (ARM / 'inputs/data' / source).read_bytes() != (data / target).read_bytes():
                raise SystemExit('t-repro original A8 rows changed')
    return receipt


def build():
    imported = verify_import()
    source = ARM / 'inputs/data'
    requests = [r for r in rows(source / 'requests.jsonl') if r['split'] in ('train', 'validation')]
    original = {'train': rows(source / 'train.jsonl'), 'validation': rows(source / 'validation.jsonl')}
    labelled = map_training_rows(requests, original)
    source_hashes = imported['corpus_sha256s']
    for pool in ('t-repro', 't-new'):
        data = Path('data/todo') / pool;data.mkdir(parents=True, exist_ok=True)
        pool_requests = [r for r in requests if r['split'] == 'train'] if pool == 't-new' else requests
        pool_rows = map_training_rows(pool_requests, {'train': original['train']}) if pool == 't-new' else labelled
        manifest = memberships(pool_requests) if pool == 't-new' else [
            {'request_id': r['id'], 'family': r['family'], 'template': r['template'],
             'group_id': r['family'], 'split': r['split']} for r in pool_requests]
        sides = {r['request_id']: r['split'] for r in manifest}
        selected = {split: [dict(r, original_split=r['split'], split=split) for r in pool_requests if sides[r['id']] == split]
                    for split in ('train', 'validation')}
        lines(data / 'train-requests.jsonl', selected['train'])
        lines(data / 'val.jsonl', selected['validation'])
        lines(data / 'requests.jsonl', selected['train'] + selected['validation'])
        if pool == 't-repro':
            shutil.copyfile(source / 'train.jsonl', data / 'train.jsonl')
            shutil.copyfile(source / 'validation.jsonl', data / 'validation-rows.jsonl')
        else:
            outputs = defaultdict(list)
            for row, ids in pool_rows:
                assigned = {sides[rid] for rid in ids}
                if len(assigned) != 1:raise ValueError('ambiguous training-row split')
                outputs[next(iter(assigned))].append(row)
            lines(data / 'train.jsonl', outputs['train'])
            lines(data / 'validation-rows.jsonl', outputs['validation'])
        dump(data / 'split-membership.json', manifest)
        files = ('train.jsonl', 'validation-rows.jsonl', 'train-requests.jsonl', 'val.jsonl', 'requests.jsonl', 'split-membership.json')
        receipt = {'pool': pool, 'seed': 7311 if pool == 't-new' else None, 'validation_group_fraction': .1 if pool == 't-new' else None,
                   'source_sha256s': source_hashes, 'sha256s': {n: sha256(data / n) for n in files},
                   'counts': {s: len(v) for s, v in selected.items()},
                   'row_counts': {'train': len(rows(data / 'train.jsonl')), 'validation': len(rows(data / 'validation-rows.jsonl'))},
                   'strata': {s: dict(Counter(r['group'] for r in v)) for s, v in selected.items()},
                   'group_counts': dict(Counter({s: len({r['group_id'] for r in manifest if r['split'] == s}) for s in selected})),
                   'group_method': 'family + template + normalized exact + char5 Jaccard >=0.8 single linkage' if pool == 't-new' else 'original A8 split unchanged',
                   'historical_test_requests_used': 0, 'source_non_test_requests': len(pool_requests),
                   'source_label': 'A8 arm-1 training requests only' if pool == 't-new' else 'original A8 train/validation'}
        dump(data / 'split-receipt.json', receipt)
        verify(pool)
    # Same seven-corpus custody interface as desk. The todo development coverage
    # is the full public train/validation request universe, not historical test.
    lines('data/todo/dev-corpus.jsonl', requests)
    shutil.copyfile(source / 'train.jsonl', 'data/todo/a8-train.jsonl')
    shutil.copyfile('data/custody/a8-v4-validation.jsonl', 'data/todo/a8-val.jsonl')
    print('todo splits frozen; historical test partition excluded')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify', choices=('t-new', 't-repro'))
    a = ap.parse_args(argv)
    verify(a.verify) if a.verify else build()


if __name__ == '__main__':main()
