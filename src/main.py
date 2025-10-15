import os
import shutil
import sys

def main():
    try:
        recreate_source_in_destination("./static", "./public")
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

if __name__ == "__main__":
    main()
