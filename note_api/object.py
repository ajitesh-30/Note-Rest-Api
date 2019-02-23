class Notes(object):
	def __init__(self,**kwargs):
		for field in ('id','name','description','creater'):
			setattr(self,field,kwargs.get(field,None))
