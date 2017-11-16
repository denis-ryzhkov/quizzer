
### const shortcuts

MAX_LEN = 200                           # Default maximal length of simple fields like "name".
NO_DEFAULT = object()                   # Special unique value for FIELDS-default to indicate there is no default value.

### Model

class MetaModel(type):
    """
    Metaclass of Model, see its docstring.
    """
    def __new__(metacls, cls_name, cls_bases, cls_dict):
        cls_dict['objects'] = set()
        return super(MetaModel, metacls).__new__(metacls, cls_name, cls_bases, cls_dict)

class Model(object):
    """
    Abstract base model.

    We are not required to use any database or other storage yet,
    so let's start with python-level data structure and validation.

    Each model class has a separate "objects" set
    until a shared persistent storage is selected.

    Define FIELDS in a subclass of Model:
        class Grandparent(Model):
            FIELDS = dict(field_name=dict(
                types=object,           # One type, or tuple(types).
                null=False,             # If True, then None is expected and not validated by "length", etc.
                length=None,            # Length required: None or tuple(min, max), each is None or int.
                default=NO_DEFAULT,     # NO_DEFAULT, default value, or function to create default value.
                validate=None,          # Custom validation: None or function(field_value) raising TypeError, if any.
            ))

    FIELDS are inherited naturally:
        class Parent(Grandparent):
            pass

    If you need to modify inherited FIELDS:
        class Kid(Parent):
            FIELDS = Parent.FIELDS.copy()
            FIELDS.update(Mixin.FIELDS)
            FIELDS.update(
                one_more_field=dict(...),
            )
            del FIELDS['deprecated_field']
    """

    __metaclass__ = MetaModel

    ### init

    def __init__(self, **fields):
        """
        Init the model:
        validate "fields" against "FIELDS",
        populate "self" with "fields" and defaults.

        @param fields: dict - Names and values of the fields to init.
        @raises NotImplementedError(reason: str)
        @raises TypeError(reason: str)
        """
        if not hasattr(self, 'FIELDS'):
            raise NotImplementedError('Define FIELDS')

        for field_name, field_value in fields.iteritems():
            setattr(self, field_name, field_value)
            # Validation when field is created or updated - is done in "__setattr__".

        ### default

        for field_name in set(self.FIELDS) - set(fields):
            default = self.FIELDS[field_name].get('default', NO_DEFAULT)

            if default is NO_DEFAULT:
                raise TypeError('"{}" requires field "{}"'.format(self.__class__.__name__, field_name))

            if callable(default):
                default = default()

            setattr(self, field_name, default)

    ### setattr

    def __setattr__(self, field_name, field_value):
        """
        Validate public field against "FIELDS" before updating "self".

        @param field_name: str
        @param field_value: object
        @raises TypeError(reason: str)
        """
        if not field_name.startswith('_'):
            self.validate(field_name, field_value)

        super(Model, self).__setattr__(field_name, field_value)

    ### delattr

    def __delattr__(self, field_name):
        """
        Fields defined in model should always exist - with explicit or default values.

        @param field_name: str
        @raises TypeError(reason: str)
        """
        if field_name in self.FIELDS:
            raise TypeError('Field "{}" defined in "{}" should always exist'.format(field_name, self.__class__.__name__))

        super(Model, self).__delattr__(field_name)

    ### validate

    @classmethod
    def validate(cls, field_name, field_value):
        """
        Validate field against "FIELDS".

        @param field_name: str
        @param field_value: object
        @raises TypeError(reason: str)
        """
        field_format = cls.FIELDS.get(field_name)
        if field_format is None:
            raise TypeError('"{}" does not have "{}"'.format(cls.__name__, field_name))

        for validate in cls.validate_types, cls.validate_length, cls.validate_custom:
            validate(field_format, field_name, field_value)

    @classmethod
    def validate_types(cls, field_format, field_name, field_value):
        """
        Validate types of field against "field_format".
        Can also be called from custom "validate" for container types.

        @param field_format: dict
        @param field_name: str
        @param field_value: object
        @raises TypeError(reason: str)
        """
        required_types = field_format.get('types', object)
        nullable = field_format.get('null', False)

        if (
            not isinstance(field_value, required_types)
            and not (nullable and field_value is None)
        ):
            raise TypeError('"{}" requires type of field "{}" to be {}{}, not {}'.format(
                cls.__name__, field_name, required_types,
                ' or None' if nullable else '',
                type(field_value)
            ))

    @classmethod
    def validate_length(cls, field_format, field_name, field_value):
        """
        Validate length of field against "field_format".
        Can also be called from custom "validate" for container types.

        @param field_format: dict
        @param field_name: str
        @param field_value: object
        @raises TypeError(reason: str)
        """
        required_length = field_format.get('length')
        nullable = field_format.get('null', False)

        if required_length is not None and not (nullable and field_value is None):
            min_length, max_length = required_length
            field_length = len(field_value)

            if min_length is not None and field_length < min_length:
                raise TypeError('"{}" requires length of field "{}" to be {} or more, not {}'.format(
                    cls.__name__, field_name, min_length, field_length
                ))

            if max_length is not None and field_length > max_length:
                raise TypeError('"{}" requires length of field "{}" to be {} or less, not {}'.format(
                    cls.__name__, field_name, max_length, field_length
                ))

    @classmethod
    def validate_custom(cls, field_format, field_name, field_value):
        """
        Custom validation of field against "field_format".

        @param field_format: dict
        @param field_name: str
        @param field_value: object
        @raises TypeError(reason: str)
        """
        validate = field_format.get('validate')
        if validate:
            validate(field_value)
