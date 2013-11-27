from csv          import writer
from math         import exp, acos
from numpy        import array, dot, cross, sqrt, zeros, float64
from numpy.linalg import norm
from random       import uniform, randint, random







minimal_point_offset_step = 0.001
maximal_point_offset_step = 1.0
force_magnitude_threshold = 0.1


points_records   = None
polygons_records = None







impossibility_matrix = \
	array(
		[[    1.,    9.,    1.,    1.,    1.,     1.,     1.],
		 [    1.,    9.,    1.,    9.,    9.,     9.,     9.],
		 [    1.,    9.,    1.,    9.,    1.,     1.,     1.],
		 [    1.,    1.,    1.,    9.,    1.,     9.,     1.],
		 [    9.,    1.,    9.,    9.,    9.,     9.,     1.],
		 [    9.,    1.,    1.,    1.,    1.,     1.,     1.],
		 [    9.,    5.,    5.,    1.,    9.,     1.,     9.],
		 [    1.,    1.,    1.,    1.,    9.,     1.,     9.]]
	)
	# array(
	# 	[[2., 1.],
	# 	 [1., 5.]]
	# )
	
	
	
def e():
	im = zeros((64, 64), dtype = float64)
	
	def is_road(h, v):
		return v <= 0.85 * h - 16 and v >= 0.85 * h - 32
		
	def is_lake(h, v):
		distance = (h**2 + v**2) ** 0.5
		alpha    = acos(h / distance)
		
		a = (distance - 54.0) ** 2.0 + 250 * (alpha - 0.9) ** 2.0
		return a < 30.0
		
	def is_wall(h, v):
		return  h >= 58 and h <= 60 and v > 45
		
		
	trees = list()
	
	while len(trees) < 30:
		th, tv = (randint(0, 64), randint(0, 64))
		if not is_road(th, tv) and not is_lake(th, tv) and not is_wall(th, tv):
			trees.append((th, tv))
			
	def is_tree(h, v):
		for th, tv in trees:
			a = (h) ** 2 + (v) ** 2 > 16 and (h) ** 2 + (v) ** 2 < 3500
			if (h - th) ** 2 + (v - tv) ** 2 < 2.25:
				return True
				
		return False
		
	for v in range(64):
		for h in range(64):
			if is_road(h, 64 - v):
				im[v,h] = 1.0
			elif is_lake(h, 64 - v):
				im[v,h] = 10.0
			elif is_wall(h, 64 - v):
				im[v,h] = 17.0
			elif is_tree(h, 64 - v):
				im[v,h] = 17.0
			else:
				im[v,h] = uniform(3.0, 7.0)
				
	return im
	
impossibility_matrix = e()


def get_point_impossibility(point_record_index, x_size, y_size):
	point_record = points_records[point_record_index]
	point        = point_record['coordinates']
	
	
	vertical_dimension, horizontal_dimension = impossibility_matrix.shape
	
	
	horizontal_index = \
		int(
			point[0] * horizontal_dimension \
				/ x_size
		)
		
	if horizontal_index == horizontal_dimension:
		horizontal_index = horizontal_dimension - 1
		
		
	vertical_index = \
		int(
			(y_size - point[1]) * vertical_dimension \
				/ y_size
		)
		
	if vertical_index == vertical_dimension:
		vertical_index = vertical_dimension - 1
		
		
	return impossibility_matrix[vertical_index, horizontal_index]
	
	
	
def get_polygon_impossibility(polygon_record_index, x_size, y_size):
	polygon_record = polygons_records[polygon_record_index]
	
	
	points_impossibilities = []
	
	for point_record_index in polygon_record['points']:
		point_impossibility = \
			get_point_impossibility(
				point_record_index,
				x_size,
				y_size
			)
			
		points_impossibilities.append(point_impossibility)
		
	polygon_impossibility = \
		sum(points_impossibilities) \
			/ len(points_impossibilities)
			
			
	return polygon_impossibility
	
	
	
	
	
	
	
precision_matrix = \
	array(
		[[1., 1.],
		 [1., 1.]]
	)
	# array(
	# 	[[    1., 0.001,    1.,    1.,    1.,     1.,     1.],
	# 	 [    1., 0.001,    1., 0.001, 0.001,  0.001,  0.001],
	# 	 [    1.,    1.,    1., 0.001,    1.,     1.,     1.],
	# 	 [ 0.001,    1., 0.001, 0.001,    1.,  0.001,     1.],
	# 	 [    1.,    1.,    1., 0.001, 0.001,  0.001,     1.],
	# 	 [    1., 0.001,    1.,    1.,    1.,     1.,     1.],
	# 	 [ 0.001, 0.001,    1., 0.001, 0.001,     1.,  0.001],
	# 	 [    1.,    1.,    1., 0.001,    1.,     1.,  0.001]]
	# )
	
	
def get_point_precision(point_record_index, x_size, y_size):
	point_record = points_records[point_record_index]
	point        = point_record['coordinates']
	
	
	vertical_dimension, horizontal_dimension = precision_matrix.shape
	
	
	horizontal_index = \
		int(
			point[0] * horizontal_dimension \
				/ x_size
		)
		
	if horizontal_index == horizontal_dimension:
		horizontal_index = horizontal_dimension - 1
		
		
	vertical_index = \
		int(
			(y_size - point[1]) * vertical_dimension \
				/ y_size
		)
		
	if vertical_index == vertical_dimension:
		vertical_index = vertical_dimension - 1
		
		
	return precision_matrix[vertical_index, horizontal_index]
	
	
	
def get_polygon_precision(polygon_record_index, x_size, y_size):
	polygon_record = polygons_records[polygon_record_index]
	
	
	points_precisions = []
	
	for point_record_index in polygon_record['points']:
		point_precision = \
			get_point_precision(
				point_record_index,
				x_size,
				y_size
			)
			
		points_precisions.append(point_precision)
		
	polygon_precision = \
		sum(points_precisions) \
			/ len(points_precisions)
			
			
	return polygon_precision
	
	
	
	
	
	
	
def generate_regular_surface(horizontal_dimension, vertical_dimension,
								scaling_factor):
	points_records = list()
	
	for vertical_index in range(vertical_dimension + 1):
		for horizontal_index in range(horizontal_dimension + 1):
			point = \
				array([
					float(horizontal_index) * scaling_factor, \
						float(vertical_index) * scaling_factor, \
						0.0
				])
				
			points_records.append(
				{
					'coordinates':     point,
					'polygons':        set(),
					
					'is_left_point':   horizontal_index == 0,
					'is_right_point':  horizontal_index == horizontal_dimension,
					'is_bottom_point': vertical_index == 0,
					'is_top_point':    vertical_index == vertical_dimension
				}
			)
			
			
			
	polygons_records  = list()
	last_polygons_row = []
	
	for vertical_index in range(vertical_dimension):
		current_polygons_row = []
		
		
		for horizontal_index in range(horizontal_dimension):
			polygon_0_record = \
				{
					'points':    list(),
					'relations': dict()
				}
				
			polygon_1_record = \
				{
					'points':    list(),
					'relations': dict()
				}
				
			polygon_0_record_index = len(polygons_records)
			polygon_1_record_index = polygon_0_record_index + 1
			
			polygons_records.extend(
				[polygon_0_record, \
					polygon_1_record]
			)
			
			
			
			point_0_record_index = \
				vertical_index * (horizontal_dimension + 1) \
					+ horizontal_index
					
			point_1_record_index = \
				vertical_index * (horizontal_dimension + 1) \
					+ (horizontal_index + 1)
					
			point_2_record_index = \
				(vertical_index + 1) * (horizontal_dimension + 1) \
					+ horizontal_index
					
			point_3_record_index = \
				(vertical_index + 1) * (horizontal_dimension + 1) \
					+ (horizontal_index + 1)
					
			point_0_record = points_records[point_0_record_index]
			point_1_record = points_records[point_1_record_index]
			point_2_record = points_records[point_2_record_index]
			point_3_record = points_records[point_3_record_index]
			
			
			
			if not bool(vertical_index % 2):
				point_0_record['polygons'].add(polygon_0_record_index)
				point_1_record['polygons'].add(polygon_0_record_index)
				point_2_record['polygons'].add(polygon_0_record_index)
				
				polygon_0_record['points'].extend(
					[point_0_record_index, \
						point_1_record_index, \
						point_2_record_index]
				)
				
				if current_polygons_row:
					polygon_0_record['relations'][2] = \
						current_polygons_row[-1], 1
						
				if last_polygons_row:
					polygon_0_record['relations'][0] = \
						last_polygons_row[horizontal_index * 2 + 1], 2
						
						
						
				point_2_record['polygons'].add(polygon_1_record_index)
				point_1_record['polygons'].add(polygon_1_record_index)
				point_3_record['polygons'].add(polygon_1_record_index)
				
				polygon_1_record['points'].extend(
					[point_2_record_index, \
						point_1_record_index, \
						point_3_record_index]
				)
				
				polygon_1_record['relations'][0] = polygon_0_record_index, 1
			else:
				point_0_record['polygons'].add(polygon_0_record_index)
				point_1_record['polygons'].add(polygon_0_record_index)
				point_3_record['polygons'].add(polygon_0_record_index)
				
				polygon_0_record['points'].extend(
					[point_0_record_index, \
						point_1_record_index, \
						point_3_record_index]
				)
				
				if last_polygons_row:
					polygon_0_record['relations'][0] = \
						last_polygons_row[horizontal_index * 2 + 1], 2
						
						
						
				point_2_record['polygons'].add(polygon_1_record_index)
				point_0_record['polygons'].add(polygon_1_record_index)
				point_3_record['polygons'].add(polygon_1_record_index)
				
				polygon_1_record['points'].extend(
					[point_2_record_index, \
						point_0_record_index, \
						point_3_record_index]
				)
				
				polygon_1_record['relations'][1] = polygon_0_record_index, 2
				
				if current_polygons_row:
					polygon_1_record['relations'][0] = \
						current_polygons_row[-2], 1
						
						
			current_polygons_row.extend(
				[polygon_0_record_index, \
					polygon_1_record_index]
			)
			
		last_polygons_row =	current_polygons_row
		
		
		
	return points_records, polygons_records
	
	
	
	
	
	
	
def disturb_surface_regularity(x_size, y_size):
	polygons_number           = len(polygons_records)
	polygons_total_precisions = \
		[sum(
			[get_polygon_precision(polygon_record_index, x_size, y_size) \
				for polygon_record_index \
				in  range(polygons_number)]
		)]
		
		
		
	def compute_point_force(point_record_index):
		def compute_point_force_component(polygon_record_index):
			polygon_record         = polygons_records[polygon_record_index]
			points_records_indexes = polygon_record['points']
			
			while points_records_indexes[0] != point_record_index:
				first_point_record_index = points_records_indexes.pop(0)
				
				points_records_indexes.append(
					first_point_record_index
				)
				
				
			points = \
				[points_records[point_record_index]['coordinates'] \
					for point_record_index \
					in  points_records_indexes]
					
			adjacent_vector = points[0] - points[1]
			base_vector     = points[2] - points[1]
			
			adjacent_vector_norm = norm(adjacent_vector)
			base_vector_norm     = norm(base_vector)
			
			
			height = \
				norm(
					cross(adjacent_vector, base_vector) \
						/ base_vector_norm
				)
				
			area      = base_vector_norm * height / 2.0
			perimeter = \
				adjacent_vector_norm \
					+ base_vector_norm \
					+ norm(adjacent_vector - base_vector)
					
					
					
			# Вычисление поперечной силы
			lower_limit = \
				sqrt(2.0 / (base_vector_norm ** 2.0) \
						+ 1.0 / (2.0 * height ** 2.0)) \
					+ 2.0
					
			# perimeter / area - lower_limit
			transverse_force_magnitude = \
				0.5 * base_vector_norm \
					- dot(adjacent_vector, base_vector) / base_vector_norm
					
			transverse_force_magnitude = transverse_force_magnitude ** 3.0
			
			# is_reverse_direction = \
			# 	dot(adjacent_vector, base_vector) / base_vector_norm \
			# 		> 0.5 * base_vector_norm
					
			# if is_reverse_direction:
			# 	transverse_force_direction = - base_vector / base_vector_norm
			# else:
			# 	transverse_force_direction = base_vector / base_vector_norm
			transverse_force_direction = base_vector / base_vector_norm
				
				
			transverse_force = \
				transverse_force_magnitude \
					* transverse_force_direction
					
					
					
			# Вычисление продольной силы
			polygon_precision = \
				get_polygon_precision(
					polygon_record_index,
					x_size,
					y_size
				)
				
			required_area = \
				x_size * y_size \
					* polygon_precision / polygons_total_precisions[0]
					
			#!!!!! Здесь уже содержится информация о направлении,
			#!!!!!     т.ч. необходимо заменить названиее переменной
			lengthwise_force_magnitude = (required_area - area) ** 3.0
				# required_area / area \
				# 	- (area - required_area) \
				# 	- 1.0
					
					
			rotation_matrix = \
				array(
					[[0.0, -1.0,  0.0],
					 [1.0,  0.0,  0.0],
					 [0.0,  0.0,  1.0]]
				)
				
			lengthwise_force_direction = \
				dot(
					rotation_matrix,
						base_vector / base_vector_norm
				)
				
				
			lengthwise_force = \
				lengthwise_force_magnitude \
					* lengthwise_force_direction
					
					
					
			# Вычисление суммарной силы
			force_component = \
				transverse_force \
					+ lengthwise_force
					
			if base_vector_norm == 0.0:
				print('\n\n\n1')
				print(base_vector_norm)
			if adjacent_vector_norm == 0.0:
				print('\n\n\n2')
				print(adjacent_vector_norm)
			if norm(adjacent_vector - base_vector) == 0.0:
				print('\n\n\n3')
				print(norm(adjacent_vector - base_vector))
			if height == 0.0:
				print('\n\n\n3')
				print(height)
			return force_component
			
			
			
		point_force  = zeros(3, dtype = float64)
		point_record = points_records[point_record_index]
		
		for polygon_record_index in point_record['polygons']:
			point_force += \
				compute_point_force_component(
					polygon_record_index
				)
				
		if point_record['is_left_point'] or point_record['is_right_point']:
			point_force[0] = 0.0
			
		if point_record['is_bottom_point'] or point_record['is_top_point']:
			point_force[1] = 0.0
			
			
		point_force_magnitude = norm(point_force)
		
		if point_force_magnitude != 0.0:
			point_force_direction = point_force / norm(point_force)
		else:
			point_force_direction = None
			
			
			
		return point_force, point_force_direction
		
		
		
	def check_polygon_orientation(polygon_record_index):
		is_polygon_orientation_positive = True
		
		
		polygon_record         = polygons_records[polygon_record_index]
		points_records_indexes = polygon_record['points']
		
		points = \
			[points_records[point_record_index]['coordinates'] \
				for point_record_index \
				in  points_records_indexes]
				
		points_number = len(points)
		
		
		edges = list()
		
		for edge_number in range(points_number):
			if edge_number < points_number - 1:
				first_point  = points[edge_number]
				second_point = points[edge_number + 1]
			else:
				first_point  = points[edge_number]
				second_point = points[0]
				
			edges.append(
				second_point \
					- first_point
			)
			
			
		for edge_pair_number in range(points_number):
			if edge_pair_number < points_number - 1:
				first_edge  = edges[edge_pair_number]
				second_edge = edges[edge_pair_number + 1]
			else:
				first_edge  = edges[edge_pair_number]
				second_edge = edges[0]
				
				
			cross_product = cross(first_edge, second_edge)
			
			if cross_product[2] <= 0.0:
				is_polygon_orientation_positive = False
				break
				
				
		return is_polygon_orientation_positive
		
		
		
	def minimize_point_force(point_record_index, shift_step):
		point_record = points_records[point_record_index]
		point        = point_record['coordinates']
		
		
		adjacent_polygons_total_precision = \
			sum(
				[get_polygon_precision(polygon_record_index, x_size, y_size) \
					for polygon_record_index \
					in  point_record['polygons']]
			)
			
			
		point_force, point_force_direction = \
			compute_point_force(
				point_record_index
			)
			
		shift_step = maximal_point_offset_step
		
		
		while norm(point_force) >= force_magnitude_threshold:
			if shift_step >= minimal_point_offset_step:
				point_offset = \
					shift_step \
						* point_force_direction
						
				point_copy  = point.copy()
				point      += point_offset
				
				
				is_shift_successful = True
				
				for polygon_record_index in point_record['polygons']:
					is_shift_successful &= \
						check_polygon_orientation(
							polygon_record_index
						)
						
				if is_shift_successful:
					shifted_point_force, shifted_point_force_direction = \
						compute_point_force(
							point_record_index
						)
						
					is_shift_successful &= \
						norm(shifted_point_force) \
							< norm(point_force)
							
							
							
				if is_shift_successful:
					polygons_total_precisions[0] -= \
						adjacent_polygons_total_precision
						
						
					adjacent_polygons_total_precision = 0.0
					
					for polygon_record_index in point_record['polygons']:
						adjacent_polygons_total_precision += \
							get_polygon_precision(
								polygon_record_index,
								x_size,
								y_size
							)
							
							
					polygons_total_precisions[0] += \
						adjacent_polygons_total_precision
						
						
					point_force, point_force_direction = \
						shifted_point_force, \
							shifted_point_force_direction
							
					# shift_step = \
					# 	min(
					# 		shift_step * 2.0,
					# 			maximal_point_offset_step
					# 	)
						
					# is_computing_finished = False
					
					
					# if shifted_point_force_direction is None:
					# 	return True
						
					# dot_product = \
					# 	dot(
					# 		point_force_direction,
					# 		shifted_point_force_direction
					# 	)
						
					# if dot_product < 0.0:
					# 	return True
					# break
				else:
					point                       = point_copy
					point_record['coordinates'] = point
					
					shift_step /= 2.0
					# break
			else:
				break
				
				
				
	is_computing_finished = False
	points_number         = len(points_records)
	
	
	# shift_step = maximal_point_offset_step
	
	# factor = 0.5
	# while True:
	# 	for _ in range(points_number):
	# 		point_record_index = randint(0, points_number - 1)
			
	# 		minimize_point_force(point_record_index, shift_step)
			
	# 	shift_step *= factor
	# 	print(shift_step)
	# 	if shift_step < minimal_point_offset_step:
	# 		break
		# is_iteration_finished = False
		
		# while not is_iteration_finished:
		# 	is_iteration_finished = True
			
			
	for _ in range(points_number * 32):
		point_record_index = randint(0, points_number - 1)
		
		minimize_point_force(point_record_index, minimal_point_offset_step)
				
				
				
		# computing_queue = []
		
		# for point_record_index in range(points_number):
		# 	point_force, point_force_direction = \
		# 		compute_point_force(
		# 			point_record_index
		# 		)
				
		# 	computing_queue.append(
		# 		[point_record_index, norm(point_force)]
		# 	)
			
		# computing_queue = \
		# 	sorted(
		# 		computing_queue,
		# 		key = lambda r: - r[1]
		# 	)
		
		# point_record_index = computing_queue[0][0]
		# minimize_point_force(point_record_index)
		
		# is_computing_finished = True
		
		#points_number // 256 + 1):
		# for a in range(points_number):
			# point_record_index = randint(0, points_number - 1)
			#point_record_index = a % points_number
			
			
		# print(point_record_index)
		# print('%s; %s' % (point_force, norm(point_force)))
		# print(point_offset_step)
		# print('\n\n\n')
def write_csv_file(file_name, x_size, y_size):
	def form_csv_records():
		polygons_number = len(polygons_records)
		
		for polygon_record_index in range(polygons_number):
			polygon_record    = polygons_records[polygon_record_index]
			polygon_points    = polygon_record['points']
			polygon_relations = polygon_record['relations']
			
			
			def form_vertex_record(point_record_index):
				point_record = points_records[point_record_index]
				point        = point_record['coordinates']
				
				vertex_record = \
					"(%s,%s,%s)" \
						% (point[0], point[1], point[2])
						
				return vertex_record
				
			vertices_records = \
				[form_vertex_record(point_record_index) for point_record_index \
					in polygon_points]
					
			vertices_record = ','.join(vertices_records)
			
			
			def form_relation_record(polygon_edge_index):
				adjacent_polygon_index, adjacent_polygon_edge_index = \
					polygon_relations[polygon_edge_index]
					
				substitutions = \
					polygon_edge_index, \
						adjacent_polygon_index, \
						adjacent_polygon_edge_index
						
						
				relation_record = '(%s,%s:%s)' % substitutions
				
				return relation_record
				
			relations_records = \
				[form_relation_record(polygon_edge_index) \
					for polygon_edge_index \
					in  polygon_relations]
					
			relations_record = ','.join(relations_records)
			
			
			polygon_impossibility = \
				get_polygon_impossibility(
					polygon_record_index,
					x_size,
					y_size
				)
				
			impossibility_record = str(polygon_impossibility)
			
			
			yield vertices_record, relations_record, impossibility_record
			
			
	with open(file_name, 'w') as csv_file:
		csv_file_writer = writer(csv_file, delimiter = ';')
		
		csv_file_writer.writerows(
			form_csv_records()
		)
		
		
		
		
		
		
		
def generate_surface(file_name,
						horizontal_dimension, vertical_dimension,
						scaling_factor):
	global points_records, polygons_records
	
	points_records, polygons_records = \
		generate_regular_surface(
			horizontal_dimension,
			vertical_dimension,
			scaling_factor
		)
		
		
	x_size = scaling_factor * float(horizontal_dimension)
	y_size = scaling_factor * float(vertical_dimension)
	
	disturb_surface_regularity(x_size, y_size)
	write_csv_file(file_name, x_size, y_size)
	