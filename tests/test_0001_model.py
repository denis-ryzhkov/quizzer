
### import

import pytest

from quizzer.models.model import Model

### test abstract base Model

def test_model():
    with pytest.raises(NotImplementedError) as e:
        model = Model()
    assert 'Define FIELDS' in str(e)
    # Abstract base Model can not be tested until implemented in subclasses like Teacher or Class, see their tests.
