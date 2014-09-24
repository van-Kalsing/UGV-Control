from planning.planning.local_planning.geometry.line \
	import Line
	
from planning.utilities.filter \
	import Filter
	
	
	
	
	
	
	
class Polygon:
	@classmethod
	def from_vertices(cls, vertices):
		polygon = cls(vertices)
		
		return polygon
		
		
		
		
		
	def __init__(self, vertices, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__vertices = list(vertices)
		
		
		# Проверка вершин (должно быть не менее 3 вершин)
		if len(self.__vertices) < 3:
			raise Exception() #!!!!!
			
			
		# Проверка вершин (должны образовывать выпуклый многоугольник)
		# и вычисление ориентации полигона - направления обхода вершин
		# (положительное значение соответствует обходу против часовой стрелки)
		area_filter = Filter()
		
		
		last_vector = self.__vertices[-1] - self.__vertices[-2]
		last_vertex = self.__vertices[-1]
		
		for vertex in self.__vertices:
			first_vector  = last_vector
			second_vector = vertex - last_vertex
			
			
			area = \
				first_vector.real * second_vector.imag \
					- first_vector.imag * second_vector.real
					
			if area == 0.0:
				raise Exception() #!!!!!
			else:
				area_filter.check_element(area)
				
				
			last_vector = second_vector
			last_vertex = vertex
			
			
		if area_filter.minimal_element < 0.0 < area_filter.maximal_element:
			raise Exception() #!!!!!
		else:
			self.__orientation = \
				area_filter.maximal_element \
					/ abs(area_filter.maximal_element)
					
					
					
					
					
	@property
	def vertices(self):
		return list(self.__vertices)
		
		
		
	@property
	def orientation(self):
		return self.__orientation
		
		
		
	@property
	def lines(self):
		lines = []
		
		
		last_vertex = self.__vertices[-1]
		
		for vertex in self.__vertices:
			line = Line.from_points(last_vertex, vertex)
			lines.append(line)
			
			last_vertex = vertex
			
			
		return lines
		
		
		
		
		
	def is_inner_point(self, point):
		general_sign   = 0.0
		is_inner_point = True
		
		
		# Т.к. вершины обходятся последовательно, то ориентированные
		# площади всех параллелограммов, составленных из векторов
		# point - last_vertex и vertex - last_vertex (в указанном порядке),
		# должны иметь один знак (допускается равенство нулю)
		last_vertex = self.__vertices[-1]
		
		for vertex in self.__vertices:
			first_vector  = point - last_vertex
			second_vector = vertex - last_vertex
			
			
			area = \
				first_vector.real * second_vector.imag \
					- first_vector.imag * second_vector.real
					
			if area != 0.0:
				sign = area / abs(area)
				
				if sign * general_sign < 0.0:
					is_inner_point = False
					break
					
				general_sign = sign
				
				
			last_vertex = vertex
			
			
		return is_inner_point
		
		
		
		
		
	def compute_circle_intersections(self, circle_center, circle_radius):
		intersections = []
		
		for line in self.lines:
			intersections += \
				line.compute_circle_intersections(
					circle_center,
					circle_radius
				)
				
		return intersections
		