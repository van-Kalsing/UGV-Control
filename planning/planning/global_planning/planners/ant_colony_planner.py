from planning.global_planning.smoothing   import Smoother			
from planning.global_planning.state_space import State







class AntColonyPlanner:
	def __init__(self, planning_parameters, *args, **kwargs):
		if not planning_parameters.is_correct:
			raise Exception() #!!!!!
			
			
		super().__init__(*args, **kwargs)
		
		self.__planning_parameters = planning_parameters.copy()
		
		
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
		
		
	def plan(self):
		return [], 0.0
		