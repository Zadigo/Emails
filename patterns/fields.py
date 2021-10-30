class EmailField:
    def __init__(self, values: list, pattern: str = None, structure: str = None, **kwargs):
        self.pattern = pattern
        self.structure = structure
        self.kwargs = kwargs
        self.email = ''.join(values)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.email})"

    def __str__(self):
        return self.email
