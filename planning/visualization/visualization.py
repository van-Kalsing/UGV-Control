from planning.surface.polygon import Point
from svgwrite                 import Drawing, rgb
from svgwrite.shapes          import Polygon, Circle, Line
from svgwrite.text            import Text
from numpy                    import array

from planning.planning.global_planning.smoothing \
	import Smoother
	
	
	
	
	
def create_svg(file, surface, controls_sequence = None, sn = None):
	min_x, max_x = None, None
	min_y, max_y = None, None
	
	for polygon in surface.polygons:
		for vertex in polygon.vertices:
			if min_x is None:
				min_x, max_x = vertex[0], vertex[0]
				min_y, max_y = vertex[1], vertex[1]
			else:
				min_x, max_x = min(vertex[0], min_x), max(vertex[0], max_x)
				min_y, max_y = min(vertex[1], min_y), max(vertex[1], max_y)
				
				
	a = (min_x, max_x, min_y, max_y)
	b = (max_x - min_x, max_y - min_y, 10.0)


	surface_view = Drawing(size = (max_x - min_x, max_y - min_y))
	
	
	def correct_vertex(vertex, surface_bounds, canvas_bounds):
		x_coordinate, y_coordinate                       = vertex
		left_bound, right_bound, bottom_bound, top_bound = surface_bounds
		canvas_width, canvas_height, canvas_padding      = canvas_bounds
		
		
		x_coordinate_scaling = \
			(canvas_width - 2.0 * canvas_padding) \
				/ (right_bound - left_bound)
				
		y_coordinate_scaling = \
			(canvas_height - 2.0 * canvas_padding) \
				/ (top_bound - bottom_bound)
				
				
		x_coordinate = \
			x_coordinate_scaling * (x_coordinate - left_bound) \
				+ canvas_padding
				
		y_coordinate = \
			y_coordinate_scaling * (y_coordinate - bottom_bound) \
				+ canvas_padding
				
		y_coordinate = canvas_height - y_coordinate
		
		
		return x_coordinate, y_coordinate
		
		
	for polygon in surface.polygons:
		vertices = \
			[correct_vertex((x_coordinate, y_coordinate), a, b) \
				for x_coordinate, y_coordinate, z_coordinate \
				in  polygon.vertices]
				
				
		if surface.maximal_impossibility - surface.minimal_impossibility > 0.0:
			relative_impossibility = \
				(polygon.impossibility - surface.minimal_impossibility) \
					/ (surface.maximal_impossibility - surface.minimal_impossibility)
		else:
			relative_impossibility = 0.0
			
		fill_color_red_component   = round(255.0 * relative_impossibility)
		fill_color_green_component = round(255.0 - 255.0 * relative_impossibility)
		fill_color_blue_component  = 0
		fill_color                 = \
			rgb(
				fill_color_red_component,
				fill_color_green_component,
				fill_color_blue_component
			)
			
		polygon_view = \
			Polygon(
				vertices,
				stroke_width = 1,
				stroke       = rgb(0, 0, 0),
				fill         = fill_color
			)
			
		surface_view.add(polygon_view)
		
		
	if sn is not None:
		for polygon_index, polygon in enumerate(surface.polygons):
			polygon_index_view = \
				Text(
					str(polygon_index),
					insert = \
						correct_vertex(
							(polygon.center[0], polygon.center[1]),
							a, b
						)
				)
				
			surface_view.add(polygon_index_view)
			
			
	# if sn is not None:
	# 	from svgwrite.text import Text
	# 	for state in sn:
	# 		polygon = state.polygon
	# 		polygon_number = sn[state]
			
	# 		polygon_center      = polygon.center[0], polygon.center[1]
	# 		q,w = correct_vertex(polygon_center, a, b)
	# 		polygon_center_view = \
	# 			Text(
	# 				str(polygon_number),
	# 				insert = (q+2,w+2),
	# 				style = "font-size: 50%; font-color: #808080"
	# 			)
				
	# 		surface_view.add(polygon_center_view)
			
			
	if controls_sequence is not None:
		last_state          = None
		last_polygon_center = None
		smoother            = Smoother(surface = surface, smoothing_depth = 1)
		
		
		for state in controls_sequence:
			polygon = state.polygons_sequence[-1]
			
			polygon_center      = polygon.center[0], polygon.center[1]
			polygon_center_view = \
				Circle(
					correct_vertex(polygon_center, a, b),
					2,
					stroke_width = 0,
					fill         = rgb(0, 0, 0),
				)
				
			surface_view.add(polygon_center_view)
			
			
			if last_state is not None:
				smoother.push_transfer(
					last_state.get_transfer(state)
				)
				
				first_transfer_point, second_transfer_point = \
					smoother.transfers_points_sequence[0]
					
					
				first_trek_view = \
					Line(
						correct_vertex(last_polygon_center, a, b),
						correct_vertex(
							(first_transfer_point.coordinates[0],
								first_transfer_point.coordinates[1]),
							a,
							b
						),
						stroke_width = 1,
						stroke       = rgb(0, 0, 0),
					)
					
				first_trek_end_view = \
					Circle(
						correct_vertex(
							(first_transfer_point.coordinates[0],
								first_transfer_point.coordinates[1]),
							a,
							b
						),
						2,
						stroke_width = 0,
						fill         = rgb(0, 0, 0),
					)
					
				second_trek_view = \
					Line(
						correct_vertex(
							(second_transfer_point.coordinates[0],
								second_transfer_point.coordinates[1]),
							a,
							b
						),
						correct_vertex(polygon_center, a, b),
						stroke_width = 1,
						stroke       = rgb(0, 0, 0),
					)
					
				second_trek_start_view = \
					Circle(
						correct_vertex(
							(second_transfer_point.coordinates[0],
								second_transfer_point.coordinates[1]),
							a,
							b
						),
						2,
						stroke_width = 0,
						fill         = rgb(0, 0, 0),
					)
					
					
				surface_view.add(first_trek_view)
				surface_view.add(first_trek_end_view)
				surface_view.add(second_trek_view)
				surface_view.add(second_trek_start_view)
				
				
			last_state          = state
			last_polygon_center = polygon_center
			
			
	surface_view.write(file)
	