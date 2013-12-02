def memoization(function):
	function_value = [None]
	is_memorized   = [False]
	
	def memoization_function(*args, **kwargs):
		if not is_memorized[0]:
			function_value[0] = function(*args, **kwargs)
			is_memorized[0]   = True
			
		return function_value[0]
		
		
	return memoization_function
	