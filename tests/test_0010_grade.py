
### import

from quizzer.models.attendance import Attendance
from quizzer.models.semester import Semester

### test grade

def test_good_grade(attendance, quiz, semester, student, teacher):
    Semester.objects.add(semester)
    Attendance.objects.add(attendance)
    teacher.assign(quiz)

    student.submit(quiz, add_answers={0: set([0, 2])})
    teacher.grade(quiz)
    quiz_answers = next(quiz_answers for quiz_answers in student.quizzes)
    assert quiz_answers.quiz == quiz
    assert quiz_answers.grade == 100

def test_not_equal_grade(attendance, quiz, semester, student, teacher):
    Semester.objects.add(semester)
    Attendance.objects.add(attendance)
    teacher.assign(quiz)

    student.submit(quiz, add_answers={0: set([2])})
    teacher.grade(quiz)
    quiz_answers = next(quiz_answers for quiz_answers in student.quizzes)
    assert quiz_answers.quiz == quiz
    assert quiz_answers.grade == 50

# TODO: Add tests for different grade scenarios.
