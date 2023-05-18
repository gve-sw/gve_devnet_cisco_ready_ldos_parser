from django import forms
from django.core.exceptions import ValidationError
import datetime


class DateInput(forms.DateInput):
    input_type = "date"


def minor_items_radio():
    YES = "yes"
    NO = "no"
    CHOICES = (
        (NO, "no"),
        (YES, "yes"),
    )
    return forms.ChoiceField(choices=CHOICES)


def single_or_many_customers_per_file():
    SINGLE = "single customer"
    MULTIPLE = "multiple customers"
    CHOICES = (
        (SINGLE, "single customer per file"),
        (MULTIPLE, "multiple customers per file"),
    )
    return forms.ChoiceField(choices=CHOICES)


def time_filter_selection():
    LDOS = "Last Date of Support"
    EOSMD = "End of Software Maintenance Date"
    EOPSD = "End of Product Sale Date"
    LRD = "Last Renewal Date"

    CHOICES = (
        (LDOS, "Last Date of Support"),
        (EOSMD, "End of Software Maintenance Date"),
        (EOPSD, "End of Product Sale Date"),
        (LRD, "Last Renewal Date"),
    )
    return forms.ChoiceField(choices=CHOICES)


def output_date_format():
    DDMMYYYY = "DD/MM/YYYY"
    MMDDYYYY = "MM/DD/YYYY"
    YYYYMMDD = "YYYY/MM/DD"

    CHOICES = (
            (DDMMYYYY, "DD/MM/YYYY"),
            (MMDDYYYY, "MM/DD/YYYY"),
            (YYYYMMDD, "YYYY/MM/DD"),
    )
    return forms.ChoiceField(choices=CHOICES)

class UploadFileForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    file = forms.FileField()
    name = forms.CharField(max_length=255, required=False)

    include_minor_items = minor_items_radio()
    base_date_selection_on = time_filter_selection()
    file_type = single_or_many_customers_per_file()
    output_date_format = output_date_format()


class UploadFolderForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))
    include_minor_items = minor_items_radio()
    base_date_selection_on = time_filter_selection()
    output_date_format = output_date_format()
