
### import

from quizzer.models.model import Model, MAX_LEN
from quizzer.models.teacher import Teacher

### Class

class Class(Model):

    FIELDS = dict(
        number=dict(types=unicode, length=(1, MAX_LEN)),
        name=dict(types=unicode, length=(1, MAX_LEN)),
        teacher=dict(types=Teacher, null=True, default=None),
    )
