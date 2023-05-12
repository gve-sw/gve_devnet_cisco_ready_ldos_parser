import os

from .parser import Parser


def parse_file(
    file_to_parse,
    output,
    start_date,
    end_date,
    include_minor_items,
    selected_date_target,
    file_type="single customer",
):
    """
    Description: Function used by Django views to pass form parameters to the Parser object.

    Args:
        file_to_parse (str): Path to file that we want to process.
        output (str): Path where the resulting file is written to.
        start_date (str): Lower end of the date filter done by the Parser object.
        end_date (str): Higher end of the date fitler done by the Parser object.
        include_minor_items (str): yes/no value that decides whether we include Minor items.
        selected_date_target (str): One of \'Last Date of Support\',
                                           \'End of Software Maintenance Date\',
                                           \'End of Product Sale Date\',
                                           \'Last Renewal Date\'
    """
    parser = Parser(
        file_to_parse,
        output,
        start_date,
        end_date,
        include_minor_items,
        selected_date_target,
        file_type,
    )


def threading_for_folder(
    name, start_date, end_date, include_minor_items, selected_date_target
):
    """
    Description: Function used by the Django views, upload_folder, as it uses multiprocessing.
                 Passes values from the upload_folder view to the parse_file function.

    Args:
        name (str): Name of the file to process with the Parser object.
        start_date (str): Lower end of the date filter done by the Parser object.
        end_date (str): Higher end of the date fitler done by the Parser object.
        include_minor_items (str): yes/no value that decides whether we include Minor items.
        selected_date_target (str): One of \'Last Date of Support\',
                                           \'End of Software Maintenance Date\',
                                           \'End of Product Sale Date\',
                                           \'Last Renewal Date\'
    """

    unparsed_path = os.path.join("media", "unparsed")
    parsed_path = os.path.join("media", "parsed")
    unparsed_file_path = os.path.join(unparsed_path, name)
    parsed_file_path = f"{parsed_path}/{name}_parsed.xlsx"
    print(parsed_file_path)
    parse_file(
        unparsed_file_path,
        parsed_file_path,
        start_date,
        end_date,
        include_minor_items,
        selected_date_target,
    )
