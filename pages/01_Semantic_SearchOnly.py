import os
import streamlit as st
import openai
from elasticsearch import Elasticsearch

# This code is part of an Elastic Blog showing how to combine
# Elasticsearch's search relevancy power with 
# OpenAI's GPT's Question Answering power
# https://www.elastic.co/blog/chatgpt-elasticsearch-openai-meets-private-data

# Code is presented for demo purposes but should not be used in production
# You may encounter exceptions which are not handled in the code

# Required Environment Variables
cloud_id = os.environ['cloud_id']
cloud_user = os.environ['cloud_user']
cloud_pass = os.environ['cloud_pass']
openai.api_key = os.environ['api_key']
openai.api_base = os.environ['api_base']
openai.api_type = os.environ['api_type']
openai.api_version = os.environ['api_version']
deployment_name=os.environ['deployment_name'] #This will correspond to the custom name you chose for your deployment when you deployed a model. 

# Connect to Elastic Cloud cluster
def es_connect(cid, user, passwd):
    es = Elasticsearch(cloud_id=cid, http_auth=(user, passwd))
    return es

# Search ElasticSearch index and return body and URL of the result
def search(query_text):
    cid = cloud_id
    cp = cloud_pass
    cu = cloud_user
    es = es_connect(cid, cu, cp)

    # Elasticsearch query (BM25) and kNN configuration for hybrid search
    query = {
        "bool": {
            "should": [{
                "match": {
                    "main_content": {
                        "query": query_text,
                        "boost": 1
                    }
                }
            }],
            "filter": [{
                "exists": {
                    "field": "ml.inference.main_content_vector.predicted_value"
                }
            }]
        }
    }

    knn = {
        "field": "ml.inference.main_content_vector.predicted_value",
        "k": 1,
        "num_candidates": 20,
        "query_vector_builder": {
            "text_embedding": {
                "model_id": "sentence-transformers__all-minilm-l6-v2",
                "model_text": query_text
            }
        },
        "boost": 30
    }

    fields = ["title", "main_content", "url"]
    index = 'search-demolab'
    resp = es.search(index=index,
                     query=query,
                     knn=knn,
                     fields=fields,
                     size=3,
                     source=False)
    
    body = []
    url = []

    for b in range(0,3):
        body.append(resp['hits']['hits'][b]['fields']['main_content'][0])
        url.append(resp['hits']['hits'][b]['fields']['url'][0])
    return body, url

st.title("Semantic Search only")

# Main chat form
with st.form("chat_form"):
    query = st.text_input("You: ")
    submit_button = st.form_submit_button("Send")

# Generate and display response on form submission
if submit_button:
    body, url = search(query)
    st.write(f"Here is the top 3 of matching result: ")
    for res in url:
        st.write(f"{res}\n\n")