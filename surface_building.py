from csv             import reader
from re              import compile
from surface.polygon import Polygon, Edge
from surface.surface import Surface







def build_surface(file_name, equivalence_distance):
	surface  = Surface(equivalence_distance)
	polygons = []
	
	
	
	vertices_pattern = \
		compile(
			'\(\s*' \
				+ '(-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?)\s*,\s*' \
				+ '(-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?)\s*,\s*' \
				+ '(-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?)' \
				+ '\s*\)'
		)
		
	relation_pattern = \
		compile(
			'\(\s*' \
				+ '([0-9]+)\s*,\s*([0-9]+)\s*:\s*([0-9]+)' \
				+ '\s*\)'
		)
		
		
	def get_polygon(vertices_record, impassibility_record):
		def get_vertex(vertex_record):
			coordinates = \
				[float(coordinate_record) for coordinate_record \
					in vertex_record]
					
			return coordinates
			
		vertices = \
			[get_vertex(vertex_record) for vertex_record \
				in vertices_pattern.findall(vertices_record)]
				
				
		# impassibility_record = impassibility_record.strip()
		# impassibility_record = impassibility_record.lower()
		
		# if impassibility_record == 'infinity':
		impassibility = float(impassibility_record)
		
		
		polygon = \
			Polygon(
				vertices,
				impassibility
			)
			
		return polygon
		
		
	def get_relations(polygon, relations_record):
		def get_relation(relation_record):
			def get_edge(polygon, edge_number):
				if edge_number < polygon.vertices_number - 1:
					edge = Edge(polygon, edge_number, edge_number + 1)
				else:
					edge = Edge(polygon, edge_number, 0)
					
				return edge
				
				
			first_polygon_edge_number  = int(relation_record[0])
			second_polygon_number      = int(relation_record[1])
			second_polygon_edge_number = int(relation_record[2])
			
			first_edge  = get_edge(polygon, first_polygon_edge_number)
			second_edge = \
				get_edge(
					polygons[second_polygon_number],
					second_polygon_edge_number
				)
				
				
			return first_edge, second_edge
			
			
		relations = \
			[get_relation(relation_record) for relation_record \
				in relation_pattern.findall(relations_record)]
				
		return relations
		
		
		
	#!!!!! Обрабатывать исключения в случае ошибки файла
	with open(file_name) as csv_file:
		csv_file_reader = reader(csv_file, delimiter = ';')
		
		for csv_record in csv_file_reader:
			vertices_record      = csv_record[0]
			relations_record     = csv_record[1]
			impassibility_record = csv_record[2]
			
			polygon   = get_polygon(vertices_record, impassibility_record)
			relations = get_relations(polygon, relations_record)
			
			
			surface.add_polygon(polygon)
			
			for first_edge, second_edge in relations:
				surface.set_relation(first_edge, second_edge)
				
				
			polygons.append(polygon)
		# try:
		# except:
		# 	raise Exception() #!!!!!
			
			
	return surface
	