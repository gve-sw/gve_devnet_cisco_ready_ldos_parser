from django.shortcuts import render, redirect
from .forms import UploadFileForm, UploadFolderForm
from django.http import FileResponse, HttpResponse, JsonResponse
import os, io, zipfile
import datetime
import pathlib
import time
import multiprocessing

from .file_handler import *
from .threading_handle import threading_for_folder, parse_file
from .error_messages import INVALID_DATE

DIR = f"{str(pathlib.Path().resolve())}"
create_folders_for_uploaded_files()


def download_file(file_path, file_name):
    """
    Description: Downloads a file from the specified path and returns it as a Django HTTP response.

    Args:
        file_path (str): The path to the file to be downloaded.
        file_name (str): The name of the file.

    Returns:
        FileResponse: An HTTP response containing the file to be downloaded.
    """
    file = open(file_path, "rb")
    response = FileResponse(file)
    # Set the content type header based on the file type
    response["Content-Type"] = "application/octet-stream"
    # Set the content-disposition header to force download
    split_name = file_name.split("/")
    response["Content-Disposition"] = f'attachment; filename="{split_name[-1]}"'
    return response


def download_folder():
    """
    Description: Downloads a folder as a zip file and returns it as a Django HTTP response.

    Returns:
        HttpResponse: An HTTP response containing the zip file to be downloaded.
    """
    folder_path = "media/parsed"  # Replace with the path to your folder
    file_list = os.listdir(folder_path)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in file_list:
            file_path = os.path.join(folder_path, f)
            zf.write(file_path, f)

    response = HttpResponse(buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=download.zip"
    return response


def date_interval_is_valid(start_date, end_date):
    """
    Description: Checks if the given start and end dates fall within a valid range.

    Args:
        start_date (str): The start date of the interval in the format YYYY-MM-DD.
        end_date (str): The end date of the interval in the format YYYY-MM-DD.

    Returns:
        bool: True if the interval is valid, False otherwise.

    """
    lower_date_limit = datetime.datetime(1984, 1, 1)
    upper_date_limit = datetime.datetime(2200, 1, 1)
    try:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except Exception as error:
        print(error)
        return False
    if start < lower_date_limit or end > upper_date_limit:
        return False
    if start > end:
        return False
    return True


def home(request):
    return render(request, "website/base.html")


def upload_file(request):
    """
    Description: This view handles file uploads and returns the parsed file for download.
                 It expects a POST request containing a file and other data needed for parsing
                 the file, or a GET request to render the upload form.

    Parameters:
        request (HttpRequest): The HTTP request object that contains information about the request.

    Returns:
        HttpResponse: A HttpResponse object containing either the parsed file for download, or the rendered upload form.

    Methods:
        GET: Renders the upload form.
        POST: Handles the uploaded file, parses it, and returns the parsed file for download.

    Form Fields:
        name (CharField): The name of the file to be uploaded. Defaults to the name of the uploaded file.
        file (FileField): The file to be uploaded.
        start_date (DateField): The start date for the date range to filter data by.
        end_date (DateField): The end date for the date range to filter data by.
        include_minor_items (ChoiceField): A flag to indicate whether or not to include minor items in the parsed data.
        base_date_selection_on (ChoiceField): The criteria for selecting the date field to filer for.

    """
    form = UploadFileForm()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        name = request.POST["name"]
        file = request.FILES["file"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        include_minor_items = request.POST["include_minor_items"]
        selected_date_target = request.POST["base_date_selection_on"]
        file_type = request.POST["file_type"]

        if date_interval_is_valid(start_date, end_date):
            if name == "":
                name = format_file_name(file)

            path_and_extension = f"media/unparsed/{name}.xlsb"
            output_name = f"media/parsed/{name}_parsed.xlsx"
            handle_uploaded_file(file, path_and_extension)
            print("Reading the file")
            start_time = time.time()
            parse_file(
                path_and_extension,
                output_name,
                start_date,
                end_date,
                include_minor_items,
                selected_date_target,
                file_type,
            )
            end_time = time.time()
            print("Finished reading the file")
            print(f"Took {end_time - start_time} seconds")
            output_name = f"{DIR}/{output_name}"
            build_download_file = download_file(output_name, output_name)
            remove_files()
            return build_download_file
        else:
            error_message = INVALID_DATE.format(start_date, end_date)
            context = {"form": form, "error_message": error_message}
            return render(request, "website/upload_file.html", context, status=400)

    elif request.method == "GET":
        return render(
            request,
            "website/upload_file.html",
            {
                "form": form,
            },
        )
    else:
        context = {
            "error_message": "This resource only accepts POST or GET requests",
            "form": form,
        }
        return render(request, "website/upload_file.html", context, status=400)


def upload_folder(request):
    """
    Description: This view handles multi-file uploads and returns the parsed file for download.
                 It expects a POST request containing a multiple files and other data needed for parsing
                 the files, or a GET request to render the upload form.

    Parameters:
        request (HttpRequest): The HTTP request object that contains information about the request.

    Returns:
        HttpResponse: A HttpResponse object containing either the parsed file for download, or the rendered upload form.

    Methods:
        GET: Renders the upload form.
        POST: Handles the uploaded file, parses it, and returns the parsed file for download.

    Form Fields:
        files (FileField): The list of files to be uploaded.
        start_date (DateField): The start date for the date range to filter data by.
        end_date (DateField): The end date for the date range to filter data by.
        include_minor_items (ChoideField): A flag to indicate whether or not to include minor items in the parsed data.
        base_date_selection_on (ChoiceField): The criteria for selecting the date field to filer for.
    """

    form = UploadFolderForm()
    if request.method == "POST":
        form = UploadFolderForm(request.POST, request.FILES)
        folder = request.FILES.getlist("files")
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        include_minor_items = request.POST["include_minor_items"]
        selected_date_target = request.POST["base_date_selection_on"]

        if date_interval_is_valid(start_date, end_date):
            threads = []

            start_timer = time.time()
            for index, file in enumerate(folder):
                print(f"MAIN: Create and start thread {index}")

                name = format_file_name(file)
                unparsed_path = os.path.join("media", "unparsed")
                parsed_path = os.path.join("media", "parsed")
                unparsed_file_path = os.path.join(unparsed_path, name)
                parsed_file_path = f"{parsed_path}/{name}_parsed.xlsx"
                handle_uploaded_file(file, unparsed_file_path)

                process = multiprocessing.Process(
                    target=threading_for_folder,
                    args=(
                        name,
                        start_date,
                        end_date,
                        include_minor_items,
                        selected_date_target,
                    ),
                )
                threads.append(process)
                process.start()
            for index, thread in enumerate(threads):
                print(f"MAIN: before joining thread {index}")
                thread.join()
                print(f"MAIN: thread {index} is finished")
            end_timer = time.time()
            diff = end_timer - start_timer
            print(diff)
            build_download_file = download_folder()
            remove_files()
            return build_download_file
        else:
            error_message = INVALID_DATE.format(start_date, end_date)
            context = {"form": form, "error_message": error_message}
            return render(request, "website/upload_file.html", context, status=400)

    elif request.method == "GET":
        return render(request, "website/upload_folder.html", {"form": form})
    else:
        context = {
            "error_message": "This resource only accepts POST or GET requests",
            "form": form,
        }
        return render(request, "website/upload_folder.html", context, status=400)
