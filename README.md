# medical_rag_evidence

## Install dependencies
```
pip install -r requirements.txt
```
Please place all pickle files into the `./pickle` folder. Those files will be used to build index and saved in `./storage` later.


## Documents
Discription of `pubmed_abstract_sample.pkl`:
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
Run `python query.py --similarity_top_k=3 --question="How can diabetes affect my eyesight?"` to retrieve answers with the top 3 selected references.

## Answer

```
query_answer: Diabetes can impact eyesight through various mechanisms. One significant complication is diabetic retinopathy, which arises from damage to the retina's blood vessels due to elevated blood sugar levels. If left untreated, this condition can result in vision loss. Moreover, diabetes can induce alterations in the corneal endothelium, leading to changes in cell size and shape. Additionally, individuals with diabetes may develop cataracts at an earlier age compared to those without the condition. Regular eye examinations are crucial for individuals with diabetes to monitor and address any potential eye-related complications.

References:
1. Dhillon N, et al. Natural history of retinopathy in children and young people with type 1 diabetes. Eye (Lond). 2016;30(7):987-991.
2. Kato S, et al. Anterior capsular contraction after cataract surgery in eyes of diabetic patients. Br J Ophthalmol. 2001;85(1):21-24.
3. Ohguro N, et al. Topical aldose reductase inhibitor for correcting corneal endothelial changes in diabetic patients. Br J Ophthalmol. 1995;79(12):1074-1077.
```
