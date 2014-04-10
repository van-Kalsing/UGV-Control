from surface.polygon import Point







class UGVState:
	def __init__(self, position, orientation, speed, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить
		
		self.__position    = position
		self.__orientation = orientation #!!!!! Нормировать
		self.__speed       = speed #!!!!! Проверить на знак
		
		
		
	@property
	def position(self):
		return self.__position
		
		
	@property
	def orientation(self):
		return self.__orientation
		
		
	@property
	def speed(self):
		return self.__speed
		
		
		
		
		
		
		
class UGVStateTolerance:
	def __init__(self,
					position_tolerance    = None,
					orientation_tolerance = None,
					speed_tolerance       = None,
					*args,
					**kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить допустимые отклонения
		
		self.__position_tolerance    = position_tolerance
		self.__orientation_tolerance = orientation_tolerance
		self.__speed_tolerance       = speed_tolerance
		
		
		
	@property
	def position_tolerance(self):
		return self.__position_tolerance
		
		
	@property
	def orientation_tolerance(self):
		return self.__orientation_tolerance
		
		
	@property
	def speed_tolerance(self):
		return self.__speed_tolerance
		
		
		
	def match_ugv_states(self, first_ugv_state, second_ugv_state):
		result = True
		
		
		if self.__position_tolerance is not None:
			result &= \
				Point.match_points(
					first_ugv_state.position,
					second_ugv_state.position
				)
				
		#!!!!! Проверить остальные пункты
		
		
		return result
		
		
		
		
		
		
		
class UGVStatesRange:
	def __init__(self, ugv_median_state, ugv_state_tolerance, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить допустимые отклонения
		
		self.__ugv_median_state    = ugv_median_state
		self.__ugv_state_tolerance = ugv_state_tolerance
		
		
		
	@property
	def ugv_median_state(self):
		return self.__ugv_median_state
		
		
	@property
	def ugv_state_tolerance(self):
		return self.__ugv_state_tolerance
		
		
		
	def match_ugv_state(self, ugv_state):
		result = \
			self.__ugv_state_tolerance.match_ugv_states(
				self.__ugv_median_state,
				ugv_state
			)
			
			
		return result
		