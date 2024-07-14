import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_text_splitters import CharacterTextSplitter
import sqlite3
from langchain.vectorstores.faiss import FAISS
from langchain_community.chat_models import ChatOllama
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
import gradio as gr

# Load the CSV file
df = pd.read_csv('web_scraping/mayo_clinic_wellness_tips.csv')

df['text'] = "For " + df['disease'] + 'consider ' + df['tip']
texts = df['text'].tolist()

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

embeddings = hf.embed_documents(texts)

df = pd.DataFrame(embeddings, columns=[f"dim_{i}" for i in range(len(embeddings[0]))])
df['text'] = texts

# Create a SQLite database
conn = sqlite3.connect('embeddings.db')
df.to_sql('embeddings', conn, if_exists='replace', index=False)

# Close the connection
conn.close()



documents = texts
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents(documents)
db = FAISS.from_documents(docs,hf)
# Step 2: Create a FAISS Vector Store
vector_store = FAISS.from_texts(texts, hf)

llm = ChatOllama(model="mistral", callbacks=[StreamingStdOutCallbackHandler()])


# Create a RetrievalQA Chain
retriever = VectorStoreRetriever(vectorstore=vector_store)

# Define the system prompt
system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentences maximum and keep the answer concise. "
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

# Function to handle query
def answer_query(query):
    result = retrieval_chain.invoke({"input": query})
    return result["answer"]

# Create the Gradio interface
iface = gr.Interface(
    fn=answer_query,
    inputs="text",
    outputs="text",
    title="Health Information RAG",
    description="Ask questions about health and get concise answers based on the context."
)

# Launch the Gradio interface
iface.launch()
