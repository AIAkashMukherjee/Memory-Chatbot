from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import Pinecone as LC_Pinecone
from constant import *
from memory_store import MemoryStore

class ChatBot:
    def __init__(self,open_ai_api=None,):
        self.open_ai=open_ai_api
        self.groq_api = groq_api_key
        self.memory_store=MemoryStore()
        self.llm, self.embeddings = self.initialize_models()
        self.vector_store = self.initialize_vector_store()
        self.conversation_chain = self.build_chain()



    def initialize_models(self):
        if self.open_ai:
            llm=ChatOpenAI(
                model_name=DEFAULT_OPENAI_MODEL,
                temperature=0.9,
                openai_api_key=self.open_ai
            )        

            # embeddings = OpenAIEmbeddings(openai_api_key=self.open_ai)

        else:
            llm = ChatGroq(
            model_name="Llama-3.3-70b-Versatile",  
            temperature=0.9,
            groq_api_key=self.groq_api)
            
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")



        return llm, embeddings    


    
    def initialize_vector_store(self):
        pc = Pinecone(api_key=pinecone_api)
        if PINECONE_INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,            #
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    
        return LC_Pinecone(
        index_name=PINECONE_INDEX_NAME,  
        embedding=self.embeddings,
        text_key="text",
        )

    
    def upload_document(self, file_path):
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            if not documents:
                raise ValueError("No content found in the PDF.")
        except Exception as e:
            return {"error": f"An error occurred while uploading the document: {str(e)}"}

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
        docs = text_splitter.split_documents(documents)
        self.vector_store.add_documents(docs)
        # self.vector_store.persist()
        print(f"Uploaded and indexed {len(docs)} chunks from {file_path}")


    def build_chain(self):
        retriever = self.vector_store.as_retriever()
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory_store.get_memory(),
            # combine_docs_chain_kwargs={"prompt": self.prompt_template},
            chain_type="stuff",
            verbose=True
        )
    
    def chat(self, question):
    # Pass the question and context to the prompt template
        # result = self.conversation_chain({"question": question})

        # print("🔍 Result from conversation chain:", result)

        # if isinstance(result, dict):
        #     if "answer" in result:
        #         return result
        #     else:
        #         return {"answer": "⚠️ No 'answer' key in response."}
        # else:
        #     return {"answer": "⚠️ Unexpected response format."}

        result = self.conversation_chain({"question": question})
    
    # Ensure consistent result format
        if isinstance(result, dict) and "answer" in result:
            return result["answer"]
        else:
            return "⚠️ Unexpected response format or no answer found."