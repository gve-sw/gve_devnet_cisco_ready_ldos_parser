from django.test import TestCase
from .forms import UploadFileForm, UploadFolderForm
from django.urls import reverse
import datetime, random


def random_dates(start_year, end_year):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 1, 1)

    # Generate a random number of days between the start and end dates
    days_between = (end_date - start_date).days
    random_number_of_days = random.randint(0, days_between)

    # Add the random number of days to the start date to get a random date
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


class FileViewTestCase(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse("upload_file"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/upload_file.html")
        self.assertIsInstance(response.context["form"], UploadFileForm)

    def test_post_request_valid_data_for_single_customer_file(self):
        date_selection_options = [
            "Last Date of Support",
            "End of Software Maintenance Date",
            "Last Renewal Date",
            "End of Product Sale Date",
        ]
        minor_inclusion = ["yes", "no"]
        for date_option in date_selection_options:
            for flag in minor_inclusion:
                start_date = random_dates(1984, 2000)
                end_date = random_dates(2001, 2200)
                with open("media/test_files/empty.xlsb", "rb") as f:
                    data = {
                        "name": "test_file",
                        "file": f,
                        "start_date": start_date,
                        "end_date": end_date,
                        "include_minor_items": flag,
                        "base_date_selection_on": date_option,
                        "file_type": "single customer",
                    }
                    response = self.client.post(reverse("upload_file"), data=data)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response["Content-Disposition"],
                        'attachment; filename="test_file_parsed.xlsx"',
                    )
                    f.close()

    def test_post_request_valid_data_for_multiple_file(self):
        date_selection_options = [
            "Last Date of Support",
            "End of Software Maintenance Date",
            "Last Renewal Date",
            "End of Product Sale Date",
        ]
        minor_inclusion = ["yes", "no"]
        for date_option in date_selection_options:
            for flag in minor_inclusion:
                start_date = random_dates(1984, 2000)
                end_date = random_dates(2001, 2200)
                with open("media/test_files/empty.xlsb", "rb") as f:
                    data = {
                        "name": "test_file",
                        "file": f,
                        "start_date": start_date,
                        "end_date": end_date,
                        "include_minor_items": flag,
                        "base_date_selection_on": date_option,
                        "file_type": "multiple customers",
                    }
                    response = self.client.post(reverse("upload_file"), data=data)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response["Content-Disposition"],
                        'attachment; filename="test_file_parsed.xlsx"',
                    )
                    f.close()

    def test_post_request_invalid_date_for_single_file(self):
        # lower bound outside range
        # upper bound outside range
        # lower > upper
        date_selection_options = [
            "Last Date of Support",
            "End of Software Maintenance Date",
            "Last Renewal Date",
            "End of Product Sale Date",
        ]
        minor_inclusion = ["yes", "no"]
        date_pairs = [
            ("1800-01-01", "2100-01-01"),
            ("2000-01-01", "2201-01-01"),
            ("2031-01-01", "2019-01-01"),
        ]
        for date_option in date_selection_options:
            for flag in minor_inclusion:
                for date_pair in date_pairs:
                    with open("media/test_files/empty.xlsb", "rb") as f:
                        data = {
                            "name": "test_file",
                            "file": f,
                            "start_date": date_pair[0],
                            "end_date": date_pair[1],
                            "include_minor_items": flag,
                            "base_date_selection_on": date_option,
                            "file_type": "multiple customers",
                        }
                        response = self.client.post(reverse("upload_file"), data=data)
                        self.assertEqual(response.status_code, 400)
                        self.assertTemplateUsed(response, "website/upload_file.html")
                        self.assertIsInstance(response.context["form"], UploadFileForm)
                        self.assertTemplateUsed(response, "website/upload_file.html")
                        self.assertContains(
                            response,
                            "Unacceptable dates were provided",
                            status_code=400,
                        )
                        f.close()

    def not_post_get_request(self, method):
        with open("media/test_files/empty.xlsb", "rb") as f:
            data = {
                "name": "test_file",
                "file": f,
                "start_date": "2022-01-01",
                "end_date": "2022-01-31",
                "include_minor_items": "yes",
                "base_date_selection_on": "Last Date of Support",
                "file_type": "single customer",
            }
            if method.lower() == "put":
                response = self.client.put(reverse("upload_file"), data=data)
            elif method.lower() == "delete":
                response = self.client.delete(reverse("upload_file"), data=data)
            elif method.lower() == "patch":
                response = self.client.patch(reverse("upload_file"), data=data)
            self.assertEqual(response.status_code, 400)
            self.assertContains(
                response,
                "This resource only accepts POST or GET requests",
                status_code=400,
            )

    def test_put_request_returns_400(self):
        self.not_post_get_request("put")

    def test_patch_request_returns_400(self):
        self.not_post_get_request("patch")

    def test_delete_request_returns_400(self):
        self.not_post_get_request("delete")
