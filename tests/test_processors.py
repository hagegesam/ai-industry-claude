import pytest
import requests_mock
from unittest.mock import patch, MagicMock
import io
from processors import ArticleProcessor, PDF_AVAILABLE
from langchain.schema import Document

@pytest.fixture
def processor():
    return ArticleProcessor()

@pytest.fixture
def mock_pdf_content():
    # Create a simple PDF content for testing
    return b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"

def test_load_pdf_success(processor, requests_mock, mock_pdf_content):
    """Test successful PDF loading with PyPDF2 available."""
    url = "http://example.com/test.pdf"
    requests_mock.get(url, content=mock_pdf_content)
    
    with patch('processors.PDF_AVAILABLE', True), patch('processors.PyPDF2') as mock_pypdf:
        # Mock the PDF reader to return some test content
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test PDF Content"
        mock_pdf_reader = MagicMock()
        mock_pdf_reader.pages = [mock_page] * 3
        mock_pypdf.PdfReader.return_value = mock_pdf_reader
        
        result = processor._load_pdf(url)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)
        assert "Test PDF Content" in result[0].page_content
        assert result[0].metadata["source"] == url

def test_load_pdf_network_error(processor, requests_mock):
    """Test PDF loading when network request fails."""
    url = "http://example.com/test.pdf"
    requests_mock.get(url, status_code=404)
    
    result = processor._load_pdf(url)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Document)
    assert "Error loading PDF" in result[0].page_content
    assert result[0].metadata["source"] == url

def test_load_pdf_missing_pypdf(processor, requests_mock, mock_pdf_content):
    """Test PDF loading when PyPDF2 is not installed."""
    url = "http://example.com/test.pdf"
    requests_mock.get(url, content=mock_pdf_content)
    
    with patch('processors.PDF_AVAILABLE', False):
        result = processor._load_pdf(url)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)
        assert "PDF processing requires the PyPDF2 library" in result[0].page_content
        assert result[0].metadata["source"] == url

def test_load_pdf_large_document(processor, requests_mock, mock_pdf_content):
    """Test PDF loading with a large document (more than 5 pages)."""
    url = "http://example.com/large.pdf"
    requests_mock.get(url, content=mock_pdf_content)
    
    with patch('processors.PDF_AVAILABLE', True), patch('processors.PyPDF2') as mock_pypdf:
        # Mock 10 pages
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test PDF Content"
        mock_pdf_reader = MagicMock()
        mock_pdf_reader.pages = [mock_page] * 10
        mock_pypdf.PdfReader.return_value = mock_pdf_reader
        
        result = processor._load_pdf(url)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)
        assert "Test PDF Content" in result[0].page_content
        assert "truncated version" in result[0].page_content
        assert result[0].metadata["source"] == url

def test_load_article_pdf(processor, requests_mock, mock_pdf_content):
    """Test the main load_article method with a PDF URL."""
    url = "http://example.com/test.pdf"
    requests_mock.get(url, content=mock_pdf_content)
    
    with patch('processors.PDF_AVAILABLE', True), patch('processors.PyPDF2') as mock_pypdf:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test PDF Content"
        mock_pdf_reader = MagicMock()
        mock_pdf_reader.pages = [mock_page] * 3
        mock_pypdf.PdfReader.return_value = mock_pdf_reader
        
        result = processor.load_article(url)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)
        assert "Test PDF Content" in result[0].page_content
        assert result[0].metadata["source"] == url

def test_load_article_webpage(processor, requests_mock):
    """Test loading a regular webpage."""
    url = "http://example.com/article.html"
    html_content = "<html><body><p>Test content</p></body></html>"
    requests_mock.get(url, text=html_content)
    
    with patch('processors.WebBaseLoader') as mock_loader:
        mock_doc = Document(page_content="Test content", metadata={"source": url})
        mock_loader.return_value.load.return_value = [mock_doc]
        
        result = processor.load_article(url)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)
        assert result[0].page_content == "Test content"
        assert result[0].metadata["source"] == url

def test_load_article_large_webpage(processor, requests_mock):
    """Test loading a large webpage that needs truncation."""
    url = "http://example.com/large.html"
    # Create content that will definitely trigger truncation
    long_content = "Test content " * 10000
    html_content = f"<html><body><p>{long_content}</p></body></html>"
    requests_mock.get(url, text=html_content)
    
    with patch('processors.WebBaseLoader') as mock_loader:
        mock_doc = Document(page_content=long_content, metadata={"source": url})
        mock_loader.return_value.load.return_value = [mock_doc]
        
        result = processor.load_article(url)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Document)
        assert "Test content" in result[0].page_content
        assert "Document truncated" in result[0].page_content
        assert len(result[0].page_content) <= 50000
        assert result[0].metadata["source"] == url

def test_handle_large_document(processor):
    """Test the _handle_large_document method."""
    # Create a document with exactly 50,001 characters to test truncation
    base_text = "Test content "
    num_repeats = 50001 // len(base_text) + 1
    long_text = base_text * num_repeats
    docs = [Document(page_content=long_text, metadata={"source": "test"})]
    
    result = processor._handle_large_document(docs)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Document)
    assert len(result[0].page_content) <= 50000  # Should be truncated
    assert "Document truncated" in result[0].page_content
    assert result[0].metadata["source"] == "test"

def test_extract_key_information(processor):
    """Test the extract_key_information method."""
    test_doc = Document(
        page_content="This is a test document with some content that should be split into chunks.",
        metadata={"source": "test"}
    )
    
    result = processor.extract_key_information([test_doc])
    
    assert isinstance(result, list)
    assert all(isinstance(chunk, Document) for chunk in result)
    assert len(result) > 0 