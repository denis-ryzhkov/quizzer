
### import

import datetime

from quizzer.models.person import Person

### Teacher

class Teacher(Person):

    ### assign

    def assign(self, quiz):
        """
        Assign the quiz to students attending its class now.

        @param quiz: Quiz
        """
        from quizzer.models.quiz import QuizAnswers

        for student in self._find_students_for_quiz(quiz):
            if not any(quiz_answers.quiz == quiz for quiz_answers in student.quizzes):
                student.quizzes.add(QuizAnswers(quiz=quiz))

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

        for student in self._find_students_for_quiz(quiz):
            for quiz_answers in student.quizzes:
                if quiz_answers.quiz == quiz:

                    correct_answers = 0
                    for question_index in correct_choices:
                        selected_choices = quiz_answers.answers.get(question_index)
                        if selected_choices == correct_choices[question_index]:
                            # TODO: Ask how to grade, maybe we can value more the more selected and correct choices are intersected.
                            correct_answers += 1

                    correct_ratio = correct_answers / float(len(correct_choices))
                    quiz_answers.grade = 50 + int(round(50 * correct_ratio))  # 50..100

    ### get_total_grades

    def get_total_grades(self):
        """
        Get total grades for all students accumulated over a current semester for the classes of this teacher.

        @return total_grades: list(dict(
            student: Student,
            class_: Class,
            total_grade: int,  # 50..100
        ))
        """
        # TODO: Use http://members.logical.net/~marshall/uab/howtocalculategrade.html
        # TODO: Create "Syllabus" model with percents.
        raise NotImplementedError

    ### _find_students_for_quiz

    def _find_students_for_quiz(self, quiz):
        """
        Find students attending the class of this quiz now.

        @param quiz: Quiz
        @yield students: list(Student)
        """
        from quizzer.models.attendance import Attendance
        from quizzer.models.semester import Semester

        now = datetime.datetime.utcnow()  # TODO: Adjust to timezone of the School, out of scope now.

        for semester in Semester.objects:  # TODO: Use indexed query later.
            if semester.begins <= now <= semester.ends:

                for attendance in Attendance.objects:  # TODO: Use indexed query later.
                    if attendance.class_ == quiz.class_ and attendance.semester == semester:
                        yield attendance.student

