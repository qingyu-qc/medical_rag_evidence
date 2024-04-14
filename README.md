# medical_rag_evidence

## Install dependencies
```
pip install -r requirements.txt
```
Please place all pickle files into the `./pickle` folder, and all PDF files into the `./pdf` folder, accordingly. Those files will be used to build index and saved in `./storage` later.


## Documents
Meta data of `journals_all_time.pkl`, `retina_glaucoma_cataract.pkl` and `arvo_ap_survey.pkl`:
```
{
  "ID": {
    "title": "String - The title of the document or article",
    "abstract_text": "String - A brief summary of the document, can be empty",
    "journal": "String - The name of the journal where the document was published",
    "mesh_terms": [
      "String - Medical Subject Headings (MeSH) terms related to the document"
    ],
    "doi": "String - The Digital Object Identifier for the document",
    "year": "String - The year the document was published",
    "authors": [
      "String - Names of authors"
    ]
  }
}
```

## Build index
Run `build_index.py` to build index from documents and save it in `./storage`.

## Query
Run `query.py --similarity_top_k=10 --question="What causes eye strain?"` to retrieve answers with the top 10 selected references.
