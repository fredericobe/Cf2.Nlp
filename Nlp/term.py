from jsonConvert import JsonConvert

@JsonConvert.register
class Term():
    """ A structure to maintain a vlue and its stem """
    def __init__(self):
        self.value = ""
        self.stem = "" 

    def __repr__(self):
        return str({'value': self.value, 'stem': self.stem})