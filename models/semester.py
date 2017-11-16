
### import

import datetime

from quizzer.models.model import Model

### Semester

class Semester(Model):

    FIELDS = dict(
        begins=dict(types=datetime.datetime),
        ends=dict(types=datetime.datetime),
    )
