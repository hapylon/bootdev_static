from src.markdown_to_html import markdown_to_html

from pathlib import Path

md = Path("content/index.md").read_text()
root = markdown_to_html(md)
print(root.to_html())