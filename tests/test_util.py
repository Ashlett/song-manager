from datetime import date

from songmgr.util.util import str_to_date


def test_str_to_date():
    result = str_to_date('2010-10-10')
    expected = date(2010, 10, 10)
    assert result == expected
