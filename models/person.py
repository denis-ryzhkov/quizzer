
### import

from quizzer.models.model import Model, MAX_LEN

### Person

class Person(Model):
    """
    Abstract person to inherit from.
    """

    FIELDS = dict(
        first_name=dict(types=unicode, length=(1, MAX_LEN)),
        last_name=dict(types=unicode, length=(1, MAX_LEN)),
    )
