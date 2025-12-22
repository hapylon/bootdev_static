import markdown_to_html
from markdown_to_html import markdown_to_html
from test_markdown import test_text


def main():
    html_text = markdown_to_html(test_text).to_html
    print(html_text)

if __name__ == "__main__":
    main()
