
### import

import datetime
import pytest

from quizzer.models.semester import Semester

### test Semester

def test_good_semester():
    semester = Semester(
        begins=datetime.datetime(2017, 8, 20),
        ends=datetime.datetime(2017, 12, 20),
    )
    # Skipping other tests of abstract base Model here, see Teacher tests.

def test_no_current_semester():
    with pytest.raises(ValueError) as e:
        current_semester = Semester.get_current()
    assert 'Current semester is not defined' in str(e)

def test_good_current_semester(semester):
    Semester.objects.add(semester)
    current_semester = Semester.get_current()
    assert current_semester == semester

