from PIL import Image, ImageDraw







def visualize_trajectory(trajectories, polygons):
	image_width  = 500
	image_height = 500
	
	image = \
		Image.new(
			mode  = "RGB",
			size  = (image_width, image_height),
			color = (255, 255, 255)
		)
		
	image_draw = ImageDraw.Draw(image)
	
	
	
	parameters = [parameter * 0.001 for parameter in range(3001)]
	
	
	
	
	
	points_x = []
	points_y = []
	
	
	for trajectory in trajectories:
		for parameter in parameters:
			trajectory_point = trajectory(parameter)
			
			points_x.append(trajectory_point.real)
			points_y.append(trajectory_point.imag)
			
			
	for polygon in polygons:
		for vertex in polygon.vertices:
			points_x.append(vertex.real)
			points_y.append(vertex.imag)
			
			
	min_x = min(points_x)
	max_x = max(points_x)
	min_y = min(points_y)
	max_y = max(points_y)
	
	scale = 500.0 / max(max_x - min_x, max_y - min_y)
	
	
	
	
	
	for trajectory in trajectories:
		last_point = None
		is_first   = True
		
		for parameter in parameters:
			point = trajectory(parameter)
			point = point.real, point.imag
			point = \
				int((point[0] - min_x) * scale), \
					image_height - int((point[1] - min_y) * scale)
					
			if is_first:
				is_first = False
				
				image_draw.ellipse(
					(point[0] - 2, point[1] - 2, \
						point[0] + 2, point[1] + 2),
					fill = (0, 0, 0)
				)
				
			if last_point is not None:
				image_draw.line(
					last_point + point,
					fill = (0, 0, 0)
				)
				
			last_point = point
			
		image_draw.ellipse(
			(last_point[0] - 2, last_point[1] - 2, \
				last_point[0] + 2, last_point[1] + 2),
			fill = (0, 0, 0)
		)
		
		
		
	for polygon in polygons:
		last_vertex = polygon.vertices[-1].real, polygon.vertices[-1].imag
		last_vertex = \
			int((last_vertex[0] - min_x) * scale), \
				image_height - int((last_vertex[1] - min_y) * scale)
		
		for vertex in polygon.vertices:
			vertex = vertex.real, vertex.imag
			vertex = \
				int((vertex[0] - min_x) * scale), \
					image_height - int((vertex[1] - min_y) * scale)
					
			image_draw.line(
				last_vertex + vertex,
				fill = (0, 0, 0)
			)
			
			last_vertex = vertex
			
			
			
			
			
	image.show()
	