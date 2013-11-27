from surface.polygon import Point
from svgwrite        import Drawing, rgb
from svgwrite.shapes import Polygon, Circle, Line





def create_svg(filename, surface, controls_sequence = None):
	a = (0.0, 64.0, 0.0, 64.0)
	b = (1500.0, 1500.0, 10.0)


	surface_view = Drawing(filename, size = (1500, 1500))
	
	
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
				
				
		if surface.maximal_impassability - surface.minimal_impassability > 0.0:
			relative_impassability = \
				(polygon.impassability - surface.minimal_impassability) \
					/ (surface.maximal_impassability - surface.minimal_impassability)
		else:
			relative_impassability = 0.0
			
		fill_color_red_component   = round(255.0 * relative_impassability)
		fill_color_green_component = round(255.0 - 255.0 * relative_impassability)
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
		
		
	if controls_sequence is not None:
		last_polygon_center = None
		
		for polygon in controls_sequence:
			polygon_center      = polygon.center[0], polygon.center[1]
			polygon_center_view = \
				Circle(
					correct_vertex(polygon_center, a, b),
					2,
					stroke_width = 0,
					fill         = rgb(0, 0, 0),
				)
				
			surface_view.add(polygon_center_view)
			
			
			if last_polygon_center is not None:
				trek_view = \
					Line(
						correct_vertex(polygon_center, a, b),
						correct_vertex(last_polygon_center, a, b),
						stroke_width = 1,
						stroke       = rgb(0, 0, 0),
					)
					
				surface_view.add(trek_view)
				
				
			last_polygon_center = polygon_center
			
			
	surface_view.save()
	