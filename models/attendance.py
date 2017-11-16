
### import

from quizzer.models.class_ import Class
from quizzer.models.model import Model
from quizzer.models.semester import Semester
from quizzer.models.student import Student

### Attendance

class Attendance(Model):
    """
    Relation of a student attending a class in a semester.
    """

    FIELDS = dict(
        student=dict(types=Student),
        class_=dict(types=Class),
        semester=dict(types=Semester),
    )
