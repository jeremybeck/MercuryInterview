import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from language_models import embeddings

def extract_pdf_structure(file_path):
    doc = fitz.open(file_path)
    content = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text']
                        font_size = span['size']
                        # Identify headings based on font size or style
                        if font_size > 15:
                            content.append(f"# {text}")  # H1
                        elif font_size > 12:
                            content.append(f"## {text}")  # H2
                        else:
                            content.append(text)
    return "\n".join(content)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=100,
    separators=["\n## ", "\n# ", "\n", "."]
)

try:
    retriever_db = FAISS.load_local('vector_db/policy_info.faiss', embeddings, allow_dangerous_deserialization=True).as_retriever(search_kwargs={"k": 10})
except Exception as e:
    print(f'Failed to load retriever, {e}')
    print('Please run `python ./src/vector_db.py` before proceeding')

if __name__=="__main__":

    onsite_policy = extract_pdf_structure("../data/Mercury Onsite Policy.pdf")
    onsite_policy_chunks = text_splitter.create_documents([onsite_policy])

    default_policy = extract_pdf_structure("../data/Mercury_Expense_General_Policy.pdf")
    default_policy_chunks = text_splitter.create_documents([default_policy])

    faiss_index = FAISS.from_documents(onsite_policy_chunks, embeddings)

    faiss_index.save_local('../vector_db/policy_info.faiss')