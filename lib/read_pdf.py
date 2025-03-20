from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

def read_pdf(file_path: Path) -> str:
    pdf_loader = PyPDFLoader(file_path)
    pages = pdf_loader.load_and_split()
    pdf_raw_text = " ".join(list(map(lambda page: page.page_content, pages)))
    
    return pdf_raw_text