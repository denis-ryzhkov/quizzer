
### import

from quizzer.models.attendance import Attendance
from quizzer.models.semester import Semester

### test submit

def test_good_submit(attendance, quiz, semester, student, teacher):
    Semester.objects.add(semester)
    Attendance.objects.add(attendance)
    teacher.assign(quiz)

    student.submit(quiz, add_answers={
        0: set([1, 2]),
    })

    quiz_answers = next(quiz_answers for quiz_answers in student.quizzes)
    assert quiz_answers.quiz == quiz
    assert isinstance(quiz_answers.answers, dict)
    assert len(quiz_answers.answers) == 1
    assert quiz_answers.answers[0] == set([1, 2])

# TODO: Add tests for multiple submits to the same quiz, submit to invalid quiz, etc.
