import sys
from pathlib import Path

lines = [l.strip() for l in sys.stdin if l.strip()]

files = {}
for line in lines:
    parts = line.split('\t', 2)
    if len(parts) == 3:
        added, deleted, path = parts
        try:
            a, d = int(added), int(deleted)
            bar = '+' * min(a, 20) + '-' * min(d, 20)
            stat = f"{a + d} {bar}"
        except ValueError:
            stat = f"{added}/{deleted}"
        files[Path(path)] = stat

tree = {}
for f in files:
    node = tree
    for part in f.parts[:-1]:
        node = node.setdefault(part, {})
    node[f.name] = files[f]


def render(node, prefix=''):
    items = list(node.items())
    for i, (name, child) in enumerate(items):
        last = i == len(items) - 1
        connector = '└── ' if last else '├── '
        if isinstance(child, str):
            print(f"{prefix}{connector}{name} | {child}")
        else:
            print(f"{prefix}{connector}{name}")
            render(child, prefix + ('    ' if last else '│   '))


render(tree)
