# app.py

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

from rag import RAGSystem
from nlp import NLPClassifier
from bible import get_bible_verse

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create Page Look
st.set_page_config(page_title="LuxScriptura", layout="wide")
st.title("✝️ LuxScriptura")

# Implement Models Here
rag = RAGSystem("ccc.json")
nlp = NLPClassifier()

user_input = st.text_area("Enter a theological question or statement")

def generate_answer(query, passages):
    context = "\n\n".join([f"(CCC {p['ref']}) {p['text']}" for p in passages])

    prompt = f"""
    You are LuxScriptura, faithful to Catholic teaching.

    User:
    {query}

    Catechism:
    {context}

    Explain clearly, correct errors, include CCC references and 1 Bible verse.
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def score(query, passages):
    context = "\n\n".join([p["text"] for p in passages])

    prompt = f"Score 0-100 theological accuracy:\n\n{query}\n\n{context}"

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


if st.button("Analyze") and user_input:

    topic, error = nlp.classify(user_input)
    passages = rag.retrieve(user_input)

    st.subheader("🧠 NLP")
    st.write(topic, error)

    st.subheader("📖 CCC References")
    for p in passages:
        st.write(f"CCC {p['ref']}")
        st.caption(p["text"][:250])

    st.subheader("✝️ Response")
    st.write(generate_answer(user_input, passages))

    st.subheader("📊 Score")
    st.write(score(user_input, passages))


st.sidebar.header("📖 Bible")
verse = st.sidebar.text_input("Enter verse")

if st.sidebar.button("Get Verse"):
    st.sidebar.write(get_bible_verse(verse))