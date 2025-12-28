import markdown_to_html
import os
import sys
from pathlib import Path
import re
import shutil

from markdown_to_html import markdown_to_html
from test_markdown import test_text


def main():
    # If an argument is provided, use it, otherwise default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

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
    
    generate_pages_recursive("content", "template.html", "public", basepath)
    # generate_page("content/index.md", "template.html", "public/index.html")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_root = Path(dir_path_content)
    dest_root = Path(dest_dir_path)

    for root, dirs, files in os.walk(content_root):
        root_path = Path(root)

        for filename in files:
            if not filename.endswith(".md"):
                continue

            src_md_path = root_path / filename
            rel_path = src_md_path.relative_to(content_root)
            dest_html_rel = rel_path.with_suffix(".html")
            dest_html_path = dest_root / dest_html_rel

            # Call generate_page for each markdown file
            generate_page(src_md_path, template_path, dest_html_path, basepath)
            
# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
#     content_root = Path(dir_path_content)
#     template_path = Path(template_path)
#     dest_root = Path(dest_dir_path)

#     with template_path.open("r", encoding="utf-8") as f:
#         template = f.read()

#     # Walk the content tree
#     for root, dirs, files in os.walk(content_root):
#         root_path = Path(root)

#         for filename in files:
#             if not filename.endswith(".md"):
#                 continue

#             src_md_path = root_path / filename

#             # Compute relative path from content root, and mirror into dest_root
#             rel_path = src_md_path.relative_to(content_root)
#             dest_html_rel = rel_path.with_suffix(".html")
#             dest_html_path = dest_root / dest_html_rel

#             # Ensure destination directory exists
#             dest_html_path.parent.mkdir(parents=True, exist_ok=True)

#             # Read markdown
#             with src_md_path.open("r", encoding="utf-8") as f:
#                 markdown = f.read()

#             # Convert markdown to HTML
#             html_node = markdown_to_html(markdown)
#             content_html = html_node.to_html()

#             # Inject into template
#             page_html = template.replace("{{ Content }}", content_html)

#             # Write output file
#             with dest_html_path.open("w", encoding="utf-8") as f:
#                 f.write(page_html)

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
    
def generate_page(from_path, template_path, dest_path, basepath):
    
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
    
    page_html = page_html.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')
    
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
