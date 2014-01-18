class UndefinedMethod(Exception):
	def __init__(self, msg=''):
		self.message = msg
	def __str__(self):
		return self.message

class InvalidIndex(Exception):
    def __init__(self, msg=''):
        self.message = msg
    def __str__(self):
        return self.message

class TypeError(Exception):
    def __init__(self, msg=''):
        self.message = msg
    def __str__(self):
        return self.message