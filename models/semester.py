
### import

import datetime

from quizzer.models.model import Model

### Semester

class Semester(Model):

    FIELDS = dict(
        begins=dict(types=datetime.datetime),
        ends=dict(types=datetime.datetime),
    )

    ### get_current

    @classmethod
    def get_current(cls):
        """
        Get current semester.

        @return semester: Semester
        @raises ValueError - If current semester is not defined.
        """
        now = datetime.datetime.utcnow()  # TODO: Adjust to timezone of the School, out of scope now.
        for semester in Semester.objects:  # TODO: Use indexed query later.
            if semester.begins <= now <= semester.ends:
                return semester
        raise ValueError('Current semester is not defined')
