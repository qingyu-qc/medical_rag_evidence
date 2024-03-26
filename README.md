# medical_rag_evidence

## Install dependencies
```
pip install -r requirements.txt
```

Put all documents in the folder `pickle` or `pdf` depending on whether they are pickle files or pdf files.

## Build index
Run `build_index.py` to build index and save it in storage folder.

## Query
Run `query.py` to query answer with top 10 selected references.
