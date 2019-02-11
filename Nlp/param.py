class Parameter:
    """A Parameter is the identifier of an Entity inside a Intent, usually, a parameter is linked to a Entity in a phrase of the intent"""

    def __init__(self):
        self.name= "" #unique name in a Phrase or Intent, normally auto-generated
        self.sharedName = "" #sharedName used to link parameter name between phrases in the same intent
                            #if a new sharedName in a phrase has a correlated name in a Intent, the phrase parameter is linked to the parameter in the Intent
                            #if a new sharedName in a phrase has not correlated name in a intent, the phrase parameter name is added as a new parameter in the intent
        self.visibleName = "" #visible name for UI purpose
        self.type = None
        self.actualValue = None
        self.resolvedValue = None