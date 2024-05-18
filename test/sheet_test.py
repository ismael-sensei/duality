import pytest
from use_cases import sheet

def test_import():
    char = sheet.import_sheet('4f7a9c6c-32b1-441d-bebb-e99d8e75970a')
    
    assert char.level == 1

