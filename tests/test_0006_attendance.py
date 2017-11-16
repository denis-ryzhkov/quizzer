
### import

from quizzer.models.attendance import Attendance

### test Attendance

def test_good_attendance(student, class_, semester):
    attendance = Attendance(student=student, class_=class_, semester=semester)
    # Skipping other tests of abstract base Model here, see Teacher tests.
