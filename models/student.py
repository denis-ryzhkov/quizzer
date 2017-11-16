
### import

from quizzer.models.person import Person

### Student

class Student(Person):

    FIELDS = Person.FIELDS.copy()
    FIELDS.update(
        quizzes=dict(type=set, default=set),
    )

    ### submit

    def submit(self, quiz, add_answers):
        """
        Submits more answers to the quiz.

        @param quiz: Quiz
        @param add_answers: dict(
            question_index: int,
            selected_choices: set(
                selected_choice_index: int
            )
        )
        """
        quiz_answers = next(quiz_answers for quiz_answers in self.quizzes if quiz_answers.quiz == quiz)
        quiz_answers.answers.update(add_answers)
