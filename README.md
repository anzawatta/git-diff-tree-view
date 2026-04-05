# git-diff-tree-view

A pipe filter that renders `git diff --numstat` output as a tree. Python stdlib only, zero dependencies.

See [DESIGN.md](./DESIGN.md) for design principles.

## Usage

```bash
git diff --numstat HEAD~1 | python3 git-diff-tree-view.py
```

```
├── docs
│   └── adr
│       └── 002-backlink-index.md | 22 ++++++++++++++++++++++
└── scripts
    ├── embed.py | 69 ++++++++++++++++++++++++
    └── train.py | 28 ++++++++--
```

Diff against a branch:

```bash
git diff --numstat $(git merge-base HEAD main)..HEAD | python3 git-diff-tree-view.py
```

Git alias:

```ini
[alias]
    tdiff = "!f(){ git diff --numstat \"$@\" | python3 ~/path/to/git-diff-tree-view.py; }; f"
```

## License

MIT
