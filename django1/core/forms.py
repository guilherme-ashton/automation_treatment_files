from django import forms
import lxml.etree as ET
import pandas as pd
import re

from pandas import DataFrame
from pylogix import PLC
import os


class UploadFileXml(forms.Form):
    arquivo_xml = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))


class UploadFileL5X(forms.Form):
    arquivo_L5X = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))


class UploadFileForm(forms.Form):
    arquivo_L5X = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    arquivo_xml = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))


