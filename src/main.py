import os
import shutil
import sys

from markdown_to_html_node import markdown_to_html_node, extract_title


def main():
    try:
        recreate_source_in_destination("./static", "./public")
        generate_pages_recursive("./content", "./template.html", "./public")
    except ValueError as e:
        sys.exit(f"Execution aborted. Error: {e}")
    pass


def recreate_source_in_destination(source, destination):
    prepare_destination(destination)
    copy_source_to_destination(source, destination)


def prepare_destination(destination):
    if os.path.exists(destination):
        print(f"cleaning destination: {destination}")
        shutil.rmtree(destination)

    print(f"Creating folder {destination}.")
    os.mkdir(destination)


def copy_source_to_destination(source, destination):
    if not os.path.exists(source):
        raise ValueError(f"source '{source}' doesn't exist")
    if not os.path.exists(destination):
        raise ValueError(f"destination '{destination}' doesn't exist")

    source_list = os.listdir(source)
    for item in source_list:
        if item[0] == ".":
            continue
        item_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(item_path):
            file_copied = shutil.copy(item_path, destination_path)
            print(f"copied {item_path} to {file_copied}")
        else:
            if not os.path.exists(destination_path):
                print(f"Creating folder {destination_path}.")
                os.mkdir(destination_path)
            copy_source_to_destination(item_path, destination_path)


def generate_pages_recursive(source_dir_path, template_path, dest_dir_path):
    if not os.path.exists(source_dir_path):
        raise ValueError(f"source path '{source_dir_path}' not found")

    source_list = os.listdir(source_dir_path)
    for item in source_list:
        source_path = os.path.join(source_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_path):
            dest_file = str.replace(dest_path, ".md", ".html")
            generate_page(source_path, template_path, dest_file)
        else:
            prepare_destination(dest_path)
            generate_pages_recursive(source_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )
    if not os.path.exists(from_path):
        raise ValueError(f"path '{from_path}' not found")
    if not os.path.isfile(from_path):
        raise ValueError(f"'{from_path}' is not a file")
    if os.path.exists(dest_path):
        raise ValueError(f"destiny page '{dest_path}' shouldn't exist yet")

    with open(from_path, "r") as file:
        file_contents = file.read()
    with open(template_path, "r") as template:
        template_contents = template.read()

    doc_title = extract_title(file_contents)
    document_in_html = markdown_to_html_node(file_contents)
    document_text = document_in_html.to_html()

    final_doc = str.replace(template_contents, "{{ Title }}", doc_title)
    final_doc = str.replace(final_doc, "{{ Content }}", document_text)

    with open(dest_path, "w") as page:
        page.write(final_doc)
        print(
            f"Successfully wrote to '{dest_path}' ({len(final_doc)} characters written)"
        )


if __name__ == "__main__":
    main()
