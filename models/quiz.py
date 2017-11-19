
### import

import datetime

from quizzer.models.class_ import Class
from quizzer.models.model import Model, MAX_LEN
from quizzer.models.teacher import Teacher
from quizzer.models.semester import Semester

### Quiz

def validate_questions(questions):
    field_format = dict(types=QuizQuestion)
    for i, question in enumerate(questions):
        Quiz.validate_types(field_format, 'questions[{}]'.format(i), question)

class Quiz(Model):

    FIELDS = dict(
        name=dict(types=unicode, length=(1, MAX_LEN)),
        class_=dict(types=Class),
        percentage=dict(types=int),
        owner=dict(types=Teacher),
        created=dict(types=datetime.datetime, default=lambda: datetime.datetime.utcnow()),
        questions=dict(types=list, validate=validate_questions),  # Document-oriented structure fits better here. May map to relational if we use RDBMS.
    )

### QuizQuestion

def validate_choices(choices):
    field_format = dict(types=QuizQuestionChoice)
    for i, choice in enumerate(choices):
        QuizQuestion.validate_types(field_format, 'choices[{}]'.format(i), choice)

class QuizQuestion(Model):

    FIELDS = dict(
        # May add some "id" if needed. Using natural index in Quiz.questions list until then.
        text=dict(types=unicode, length=(1, 5000)),  # Text of question may be big enough.
        choices=dict(types=list, validate=validate_choices),  # See above re document-oriented structure.
    )

### QuizQuestionChoice

class QuizQuestionChoice(Model):

    FIELDS = dict(
        # May add some "id" or "order" if needed. Using natural index in QuizQuestion.choices list until then.
        text=dict(types=unicode, length=(1, MAX_LEN)),
        is_correct=dict(types=bool, default=False),
    )

### QuizAnswers

def validate_answers(answers):
    question_index_format = dict(types=int)
    selected_choices_format = dict(types=set)
    selected_choice_index_format = dict(types=int)

    for question_index, selected_choices in answers.iteritems():
        QuizAnswers.validate_types(question_index_format, 'answers.key=question_index', question_index)
        QuizAnswers.validate_types(selected_choices_format, 'answers.value=selected_choices', selected_choices)
        for selected_choice_index in selected_choices:
            QuizAnswers.validate_types(selected_choice_index_format, 'answers.value=selected_choices.item', selected_choice_index)
            # TODO: Improve validation by consulting ranges of int indexes.

class QuizAnswers(Model):
    """
    Answers to a quiz, assigned to a student.
    Stored in student.quizzes: set
    """

    FIELDS = dict(
        quiz=dict(types=Quiz),
        answers=dict(types=dict, validate=validate_answers, default=dict),  # See above re document-oriented structure.
        grade=dict(types=int, null=True, default=None),
    )

### QuizAssignment

class QuizAssignment(Model):

    FIELDS = dict(
        quiz=dict(types=Quiz),
        semester=dict(types=Semester),
    )
