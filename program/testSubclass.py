
class supclass(object):
	def __init__(self,a,b):
		self.a = a	
		self.b = b

class subclass(supclass):
	def __init__(self,a,b):
		super(subclass, self).__init__(a,b)
		self.c = 10
		print "a",self.a



te = subclass(10,10)	
