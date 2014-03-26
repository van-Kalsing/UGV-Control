from collections     import deque
from numpy           import array
from numpy.linalg    import norm
from surface.polygon import Point







class Smoother:
	def __init__(self, surface, smoothing_depth, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		if smoothing_depth < 1:
			raise Exception() #!!!!!
			
			
		self.__surface         = surface
		self.__smoothing_depth = smoothing_depth
		
		self.__last_surface_polygon         = None
		self.__is_ratios_sequence_minimized = True
		
		self.__polygons_sequence         = deque()
		self.__transfers_sequence        = deque()
		self.__elementary_cost_computers = deque()
		self.__ratios_sequence           = deque()
		
		
		
	def copy(self):
		smoother = Smoother(self.__surface, self.__smoothing_depth)
		
		
		last_surface_polygon         = self.__last_surface_polygon
		is_ratios_sequence_minimized = self.__is_ratios_sequence_minimized
		polygons_sequence            = deque(self.__polygons_sequence)
		transfers_sequence           = deque(self.__transfers_sequence)
		elementary_cost_computers    = deque(self.__elementary_cost_computers)
		ratios_sequence              = deque(self.__ratios_sequence)
		
		smoother.__last_surface_polygon         = last_surface_polygon
		smoother.__is_ratios_sequence_minimized = is_ratios_sequence_minimized
		smoother.__polygons_sequence            = polygons_sequence
		smoother.__transfers_sequence           = transfers_sequence
		smoother.__elementary_cost_computers    = elementary_cost_computers
		smoother.__ratios_sequence              = ratios_sequence
		
		
		return smoother
		
		
		
		
		
	@property
	def surface(self):
		return self.__surface
		
		
		
	@property
	def smoothing_depth(self):
		return self.__smoothing_depth
		
		
		
		
		
	@staticmethod
	def __get_interjacent_point_computer(edge):
		#!!!!! Потом убрать array
		first_point  = array(edge.first_vertex.coordinates)
		second_point = array(edge.second_vertex.coordinates)
		
		def compute_interjacent_point(ratio):
			interjacent_point = \
				ratio * first_point \
					+ (1.0 - ratio) * second_point
					
			return interjacent_point
			
			
		return compute_interjacent_point
		
		
	@staticmethod
	def __compute_elementary_cost(impossibility, first_point, second_point):
		points_distance = \
			norm(
				first_point \
					- second_point
			)
			
			
		return impossibility * points_distance
		
		
		
	@staticmethod
	def __get_base_cost_computer(polygon, edge):
		compute_interjacent_point = \
			Smoother.__get_interjacent_point_computer(
				edge
			)
			
		#!!!!! Потом убрать array
		polygon_center = array(polygon.center)
		
		
		def compute_base_cost(ratio):
			point = compute_interjacent_point(ratio)
			
			base_cost = \
				Smoother.__compute_elementary_cost(
					polygon.impossibility,
					polygon_center,
					point
				)
				
			return base_cost
			
			
		return compute_base_cost
		
		
	@staticmethod
	def __get_transition_cost_computer(polygon, first_edge, second_edge):
		compute_first_interjacent_point = \
			Smoother.__get_interjacent_point_computer(
				first_edge
			)
			
		compute_second_interjacent_point = \
			Smoother.__get_interjacent_point_computer(
				second_edge
			)
			
			
		def compute_transition_cost(first_ratio, second_ratio):
			first_point  = compute_first_interjacent_point(first_ratio)
			second_point = compute_second_interjacent_point(second_ratio)
			
			transition_cost = \
				Smoother.__compute_elementary_cost(
					polygon.impossibility,
					first_point,
					second_point
				)
				
			return transition_cost
			
			
		return compute_transition_cost
		
		
		
	@property
	def transfers_sequence_length(self):
		return len(self.__transfers_sequence)
		
		
		
	def push_transfer(self, transfer):
		first_connecting_edge, second_connecting_edge = transfer
		
		
		if self.__transfers_sequence:
			is_correct_transfer = True #!!!!! Проверить равенство полигонов
		else:
			is_correct_transfer = True
			
		if is_correct_transfer:
			pass #!!!!! Проверить принадлженость поверхности полигона
			
			
		if is_correct_transfer:
			if self.__transfers_sequence:
				last_polygon                    = self.__polygons_sequence[-1]
				_, last_polygon_connecting_edge = self.__transfers_sequence[-1]
				
				self.__elementary_cost_computers[-1] = \
					Smoother.__get_transition_cost_computer(
						last_polygon,
						last_polygon_connecting_edge,
						first_connecting_edge
					)
			else:
				cost_computer = \
					Smoother.__get_base_cost_computer(
						first_connecting_edge.polygon,
						first_connecting_edge
					)
					
				self.__polygons_sequence.append(first_connecting_edge.polygon)
				self.__elementary_cost_computers.append(cost_computer)
				
				
			cost_computer = \
				Smoother.__get_base_cost_computer(
					second_connecting_edge.polygon,
					second_connecting_edge
				)
				
			self.__polygons_sequence.append(second_connecting_edge.polygon)
			self.__transfers_sequence.append(transfer)
			self.__elementary_cost_computers.append(cost_computer)
			self.__ratios_sequence.append(0.5)
			
			
			
			if len(self.__transfers_sequence) > self.__smoothing_depth:
				self.pop_transfer()
				
				
				
			#!!!!! Получить __last_surface_polygon
			self.__is_ratios_sequence_minimized = False
		else:
			raise Exception() #!!!!!
			
			
			
	def pop_transfer(self):
		if self.__transfers_sequence:
			self.__polygons_sequence.popleft()
			self.__transfers_sequence.popleft()
			self.__elementary_cost_computers.popleft()
			self.__ratios_sequence.popleft()
			
			
			if self.__transfers_sequence:
				first_polygon                    = self.__polygons_sequence[0]
				first_polygon_connecting_edge, _ = self.__transfers_sequence[0]
				
				self.__elementary_cost_computers[0] = \
					Smoother.__get_base_cost_computer(
						first_polygon,
						first_polygon_connecting_edge
					)
					
					
				self.__is_ratios_sequence_minimized = False
			else:
				self.__polygons_sequence.clear()
				self.__elementary_cost_computers.clear()
				
				self.__last_surface_polygon         = None
				self.__is_ratios_sequence_minimized = True
		else:
			raise Exception() #!!!!!
			
			
			
			
			
	def __compute_transfers_sequence_cost(self):
		def iterate_ratios():
			def iterate_ratios_indexes():
				ratios_sequence_length = len(self.__ratios_sequence)
				ratios_indexes_pairs   = \
					zip(
						range(ratios_sequence_length - 1),
						range(1, ratios_sequence_length)
					)
					
				yield 0, None
				yield from ratios_indexes_pairs
				yield None, ratios_sequence_length - 1
				
				
			for ratios_indexes in iterate_ratios_indexes():
				first_ratio_index, second_ratio_index = ratios_indexes
				
				if first_ratio_index is None:
					yield self.__ratios_sequence[second_ratio_index],
				if second_ratio_index is None:
					yield self.__ratios_sequence[first_ratio_index],
				else:
					yield \
						self.__ratios_sequence[first_ratio_index], \
							self.__ratios_sequence[second_ratio_index]
							
							
		sequence_cost = \
			sum(
				[compute_elementary_cost(*ratios) \
					for compute_elementary_cost, ratios \
					in  zip(self.__elementary_cost_computers, iterate_ratios())]
			)
			
		return sequence_cost
		
		
		
	def __minimize_ratio(self, ratio_index):
		factor = (3.0 - 5.0 ** 0.5) / 2.0
		
		left_bound, right_bound         = 0.0, 1.0
		left_separator, right_separator = \
			left_bound + factor * (right_bound - left_bound), \
				right_bound - factor * (right_bound - left_bound)
				
				
		ratios        = self.__ratios_sequence
		initial_ratio = ratios[ratio_index]
		
		ratios[ratio_index] = left_separator
		left_cost           = self.__compute_transfers_sequence_cost()
		
		ratios[ratio_index] = right_separator
		right_cost          = self.__compute_transfers_sequence_cost()
		
		
		#!!!!! Точность разместить в planning_parameters
		while right_bound - left_bound > 0.1:
			if left_cost < right_cost:
				right_bound     = right_separator
				right_separator = left_separator
				left_separator  = left_bound + (right_bound - right_separator)
				
				
				ratios[ratio_index] = left_separator
				
				right_cost = left_cost
				left_cost  = self.__compute_transfers_sequence_cost()
			else:
				left_bound      = left_separator
				left_separator  = right_separator
				right_separator = right_bound - (left_separator - left_bound)
				
				
				ratios[ratio_index] = right_separator
				
				left_cost  = right_cost
				right_cost = self.__compute_transfers_sequence_cost()
		else:
			final_ratio         = (right_bound + left_bound) / 2.0
			ratios[ratio_index] = final_ratio
			
			
		return abs(final_ratio - initial_ratio)
		
		
		
	def __minimize_ratios_sequence(self):
		ratios_number     = len(self.__ratios_sequence)
		need_minimization = True
		
		while need_minimization:
			maximal_error = 0.0
			
			for ratio_index in range(ratios_number):
				maximal_error = \
					max(
						self.__minimize_ratio(ratio_index),
						maximal_error
					)
					
			need_minimization = maximal_error > 0.1 #!!!!! Вынести константу
			
			
		self.__is_ratios_sequence_minimized = True
		
		
		
	@property
	def transfers_sequence_cost(self):
		if self.__transfers_sequence:
			if not self.__is_ratios_sequence_minimized:
				self.__minimize_ratios_sequence()
				
			transfers_sequence_cost = self.__compute_transfers_sequence_cost()
		else:
			raise Exception() #!!!!!
			
		return transfers_sequence_cost
		
		
		
	@property
	def transfer_cost(self):
		if self.__transfers_sequence:
			transfer_cost = \
				self.transfers_sequence_cost \
					/ self.transfers_sequence_length
		else:
			raise Exception() #!!!!!
			
		return transfer_cost
		
		
		
	#!!!!! Проверить корректность и согласованность с другим кодом
	@property
	def transfers_points_sequence(self):
		if self.__transfers_sequence:
			if not self.__is_ratios_sequence_minimized:
				self.__minimize_ratios_sequence()
				
				
			transfers_points_sequence = list()
			transfers_sequence        = \
				zip(
					self.__transfers_sequence,
					self.__ratios_sequence
				)
				
			for transfer, ratio in transfers_sequence:
				def get_tranfer_point(connecting_edge):
					polygon       = connecting_edge.polygon
					decomposition = \
						[
							(connecting_edge.first_vertex_index, ratio),
							(connecting_edge.second_vertex_index, 1.0 - ratio)
						]
						
					tranfer_point = Point(polygon, decomposition)
					
					return tranfer_point
					
					
				first_connecting_edge, second_connecting_edge = transfer
				
				transfers_points_sequence.append(
					(get_tranfer_point(first_connecting_edge), \
						get_tranfer_point(second_connecting_edge))
				)
		else:
			raise Exception() #!!!!!
			
			
		return transfers_points_sequence
		