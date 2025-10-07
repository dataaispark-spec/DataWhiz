import streamlit as st
import pandas as pd
try:
    from src.core.llm import LLMHandler
    from src.core.rag import RAGHandler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    class RAGHandler:
        def __init__(self):
            self.df = None
            self._validate_data = lambda df: []
        def load_csv(self, file_path=None, df=None):
            import pandas as pd
            if df is not None:
                self.df = df
            elif file_path:
                if file_path.endswith('.csv'):
                    self.df = pd.read_csv(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    self.df = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format")
            self.validate_data(self.df)
            return f"Successfully loaded {len(self.df)} rows. RAG features disabled."
        def validate_data(self, df):
            errors = []
            if df.empty:
                errors.append("File is empty")
            if len(df.columns) == 0:
                errors.append("No columns found")
            if errors:
                raise ValueError(f"Data validation errors: {', '.join(errors)}")
        def query_data(self, query):
            return "AI features not available. Install ML dependencies for chat functionality."
        def get_preview(self):
            return self.df.head(10).to_string() if self.df is not None else "No data loaded."

    class LLMHandler:
        def __init__(self, model_choice="phi4"):
            self.model_choice = model_choice
        def generate_response(self, prompt, context=None, language="en"):
            return "AI model not available. Please install ML dependencies for chat functionality."
        def get_model_info(self):
            return {"type": "None", "optimized_for": "Not available", "features": ["None"]}

def render_chat_ui():
    st.set_page_config(page_title="PiRhoAI", page_icon="📊", layout="wide")

    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-card {
        background-color: #d2691e;
        color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #8b4513;
        margin: 10px 0;
    }
    .benefit-box {
        background-color: #cd853f;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #a0522d;
    }
    .journey-step {
        background-color: #deb887;
        color: black;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #bc8f8f;
    }
    table {
        background-color: #8b4513;
        color: white;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #654321;
        padding: 8px;
        color: white;
    }
    th {
        background-color: #654321;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #a0522d;
        color: white;
    }
    .stSuccess {
        background-color: #8b4513 !important;
    }
    .stSuccess > div {
        color: white !important;
    }
    .stInfo {
        background-color: #8b4513 !important;
    }
    .stInfo > div {
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #654321 !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header"><h1>📊 PiRhoAI - Privacy Focused AI Business Analytics Assistant</h1><p>Transform your business data into actionable insights with AI-powered natural language Q&A</p></div>', unsafe_allow_html=True)

    # Initialize session state
    if "rag" not in st.session_state:
        st.session_state.rag = RAGHandler()
    if "llm" not in st.session_state:
        st.session_state.llm = None  # Initialize later
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "model_choice" not in st.session_state:
        st.session_state.model_choice = "phi4"
    if "language" not in st.session_state:
        st.session_state.language = "en"

    # Tabs for navigation
    tab1, tab2 = st.tabs(["🚀 Analytics", "ℹ️ About"])

    with tab2:
        st.header("🎯 Idea Validation: LLM-Based Analytics Solution")

        st.markdown("""
        <div class="feature-card">
        <h4>📋 Product Overview</h4>
        <p>A lightweight, LLM-powered analytics platform that pulls data directly from accessible cloud storage like Google Drive, AWS S3, or Azure Blob Storage, positioning as a cost-effective alternative to heavy infrastructure like Snowflake for SMEs/MSMEs.</p>
        </div>
        """, unsafe_allow_html=True)

        st.header("📊 Technical Feasibility")
        with st.expander("🔍 Click to expand key technical details"):
            st.markdown("""
            **LLM Integration with Cloud Storage:**
            - Small, efficient LLMs (e.g., Phi-4, Phi-3, Gemma) with 1-7B parameters
            - Fine-tuned for analytics tasks like query generation and anomaly detection
            - Runs on modest hardware using vLLM or ONNX Runtime
            - APIs: Google Drive API, AWS SDK, Azure Storage SDKs for real-time syncing

            **Example Workflow:**
            User query → Mount storage → Embed data into FAISS vector DB → LLM generates insights
            """)

        st.header("📈 Market Fit & Product Viability")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="benefit-box">
            <h4>� Value Proposition</h4>
            <p>• Natural language interface democratizes analytics<br>• Cost savings: Avoids expensive enterprise warehouses<br>• Scales to zero when idle for ultra-low costs<br>• Predictive insights without data engineers</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="benefit-box">
            <h4>🎯 Target Market Pain Points</h4>
            <p>• 90% of global businesses are SMEs but lag in analytics<br>• Only 20-30% use advanced tools due to complexity<br>• High costs of expert services<br>• Technical barriers for non-tech users</p>
            </div>
            """, unsafe_allow_html=True)

        st.header("� Feasibility in Developing Markets")
        st.markdown("""
        <div class="journey-step">
        <h4>🌟 Key Opportunities</h4>
        <p>• MSMEs drive 40-60% of GDP in emerging economies (India, Brazil, Indonesia)<br>• Rising digital adoption (1B+ smartphones in India)<br>• Government initiatives like Digital MSME scheme<br>• Affordable access to free-tier storage (Google Drive free for 80%)<br>• Multi-language support for regional dialects</p>
        </div>

        <div class="journey-step">
        <h4>🚀 Growth Projections</h4>
        <p>• MSME analytics market to hit $50B by 2030<br>• AI tools could capture 20% share<br>• 70-90% productivity gains in affected firms<br>• Success examples: Kenyan agrotech improving crop yields by 30%</p>
        </div>
        """, unsafe_allow_html=True)

        st.header("⚖️ Comparison vs Snowflake")
        import pandas as pd
        comparison_df = pd.DataFrame({
            'Aspect': ['Setup Time', 'Cost for 100GB/month', 'User Skill Level', 'Best For'],
            'Snowflake': ['Weeks (ETL, schema design)', '$200-500+ (storage + compute)', 'Data engineers required', 'Enterprise-scale BI'],
            'Your LLM Solution': ['Hours (API connect + prompt tuning)', '$20-100 (storage free-tier + LLM tokens)', 'Business owners (conversational UI)', 'Ad-hoc SME insights (e.g., cash flow predictions)']
        })
        st.table(comparison_df)

        st.header("🔄 Comparison vs Zoho Analytics")
        zoho_df = pd.DataFrame({
            'Aspect': ['Core Features', 'Integrations', 'Ease of Use', 'Pricing (2025)', 'Scalability', 'Target Market'],
            'Your LLM Solution': ['Natural language queries; RAG for retrieval; basic LLM-generated visualizations',
                                'Native to Drive/S3/Blob; extensible via LangChain', 'High (non-tech)',
                                '$10-50/user/month; pay-per-query', '<1TB datasets; serverless to zero',
                                'SMEs/MSMEs in developing markets'],
            'Zoho Analytics': ['Drag-and-drop dashboards; 500+ reports; Zia AI conversational',
                             '500+ connectors; Zoho ecosystem seamless', 'User-friendly SMEs',
                             'Free to $575/month (enterprise)', '50M+ rows; cloud/on-prem',
                             'Global SMEs/mid-market']
        })
        st.table(zoho_df)

        st.header("🧠 Recommended LLMs")
        llm_df = pd.DataFrame({
            'Model': ['Microsoft Phi-4 (Latest)', 'Microsoft Phi-3', 'Microsoft Phi-2', 'IBM Granite 4.0 Tiny'],
            'Parameters': ['3.8B mini-reasoning; 14B full', '3.8B mini; up to 14B variants', '2.7B', '~3B Micro/H-Tiny hybrid'],
            'Key Strengths': ['Complex reasoning/math; multilingual; function-calling for APIs',
                            'Strong in coding/reasoning; 128K context; fine-tune low halluc.', 'Efficient on sparse data; outperforms larger on commonsense',
                            '2-4x efficiency hybrid; long-context; enterprise compliance'],
            'Drawbacks': ['English-primary', 'Less advanced than Phi-4', 'Weaker on math/reasoning', 'Newer ecosystem'],
            'Best For': ['Core analytics; edge deployment', 'NLP tasks', 'Budget prototypes', 'Privacy/compliance focus']
        })
        st.table(llm_df)
        st.success("**Top Recommendation:** Phi-4-mini-reasoning (3.8B) for optimal balance of accuracy and efficiency.")

        st.header("🛣️ Customer Journey")

        st.markdown("""
        <div class="journey-step">
        <h4>Step 1: Discovery & Onboarding</h4>
        <p>• User visits the MSME Analytics platform<br>• Learns about AI-powered data insights<br>• Understands ease of use and benefits<br>• Signs up or starts free trial</p>
        </div>

        <div class="journey-step">
        <h4>Step 2: Data Connection</h4>
        <p>• Upload existing CSV/Excel files from computer<br>• Provide Google Drive sharing link for cloud data<br>• See immediate data preview and validation<br>• Experience seamless integration process</p>
        </div>

        <div class="journey-step">
        <h4>Step 3: Exploration & Interaction</h4>
        <p>• Ask natural language questions in English or Hindi<br>• Receive AI-generated insights and analysis<br>• Follow up with deeper queries<br>• Customize language and model preferences</p>
        </div>

        <div class="journey-step">
        <h4>Step 4: Action & Decision Making</h4>
        <p>• Apply insights to business strategies<br>• Share findings with team members<br>• Monitor performance with regular data updates<br>• Build confidence in data-driven decisions</p>
        </div>

        <div class="journey-step">
        <h4>Step 5: Growth & Expansion</h4>
        <p>• Use advanced features as business grows<br>• Integrate with additional data sources<br>• Leverage analytics for scaling operations<br>• Become data-savvy enterprise with AI assistance</p>
        </div>
        """, unsafe_allow_html=True)

        st.header("📖 How It Works (Customer Perspective)")
        st.markdown("""
        **Simple 3-Step Process:**
        1. **Upload Your Data** - Connect your files in seconds
        2. **Ask Questions** - Type what you want to know
        3. **Get Answers** - Receive clear, actionable insights

        **Example Scenarios:**
        - "What were my top-selling products last month?"
        - "क्या मेरे ग्राहक खरीदारी पैटर्न में कोई बदलाव आया?" (Have there been changes in customer purchase patterns?)
        - "Show me customers who haven't bought in 3 months"
        - "मेरी इन्वेंटरी की स्थिति कैसी है?" (How is my inventory status?)
        - "Which suppliers give best deals?"
        """)

        st.header("🌟 Strengths & Differentiation")
        st.markdown("""
        • **Disruptive Affordability:** Pay-per-query model vs. fixed subscriptions
        • **LLM-First Approach:** Conversational AI over traditional BI tools
        • **Storage-First Integration:** Direct from Drive/S3 without warehouses
        • **Edge Deployment Capabilities:** Works offline and on low-resource hardware
        • **Developing Market Focus:** Multi-language support and regional optimizations
        """)

        st.header("� Survival & Feasibility Assessment")
        st.markdown("""
        **Survival Odds:** 70-80% in 3 years with good product-market fit
        - Feasibility: High (mature open-source stacks; weeks to MVP)
        - Market Demand: Strong (SMEs lack tools; LLMs address barriers)
        - Competition Edge: Lighter than Zoho, cheaper than Snowflake
        - Risks Mitigated: LLM hallucinations via verification; API costs via open models
        """)

        st.header("�🔜 Future Roadmap")
        st.markdown("""
        • Advanced data visualization charts
        • Voice input for hands-free operation
        • Multi-file analysis and cross-data insights
        • Automated report generation
        • Integration with accounting software (QuickBooks, etc.)
        • Predictive analytics and alerts
        • Team collaboration features
        """)

        st.header("📞 Support & Learning")
        st.markdown("""
        **Getting Started Guide:**
        - Watch our 2-minute tutorial video
        - Read quick-start documentation
        - Access sample data files
        - Join community forum for tips

        **Support Channels:**
        - In-app help tooltips
        - Email support for technical issues
        - Video tutorials for advanced features
        - Community-driven knowledge base
        """)

        st.header("🏆 Call to Action")
        st.markdown("""
        Ready to empower MSMEs with AI-driven analytics? Start exploring the platform today!

        **Product Vision:** "ChatGPT for SME spreadsheets" - Making business intelligence accessible to millions of small businesses worldwide.
        """)

    with tab1:
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
                                st.session_state.llm = LLMHandler(st.session_state.model_choice)

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

            st.markdown("---")
            st.header("🚀 Quick Start")

            if st.button("Load Sample Data", type="secondary", help="Load synthetic business data to explore PiRhoAI features"):
                try:
                    import pandas as pd
                    df = pd.read_csv("sample_data.csv")
                    result = st.session_state.rag.load_csv(df=df)
                    st.success(f"Sample data loaded: {result}")
                    st.session_state.data_loaded = True

                    # Initialize LLM if needed
                    if st.session_state.llm is None:
                        with st.spinner("Loading AI model..."):
                            st.session_state.llm = LLMHandler(st.session_state.model_choice)

                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")

            if st.session_state.data_loaded:
                st.subheader("Data Preview")
                preview = st.session_state.rag.get_preview()
                st.code(preview[:1000], language='text')  # Show first 1000 chars

            st.markdown("---")
            st.header("⚙️ Settings")

            # Model selector
            model_choice = st.selectbox(
                "AI Model",
                ["phi4", "phi3", "grok4"],
                index=["phi4", "phi3", "grok4"].index(st.session_state.model_choice),
                help="Phi-4 (latest) for MSME analytics, optimized for accuracy. Grok-4 in future release."
            )

            if model_choice != st.session_state.model_choice:
                st.session_state.model_choice = model_choice
                st.session_state.llm = LLMHandler(model_choice)  # Reinitialize with new model
                st.session_state.messages = []  # Clear chat for new model
                st.success(f"Switched to {model_choice.upper()} model")

            # Language selector
            language = st.selectbox(
                "Language",
                [("en", "English"), ("hi", "Hindi (हिंदी)")],
                index=1 if st.session_state.language == "hi" else 0,
                format_func=lambda x: x[1]
            )[0]

            if language != st.session_state.language:
                st.session_state.language = language
                st.success(f"Language set to {language.upper()}")

            # Model info
            if st.session_state.llm and hasattr(st.session_state.llm, 'get_model_info'):
                st.subheader("Model Info")
                model_info = st.session_state.llm.get_model_info()
                st.write(f"**Type**: {model_info['type']}")
                st.write(f"**Optimized for**: {model_info['optimized_for']}")
                st.write(f"**Features**: {', '.join(model_info['features'])}")

        # Main chat interface
    if not st.session_state.data_loaded:
        st.info("👋 Upload some data first to start chatting with PiRhoAI!")
        return

    st.header("💬 Ask Questions About Your Data")

    # Langfuse feedback collection
    if st.button("Rate This Session ⭐"):
        st.info("Feedback feature placeholder - Langfuse integration ready")

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
                    response = st.session_state.llm.generate_response(prompt, context, st.session_state.language)
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Voice input placeholder (would need JavaScript)
    st.markdown("---")
    st.markdown("🎤 Voice input and Hindi language support coming in future updates!")
