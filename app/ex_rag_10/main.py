from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS


from dotenv import load_dotenv

load_dotenv()


#Step 1: Convert pdf into docs 
loader = PyPDFLoader("policy.pdf")
docs= loader.load()

#Step2 Split into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = text_splitter.split_documents(docs)

#Step 3: Create Embeddings
embeddings = OpenAIEmbeddings()

#Step 4: Store in VectorDB 
vectorstore = FAISS.from_documents(chunks, embeddings)

#Step5 : Create a retriever from the vectorstore
retriever = vectorstore.as_retriever()

#Step 6: Create a prompt template for the LLM
prompt_template = ChatPromptTemplate.from_template(
    """Answer the question based on  only the context below:
    {context}
    Question: {question}
    """)

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

#Step 8 :RAG Pipeline
while True:
    query = input("Ask something and type 'exit' to quit: ")
    if query.lower() == "exit":
        break
    retrieved_docs = retriever.invoke(query)   
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    prompt = prompt_template.format(context=context, question=query)
    response = llm.invoke(prompt)
    print("Answer: ", response.content)
    
