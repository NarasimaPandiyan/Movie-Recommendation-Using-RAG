import streamlit as st
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from google.genai.types import EmbedContentConfig
from llama_index.llms.gemini import Gemini

st.set_page_config(page_title="MovieBot AI", page_icon="🍿")
st.title("Movie Recommendation System")

load_dotenv()

@st.cache_resource
def init_index():
    client = MongoClient(os.getenv("MONGODB_URI"))
    db_name = os.getenv("DB_NAME", "movie_recommender")
    col_name = os.getenv("COLLECTION_NAME", "movies")
    
    embed_model = GoogleGenAIEmbedding(
        model_name="models/gemini-embedding-001",
        embedding_config=EmbedContentConfig(output_dimensionality=3072)
    )
    
    llm = Gemini(model="models/gemini-2.5-flash")
    
    Settings.embed_model = embed_model
    Settings.llm = llm

    vector_store = MongoDBAtlasVectorSearch(
        client,
        db_name=db_name,
        collection_name=col_name,
        vector_index_name=os.getenv("VS_INDEX_NAME", "vector_index"),
        fulltext_index_name=os.getenv("FTS_INDEX_NAME", "fts_index"),
        embedding_key="embedding",
        text_key="text",
    )
    
    return VectorStoreIndex.from_vector_store(vector_store)

index = init_index()

with st.sidebar:
    st.header("Search Settings")
    search_mode = st.selectbox("Search Mode", ["hybrid", "default", "text_search"])
    alpha_val = st.slider("Alpha (AI vs Keywords)", 0.0, 1.0, 0.7)
    top_k = st.slider("Number of Movies", 1, 10, 5)
    st.info("Alpha 0.0 = Pure Keywords\nAlpha 1.0 = Pure AI Meaning")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I've indexed your movie library. What are you in the mood for?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask for a recommendation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the cloud..."):
            query_engine = index.as_query_engine(
                similarity_top_k=top_k, 
                vector_store_query_mode=search_mode,
                alpha=alpha_val
            )
            
            response = query_engine.query(prompt)
            st.markdown(response.response)
            
            with st.expander("Movies I found in your database:"):
                for node in response.source_nodes:
                    title = node.metadata.get('title', 'Unknown')
                    rating = node.metadata.get('rating', 'N/A')
                    st.write(f"**{title}** — ⭐ {rating}")
    
    st.session_state.messages.append({"role": "assistant", "content": response.response})