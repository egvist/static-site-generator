
import os
from markdown_to_html import markdown_to_html_node

def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("No H1 heading found in markdown")



def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    # 1. Markdown dosyasını oku
    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    # 2. HTML template dosyasını oku
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    # 3. Markdown'ı HTML'e çevir
    html_content = markdown_to_html_node(markdown).to_html()

    # 4. Başlığı çıkar
    title = extract_title(markdown)

    # 5. Template içindeki placeholder'ları değiştir
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)

    # YENİ: GitHub Pages için basepath ekle
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    # 6. Hedef klasörü oluştur
    destination_dir = os.path.dirname(dest_path)

    if destination_dir:
        os.makedirs(destination_dir, exist_ok=True)

    # 7. HTML dosyasını yaz
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(page)




def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(source_path):
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
                basepath
            )

        elif os.path.isfile(source_path) and item.endswith(".md"):
            destination_path = os.path.splitext(destination_path)[0] + ".html"

            generate_page(
                source_path,
                template_path,
                destination_path,
                basepath
            )
