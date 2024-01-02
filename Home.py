import streamlit as st

st.set_page_config(
    page_title="ESRE Lab",
    layout="centered",
    page_icon="👋",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'This App shows you how to use Elasticsearch with LLM'
    }
)

st.image('https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt601c406b0b5af740/620577381692951393fdf8d6/elastic-logo-cluster.svg', width=75)

st.header("Chat with your Elasticsearch data using Large Language Models (LLMs)")