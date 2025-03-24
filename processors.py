# processors.py
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
import io
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class ArticleProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def load_article(self, url):
        """Load and process an article from a URL."""
        try:
            # Check if it's a PDF
            if url.lower().endswith('.pdf'):
                return self._load_pdf(url)

            # Regular web page
            loader = WebBaseLoader(url)
            documents = loader.load()

            # Check content size and handle large documents
            total_content_length = sum(len(doc.page_content) for doc in documents)

            # If content is too large (over 100,000 characters), summarize it
            if total_content_length > 100000:
                return self._handle_large_document(documents)

            return documents

        except Exception as e:
            print(f"  Warning during article loading: {e}")
            # Return a minimal document so processing can continue
            return [Document(page_content=f"Error loading content from {url}: {str(e)}", metadata={"source": url})]

    def _load_pdf(self, url):
        """Handle PDF documents with special processing to avoid token limits."""
        try:
            # For PDF files, we download first
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Try to use PyPDF or a similar library if available
            if PDF_AVAILABLE:
                pdf_file = io.BytesIO(response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Extract text from only the first few pages (to stay within token limits)
                text = ""
                max_pages = min(5, len(pdf_reader.pages))

                for i in range(max_pages):
                    page = pdf_reader.pages[i]
                    text += page.extract_text() + "\n\n"

                # Add a note that this is a truncated version
                if max_pages < len(pdf_reader.pages):
                    text += f"\n[Note: This is a truncated version of the document. Only the first {max_pages} of {len(pdf_reader.pages)} pages were processed due to token limitations.]"

                return [Document(page_content=text, metadata={"source": url})]
            else:
                # If PyPDF is not available, return a note
                return [Document(
                    page_content=f"This is a PDF document from {url}. PDF processing requires the PyPDF2 library. Please install it with: pip install PyPDF2",
                    metadata={"source": url}
                )]

        except Exception as e:
            print(f"  Error processing PDF: {e}")
            return [Document(page_content=f"Error loading PDF from {url}: {str(e)}", metadata={"source": url})]

    def _handle_large_document(self, documents):
        """Handle large documents by extracting key information to stay within token limits."""
        combined_text = "\n\n".join([doc.page_content for doc in documents])
        
        # Ensure the document is truncated to 50,000 characters
        if len(combined_text) > 50000:
            # Take first 25k and last 25k characters
            intro = combined_text[:25000]
            outro = combined_text[-25000:]
            truncated_text = intro + "\n\n[...Document truncated due to length...]\n\n" + outro
            
            # Double-check the length after adding the truncation message
            if len(truncated_text) > 50000:
                # If still too long, adjust the intro and outro lengths
                message_length = len("\n\n[...Document truncated due to length...]\n\n")
                available_length = 50000 - message_length
                intro = combined_text[:available_length // 2]
                outro = combined_text[-(available_length // 2):]
                truncated_text = intro + "\n\n[...Document truncated due to length...]\n\n" + outro
        else:
            truncated_text = combined_text

        return [Document(
            page_content=truncated_text,
            metadata={"source": documents[0].metadata.get("source", "unknown")}
        )]

    def extract_key_information(self, documents):
        """Extract key information about AI use cases from documents."""
        chunks = self.text_splitter.split_documents(documents)
        return chunks