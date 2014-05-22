from csv import reader, writer
from PIL import Image







def generate_surface(map_file, csv_file, step = 10):
	points_records   = list()
	polygons_records = list()
	
	image = Image.open(map_file)
	image = image.convert("RGB")
	
	image_x_size, image_y_size = image.size
	
	
	
	
	
	for y in range(0, image_y_size + 1, step):
		for x in range(0, image_x_size + 1, step):
			points_records.append({
				'coordinates': (float(x), float(y), 0.0)
			})
			
			
			
			
			
	for y in range(image_y_size // step):
		for x in range(image_x_size // step):
			polygon_points = \
				tuple([
					(y + 1) * (image_x_size // step + 1) + (x),
					(y + 1) * (image_x_size // step + 1) + (x + 1),
					(y)     * (image_x_size // step + 1) + (x + 1),
					(y)     * (image_x_size // step + 1) + (x),
				])
				
				
			polygon_relations = dict()
			
			if y != 0:
				polygon_relations[2] = \
					(y - 1) * (image_x_size // step) + x, \
						0
						
			if x != 0:
				polygon_relations[3] = \
					y * (image_x_size // step) + (x - 1), \
						1
						
						
			color = \
				image.getpixel(
					(x * step + 5, \
						image_y_size - (y * step + 5))
				)
				
			if color == (255, 255, 255):
				polygon_impossibility = 0.01
			elif color == (255, 255, 128):
				polygon_impossibility = 2.5
			elif color == (128, 255, 128):
				polygon_impossibility = 7
			else:
				polygon_impossibility = 10
				
				
				
			polygons_records.append({
				'points':        polygon_points,
				'relations':     polygon_relations,
				'impossibility': polygon_impossibility
			})
			
			
			
			
			
	def form_csv_records():
		polygons_number = len(polygons_records)
		
		for polygon_record_index in range(polygons_number):
			polygon_record        = polygons_records[polygon_record_index]
			polygon_points        = list(polygon_record['points'])
			polygon_relations     = dict(polygon_record['relations'])
			polygon_impossibility = polygon_record['impossibility']
			
			
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
			
			
			yield vertices_record, relations_record, polygon_impossibility
			
			
	csv_file_writer = writer(csv_file, delimiter = ';')
	
	csv_file_writer.writerows(
		form_csv_records()
	)
	