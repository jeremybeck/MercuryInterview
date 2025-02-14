from langchain_openai import ChatOpenAI
from typing import List
import streamlit as st
import os
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings



base_llm = ChatOpenAI(openai_api_key=st.secrets['hg_key'], model='gpt-4o-mini', temperature=0.5)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")