##################################### Import libraries #####################################
import os
from llama_index.core import Document, StorageContext, load_index_from_storage, SimpleDirectoryReader, VectorStoreIndex
import openai

##################################### Set up path, key and var #####################################

os.environ["OPENAI_API_KEY"] = "Your OpenAI Key"
openai.api_key = os.environ["OPENAI_API_KEY"]

PERSIST_DIR = "./storage"
similarity_top_k = 10  # Number of selected references


##################################### functions #####################################

def query_llama(prompt, question):
    response = full_query_engine.query(prompt + question)
    return response


##################################### Load index #####################################

# load the existing index
storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
index = load_index_from_storage(storage_context)

##################################### Query #####################################

# load query
full_query_engine = index.as_query_engine(similarity_top_k=similarity_top_k)

# query an example question
question = 'your eye related question'
query_answer = query_llama(
    'Answer this paitients question and provide references at the end of your responses. The references should follow the AMA format: \n',
    question)

print("query_answer:", query_answer)
