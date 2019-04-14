class Term:
    """ A structure to maintain a vlue and its stem """

    value = ""
    stem = "" 

    def __repr__(self):
        return str({'value': self.value, 'stem': self.stem})