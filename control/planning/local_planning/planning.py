class Control(State):
	def __init__(self, planning_parameters, ugv_state, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__planning_parameters = planning_parameters
		self.__ugv_state           = ugv_state
		
		
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters
		
		
		
	@property
	def ugv_state(self):
		return self.__ugv_state
		
		
		
		
		
	@property
	def is_goal(self):
		is_goal = \
			planning_parameters.goal_range.match_ugv_state(
				self.__ugv_state
			)
			
		return is_goal
		
		
		
	def get_successor(self, ugv_action):
		ugv_state_tolerance = \
			UGVStateTolerance(
				position_tolerance    = 0.0,
				orientation_tolerance = 0.0,
				speed_tolerance       = 0.0
			)
			
		are_states_equals = \
			ugv_state_tolerance.match_ugv_states(
				self.__ugv_state,
				ugv_action.ugv_departure_state
			)
			
			
		if are_states_equals:
			successor = ugv_action.ugv_destination_state
		else:
			raise Exception() #!!!!!
			
			
		return successor
		
		
		
	def get_successors(self):
		pass #!!!!!
		
		
		
		
		
		
		
class Execution(Shift):
	def __init__(self,
					planning_parameters,
					ugv_departure_state,
					ugv_destination_state,
					*args,
					**kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить состояния: должны лежать на одном полигоне
		
		self.__planning_parameterse  = planning_parameterse
		self.__ugv_departure_state   = ugv_departure_state
		self.__ugv_destination_state = ugv_destination_state
		
		
		
	@property
	def planning_parameterse(self):
		return self.__planning_parameterse
		
		
	@property
	def ugv_departure_state(self):
		return self.__ugv_departure_state
		
		
	@property
	def ugv_destination_state(self):
		return self.__ugv_destination_state
		
		
		
	@property
	def cost(self):
		return 1.0 #!!!!! Провести эксперимент
		
		
		
		
		
		
		
class PlanningParameters:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__surface           = None
		self.__goal_range        = None
		# self.__control_step      = None
		self.__control_tolerance = None
		
		
		
	def copy(self):
		pass #!!!!!
		
		
		
		
		
	@property
	def surface(self):
		return self.__surface
		
		
	@surface.setter
	def surface(self, surface):
		self.__surface = surface
		
		
		
	@property
	def goal_range(self):
		return self.__goal_range
		
		
	@goal_range.setter
	def goal_range(self, goal_range):
		self.__goal_range = goal_range
		
		
		
	# @property
	# def control_step(self):
	# 	return self.__control_step
		
		
	# @control_step.setter
	# def control_step(self, control_step):
	# 	self.__control_step = control_step
		
		
		
	@property
	def control_tolerance(self):
		return self.__control_tolerance
		
		
	@control_tolerance.setter
	def control_tolerance(self, control_tolerance):
		self.__control_tolerance = control_tolerance
		
		
		
		
		
	@property
	def is_correct(self):
		return True #!!!!! Заглушка
		
		
		
		
		
		
		
class Planner:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!!
		
		
		
	def get_control_sequence(self, ugv):
		return [] #!!!!! Поиск
		