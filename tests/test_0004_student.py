
### import

from quizzer.models.student import Student

### test Student

def test_good_student():
    student = Student(first_name=u'Edwin', last_name=u'Aldrin')
    # Skipping other tests of abstract base Model here, see Teacher tests.
