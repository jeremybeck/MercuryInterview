from langchain_openai import ChatOpenAI
import streamlit as st

base_llm = ChatOpenAI(openai_api_key=st.secrets['hg_key'], model='gpt-4o-mini', temperature=0.5)