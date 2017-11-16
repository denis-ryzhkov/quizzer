
### import

import datetime

from quizzer.models.semester import Semester

### test Semester

def test_good_semester():
    semester = Semester(
        begins=datetime.datetime(2017, 8, 20),
        ends=datetime.datetime(2017, 12, 20),
    )
    # Skipping other tests of abstract base Model here, see Teacher tests.
