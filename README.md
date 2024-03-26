# medical_rag_evidence

## Install dependencies
```
pip install -r requirements.txt
```
Please place all pickle files into the `pickle` folder, and all PDF files into the `pdf` folder, accordingly. Those files will be used to build index and saved in `storage` later.


## Documents
```
Meta data of pickle files: journals_all_time.pkl, retina_glaucoma_cataract.pkl
and arvo_ap_survey.pkl
    {
    "ID": {
        "title": "String - The title of the document or article",
        "abstract_text": "String - A brief summary of the document, can be empty",
        "journal": "String - The name of the journal where the document was published",
        "mesh_terms": [
            "String - Medical Subject Headings (MeSH) terms related to the document"
        ],
        "doi": "String - The Digital Object Identifier for the document",
        "year": "String - The year the document was published"
    }
}

Meta data of pickle files: eye_wiki

- Top-Level Categories: Dict - Includes various ophthalmology subfields such as Cataract Anterior Segment,
  Cornea External Disease, Glaucoma, etc.

- Subcategories Example: Dict - Contains specific topics like 
  "A Review of Post-Operative Drops used in Cataract Surgery", "Aniridic Fibrosis Syndrome", etc.
  
- Content Type: List - Each topic under subcategories is a list of explanations/references/citations providing detailed
  information, e.g., authors, title, journal, and DOI for further reading.
```



## Build index
Run `build_index.py` to build index and save it in storage folder.

## Query
Run `query.py` to retrieve answers with the top 10 selected references,
