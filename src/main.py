import markdown_to_html
import os
from pathlib import Path
import re
import shutil

from markdown_to_html import markdown_to_html
from test_markdown import test_text


def main():
    path_to_clear = "/mnt/c/Users/JohnC/github/bootdotdev/static/bootdev_static/public"
    clear_public(path_to_clear)

    source_dir = "/mnt/c/Users/JohnC/github/bootdotdev/static/bootdev_static/static/"
    dest_dir = "/mnt/c/Users/JohnC/github/bootdotdev/static/bootdev_static/public/"
    try:
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        print(f'Directory {source_dir} successfully copied to {dest_dir}')
    except FileExistsError:
        print(f"Error: Destination directory {dest_dir} already exists!")
    except OSError as e:
        print(f"ErrorL {e}")

    generate_page("content/index.md", "template.html", "public/index.html")
    
def clear_public(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason %s' % (file_path, e))
    
def extract_title(markdown):
    lines = markdown.split("\n\n")
    title = ""
    found = False
    for line in lines:
        if found == True:
            break
        elif re.match(r"^#{1}\s", line):
            title = line[2:]
    if title == "":
        raise Exception("failed to extract_title!") 
    else:
        return title.strip()
    
def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # md_file = find_ext_files(from_path, "md")
    
    with open(from_path, 'r') as file:
        src_md = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    html_content = markdown_to_html(src_md).to_html()
    title = extract_title(src_md)

    # Fill template
    page_html = template.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", html_content)

    # Ensure parent directory exists
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        print("DEBUG: writing HTML:\n", page_html[:500])
        f.write(page_html)

        
    # Write directly to dest_path (e.g. "public/index.html")
    with open(dest_path, "w") as f:
        f.write(page_html)

    print(f"Wrote page to {dest_path}")
    # template = os.read(find_ext_files(template_path, "html", "template"))
    # template = template_path
    
    # HTML_string = markdown_to_html(src_md).to_html()
    # title = extract_title(src_md)
    # template.replace("{{ Title }}", title)
    # template.replace("{{ Content }}", HTML_string)

    # try:
    #     path = Path(dest_path)
    #     os.makedirs(path, exist_ok=True)
    # except OSError as e:
    #     print(f"Error creating directory {dest_path}: {e}")
    # path = Path(dest_path)
    # new_page = os.path.join(path, f"{title}.html")
    # try:
    #     with open(new_page, 'w') as f:
    #         f.write(HTML_string)
    #     print(f"[title].html written to {dest_path}")
    # except IOError as e:
    #     print(f"Error writing to file {new_page}: {e}")



def find_ext_files(search_path, ext, name="*"):
    p = Path(search_path)
    md_files = list(p.glob(f'{name}.{ext}'))
    if len(md_files) < 1:
        raise Exception("NO MD FILES FOUND!")
    if len(md_files) > 1:
        print("MULTIPLE MD FILES FOUND")
    return md_files[0]

if __name__ == "__main__":
    main()
