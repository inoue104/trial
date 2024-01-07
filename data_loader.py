from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch

loader = CSVLoader(
    file_path="./emails.csv", 
    encoding="utf-8",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ["From", "To", "Date", "Subject", "Message-Id", "In-Reply-To", "References", "Body"]
    },
)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200, add_start_index=True)
splits = text_splitter.split_documents(data)

ES_USER = "elastic"
ES_PASSWORD = "RfTC8PcVbsCBad0+nlYz"
ES_CA_CERTS_PATH = "./http_ca.crt"

embeddings = OpenAIEmbeddings()
vector_store = ElasticVectorSearch(
    elasticsearch_url = "https://elastic:RfTC8PcVbsCBad0+nlYz@localhost:9200", 
    ssl_verify = {
    #        "verify_certs": False,
            "basic_auth": (ES_USER, ES_PASSWORD),
            "ca_certs": ES_CA_CERTS_PATH,
        },
    index_name = "es_mails",
    embedding = embeddings
)

def create_index(vector_store: ElasticVectorSearch):
    docs = splits
    vector_store.add_documents(
        docs,
        bulk_kwargs = {
            "chunk_size": 500,
            "max_chunk_bytes": 50000000,
        }
    )

if __name__ == "__main__":
    create_index(vector_store)



