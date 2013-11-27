from utilities.search.searchers.uniform_cost_searcher \
	import UniformCostSearcher
	
from utilities.search.searchers.breadth_first_searcher \
	import BreadthFirstSearcher
	
from utilities.search.searchers.a_star_searcher \
	import AStarSearcher
	
from utilities.search.searchers.greedy_searcher \
	import GreedySearcher
	
from utilities.search.searchers.very_greedy_searcher \
	import VeryGreedySearcher
	
from utilities.search.searchers.a_star_greedy_searcher \
	import AStarGreedySearcher
	
# from utilities.search.searchers.greedy_a_star_searcher \
# 	import GreedyAStarSearcher
	
# from utilities.search.searchers.local_a_star_searcher \
# 	import LocalAStarSearcher
	
from surface.polygon \
	import Point, \
				match_polygons, \
				compute_coordinates_distance
				
from utilities.search.state_space import State, Shift







class Execution(Shift):
	def __init__(self,
					planning_parameters,
					departure_polygon,
					destination_polygon,
					cost,
					*args,
					**kwargs):
		super().__init__(*args, **kwargs)
		
		
		if not planning_parameters.is_correct:
			raise Exception() #!!!!!
			
		#!!!!! Проверить полигоны: должны присутствовать на поверхности и быть
		#!!!!!     смежными
		
		
		self.__planning_parameters = planning_parameters.copy()
		self.__departure_polygon   = departure_polygon
		self.__destination_polygon = destination_polygon
		self.__cost                = cost
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
	@property
	def departure_polygon(self):
		return self.__departure_polygon
		
		
	@property
	def destination_polygon(self):
		return self.__destination_polygon
		
		
	@property
	def cost(self):
		return self.__cost
		
		
		
		
		
class Control(State):
	def __init__(self, planning_parameters, polygon, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		if not planning_parameters.is_correct:
			raise Exception() #!!!!!
			
		try:
			surface_polygon = \
				planning_parameters.surface \
					.get_existing_polygon(
						polygon
					)
		except:
			raise Exception() #!!!!!
			
			
		self.__planning_parameters = planning_parameters.copy()
		self.__polygon             = polygon
		self.__surface_polygon     = surface_polygon
		
		
		
	def __hash__(self):
		hash = round(self.__surface_polygon.center_module)
		
		return hash
		
		
	def __eq__(self, control):
		are_polygons_equivalent = \
			match_polygons(
				control.polygon,
				self.__surface_polygon,
				self.__planning_parameters.surface.equivalence_distance
			)
			
		return are_polygons_equivalent
		
		
	def __ne__(self, control):
		return not self.__eq__(control)
		
		
		
	@property
	def polygon(self):
		return self.__polygon
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
	@property
	def is_goal(self):
		is_final_polygon = \
			match_polygons(
				self.__polygon,
				self.__planning_parameters.final_polygon,
				self.__planning_parameters.surface.equivalence_distance
			)
			
		return is_final_polygon
		
		
	@property
	def cost_estimation(self):
		surface         = self.__planning_parameters.surface
		current_polygon = self.__polygon
		final_polygon   = self.__planning_parameters.final_polygon
		
		vertices_number        = current_polygon.vertices_number
		current_polygon_center = current_polygon.center
		final_polygon_center   = final_polygon.center
		
		
		def compute_rest_path_cost(base_vertex_index):
			if base_vertex_index == 0:
				first_vertex_index  = vertices_number - 1
				second_vertex_index = 0
			else:
				first_vertex_index  = base_vertex_index - 1
				second_vertex_index = base_vertex_index
				
				
			edge_center_point = \
				Point(
					current_polygon,
					[(first_vertex_index, 0.5), (second_vertex_index, 0.5)]
				)
				
			edge_center = edge_center_point.coordinates
			
			
			current_polygon_path_length = \
				compute_coordinates_distance(
					edge_center,
					current_polygon_center
				)
				
			current_polygon_path_cost = \
				current_polygon.impassability \
					* current_polygon_path_length
					
					
			rest_path_length = \
				compute_coordinates_distance(
					edge_center,
					final_polygon_center
				)
				
			rest_path_cost = \
				surface.minimal_impassability \
					* rest_path_length
					
					
			return current_polygon_path_cost + rest_path_cost
			
			
		cost_estimation = \
			min(
				(compute_rest_path_cost(base_vertex_index) \
					for base_vertex_index \
					in  range(vertices_number))
			)
			
		return cost_estimation
		
		
		
	def get_successor(self, execution):
		is_departure_polygon = \
			match_polygons(
				execution.departure_polygon,
				self.__polygon,
				self.__planning_parameters.surface.equivalence_distance
			)
			
		if not is_departure_polygon:
			raise Exception() #!!!!!
			
			
		successor = \
			Control(
				self.__planning_parameters,
				execution.destination_polygon
			)
			
		return successor
		
		
	def get_successors(self):
		successors = []
		
		
		surface   = self.__planning_parameters.surface
		relations = surface.get_relations(self.__polygon)
		
		for relation_key in relations:
			def compute_polygon_path_cost(polygon, vertices_indexes):
				edge_center_point = \
					Point(
						self.__polygon,
						[(vertices_indexes[0], 0.5), (vertices_indexes[1], 0.5)]
					)
					
				edge_center    = edge_center_point.coordinates
				polygon_center = polygon.center
				
				
				polygon_path_length = \
					compute_coordinates_distance(
						edge_center,
						polygon_center
					)
					
				polygon_path_cost = polygon.impassability * polygon_path_length
				
				
				return polygon_path_cost
				
				
			adjacent_edge             = relations[relation_key]
			adjacent_polygon          = adjacent_edge.polygon
			adjacent_vertices_indexes = \
				adjacent_edge.first_vertex_index, \
					adjacent_edge.second_vertex_index
					
			cost  = compute_polygon_path_cost(self.__polygon, relation_key)
			cost += \
				compute_polygon_path_cost(
					adjacent_polygon,
					adjacent_vertices_indexes
				)
				
				
			execution = \
				Execution(
					self.__planning_parameters,
					self.__polygon,
					adjacent_polygon,
					cost
				)
				
			control = \
				Control(
					self.__planning_parameters,
					adjacent_polygon
				)
				
			successors.append(
				(execution, control)
			)
			
			
		return successors
		
		
	def get_predecessors(self):
		return self.get_successors()
		
		
		
		
		
class PlanningParameters:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__surface         = None
		self.__initial_polygon = None
		self.__final_polygon   = None
		
		
		
	def copy(self):
		planning_parameters = PlanningParameters()
		
		planning_parameters.__surface         = self.__surface
		planning_parameters.__initial_polygon = self.__initial_polygon
		planning_parameters.__final_polygon   = self.__final_polygon
		
		
		return planning_parameters
		
		
		
	@property
	def is_correct(self):
		is_correct = True
		
		
		is_correct &= self.__surface is not None
		is_correct &= self.__initial_polygon is not None
		is_correct &= self.__final_polygon is not None
		
		if is_correct:
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
		return self.__surface #.copy()
		
		
	@surface.setter
	def surface(self, surface):
		self.__surface = surface #.copy()
		
		
		
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
		
		
		
		
		
class Planner:
	def __init__(self, planning_parameters, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		if not planning_parameters.is_correct:
			raise Exception() #!!!!!
			
			
		self.__planning_parameters = planning_parameters.copy()
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
	def plan_controls_sequence(self):
		#searcher = BreadthFirstSearcher()
		#searcher = UniformCostSearcher()
		searcher = AStarSearcher()
		# searcher = GreedySearcher()
		#searcher = AStarGreedySearcher()
		#searcher = VeryGreedySearcher()
		#searcher = GreedyAStarSearcher()
		# searcher = LocalAStarSearcher()
		
		initial_state = \
			Control(
				self.__planning_parameters,
				self.__planning_parameters.initial_polygon
			)
			
		#!!!!! Должен возвращать не генератор, а окончательный маршрут.
		#!!!!!     Сделано так временно, потому что нет локальноого планирования
		for controls_sequence in searcher.find(initial_state):
			if controls_sequence is not None:
				polygon_sequence      = []
				polygon_sequence_cost = 0.0
				
				controls_sequence, controls_sequence_cost = controls_sequence
				polygon_sequence_cost = controls_sequence_cost
				for control in controls_sequence:
					# if execution is not None:
					# 	polygon_sequence_cost += execution.cost
						
					polygon_sequence.append(control.polygon)
					
				print("Число узлов:           %s" % searcher.a)
				#print("Число тупиков:         %s" % searcher.t)
				#print("Число смен пути:       %s" % searcher.b)
				print("Цена пути:             %s" % polygon_sequence_cost)
				
				yield polygon_sequence #!!!!! Временно добавлено
			else:
				polygon_sequence = None
				break #!!!!! Временно добавлено
				
				
		# return controls_sequence
		