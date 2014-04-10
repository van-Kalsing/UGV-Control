def compute_coordinates_distance(first_coordinates, second_coordinates):
	square_distance = 0.0
	
	for coordinates in zip(first_coordinates, second_coordinates):
		first_coordinate, second_coordinate = coordinates
		
		square_distance += \
			(first_coordinate - second_coordinate) \
				** 2.0
				
	distance = square_distance ** 0.5
	
	return distance
	
	
	
def compute_points_distance(first_point, second_point):
	distance = \
		compute_coordinates_distance(
			first_point.coordinates,
			second_point.coordinates
		)
		
	return distance
	
	
	
	
	
def match_coordinates(first_coordinates,
						second_coordinates,
						equivalence_distance):
	square_distance = 0.0
	
	for coordinates in zip(first_coordinates, second_coordinates):
		first_coordinate, second_coordinate = coordinates
		
		#!!!!! Название переменной
		coordinate_distance = first_coordinate - second_coordinate
		
		if coordinate_distance < equivalence_distance:
			square_distance += \
				(first_coordinate - second_coordinate) \
					** 2.0
		else:
			are_coordinates_equivalent = False
			break
	else:
		distance                   = square_distance ** 0.5
		are_coordinates_equivalent = distance < equivalence_distance
		
		
	return are_coordinates_equivalent
	
	
	
def match_polygons(first_polygon, second_polygon, equivalence_distance):
	def match_implication(antecedent_vertices, consequent_vertices):
		for antecedent_vertex in antecedent_vertices:
			for consequent_vertex in consequent_vertices:
				contains_equivalent_vertex = \
					match_coordinates(
						antecedent_vertex,
						consequent_vertex,
						equivalence_distance
					)
					
				if contains_equivalent_vertex:
					are_vertices_implicated = True
					break
			else:
				are_vertices_implicated = False
				break
				
				
		return are_vertices_implicated
		
		
		
	# if first_polygon is second_polygon:
	# 	are_polygons_equivalent = True
	# else:
	centers_modules_offset = \
		abs(
			first_polygon.center_module \
				- second_polygon.center_module
		)
		
	if centers_modules_offset >= equivalence_distance:
		are_polygons_equivalent = False
	else:
		first_polygon_vertices, second_polygon_vertices = \
			first_polygon.vertices, \
				second_polygon.vertices
				
				
		if len(first_polygon_vertices) == len(second_polygon_vertices):
			are_polygons_equivalent = True
			
			are_polygons_equivalent &= \
				match_implication(
					first_polygon_vertices,
					second_polygon_vertices
				)
				
			are_polygons_equivalent &= \
				match_implication(
					second_polygon_vertices,
					first_polygon_vertices
				)
		else:
			are_polygons_equivalent = False
			
			
	return are_polygons_equivalent
	
	
	
def match_points(first_point, second_point, equivalence_distance):
	are_polygons_equivalent = \
		match_polygons(
			first_point.polygon,
			second_point.polygon,
			equivalence_distance
		)
		
	if are_polygons_equivalent:
		are_points_equivalent = \
			match_coordinates(
				first_point.coordinates,
				second_point.coordinates,
				equivalence_distance
			)
	else:
		are_points_equivalent = False
		
		
	return are_points_equivalent
	
	
	
	
	
	
	
class Polygon:
	def __init__(self, vertices, impossibility, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		vertices = list(vertices)
		
		#!!!!! Проверить расстояние между точками
		#!!!!! Проверить на выпуклость
		
		
		vertices_number      = len(vertices)
		center               = []
		center_square_module = 0.0
		
		for coordinates in zip(*vertices):
			center_coordinate = sum(coordinates) / float(vertices_number)
			
			center.append(center_coordinate)
			center_square_module += center_coordinate ** 2.0
			
		center_module = center_square_module ** 0.5
		
		
		self.__vertices        = vertices
		self.__vertices_number = vertices_number
		self.__impossibility   = impossibility
		self.__center          = center
		self.__center_module   = center_module
		
		
		
	@property
	def vertices(self):
		return list(self.__vertices)
		
		
	@property
	def vertices_number(self):
		return self.__vertices_number
		
		
	@property
	def impossibility(self):
		return self.__impossibility
		
		
		
	@property
	def center(self):
		return list(self.__center)
		
		
	@property
	def center_module(self):
		return self.__center_module
		
		
		
	def get_vertex(self, vertex_index):
		if vertex_index >= len(self.__vertices):
			raise Exception() #!!!!!
			
		return self.__vertices[vertex_index]
		
		
		
		
		
		
		
class Point:
	def __init__(self, polygon, decomposition, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		decomposition = list(decomposition)
		
		if not decomposition:
			raise Exception() #!!!!!
			
		#!!!!! Проверить на дублирование вершин
		#!!!!! Удалить вершины с нулевыми весами
		#!!!!! Проверить нормировку
		
		try:
			x_coordinate, y_coordinate, z_coordinate = 0.0, 0.0, 0.0
			
			for vertex_index, vertex_weight in decomposition:
				vertex = polygon.get_vertex(vertex_index)
					
				x_coordinate += vertex[0] * vertex_weight
				y_coordinate += vertex[1] * vertex_weight
				z_coordinate += vertex[2] * vertex_weight
		except:
			raise Exception() #!!!!! В случае неверного индекса вершины
			
			
		self.__polygon       = polygon
		self.__decomposition = decomposition
		self.__coordinates   = x_coordinate, y_coordinate, z_coordinate
		
		
		
		
		
	@property
	def polygon(self):
		return self.__polygon
		
		
		
	@property
	def decomposition(self):
		return list(self.__decomposition)
		
		
		
	@property
	def coordinates(self):
		return self.__coordinates
		
		
		
		
	@property
	def is_vertex(self):
		return len(self.__decomposition) == 1
		
		
		
	# @property
	# def is_edge_point(self):
	# 	is_edge_point = False
		
		
	# 	decomposition_length = len(self.__decomposition)
		
	# 	if decomposition_length == 1:
	# 		is_edge_point = True
			
	# 	elif decomposition_length == 2:
	# 		first_vertex_index, _  = self.__decomposition[0]
	# 		second_vertex_index, _ = self.__decomposition[1]
			
	# 		vertices_offset = abs(second_vertex_index - first_vertex_index)
	# 		vertices_number = self.__polygon.vertices_number
			
	# 		if vertices_offset == 1:
	# 			is_edge_point = True
	# 		elif vertices_offset == vertices_number - 1:
	# 			is_edge_point = True
				
				
	# 	return is_edge_point
		
		
		
	# @property
	# def is_inner_point(self):
	# 	return not self.is_edge_point
		
		
		
		
		
		
		
class Edge:
	def __init__(self,
					polygon,
					first_vertex_index,
					second_vertex_index,
					*args,
					**kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить индексы: должны быть соседними вершинами
		
		
		self.__polygon             = polygon
		self.__first_vertex_index  = first_vertex_index
		self.__second_vertex_index = second_vertex_index
		
		
		
		
		
	@property
	def polygon(self):
		return self.__polygon
		
		
		
	@property
	def first_vertex_index(self):
		return self.__first_vertex_index
		
		
		
	@property
	def second_vertex_index(self):
		return self.__second_vertex_index
		
		
		
		
		
	@property
	def first_vertex(self):
		first_vertex = \
			Point(
				self.__polygon,
				[(self.__first_vertex_index, 1.0)]
			)
			
		return first_vertex
		
		
		
	@property
	def second_vertex(self):
		second_vertex = \
			Point(
				self.__polygon,
				[(self.__second_vertex_index, 1.0)]
			)
			
		return second_vertex
		
		
		
		
		
		
		
def invert_edge(edge):
	inverted_edge = \
		Edge(
			edge.polygon,
			edge.second_vertex_index,
			edge.first_vertex_index
		)
		
	return inverted_edge
	
	
	
	
	
	
def compute_polygon_center(polygon):
	vertices_weight = 1.0 / polygon.vertices_number
	decomposition   = \
		[(vertex_index, vertices_weight) for vertex_index \
			in range(polygon.vertices_number)]
			
	polygon_center = Point(polygon, decomposition)
	
	return polygon_center
	