
### import

import datetime
import pytest

from quizzer.models.attendance import Attendance
from quizzer.models.class_ import Class
from quizzer.models.quiz import Quiz, QuizQuestion, QuizQuestionChoice
from quizzer.models.semester import Semester
from quizzer.models.student import Student
from quizzer.models.teacher import Teacher

### shared fixtures

@pytest.fixture(scope='session')
def teacher():
    return Teacher(first_name=u'John', last_name=u'Guttag')

@pytest.fixture(scope='session')
def class_():
    return Class(number=u'6.00', name=u'Introduction to Computer Science and Programming')

@pytest.fixture(scope='session')
def student():
    return Student(first_name=u'Edwin', last_name=u'Aldrin')

@pytest.fixture(scope='session')
def semester():
    now = datetime.datetime.utcnow()
    return Semester(
        begins=now - datetime.timedelta(days=60),
        ends=now + datetime.timedelta(days=60),
    )

@pytest.fixture(scope='session')
def attendance(student, class_, semester):
    return Attendance(student=student, class_=class_, semester=semester)

@pytest.fixture(scope='session')
def quiz(class_, teacher):
    return Quiz(
        name=u'Object-oriented data structure design',
        class_=class_,
        percentage=100,
        owner=teacher,
        questions=[
            QuizQuestion(
                text=u'What design fits better for Quiz.questions?',
                choices=[
                    QuizQuestionChoice(text=u'Document-oriented', is_correct=True),
                    QuizQuestionChoice(text=u'Relational'),
                    QuizQuestionChoice(text=u'Any other, fast and simple enough', is_correct=True),
                    QuizQuestionChoice(text=u'Whatever'),
                ],
            ),
        ],
    )
