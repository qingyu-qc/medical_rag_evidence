##################################### Import libraries #####################################
import os
import pickle
from llama_index.core import Document, StorageContext, load_index_from_storage, SimpleDirectoryReader, VectorStoreIndex
import openai


##################################### Set up path and key #####################################
os.environ["OPENAI_API_KEY"] = "Your OpenAI Key"
openai.api_key = os.environ["OPENAI_API_KEY"]

path_pkl_files = './pickle'  # Path to the folder of pickle files

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

def create_document(source, documents_list):
    """
    Create documents from a source and append them to the documents list.

    Parameters:
    - source: The data source to process (e.g., kept_abstracts).
    - documents_list: The list to which the created documents will be appended.
    """
    for item in source:
        doc = Document(
            text=item['abstract_text'],
            extra_info={
                'title': item['title'],
                'year': item['year'],
                'doi': item['doi'],
                'journal': item['journal'],
                'authors': item['authors']
            }
        )
        documents_list.append(doc)


##################################### Load documents #####################################

documents = []

# Load pickle files
kept_abstracts = []
kept_abstracts += load_and_filter_abstracts(path_pkl_files + '/pubmed_abstract_sample.pkl')

create_document(kept_abstracts, documents)

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
