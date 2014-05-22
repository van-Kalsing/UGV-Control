from planning.surface.polygon \
	import Edge, \
				match_coordinates, \
				match_polygons, \
				invert_edge
				
				
				
				
				
				
				
class Surface:
	def __init__(self, equivalence_distance, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		if equivalence_distance < 0.0:
			raise Exception() #!!!!!
			
		self.__equivalence_distance  = equivalence_distance
		self.__polygons_records      = []
		self.__minimal_impossibility = None
		self.__maximal_impossibility = None
		
		
		
		
		
	@property
	def equivalence_distance(self):
		return self.__equivalence_distance
		
		
	@property
	def polygons(self):
		polygons = \
			(polygon_record['polygon'] for polygon_record \
				in self.__polygons_records)
				
		return polygons
		
		
	@property
	def minimal_impossibility(self):
		return self.__minimal_impossibility
		
		
	@property
	def maximal_impossibility(self):
		return self.__maximal_impossibility
		
		
	#!!!!! relations_classes
	# @property
	# def polygons(self):
	# 	return list(self.__polygons_records)
	
	
	
	
	
	def __get_polygon_record(self, polygon, equivalence_distance = None):
		if equivalence_distance is None:
			equivalence_distance = self.__equivalence_distance
			
		polygons_records_number = len(self.__polygons_records)
		
		
		left_index   = 0
		right_index  = polygons_records_number
		center_index = (left_index + right_index) // 2
		
		while left_index != right_index:
			center_polygon_record = self.__polygons_records[center_index]
			center_polygon        = center_polygon_record['polygon']
			
			if polygon.center_module < center_polygon.center_module:
				right_index = center_index
			elif polygon.center_module >= center_polygon.center_module:
				left_index = min(right_index, center_index + 1)
			else:
				break
				
			center_index = (left_index + right_index) // 2
			
			
		def get_polygon_record(polygons_records_indexes):
			contains_equivalent_polygons = False
			
			
			for polygon_record_index in polygons_records_indexes:
				polygon_record = self.__polygons_records[polygon_record_index]
				
				
				centers_modules_difference = \
					abs(
						polygon_record['polygon'].center_module \
							- polygon.center_module
					)
					
				if centers_modules_difference < equivalence_distance:
					contains_equivalent_polygons = \
						match_polygons(
							polygon_record['polygon'],
							polygon,
							equivalence_distance
						)
						
					if contains_equivalent_polygons:
						break
				else:
					break
					
					
			if contains_equivalent_polygons:
				return polygon_record_index, polygon_record
			else:
				return None
				
				
		polygon_record = \
			get_polygon_record(
				range(center_index - 1, -1, -1)
			)
			
		if polygon_record is None:
			polygon_record = \
				get_polygon_record(
					range(center_index, polygons_records_number)
				)
				
		if polygon_record is None:
			polygon_record = center_index, None
			
			
		return polygon_record
		
		
		
		
		
	def add_polygon(self, polygon, map_polygon_index):
		#!!!!! Проверить отдаленность вершин (двойная разрешающая способность)
		
		
		polygon_record_index, polygon_record = \
			self.__get_polygon_record(
				polygon,
				2.0 * self.__equivalence_distance
			)
			
		if polygon_record is None:
			polygon_record = \
				{
					'polygon':           polygon,
					'relations':         {},
					'map_polygon_index': map_polygon_index
				}
				
			self.__polygons_records.insert(polygon_record_index, polygon_record)
			
			
			if self.__minimal_impossibility is None:
				self.__minimal_impossibility = polygon.impossibility
				self.__maximal_impossibility = polygon.impossibility
			else:
				self.__minimal_impossibility = \
					min(
						self.__minimal_impossibility,
						polygon.impossibility
					)
					
				self.__maximal_impossibility = \
					max(
						self.__maximal_impossibility,
						polygon.impossibility
					)
		else:
			raise Exception() #!!!!!
			
			
			
	def get_existing_polygon(self, polygon):
		_, polygon_record = \
			self.__get_polygon_record(
				polygon,
				self.__equivalence_distance
			)
			
		if polygon_record is not None:
			existing_polygon = polygon_record['polygon']
		else:
			raise Exception() #!!!!!
			
			
		return existing_polygon
		
		
		
	def get_map_polygon_index(self, polygon):
		_, polygon_record = \
			self.__get_polygon_record(
				polygon,
				self.__equivalence_distance
			)
			
		if polygon_record is not None:
			map_polygon_index = polygon_record['map_polygon_index']
		else:
			raise Exception() #!!!!!
			
			
		return map_polygon_index
		
		
		
	# def remove_polygon(self, polygon):
	# 	existing_polygon = self.__get_polygon(polygon)
		
	# 	if existing_polygon is not None:
	# 		self.__polygons.remove(existing_polygon)
			
			
	# 		if polygon.impossibility == self.__minimal_impossibility:
	# 			is_impossibility_extreme = True
	# 		elif polygon.impossibility == self.__maximal_impossibility:
	# 			is_impossibility_extreme = True
	# 		else:
	# 			is_impossibility_extreme = False
				
				
	# 		if is_impossibility_extreme:
	# 			if self.__polygons:
	# 				polygons_iterator = iter(self.__polygons)
					
					
	# 				polygon = next(polygons_iterator)
					
	# 				self.__minimal_impossibility = polygon.impossibility
	# 				self.__maximal_impossibility = polygon.impossibility
					
					
	# 				for polygon in polygons_iterator:
	# 					self.__minimal_impossibility = \
	# 						min(
	# 							self.__minimal_impossibility,
	# 							polygon.impossibility
	# 						)
							
	# 					self.__maximal_impossibility = \
	# 						max(
	# 							self.__maximal_impossibility,
	# 							polygon.impossibility
	# 						)
	# 			else:
	# 				self.__minimal_impossibility  = None
	# 				self.__maximal_impossibility  = None
	# 	else:
	# 		raise Exception() #!!!!!
			
			
			
	def contains_polygon(self, polygon):
		polygon_record_index, polygon_record = \
			self.__get_polygon_record(
				polygon
			)
			
		return polygon_record is not None
		
		
		
		
		
		# def match_relations(first_relation, second_relation):
		# 	def match_relations(first_relation, second_relation):
		# 		def match_edges(first_edge, second_edge):
		# 			are_polygons_equivalent = \
		# 				match_polygons(
		# 					first_edge.polygon,
		# 					second_edge.polygon,
		# 					self.__equivalence_distance
		# 				)
						
		# 			if are_polygons_equivalent:
		# 				are_edges_equivalent = \
		# 					first_edge.first_vertex_index \
		# 						== second_edge.first_vertex_index
								
		# 				are_edges_equivalent &= \
		# 					first_edge.second_vertex_index \
		# 						== second_edge.second_vertex_index
		# 			else:
		# 				are_edges_equivalent = False
						
						
		# 			return are_edges_equivalent
					
					
		# 		are_relations_equivalent = \
		# 			match_edges(
		# 				first_relation[0],
		# 				second_relation[0]
		# 			)
					
		# 		are_relations_equivalent &= \
		# 			match_edges(
		# 				first_relation[1],
		# 				second_relation[1]
		# 			)
					
					
		# 		if not are_relations_equivalent:
		# 			are_relations_equivalent = \
		# 				match_edges(
		# 					first_relation[0],
		# 					invert_edge(second_relation[0])
		# 				)
						
		# 			are_relations_equivalent &= \
		# 				match_edges(
		# 					first_relation[1],
		# 					invert_edge(second_relation[1])
		# 				)
						
						
		# 		return are_relations_equivalent
				
				
		# 	are_relations_equivalent = \
		# 		match_relations(
		# 			first_relation,
		# 			second_relation
		# 		)
				
		# 	if not are_relations_equivalent:
		# 		are_relations_equivalent = \
		# 			match_relations(
		# 				first_relation,
		# 				second_relation[::-1]
		# 			)
					
					
		# 	return are_relations_equivalent
			
			
	def __map_edge(self, edge, polygon):
		# Предполагается что edge.polygon эквивалентен polygon с точностью
		# self.__equivalence_distance.
		# В этом случае отображение ребра edge на полигон polygon возможно,
		# иначе возможны следующие необрабатываемые случаи:
		#     1) не все вершины ребра edge могут быть отображены на вершины
		#        полигона polygon;
		#     2) образы вершин ребра edge на полигоне polygon не образуют
		#        на нем ребро
		
		first_vertex_index  = None
		second_vertex_index = None
		
		
		for test_vertex_index in range(polygon.vertices_number):
			test_vertex   = polygon.get_vertex(test_vertex_index)
			first_vertex  = edge.polygon.get_vertex(edge.first_vertex_index)
			second_vertex = edge.polygon.get_vertex(edge.second_vertex_index)
			
			
			are_vertices_equivalent = \
				match_coordinates(
					first_vertex,
					test_vertex,
					self.__equivalence_distance
				)
				
			if are_vertices_equivalent:
				first_vertex_index = test_vertex_index
			else:
				# Возможно отображение вершины ребра edge не более чем на одну
				# вершину полигона polygon. Таким образом при успешном
				# сопостовлении вершины полигона с одной из вершин ребра,
				# сопостовление с другой не требуется
				
				are_vertices_equivalent = \
					match_coordinates(
						second_vertex,
						test_vertex,
						self.__equivalence_distance
					)
					
				if are_vertices_equivalent:
					second_vertex_index = test_vertex_index
					
					
		mapped_edge = \
			Edge(
				polygon,
				first_vertex_index,
				second_vertex_index
			)
			
		return mapped_edge
		
		
		
	def get_relations(self, polygon):
		polygon_record_index, polygon_record = \
			self.__get_polygon_record(
				polygon
			)
			
		if polygon_record is None:
			raise Exception() #!!!!!
			
			
		existing_relations = polygon_record['relations']
		existing_polygon   = polygon_record['polygon']
		relations          = dict()
		relations_keys     = set()
		
		for existing_relation_key in existing_relations:
			if existing_relation_key[::-1] not in relations_keys:
				existing_edge = \
					Edge(
						existing_polygon,
						existing_relation_key[0],
						existing_relation_key[1]
					)
					
				edge = self.__map_edge(existing_edge, polygon)
				
				# relation_key = \
				# 	edge.first_vertex_index, \
				# 		edge.second_vertex_index
						
				# relations[relation_key] = \
				# 	existing_relations[existing_relation_key]
					
				relations[edge] = existing_relations[existing_relation_key]
				
				relations_keys.add(existing_relation_key)
				
				
		return relations
		
		
		
	def set_relation(self, first_edge, second_edge):
		def match_edges(first_edge, second_edge):
			are_polygons_equivalent = \
				match_polygons(
					first_edge.polygon,
					second_edge.polygon,
					self.__equivalence_distance
				)
				
			if are_polygons_equivalent:
				are_edges_equivalent = \
					first_edge.first_vertex_index \
						== second_edge.first_vertex_index
						
				are_edges_equivalent &= \
					first_edge.second_vertex_index \
						== second_edge.second_vertex_index
			else:
				are_edges_equivalent = False
				
				
			return are_edges_equivalent
			
			
			
		first_polygon_record_index, first_polygon_record = \
			self.__get_polygon_record(
				first_edge.polygon
			)
			
		second_polygon_record_index, second_polygon_record = \
			self.__get_polygon_record(
				second_edge.polygon
			)
			
			
		# Поверхность должна содержать полигоны эквивалентные полигонам ребер
		# с точностью до self.__equivalence_distance. В противном случае
		# хотя бы одна запись полигонов не будет найдена
		if (first_polygon_record is None) or (second_polygon_record is None):
			raise Exception() #!!!!!
			
		# Полигоны ребер не дожны быть эквивалентны одному из полигонов
		# поверхности одновременно (нельзя допускать связей полигона с самим
		# собой). В противном случае индексы будут равны
		if first_polygon_record_index == second_polygon_record_index:
			raise Exception() #!!!!!
			
			
		first_polygon      = first_polygon_record['polygon']
		first_edge         = self.__map_edge(first_edge, first_polygon)
		first_relations    = first_polygon_record['relations']
		first_relation_key = \
			first_edge.first_vertex_index, \
				first_edge.second_vertex_index
				
		first_related_edge = first_relations.get(first_relation_key)
		
		
		second_polygon      = second_polygon_record['polygon']
		second_edge         = self.__map_edge(second_edge, second_polygon)
		second_relations    = second_polygon_record['relations']
		second_relation_key = \
			second_edge.first_vertex_index, \
				second_edge.second_vertex_index
				
		second_related_edge = second_relations.get(second_relation_key)
		
		
		if first_related_edge is not None:
			if second_related_edge is not None:
				are_edges_equivalent = \
					match_edges(
						first_related_edge,
						second_related_edge
					)
					
				if not are_edges_equivalent:
					raise Exception() #!!!!!
			else:
				raise Exception() #!!!!!
		else:
			if second_related_edge is not None:
				raise Exception() #!!!!!
			else:
				first_relations[first_relation_key]       = second_edge
				first_relations[first_relation_key[::-1]] = \
					invert_edge(
						second_edge
					)
					
				second_relations[second_relation_key]       = first_edge
				second_relations[second_relation_key[::-1]] = \
					invert_edge(
						first_edge
					)
					
					
					
	# def unset_relations(self, vertex):
	# 	if not vertex.is_vertex:
	# 		raise Exception() #!!!!!
			
			
	# 	relations_class = self.__get_relations_class(vertex)
		
	# 	if relations_class is not None:
	# 		related_vertices_number = len(relations_class)
			
	# 		for related_vertex_index in range(related_vertices_number):
	# 			related_vertex = relations_class[related_vertex_index]
				
	# 			are_points_equivalent = \
	# 				match_points(
	# 					related_vertex,
	# 					vertex,
	# 					self.__equivalence_distance
	# 				)
					
	# 			if are_points_equivalent:
	# 				relations_class.pop(related_vertex_index)
	# 				break
	# 	else:
	# 		raise Exception() #!!!!!
			
			
			
	# def contains_relations(self, vertex):
	# 	if not vertex.is_vertex:
	# 		raise Exception() #!!!!!
			
			
	# 	relations_class = self.__get_relations_class(vertex)
		
	# 	return relations_class is not None
		
		
		
		
		
	# def get_adjacent_points(self, point):
	# 	if not point.is_edge_point:
	# 		raise Exception() #!!!!!
			
	# 	if self.__get_polygon(point.polygon) is None:
	# 		raise Exception() #!!!!!
			
			
	# 	def get_adjacent_vertices(vertex):
	# 		relations_class = self.__get_relations_class(vertex)
			
	# 		if relations_class is not None:
	# 			adjacent_vertices = set()
				
	# 			for related_vertex in relations_class:
	# 				are_vertices_equivalent = \
	# 					match_points(
	# 						related_vertex,
	# 						vertex,
	# 						self.__equivalence_distance
	# 					)
						
	# 				if not are_vertices_equivalent:
	# 					adjacent_vertices.add(related_vertex)
	# 		else:
	# 			adjacent_vertices = set()
				
				
	# 		return adjacent_vertices
			
			
	# 	if point.is_vertex:
	# 		adjacent_points = get_adjacent_vertices(point)
	# 	else:
	# 		first_vertex_index, first_vertex_weight   = point.decomposition[0]
	# 		second_vertex_index, second_vertex_weight = point.decomposition[1]
			
			
	# 		contains_equal_polygons = False
			
	# 		first_adjacent_vertices = \
	# 			get_adjacent_vertices(
	# 				Point(point.polygon, [(first_vertex_index, 1.0)])
	# 			)
				
	# 		second_adjacent_vertices = \
	# 			get_adjacent_vertices(
	# 				Point(point.polygon, [(second_vertex_index, 1.0)])
	# 			)
				
	# 		for first_adjacent_vertex in first_adjacent_vertices:
	# 			for second_adjacent_vertex in second_adjacent_vertices:
	# 				contains_equal_polygons = \
	# 					first_adjacent_vertex.polygon \
	# 						is second_adjacent_vertex.polygon
							
	# 				if contains_equal_polygons:
	# 					break
						
	# 			if contains_equal_polygons:
	# 				break
					
					
	# 		if contains_equal_polygons:
	# 			first_vertex_index, _  = first_adjacent_vertex.decomposition[0]
	# 			second_vertex_index, _ = second_adjacent_vertex.decomposition[0]
					
	# 			polygon       = first_adjacent_vertex.polygon
	# 			decomposition = \
	# 				[(first_vertex_index, first_vertex_weight),
	# 					(second_vertex_index, second_vertex_weight)]
						
	# 			adjacent_points = \
	# 				{
	# 					Point(polygon, decomposition)
	# 				}
	# 		else:
	# 			adjacent_points = set()
				
				
	# 	return adjacent_points
		