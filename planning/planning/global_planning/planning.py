from planning.global_planning.planners.a_star_planner \
	import AStarPlanner
	
from planning.global_planning.planners.ant_colony_planner \
	import AntColonyPlanner
	
	
	
	
	
	
	
class PlanningParameters:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__surface         = None
		self.__planner         = None
		self.__initial_polygon = None
		self.__final_polygon   = None
		self.__smoothing_depth = None
		
		
		
	def copy(self):
		planning_parameters = PlanningParameters()
		
		planning_parameters.__surface         = self.__surface
		planning_parameters.__planner         = self.__planner
		planning_parameters.__initial_polygon = self.__initial_polygon
		planning_parameters.__final_polygon   = self.__final_polygon
		planning_parameters.__smoothing_depth = self.__smoothing_depth
		
		
		return planning_parameters
		
		
		
	def __eq__(self, planning_parameters):
		return True #!!!!!
		
		
	def __ne__(self, planning_parameters):
		return not self.__eq__(planning_parameters)
		
		
		
	@property
	def is_correct(self):
		is_correct = True
		
		
		is_correct &= self.__surface is not None
		is_correct &= self.__planner is not None
		is_correct &= self.__initial_polygon is not None
		is_correct &= self.__final_polygon is not None
		is_correct &= self.__smoothing_depth is not None
		
		if is_correct:
			is_correct &= self.__smoothing_depth > 0
			
			is_correct &= \
				self.__surface.contains_polygon(
					self.__initial_polygon
				)
				
			is_correct &= \
				self.__surface.contains_polygon(
					self.__final_polygon
				)
				
				
		return is_correct
		
		
		
	@property
	def surface(self):
		return self.__surface
		
		
	@surface.setter
	def surface(self, surface):
		self.__surface = surface
		
		
		
	@property
	def planner(self):
		return self.__planner
		
		
	@planner.setter
	def planner(self, planner):
		self.__planner = planner
		
		
		
	@property
	def initial_polygon(self):
		return self.__initial_polygon
		
		
	@initial_polygon.setter
	def initial_polygon(self, initial_polygon):
		self.__initial_polygon = initial_polygon
		
		
		
	@property
	def final_polygon(self):
		return self.__final_polygon
		
		
	@final_polygon.setter
	def final_polygon(self, final_polygon):
		self.__final_polygon = final_polygon
		
		
		
	@property
	def smoothing_depth(self):
		return self.__smoothing_depth
		
		
	@smoothing_depth.setter
	def smoothing_depth(self, smoothing_depth):
		self.__smoothing_depth = smoothing_depth
		
		
		
		
		
		
		
def plan(planning_parameters):
	if planning_parameters.planner == "a-star-planner":
		planner = AStarPlanner(planning_parameters)
		result  = planner.plan_controls_sequence()
		
	elif planning_parameters.planner == "ant-colony-planner":
		planner = AntColonyPlanner(planning_parameters)
		result  = planner.plan()
		
		
	return result
	