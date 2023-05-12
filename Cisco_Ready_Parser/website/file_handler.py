import os


def handle_uploaded_file(file, path):
    """
    Description: Takes the uploaded file objects and writes it on disk.
    Args:
        file (django.core.files.uploadedfile.TemporaryUploadedFile): Uploaded file that we want to write
        path (str): Where we want to save the file.
    """
    with open(path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def remove_files():
    """
    Description: Remove the files after they have been processed.
    """

    file_cleaner("media/unparsed")
    file_cleaner("media/parsed")


def file_cleaner(path):
    file_list = os.listdir(path)

    for file_name in file_list:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def format_file_name(file):
    """
    Description: If the SE does not specify a file name directly,
                 then the files usually have a long number attached.
                 This function removes the long number.
    Args:
        file (django.core.files.uploadedfile.TemporaryUploadedFile): Uploaded file which name take care of.

    Returns:
        str: The name without the numbering.
    """
    name_split = os.path.splitext(file.name)
    name = name_split[0]
    return name


def create_folders_for_uploaded_files():
    """
    Description: Uploaded files are stored in either media/parsed or
                 media/unparsed. This function ensures the folders exist.
    """
    unparsed_path = os.path.join("media", "unparsed")
    parsed_path = os.path.join("media", "parsed")
    os.makedirs(unparsed_path, exist_ok=True)
    os.makedirs(parsed_path, exist_ok=True)
