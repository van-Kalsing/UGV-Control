from numpy                 import array
from numpy.linalg          import norm
from surface.polygon       import Edge, match_polygons
from utilities.memoization import memoization







class State:
	def __init__(self, polygon, planning_parameters, *args, **kwargs):
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
			
		planning_parameters = planning_parameters.copy()
		surface             = planning_parameters.surface
		
		
		self.__planning_parameters = planning_parameters
		self.__polygon             = polygon
		self.__surface             = surface
		self.__surface_polygon     = surface_polygon
		
		self.__hash               = memoization(self.__hash)
		self.__estimation         = memoization(self.__estimation)
		self.__get_successors_map = memoization(self.__get_successors_map)
		
		
		
		
		
	def __hash(self):
		#!!!!! Потом убрать array
		polygon_center_norm = norm(array(self.__surface_polygon.center))
		hash                = int(polygon_center_norm)
		
		return hash
		
		
		
	def __hash__(self):
		return self.__hash()
		
		
		
	def __eq__(self, state):
		if state.__planning_parameters == self.__planning_parameters:
			are_polygons_equivalent = \
				match_polygons(
					state.__surface_polygon,
					self.__surface_polygon,
					self.__surface.equivalence_distance
				)
		else:
			are_polygons_equivalent = False
			
		return are_polygons_equivalent
		
		
		
	def __ne__(self, state):
		return not self.__eq__(state)
		
		
		
		
		
	@property
	def polygon(self):
		return self.__polygon
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
		
		
	def __get_successors_map(self):
		successors_map = dict()
		
		
		polygon_relations = \
			self.__surface.get_relations(
				self.__polygon
			)
			
		for vertices_indexes in polygon_relations:
			polygon_edge = \
				Edge(
					self.__polygon,
					first_vertex_index  = vertices_indexes[0],
					second_vertex_index = vertices_indexes[1]
				)
				
			adjacent_polygon_edge = polygon_relations[vertices_indexes]
			adjacent_polygon      = adjacent_polygon_edge.polygon
			
			
			successor = \
				State(
					adjacent_polygon,
					self.__planning_parameters
				)
				
			successors_map[successor] = polygon_edge
			
			
		return successors_map
		
		
		
	@property
	def successors(self):
		yield from self.__get_successors_map()
		
		
		
	def get_connecting_edge(self, successor):
		successors_map  = self.__get_successors_map()
		connecting_edge = successors_map.get(successor)
		
		if connecting_edge is None:
			raise Exception() #!!!!!
			
			
		return connecting_edge
		
		
		
		
		
	def __estimation(self):
		final_state = \
			State(
				self.__planning_parameters.final_polygon,
				self.__planning_parameters
			)
			
		#!!!!! Потом убрать array
		polygon_center       = array(self.__surface_polygon.center)
		final_polygon_center = array(final_state.__surface_polygon.center)
		
		
		optimistic_impossibility = self.__surface.minimal_impossibility
		optimistic_distance      = \
			norm(
				final_polygon_center \
					- polygon_center
			)
			
		estimation = optimistic_impossibility * optimistic_distance
		
		
		return estimation
		
		
		
	@property
	def estimation(self):
		return self.__estimation()
		
		
		
		
		
		
		
def compute_sequence_cost(states_sequence, planning_parameters):
	def get_interjacent_point_computer(edge):
		#!!!!! Потом убрать array
		first_point  = array(edge.first_vertex.coordinates)
		second_point = array(edge.second_vertex.coordinates)
		
		def compute_interjacent_point(ratio):
			interjacent_point = \
				ratio * first_point \
					+ (1.0 - ratio) * second_point
					
			return interjacent_point
			
			
		return compute_interjacent_point
		
		
	def compute_elementary_cost(impossibility, first_point, second_point):
		points_distance = \
			norm(
				first_point \
					- second_point
			)
			
			
		return impossibility * points_distance
		
		
		
	def get_base_cost_computer(polygon, edge):
		compute_interjacent_point = \
			get_interjacent_point_computer(
				edge
			)
			
		#!!!!! Потом убрать array
		polygon_center = array(polygon.center)
		
		
		def compute_base_cost(ratio):
			point = compute_interjacent_point(ratio)
			
			base_cost = \
				compute_elementary_cost(
					polygon.impossibility,
					polygon_center,
					point
				)
				
			return base_cost
			
			
		return compute_base_cost
		
		
	def get_transition_cost_computer(polygon, first_edge, second_edge):
		compute_first_interjacent_point = \
			get_interjacent_point_computer(
				first_edge
			)
			
		compute_second_interjacent_point = \
			get_interjacent_point_computer(
				second_edge
			)
			
			
		def compute_transition_cost(first_ratio, second_ratio):
			first_point  = compute_first_interjacent_point(first_ratio)
			second_point = compute_second_interjacent_point(second_ratio)
			
			transition_cost = \
				compute_elementary_cost(
					polygon.impossibility,
					first_point,
					second_point
				)
				
			return transition_cost
			
			
		return compute_transition_cost
		
		
		
	elementary_cost_computers = list()
	
	def compute_sequence_cost(ratios):
		sequence_cost = \
			sum(
				[compute_elementary_cost(ratio) \
					for compute_elementary_cost, ratio \
					in  zip(elementary_cost_computers, ratios)]
			)
			
		return sequence_cost
		
		
	try:
		states_sequence        = list(states_sequence)
		states_sequence_length = len(states_sequence)
		
		for state_index in range(states_sequence_length):
			current_state = states_sequence[state_index]
			
			
			if state_index == 0:
				next_state = states_sequence[state_index + 1]
				
				connecting_edge = \
					current_state.get_connecting_edge(
						next_state
					)
					
					
				cost_computer = \
					get_base_cost_computer(
						current_state.polygon,
						connecting_edge
					)
					
			elif state_index == states_sequence_length - 1:
				previous_state = states_sequence[state_index - 1]
				
				connecting_edge = \
					current_state.get_connecting_edge(
						previous_state
					)
					
					
				cost_computer = \
					get_base_cost_computer(
						current_state.polygon,
						connecting_edge
					)
					
			else:
				previous_state = states_sequence[state_index - 1]
				next_state     = states_sequence[state_index + 1]
				
				first_connecting_edge = \
					current_state.get_connecting_edge(
						previous_state
					)
					
				second_connecting_edge = \
					current_state.get_connecting_edge(
						next_state
					)
					
					
				cost_computer = \
					get_transition_cost_computer(
						current_state.polygon,
						first_connecting_edge,
						second_connecting_edge
					)
					
					
			elementary_cost_computers.append(cost_computer)
	except:
		raise Exception() #!!!!!
		
		
		
	ratios = [0.5] * len(elementary_cost_computers)
	
	#!!!!! Оптимизация коэффициентов. Параметры оптимизации такие как
	#!!!!! погрешность, количество итерации и пр. должны быть размещены в
	#!!!!! planning_parameters
	
	
	
	sequence_cost = compute_sequence_cost(ratios)
	
	return sequence_cost
	