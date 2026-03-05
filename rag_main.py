import doctest
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import sqlite3
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.chat_models import ChatOllama
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import gradio as gr
    
df = pd.read_csv('web_scraping/mayo_clinic_wellness_tips.csv')

df['text'] = "For " + df['disease'] + 'consider ' + df['tip']
texts = df['text'].tolist()
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(model_name=model_name)

text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000)
docs = text_splitter.create_documents(texts)

embeddings = hf.embed_documents([doc.page_content for doc in docs])

df = pd.DataFrame(embeddings, columns=[f"dim_{i}" for i in range(len(embeddings[0]))])
df['text'] = texts
conn = sqlite3.connect('embeddings.db')
conn.close()

llm = ChatOllama(model="mistral", temperature=0.4)
system_prompt = """First only consider if the disease name is in the tips, do not include if it is just a symptom or complication is in the list. Answer the question from the documents given.
If the disease is not in the documents, say you do not know the tip for that disease.
If the question is not related to the documents, say you do not know.
Say you do not know if the answer cannot be found in the documents.
Keep it brief to 2 or 3 sentences.
"""

vector = FAISS.from_documents(docs, hf)
retriever = VectorStoreRetriever(vectorstore=vector)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input} \n\nContext: {context}")
])
question_answer_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

def answer_query(query):
    result = retrieval_chain.invoke({"input": query})
    return result["answer"]

# Create the Gradio interface
iface = gr.Interface(
    fn=answer_query,
    inputs="text",
    outputs="text",
    title="Health Information RAG",
    description="Ask questions about health tips and answers based on the context."
)

iface.launch(share=True)

def test_dummy():
    pass
test_dummy()