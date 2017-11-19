
### import

from quizzer.models.attendance import Attendance
from quizzer.models.quiz import QuizAssignment
from quizzer.models.semester import Semester

### test assign

def test_good_assign(attendance, class_, quiz, semester, student, teacher):
    Semester.objects.add(semester)
    Attendance.objects.add(attendance)

    assert isinstance(student.quizzes, set)
    assert len(student.quizzes) == 0
    assert len(QuizAssignment.objects) == 0

    teacher.assign(quiz)

    assert len(QuizAssignment.objects) == 1
    quiz_assignment = next(quiz_assignment for quiz_assignment in QuizAssignment.objects)
    assert quiz_assignment.quiz == quiz
    assert quiz_assignment.semester == semester

    assert len(student.quizzes) == 1
    quiz_answers = next(quiz_answers for quiz_answers in student.quizzes)
    assert quiz_answers.quiz == quiz
    assert isinstance(quiz_answers.answers, dict)
    assert len(quiz_answers.answers) == 0

# TODO: Add tests for students not attending the class now, etc.
