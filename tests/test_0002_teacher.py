
### import

import pytest

from quizzer.models.teacher import Teacher

### test Teacher, test abstract base Model via Teacher

def test_good_teacher():
    teacher = Teacher(first_name=u'John', last_name=u'Guttag')
    assert teacher.first_name == u'John'
    assert teacher.last_name == u'Guttag'

def test_teacher_undefined_field():
    with pytest.raises(TypeError) as e:
        teacher = Teacher(wings=2)
    assert '"Teacher" does not have "wings"' in str(e)

def test_teacher_no_first_name():
    with pytest.raises(TypeError) as e:
        teacher = Teacher()
    assert '"Teacher" requires field "first_name"' in str(e)

def test_teacher_first_name_bad_type():
    with pytest.raises(TypeError) as e:
        teacher = Teacher(first_name='John')
    assert '''"Teacher" requires type of field "first_name" to be <type 'unicode'>, not <type 'str'>''' in str(e)

def test_teacher_too_short_first_name():
    with pytest.raises(TypeError) as e:
        teacher = Teacher(first_name=u'')
    assert '"Teacher" requires length of field "first_name" to be 1 or more, not 0' in str(e)

def test_teacher_edge_case_short_first_name():
    teacher = Teacher(first_name=u'J', last_name=u'G')

def test_teacher_too_long_first_name():
    with pytest.raises(TypeError) as e:
        teacher = Teacher(first_name=u'J' + u'o' * 100500 + u'hn')
    assert '"Teacher" requires length of field "first_name" to be 200 or less, not 100503' in str(e)

def test_teacher_edge_case_long_first_name():
    teacher = Teacher(first_name=u'J' * 200, last_name=u'G')

def test_teacher_no_last_name():
    with pytest.raises(TypeError) as e:
        teacher = Teacher(first_name=u'John')
    assert '"Teacher" requires field "last_name"' in str(e)
