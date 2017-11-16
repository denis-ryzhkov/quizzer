
### import

import datetime
import pytest

from quizzer.models.quiz import Quiz, QuizQuestion, QuizQuestionChoice

### test Quiz

def test_good_quiz(class_, teacher):
    quiz = Quiz(
        name=u'Object-oriented data structure design',
        class_=class_,
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

    assert hasattr(quiz, 'created')
    assert isinstance(quiz.created, datetime.datetime)
    assert 0 <= (datetime.datetime.utcnow() - quiz.created).total_seconds() < 1
    # Skipping other tests of abstract base Model here, see Teacher tests.

### also test custom validation feature of abstract base Model

def test_bad_quiz_question_type(class_, teacher):
    with pytest.raises(TypeError) as e:
        quiz = Quiz(
            name=u'Object-oriented data structure design',
            class_=class_,
            owner=teacher,
            questions=[True],
        )
    assert '''"Quiz" requires type of field "questions[0]" to be <class 'quizzer.models.quiz.QuizQuestion'>, not <type 'bool'>''' in str(e)

def test_bad_quiz_question_choice_type(class_, teacher):
    with pytest.raises(TypeError) as e:
        quiz = Quiz(
            name=u'Object-oriented data structure design',
            class_=class_,
            owner=teacher,
            questions=[
                QuizQuestion(
                    text=u'What design fits better for Quiz.questions?',
                    choices=[True],
                ),
            ],
        )
    assert '''"QuizQuestion" requires type of field "choices[0]" to be <class 'quizzer.models.quiz.QuizQuestionChoice'>, not <type 'bool'>''' in str(e)
