from selectolax.lexbor import LexborHTMLParser

def html2text(html_content):
        if not html_content: return ""
        try:
            parser = LexborHTMLParser(html_content)
            return parser.text(separator=' ', strip=True)
        except Exception: return str(html_content)