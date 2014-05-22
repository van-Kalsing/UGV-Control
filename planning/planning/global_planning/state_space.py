from numpy                          import array
from numpy.linalg                   import norm
from planning.surface.polygon       import match_polygons
from planning.utilities.memoization import memoization







class State:
	__states_cache = dict()
	
	
	
	def __new__(cls, polygons_sequence, *args, **kwargs):
		states_cache_key = tuple(polygons_sequence)
		
		if states_cache_key in cls.__states_cache:
			states_cache_value = cls.__states_cache[states_cache_key]
		else:
			states_cache_value = super().__new__(cls)
			states_cache_value.__is_initialized = False
			states_cache_value.a = 0
			
			cls.__states_cache[states_cache_key] = states_cache_value
			
			
		return states_cache_value
		
		
		
		
		
	def __init__(self, polygons_sequence, planning_parameters, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		if not self.__is_initialized:
			#!!!!! 1. Послед-но ли распложены полигоны не проверять - долго
			#!!!!!    считает (указать на это при документировании)
			#!!!!! 2. Проверять число полигонов - оно должно быть равно
			#!!!!!    соответствующему параметру в planning_parameters, также
			#!!!!!    оно может быть меньше его в случае, если первый полигон
			#!!!!!    стартовый
			
			if not planning_parameters.is_correct:
				raise Exception() #!!!!!
				
			try:
				def get_existing_polygon(polygon):
					existing_polygon = \
						planning_parameters.surface \
							.get_existing_polygon(
								polygon
							)
							
					return existing_polygon
					
				surface_polygons_sequence = \
					[get_existing_polygon(polygon) for polygon \
						in polygons_sequence]
			except:
				raise Exception() #!!!!!
				
				
			planning_parameters = planning_parameters.copy()
			polygons_sequence   = list(polygons_sequence)
			surface             = planning_parameters.surface
			
			self.__planning_parameters       = planning_parameters
			self.__polygons_sequence         = polygons_sequence
			self.__surface                   = surface
			self.__surface_polygons_sequence = surface_polygons_sequence
			
			self.__hash               = memoization(self.__hash)
			self.__get_successors_map = memoization(self.__get_successors_map)
			self.__is_initial         = memoization(self.__is_initial)
			self.__is_final           = memoization(self.__is_final)
			self.__estimation         = memoization(self.__estimation)
			
			
			self.__is_initialized = True
			
			
			
			
			
	def __hash(self):
		#!!!!! Потом убрать array
		polygons_centers_total_norm = \
			sum(
				[norm(array(surface_polygon.center)) for surface_polygon \
					in self.__surface_polygons_sequence]
			)
			
		hash = int(polygons_centers_total_norm)
		
		
		return hash
		
		
		
	def __hash__(self):
		return self.__hash()
		
		
		
	def __eq__(self, state):
		if state.__planning_parameters == self.__planning_parameters:
			def iterate_surface_polygons():
				surface_polygons = \
					zip(
						self.__surface_polygons_sequence,
						state.__surface_polygons_sequence
					)
					
				for surface_polygons_pair in surface_polygons:
					yield surface_polygons_pair
					
					
			for surface_polygons_pair in iterate_surface_polygons():
				first_surface_polygon, second_surface_polygon = \
					surface_polygons_pair
					
				are_polygons_equivalent = \
					match_polygons(
						first_surface_polygon,
						second_surface_polygon,
						self.__surface.equivalence_distance
					)
					
				if not are_polygons_equivalent:
					are_states_equivalent = False
					break
			else:
				are_states_equivalent = True
		else:
			are_states_equivalent = False
			
			
		return are_states_equivalent
		
		
		
	def __ne__(self, state):
		return not self.__eq__(state)
		
		
		
		
		
	@property
	def polygons_sequence(self):
		return list(self.__polygons_sequence)
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
		
		
	def __get_successors_map(self):
		successors_map = dict()
		
		
		polygons_sequence_length = len(self.__polygons_sequence)
		smoothing_depth          = self.__planning_parameters.smoothing_depth
		
		if polygons_sequence_length == smoothing_depth:
			successor_polygons_sequence_base = self.__polygons_sequence[1:]
		else:
			successor_polygons_sequence_base = self.__polygons_sequence
			
			
		last_polygon           = self.__polygons_sequence[-1]
		last_polygon_relations = \
			self.__surface.get_relations(
				last_polygon
			)
			
			
		for transfer in last_polygon_relations.items():
			adjacent_polygon_edge = transfer[1]
			adjacent_polygon      = adjacent_polygon_edge.polygon
			
			successor = \
				State(
					successor_polygons_sequence_base \
						+ [adjacent_polygon],
					self.__planning_parameters
				)
				
			successors_map[successor] = transfer
			
			
		return successors_map
		
		
		
	@property
	def successors(self):
		successors_map = self.__get_successors_map()
		
		for successor in successors_map.keys():
			yield successor
			
			
			
	def get_transfer(self, successor):
		successors_map = self.__get_successors_map()
		transfer       = successors_map.get(successor)
		
		if transfer is None:
			raise Exception() #!!!!!
			
			
		return transfer
		
		
		
		
		
	def __is_initial(self):
		last_surface_polygon = self.__surface_polygons_sequence[-1]
		
		is_initial = \
			match_polygons(
				last_surface_polygon,
				self.__planning_parameters.initial_polygon,
				self.__surface.equivalence_distance
			)
			
		return is_initial
		
		
		
	@property
	def is_initial(self):
		return self.__is_initial()
		
		
		
	def __is_final(self):
		last_surface_polygon = self.__surface_polygons_sequence[-1]
		
		is_final = \
			match_polygons(
				last_surface_polygon,
				self.__planning_parameters.final_polygon,
				self.__surface.equivalence_distance
			)
			
		return is_final
		
		
		
	@property
	def is_final(self):
		return self.__is_final()
		
		
		
		
		
	def __estimation(self):
		final_surface_polygon = \
			self.__planning_parameters.surface \
				.get_existing_polygon(
					self.__planning_parameters.final_polygon
				)
				
		last_surface_polygon = self.__surface_polygons_sequence[-1]
		
		
		#!!!!! Потом убрать array
		last_polygon_center  = array(last_surface_polygon.center)
		final_polygon_center = array(final_surface_polygon.center)
		
		
		optimistic_impossibility = self.__surface.minimal_impossibility
		optimistic_distance      = \
			norm(
				final_polygon_center \
					- last_polygon_center
			)
			
		estimation = optimistic_impossibility * optimistic_distance
		
		
		return estimation
		
		
		
	@property
	def estimation(self):
		return self.__estimation()
		