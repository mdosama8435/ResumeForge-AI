import re

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        """Normalize whitespace, remove duplicates, normalize bullets."""
        if not text:
            return ""
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove strange unicode characters, preserve standard punctuation and ASCII
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Normalize bullets (e.g. •, -, *)
        text = re.sub(r'^[\s\t]*[•\-\*o]\s+', '- ', text, flags=re.MULTILINE)
        
        # Remove duplicate blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Normalize whitespace (but keep newlines)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Trim spaces
        return text.strip()
