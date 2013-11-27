def memoization(function):
	function_value = None
	is_memorized   = False
	
	def memoization_function(*args, **kwargs):
		if not is_memorized:
			function_value = function(*args, **kwargs)
			is_memorized   = True
			
		return function_value
		
		
	return memoization_function
	