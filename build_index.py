##################################### Import libraries #####################################
import os
import pickle
from llama_index.core import Document, StorageContext, load_index_from_storage, SimpleDirectoryReader, VectorStoreIndex
import openai


##################################### Set up path and key #####################################
os.environ["OPENAI_API_KEY"] = "Your OpenAI Key"
openai.api_key = os.environ["OPENAI_API_KEY"]

path_pdf_files = './pdf'  # Path to the folder of pdf files
path_pkl_files = './pickle'  # Path to the folder of pickle files


##################################### Pickle files meta info #####################################

"""
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
  
"""

##################################### Functions #####################################

def load_and_filter_abstracts(path_to_pickle, special_year_condition=False):
    """
    Load journals from a pickle file and filter abstracts based on the presence of text and publication year.

    :param path_to_pickle: Path to the pickle file.
    :param special_year_condition: Flag to apply a special condition for year formatting. Default is False.
    :return: List of filtered abstracts.
    """
    journals = pickle.load(open(path_to_pickle, 'rb'))
    filtered_abstracts = []

    for journal in journals.values():
        year = journal['year']
        abstract_text = journal['abstract_text']
        if abstract_text:  # Check if abstract text is not empty
            if special_year_condition and len(year) > 4:
                # Special condition for year formatting
                year = year.split(' ')[0] if len(year.split(' ')[0]) == 4 else 0
            try:
                year = int(year)
                if year > 1990:
                    filtered_abstracts.append(journal)
            except ValueError:
                # Handle case where year cannot be converted to int
                continue
    return filtered_abstracts

def load_and_filter_eye_wiki(eye_wiki_path):
    """
    Load EyeWiki data from a pickle file and filter it based on specific criteria.

    Parameters:
    - path_pkl_files: The path to the directory containing the EyeWiki pickle file.

    Returns:
    - A dictionary with processed EyeWiki pages, where each page is associated with its text and groups.
    """

    # Load EyeWiki Data
    with open(eye_wiki_path, 'rb') as file:
        eye_wiki = pickle.load(file)

    processed_eye_wiki = {}
    for main_category, pages in eye_wiki.items():
        for page_title, content in pages.items():
            # Filter out empty strings and strings starting with "↑"
            filtered_content = " ".join([text for text in content if text and not text.startswith("↑")])

            if page_title not in processed_eye_wiki:
                processed_eye_wiki[page_title] = {'text': filtered_content, 'groups': [main_category]}
            else:
                processed_eye_wiki[page_title]['groups'].append(main_category)

    return processed_eye_wiki

def create_document(source, document_type, documents_list):
    """
    Create documents from a source and append them to the documents list.

    Parameters:
    - source: The data source to process (e.g., kept_abstracts or processed_eye_wiki).
    - document_type: A string indicating the type of document ('abstract' or 'eyewiki').
    - documents_list: The list to which the created documents will be appended.
    """
    for item in source:
        if document_type == 'abstract':
            doc = Document(
                text=item['abstract_text'],
                extra_info={
                    'title': item['title'],
                    'year': item['year'],
                    'doi': item['doi'],
                    'journal': item['journal']
                }
            )
        elif document_type == 'eyewiki':
            doc = Document(
                text=source[item]['text'],
                extra_info={
                    'page': ', '.join(source[item]['groups']),
                    'doc_id': item
                }
            )
        documents_list.append(doc)


##################################### Load documents #####################################

# Load pdf files
documents = SimpleDirectoryReader('./pdf').load_data()

# Load pickle files
kept_abstracts = []
kept_abstracts += load_and_filter_abstracts(path_pkl_files + '/journals_all_time.pkl')
kept_abstracts += load_and_filter_abstracts(path_pkl_files + '/retina_glaucoma_cataract.pkl')
kept_abstracts += load_and_filter_abstracts(path_pkl_files + '/arvo_ap_survey.pkl', special_year_condition=True)

processed_eye_wiki = load_and_filter_eye_wiki(path_pkl_files + '/eye_wiki_text_lists.pkl')

create_document(kept_abstracts, 'abstract', documents)
create_document(processed_eye_wiki, 'eyewiki', documents)

##################################### Build index #####################################

PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
