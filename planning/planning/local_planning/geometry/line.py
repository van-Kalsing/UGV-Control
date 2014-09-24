class Line:
	@classmethod
	def from_direction(cls, point, direction):
		coefficients = \
			- direction.imag, \
				direction.real, \
				- direction.imag * point.real + direction.real * point.imag
				
		line = cls(coefficients)
		
		return line
		
		
		
	@classmethod
	def from_points(cls, first_point, second_point):
		line = cls.from_direction(first_point, second_point - first_point)
		
		return line
		
		
		
	@staticmethod
	def are_parallel(first_line, second_line):
		first_line  = first_line.__coefficients
		second_line = second_line.__coefficients
		
		
		base_determinant = \
			first_line[0] * second_line[1] \
				- first_line[1] * second_line[0]
				
		#!!!!! Переделать так, чтобы совпадающие прямые не считались парал-ми
		are_parallel = abs(base_determinant) < 0.001
		
		
		return are_parallel
		
		
		
	@staticmethod
	def are_equivalent(first_line, second_line):
		first_line  = first_line.__coefficients
		second_line = second_line.__coefficients
		
		
		base_determinant = \
			first_line[0] * second_line[1] \
				- first_line[1] * second_line[0]
				
		# if base_determinant == 0.0:
		if abs(base_determinant) < 0.001:
			if first_line[0] != 0.0:
				factor = second_line[0] / first_line[0]
			else:
				factor = second_line[1] / first_line[1]
				
				
			are_equivalent = True
			
			for coefficients in zip(first_line, second_line):
				# are_equivalent &= coefficients[0] * factor == coefficients[1]
				are_equivalent &= abs(coefficients[0] * factor - coefficients[1]) < 0.001
				
				if not are_equivalent:
					break
		else:
			are_equivalent = False
			
			
		return are_equivalent
		
		
		
	@staticmethod
	def compute_intersection(first_line, second_line):
		first_line  = first_line.__coefficients
		second_line = second_line.__coefficients
		
		
		base_determinant = \
			first_line[0] * second_line[1] \
				- first_line[1] * second_line[0]
				
		# if base_determinant != 0.0:
		if abs(base_determinant) >= 0.001:
			first_determinant = \
				first_line[2] * second_line[1] \
					- first_line[1] * second_line[2]
					
			second_determinant = \
				first_line[0] * second_line[2] \
					- first_line[2] * second_line[0]
					
					
			intersection = \
				complex(
					first_determinant / base_determinant, \
						second_determinant / base_determinant
				)
		else:
			intersection = None
			
			
		return intersection
		
		
		
		
		
	def __init__(self, coefficients):
		#!!!!! *args, **kwargs
		
		#!!!!! Проверить
		self.__coefficients = tuple(coefficients)
		
		
		
	@property
	def coefficients(self):
		return self.__coefficients
		
		
		
		
		
	def compute_perpendicular(self, point):
		first_coefficient  = self.__coefficients[1]
		second_coefficient = - self.__coefficients[0]
		third_coefficient  = \
			first_coefficient * point.real \
				+ second_coefficient * point.imag
				
		coefficients = first_coefficient, second_coefficient, third_coefficient
		line         = self.__class__(coefficients)
		
		return line
		
		
		
		
		
	def compute_circle_intersections(self, circle_center, circle_radius):
		# Смещение системы координат в центр окружности
		coefficients     = list(self.coefficients)
		coefficients[2] -= \
			coefficients[0] * circle_center.real \
				+ coefficients[1] * circle_center.imag
				
				
		# Поиск точек пересечения прямой и окружности
		if coefficients[1] != 0.0:
			# Определение коэффициентов квадратного уравнения
			a = \
				coefficients[0] ** 2.0 \
					+ coefficients[1] ** 2.0
					
			b = - 2.0 * coefficients[0] * coefficients[2]
			
			c = \
				coefficients[2] ** 2.0 \
					- (circle_radius * coefficients[1]) ** 2.0
					
					
			# Решение квадратного уравнения
			d = b ** 2.0 - 4.0 * a * c
			
			if d >= 0.0:
				first_intersection_real = (- b + d ** 0.5) / (2.0 * a)
				first_intersection_imag = \
					(coefficients[2] \
							- coefficients[0] * first_intersection_real) \
						/ coefficients[1]
						
				first_intersection  = circle_center
				first_intersection += \
					complex(
						first_intersection_real,
						first_intersection_imag
					)
					
					
				second_intersection_real = (- b - d ** 0.5) / (2.0 * a)
				second_intersection_imag = \
					(coefficients[2] \
							- coefficients[0] * second_intersection_real) \
						/ coefficients[1]
						
				second_intersection  = circle_center
				second_intersection += \
					complex(
						second_intersection_real,
						second_intersection_imag
					)
					
					
				intersections = [first_intersection, second_intersection]
			else:
				intersections = []
				
		else:
			# Определение коэффициентов квадратного уравнения
			a = \
				coefficients[0] ** 2.0 \
					+ coefficients[1] ** 2.0
					
			b = - 2.0 * coefficients[1] * coefficients[2]
			
			c = \
				coefficients[2] ** 2.0 \
					- (circle_radius * coefficients[0]) ** 2.0
					
					
			# Решение квадратного уравнения
			d = b ** 2.0 - 4.0 * a * c
			
			if d >= 0.0:
				first_intersection_imag = (- b + d ** 0.5) / (2.0 * a)
				first_intersection_real = \
					(coefficients[2] \
							- coefficients[1] * first_intersection_imag) \
						/ coefficients[0]
						
				first_intersection  = circle_center
				first_intersection += \
					complex(
						first_intersection_real,
						first_intersection_imag
					)
					
					
				second_intersection_imag = (- b - d ** 0.5) / (2.0 * a)
				second_intersection_real = \
					(coefficients[2] \
							- coefficients[1] * second_intersection_imag) \
						/ coefficients[0]
						
				second_intersection  = circle_center
				second_intersection += \
					complex(
						second_intersection_real,
						second_intersection_imag
					)
					
					
				intersections = [first_intersection, second_intersection]
			else:
				intersections = []
				
				
		return intersections
		