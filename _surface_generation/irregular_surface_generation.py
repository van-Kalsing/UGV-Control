from surface.polygon import Polygon







def generate_regular_surface(surface_width,
								surface_length,
								equivalence_distance):
	# c = min(surface_width, surface_length) / 5.0
	
	impassibility = 1.0
	
	
	initial_polygon = \
		Polygon(
			vertices      = [(0.0, 0.0, 0.0), (c, 0.0, 0.0), (0.0, c, 0.0)],
			impassibility = impassibility
		)
		
	initial_edge = Edge(initial_polygon, 1, 2)
	
	
	surface     = Surface(equivalence_distance)
	edges_front = \
		{
			(initial_edge, [initial_reflection])
		}
		
		
	def measure_point(edge, coordinates):
		
	a = True
	while edges_front and a:
		a = False
		
		last_edges_front = edges_front
		edges_front      = []
		
		
		last_edge = last_edges_front[0]
		
		for current_edge in last_edges_front[1::]:
			point_measurement_value = \
				measure_point(
					last_edge,
					current_edge.second_vertex.coordinates
				)
				
			is_merger_available = \
				point_measurement_value > 0 \
					and point_measurement_value < threshold
					
			if is_merger_available:
				vertices = \
					[
						last_edge.first_vertex.coordinates,
						last_edge.second_vertex.coordinates,
						current_edge.second_vertex.coordinates
					]
					
				new_polygon       = Polygon(vertices, impassibility)
				new_edge          = Edge(new_polygon, 0, 2)
				last_edge_twin    = Edge(new_polygon, 0, 1)
				current_edge_twin = Edge(new_polygon, 1, 2)
				
				surface.add_polygon(new_polygon)
				surface.add_relation(last_edge, last_edge_twin)
				surface.add_relation(current_edge, current_edge_twin)
				
				
				edges_front.append(new_edge)
				last_edge = new_edge
				a=True
			else:
				edges_front.append(last_edge)
				last_edge = current_edge
				#!!!!! Выбрать точку
		# if len(last_edges_front) > 1:
		# else:
			
			
	return surface
	