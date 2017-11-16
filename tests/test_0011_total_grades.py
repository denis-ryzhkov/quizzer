
### import

from quizzer.models.attendance import Attendance
from quizzer.models.semester import Semester

### test total_grades

def test_good_total_grades(attendance, class_, quiz, semester, student, teacher):
    Semester.objects.add(semester)
    Attendance.objects.add(attendance)
    teacher.assign(quiz)
    student.submit(quiz, add_answers={
        0: set([0, 2]),
    })
    teacher.grade(quiz)

    total_grades = teacher.get_total_grades()

    assert total_grades == [
        dict(student=student, class_=class_, total_grade=100),
    ]

# TODO: Add more tests.
