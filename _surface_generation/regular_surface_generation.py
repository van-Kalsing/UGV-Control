from surface.polygon import Polygon, Edge
from surface.surface import Surface







def generate_region(surface, horizontal_index, vertical_index):
	def shift_polygon_vertices(polygon_vertices):
		offset_polygon_vertices = \
			[(x + horizontal_index, y + vertical_index, z) for x, y, z \
				in polygon_vertices]
				
		return offset_polygon_vertices
		
	polygon_0_vertices = [(0.0, 0.0, 0.0), (0.5, 0.5, 0.0), (1.0, 0.0, 0.0)]
	polygon_1_vertices = [(0.0, 0.0, 0.0), (0.5, 0.5, 0.0), (0.0, 1.0, 0.0)]
	polygon_2_vertices = [(1.0, 1.0, 0.0), (0.5, 0.5, 0.0), (0.0, 1.0, 0.0)]
	polygon_3_vertices = [(1.0, 1.0, 0.0), (0.5, 0.5, 0.0), (1.0, 0.0, 0.0)]
	
	
	a = horizontal_index == 9 and vertical_index < 15 and vertical_index > 5
	a |= horizontal_index == 4 and vertical_index < 20 and vertical_index > 10
	a |= vertical_index == 15 and horizontal_index < 15 and horizontal_index > 5
	
	a |= horizontal_index == 0 and vertical_index == 2
	a |= horizontal_index == 1 and vertical_index == 2
	a |= horizontal_index == 2 and vertical_index == 2
	a |= horizontal_index == 2 and vertical_index == 1
	a |= horizontal_index == 2 and vertical_index == 0
	if a:
		impassability = 4000.3
	else:
		impassability = 1.0
		
	polygon_0 = Polygon(shift_polygon_vertices(polygon_0_vertices), impassability)
	polygon_1 = Polygon(shift_polygon_vertices(polygon_1_vertices), impassability)
	polygon_2 = Polygon(shift_polygon_vertices(polygon_2_vertices), impassability)
	polygon_3 = Polygon(shift_polygon_vertices(polygon_3_vertices), impassability)
	
	edge_0_0 = Edge(polygon_0, 2, 0)
	edge_0_1 = Edge(polygon_0, 0, 1)
	edge_0_2 = Edge(polygon_0, 1, 2)
	edge_1_0 = Edge(polygon_1, 0, 2)
	edge_1_1 = Edge(polygon_1, 2, 1)
	edge_1_2 = Edge(polygon_1, 1, 0)
	edge_2_0 = Edge(polygon_2, 2, 0)
	edge_2_1 = Edge(polygon_2, 0, 1)
	edge_2_2 = Edge(polygon_2, 1, 2)
	edge_3_0 = Edge(polygon_3, 0, 2)
	edge_3_1 = Edge(polygon_3, 2, 1)
	edge_3_2 = Edge(polygon_3, 1, 0)
	
	
	surface.add_polygon(polygon_0)
	surface.add_polygon(polygon_1)
	surface.add_polygon(polygon_2)
	surface.add_polygon(polygon_3)
	
	surface.set_relation(edge_0_1, edge_1_2)
	surface.set_relation(edge_1_1, edge_2_2)
	surface.set_relation(edge_2_1, edge_3_2)
	surface.set_relation(edge_3_1, edge_0_2)
	
	
	region_contact_points = \
		[
			edge_0_0,
			edge_1_0,
			edge_2_0,
			edge_3_0
		]
		
	return region_contact_points
	
	
	
	
	
def generate_regular_surface(width, height, equivalence_distance):
	surface = Surface(equivalence_distance)
	
	
	last_regions_contact_edges_row    = []
	current_regions_contact_edges_row = []
	
	for vertical_index in range(height):
		for horizontal_index in range(width):
			region_contact_edges = \
				generate_region(
					surface,
					horizontal_index,
					vertical_index
				)
				
				
			if last_regions_contact_edges_row:
				surface.set_relation(
					last_regions_contact_edges_row[horizontal_index][2],
					region_contact_edges[0]
				)
				
			if current_regions_contact_edges_row:
				surface.set_relation(
					current_regions_contact_edges_row[-1][3],
					region_contact_edges[1]
				)
				
				
			current_regions_contact_edges_row.append(region_contact_edges)
			
		last_regions_contact_edges_row    = current_regions_contact_edges_row
		current_regions_contact_edges_row = []
		
		
	return surface
	