import streamlit as st
import pandas as pd
from src.core.llm import LLMHandler
from src.core.rag import RAGHandler

def render_chat_ui():
    st.set_page_config(page_title="MSME Analytics", page_icon="📊", layout="wide")
    st.title("📊 MSME Analytics MVP")
    st.markdown("Turn your Google Drive CSVs/Excel files into insights with natural language Q&A")

    # Initialize session state
    if "rag" not in st.session_state:
        st.session_state.rag = RAGHandler()
    if "llm" not in st.session_state:
        st.session_state.llm = None  # Initialize later
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False

    # Sidebar for data upload
    with st.sidebar:
        st.header("📁 Data Upload")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload CSV or Excel file (<100MB)", 
                                       type=['csv', 'xlsx', 'xls'],
                                       help="Upload from Google Drive or local file")
        
        # Google Drive link
        drive_link = st.text_input("Or paste Google Drive sharing link", 
                                 placeholder="https://drive.google.com/file/...")

        if st.button("Load Data", type="primary"):
            from src.data.connector import DataConnector
            connector = DataConnector()

            if uploaded_file:
                file_details = {"filename": uploaded_file.name, "filesize": uploaded_file.size}
                st.write(file_details)

                # Save uploaded file temporarily
                file_path = f"temp_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                try:
                    result = st.session_state.rag.load_csv(file_path)
                    st.success(result)
                    st.session_state.data_loaded = True

                    # Initialize LLM if needed
                    if st.session_state.llm is None:
                        with st.spinner("Loading AI model (first time may take a while)..."):
                            st.session_state.llm = LLMHandler()

                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
                finally:
                    # Clean up temp file
                    if os.path.exists(file_path):
                        os.remove(file_path)

            elif drive_link:
                try:
                    with st.spinner("Downloading from Google Drive..."):
                        df, message = connector.load_csv_from_drive(drive_link)

                    if message == "Successfully loaded from Google Drive":
                        result = st.session_state.rag.load_csv(df=df)
                        st.success(f"From Google Drive: {result}")
                        st.session_state.data_loaded = True

                        # Initialize LLM if needed
                        if st.session_state.llm is None:
                            with st.spinner("Loading AI model..."):
                                st.session_state.llm = LLMHandler()

                        st.rerun()
                    else:
                        st.error(message)

                except Exception as e:
                    st.error(f"Error loading from Drive: {str(e)}")
            else:
                st.warning("Please upload a file or provide a Drive link")

        if st.session_state.data_loaded:
            st.subheader("Data Preview")
            preview = st.session_state.rag.get_preview()
            st.code(preview[:1000], language='text')  # Show first 1000 chars

    # Main chat interface
    if not st.session_state.data_loaded:
        st.info("👋 Upload some data first to start chatting with your MSME analytics!")
        return

    st.header("💬 Ask Questions About Your Data")

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask anything about your data... (e.g., 'What are the sales trends?', 'Show me top performers')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get context from RAG
                    context = st.session_state.rag.query_data(prompt)
                    
                    # Generate response with LLM
                    response = st.session_state.llm.generate_response(prompt, context)
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Voice input placeholder (would need JavaScript)
    st.markdown("---")
    st.markdown("🎤 Voice input and Hindi language support coming in future updates!")
