import textract

def extract_text_from_resume(file_path: str) -> str:
    try:
        text = textract.process(file_path).decode("utf-8")
        return text
    except Exception as e:
        print(f"[ERROR] Failed to extract text: {e}")
        return ""
