import sqlalchemy.types as types


class LowerCaseText(types.TypeDecorator):
    '''Converts strings to lower case on the way in.'''

    impl = types.Text

    def process_bind_param(self, value, dialect):
        return value.lower()