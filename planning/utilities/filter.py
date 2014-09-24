class Filter:
	def __init__(self, key = (lambda element: element), *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__key               = key
		self.__contains_element  = False
		self.__minimal_key_value = None
		self.__minimal_element   = None
		self.__maximal_key_value = None
		self.__maximal_element   = None
		
		
		
		
		
	@property
	def contains_element(self):
		return self.__contains_element
		
		
		
	@property
	def minimal_element(self):
		if not self.__contains_element:
			raise Exception() #!!!!!
			
		return self.__minimal_element
		
		
		
	@property
	def maximal_element(self):
		if not self.__contains_element:
			raise Exception() #!!!!!
			
		return self.__maximal_element
		
		
		
		
		
	def check_element(self, element):
		key_value = self.__key(element)
		
		
		need_update_minimal_element = False
		need_update_maximal_element = False
		
		if not self.__contains_element:
			need_update_minimal_element = True
			need_update_maximal_element = True
		elif key_value < self.__minimal_key_value:
			need_update_minimal_element = True
		elif key_value > self.__maximal_key_value:
			need_update_maximal_element = True
			
			
		if need_update_minimal_element:
			self.__minimal_element   = element
			self.__minimal_key_value = key_value
			
		if need_update_maximal_element:
			self.__maximal_element   = element
			self.__maximal_key_value = key_value
			
			
		self.__contains_element = True
		
		
		
	def check_elements(self, elements):
		for element in elements:
			self.check_element(element)
			