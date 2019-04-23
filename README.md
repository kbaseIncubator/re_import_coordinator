# Relation engine import coordinator

```sh
pipenv install
pipenv run python src/generate_db.py
MAX_COUNT=100 pipenv run python src/import_workspaces.py
```

`MAX_COUNT` is the max number of pending workspaces you want to try to import. If you dont set it, then it will go through all workspaces.
