
### import

from collections import defaultdict
import datetime

from quizzer.models.person import Person

### const

MIN_GRADE = 50
MAX_GRADE = 100

### Teacher

class Teacher(Person):

    ### assign

    def assign(self, quiz):
        """
        Assign the quiz to students attending its class now.

        @param quiz: Quiz
        """
        from quizzer.models.quiz import QuizAnswers, QuizAssignment
        from quizzer.models.semester import Semester

        for student in quiz.class_.find_students():
            if not any(quiz_answers.quiz == quiz for quiz_answers in student.quizzes):
                student.quizzes.add(QuizAnswers(quiz=quiz))

        semester = Semester.get_current()
        if not any(quiz_assignment.quiz == quiz and quiz_assignment.semester == semester for quiz_assignment in QuizAssignment.objects):
            QuizAssignment.objects.add(QuizAssignment(quiz=quiz, semester=semester))

    ### grade

    def grade(self, quiz):
        """
        Grade the quiz for all students attending its class now.

        @param quiz: Quiz
        """
        from quizzer.models.quiz import QuizAnswers

        ### cache correct shoices for this quiz

        correct_choices = {}
        for question_index, question in enumerate(quiz.questions):
            correct_choices[question_index] = set(choice_index
                for choice_index, choice in enumerate(question.choices)
                if choice.is_correct
            )

        ### compare answers of students

        for student in quiz.class_.find_students():
            for quiz_answers in student.quizzes:
                if quiz_answers.quiz == quiz:

                    correct_answers = 0
                    for question_index in correct_choices:
                        selected_choices = quiz_answers.answers.get(question_index)
                        if selected_choices == correct_choices[question_index]:
                            # TODO: Ask how to grade, maybe we can value more the more selected and correct choices are intersected.
                            correct_answers += 1

                    correct_ratio = correct_answers / float(len(correct_choices))
                    quiz_answers.grade = MIN_GRADE + int(round((MAX_GRADE - MIN_GRADE) * correct_ratio))  # 50..100

    ### get_total_grades

    def get_total_grades(self):
        """
        Get total grades for all students accumulated over a current semester for the classes of this teacher.
        Docs: http://members.logical.net/~marshall/uab/howtocalculategrade.html

        @return total_grades: list(dict(
            student: Student,
            class_: Class,
            total_grade: int,  # 50..100
        ))
        """
        from quizzer.models.quiz import QuizAssignment
        from quizzer.models.semester import Semester

        result = []
        semester = Semester.get_current()

        ### quizzes_by_classes

        quizzes_by_classes = defaultdict(set)  # Quizzes assigned in the current semester for the classes of this teacher only.
        for quiz_assignment in QuizAssignment.objects:  # TODO: Indexed query later.
            if quiz_assignment.semester == semester and quiz_assignment.quiz.class_.teacher == self:
                quizzes_by_classes[quiz_assignment.quiz.class_].add(quiz_assignment.quiz)

        ### for each class

        for class_, required_quizzes in quizzes_by_classes.iteritems():

            ### total_percentage

            total_percentage = sum(quiz.percentage for quiz in required_quizzes)
            if total_percentage != 100:
                raise ValueError('Total percentage of quizzes assigned for class number "{}" in the current semester is {}, not 100'.format(
                    class_.number.encode('utf8'), total_percentage,
                ))

            ### total_grade

            for student in class_.find_students():
                total_grade = 0.0
                assigned_quizzes = set()

                for quiz_answers in student.quizzes:
                    if quiz_answers.quiz in required_quizzes:
                        total_grade += (quiz_answers.grade or MIN_GRADE) * quiz_answers.quiz.percentage / 100.0
                        assigned_quizzes.add(quiz_answers.quiz)

                for quiz in required_quizzes - assigned_quizzes:
                    total_grade += MIN_GRADE * quiz.percentage

                ### result

                result.append(dict(student=student, class_=class_, total_grade=int(round(total_grade))))
        return result
