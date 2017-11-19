
### import

from quizzer.models.model import Model, MAX_LEN
from quizzer.models.teacher import Teacher

### Class

class Class(Model):

    FIELDS = dict(
        number=dict(types=unicode, length=(1, MAX_LEN)),
        name=dict(types=unicode, length=(1, MAX_LEN)),
        teacher=dict(types=Teacher, null=True, default=None),
    )

    ### find_students

    def find_students(self):
        """
        Find students attending this class in the current semester.

        @yield student: Student
        """
        from quizzer.models.attendance import Attendance
        from quizzer.models.semester import Semester

        semester = Semester.get_current()

        for attendance in Attendance.objects:  # TODO: Use indexed query later.
            if attendance.semester == semester and attendance.class_ == self:
                yield attendance.student
