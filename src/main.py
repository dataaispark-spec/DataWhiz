import streamlit as st
from src.ui import render_chat_ui

st.set_page_config(page_title="MSME Analytics", layout="centered")
render_chat_ui()
