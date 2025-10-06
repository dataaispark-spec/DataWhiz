# RAG module for MSME data analysis
import pandas as pd
try:
    from langchain.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

class RAGHandler:
    def __init__(self):
        if ML_AVAILABLE:
            # Initialize embeddings as specified
            self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            # Text splitter for chunking data
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
        else:
            self.embedding_model = None
            self.text_splitter = None

        self.vectorstore = None
        self.df = None

    def load_csv(self, file_path=None, df=None):
        """Load CSV/Excel data and create vector store (if ML available)"""
        if df is not None:
            self.df = df
        elif file_path:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")

        # Validate data
        validation_errors = self.validate_data(self.df)
        if validation_errors:
            return f"Data validation errors: {', '.join(validation_errors)}"

        if ML_AVAILABLE:
            # Convert dataframe to documents
            documents = self._dataframe_to_documents(self.df)
            self.vectorstore = FAISS.from_documents(documents, self.embedding_model)

            return f"Successfully loaded {len(documents)} data chunks from {len(self.df)} rows."
        else:
            return f"Successfully loaded {len(self.df)} rows. RAG features disabled (ML libraries not available)."

    def _dataframe_to_documents(self, df):
        """Convert dataframe to LangChain documents"""
        documents = []
        
        # Create summary document with general stats
        summary_text = f"""
        Dataset Overview:
        - Total rows: {len(df)}
        - Columns: {', '.join(df.columns.tolist())}
        - Data types: {[df[col].dtype for col in df.columns]}
        
        Column descriptions:
        {df.describe(include='all').to_string()}
        """
        documents.append(Document(page_content=summary_text, metadata={"type": "summary"}))
        
        # Create documents for each row/group
        for idx, row in df.iterrows():
            row_text = f"Row {idx}: " + ", ".join([f"{col}: {row[col]}" for col in df.columns])
            documents.append(Document(page_content=row_text, metadata={"row_index": idx, "type": "data"}))
        
        return documents

    def validate_data(self, df):
        """Validate uploaded data"""
        errors = []
        if df.empty:
            errors.append("File is empty")
        if len(df.columns) == 0:
            errors.append("No columns found")
        # Add more validation as needed
        return errors

    def query_data(self, query, k=5):
        """Query the data using RAG"""
        if not self.vectorstore:
            return "No data loaded yet. Please upload a CSV or Excel file first."
        
        docs = self.vectorstore.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    def get_preview(self):
        """Get data preview"""
        if self.df is not None:
            return self.df.head(10).to_string()
        return "No data loaded."
