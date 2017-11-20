
### import

import pytest

from quizzer.models.class_ import Class
from quizzer.models.teacher import Teacher

### test Class

def test_good_class():
    class_ = Class(
        number=u'6.00',
        name=u'Introduction to Computer Science and Programming',
        # Once required, can also reference:
        # course=Course(
        #   number=u'6',
        #   name=u'Electrical Engineering and Computer Science',
        #   institution=Institution(name=u'MIT',..),
        # )
    )

    assert class_.number == u'6.00'
    assert class_.name == u'Introduction to Computer Science and Programming'

def test_bad_class():
    with pytest.raises(TypeError):
        class_ = Class()
    # Skipping other tests of abstract base Model here, see Teacher tests.

### test Class.teacher default and delete - and these features of abstract base Model too

def test_class_teacher_default():
    class_ = Class(number=u'6.00', name=u'Introduction to Computer Science and Programming')
    assert hasattr(class_, 'teacher')
    assert class_.teacher is None

def test_class_teacher_delete(class_):
    with pytest.raises(TypeError) as e:
        del class_.teacher
    assert 'Field "teacher" defined in "Class" should always exist' in str(e)

### test Class.teacher update - and this feature of abstract base Model too

def test_class_teacher_nullable(class_, teacher):
    class_.teacher = None
    assert class_.teacher is None

def test_good_class_teacher(class_, teacher):
    class_.teacher = teacher
    assert isinstance(class_.teacher, Teacher)

def test_bad_class_teacher(class_):
    with pytest.raises(TypeError) as e:
        class_.teacher = True
    assert '''"Class" requires type of field "teacher" to be <class 'quizzer.models.teacher.Teacher'> or None, not <type 'bool'>''' in str(e)
