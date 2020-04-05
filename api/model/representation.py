class PrettyPrint:
    def __repr__(self):
        values = ', '.join([f'{key}: \"{value}\"' for key, value in self.__dict__.items()])
        return f'<{self.__class__.__name__}>[{values}]'


class EnvPrint:
    def __repr__(self):
        return ' '.join([f'{self.__class__.__name__.upper()}_{name.upper()}: {value}'
                         for name, value in self.__dict__.items()])
