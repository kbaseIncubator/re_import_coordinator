# Relation engine import coordinator

```sh
$ pipenv install
$ MAX_COUNT=100 pipenv run src/import_workspaces.py
```

`MAX_COUNT` is the max number of pending workspaces you want to try to import. If you dont set it, then it will go through all workspaces.
