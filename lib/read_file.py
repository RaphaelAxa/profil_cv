from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader


def read_cv(file_path: str) -> str:
    extension = file_path.split(".")[-1]

    if extension == "pdf":
        file_loader = PyPDFLoader(file_path)
    elif extension == "docx":
        file_loader = Docx2txtLoader(file_path)
    else:
        raise NameError("File Extension not supported. Should be .pdf or .docx only.")

    pages = file_loader.load_and_split()
    raw_text = " ".join(list(map(lambda page: page.page_content, pages)))

    return raw_text
