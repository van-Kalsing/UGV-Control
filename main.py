from control.planning.global_planning.planning \
	import PlanningParameters, \
				Planner
				
# from surface_generation.regular_surface_generation \
# 	import generate_regular_surface
	
from surface.polygon             import Polygon, Point
from surface.surface             import Surface
from time                        import time
from visualization.visualization import create_svg


# surface = Surface(equivalence_distance = 0.1)

# polygon11 = Polygon([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)], 1.0)
# polygon12 = Polygon([(0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 1.0, 0.0)], 5.0)
# polygon21 = Polygon([(0.0, 2.0, 0.0), (0.0, 1.0, 0.0), (1.0, 1.0, 0.0)], 5.0)
# polygon22 = Polygon([(0.0, 2.0, 0.0), (1.0, 2.0, 0.0), (1.0, 1.0, 0.0)], 1.0)
# polygon31 = Polygon([(2.0, 2.0, 0.0), (1.0, 2.0, 0.0), (1.0, 1.0, 0.0)], 1.0)
# polygon32 = Polygon([(2.0, 2.0, 0.0), (2.0, 1.0, 0.0), (1.0, 1.0, 0.0)], 5.0)
# polygon41 = Polygon([(2.0, 0.0, 0.0), (2.0, 1.0, 0.0), (1.0, 1.0, 0.0)], 1.0)
# polygon42 = Polygon([(2.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)], 1.0)

# surface.add_polygon(polygon11)
# surface.add_polygon(polygon12)
# surface.add_polygon(polygon21)
# surface.add_polygon(polygon22)
# surface.add_polygon(polygon31)
# surface.add_polygon(polygon32)
# surface.add_polygon(polygon41)
# surface.add_polygon(polygon42)

# surface.set_relation(Point(polygon11, [(0, 1.0)]), Point(polygon12, [(0, 1.0)]))
# surface.set_relation(Point(polygon11, [(2, 1.0)]), Point(polygon12, [(2, 1.0)]))
# surface.set_relation(Point(polygon12, [(1, 1.0)]), Point(polygon21, [(1, 1.0)]))
# surface.set_relation(Point(polygon12, [(2, 1.0)]), Point(polygon21, [(2, 1.0)]))
# surface.set_relation(Point(polygon21, [(0, 1.0)]), Point(polygon22, [(0, 1.0)]))
# surface.set_relation(Point(polygon21, [(2, 1.0)]), Point(polygon22, [(2, 1.0)]))
# surface.set_relation(Point(polygon22, [(1, 1.0)]), Point(polygon31, [(1, 1.0)]))
# surface.set_relation(Point(polygon22, [(2, 1.0)]), Point(polygon31, [(2, 1.0)]))
# surface.set_relation(Point(polygon31, [(0, 1.0)]), Point(polygon32, [(0, 1.0)]))
# surface.set_relation(Point(polygon31, [(2, 1.0)]), Point(polygon32, [(2, 1.0)]))
# surface.set_relation(Point(polygon32, [(1, 1.0)]), Point(polygon41, [(1, 1.0)]))
# surface.set_relation(Point(polygon32, [(2, 1.0)]), Point(polygon41, [(2, 1.0)]))
# surface.set_relation(Point(polygon41, [(0, 1.0)]), Point(polygon42, [(0, 1.0)]))
# surface.set_relation(Point(polygon41, [(2, 1.0)]), Point(polygon42, [(2, 1.0)]))
# surface.set_relation(Point(polygon42, [(1, 1.0)]), Point(polygon11, [(1, 1.0)]))
# surface.set_relation(Point(polygon42, [(2, 1.0)]), Point(polygon11, [(2, 1.0)]))


# p1, = surface.get_adjacent_points(Point(polygon11, [(1, 0.5), (2, 0.5)]))
# p2, = surface.get_adjacent_points(Point(polygon42, [(1, 0.5), (2, 0.5)]))
# p3, = surface.get_adjacent_points(Point(polygon11, [(1, 1.0)]))
# p4, = surface.get_adjacent_points(Point(polygon42, [(1, 1.0)]))
# print(p1.polygon)
# print(p2.polygon)
# print(p3.polygon)
# print(p4.polygon)
# exit()



# start_time = round(time() * 1000)
# surface = generate_regular_surface(20, 20, equivalence_distance = 0.001)
# end_time = round(time() * 1000)
# print(end_time - start_time)


# initial_polygon = Polygon([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 0.5, 0.0)], 1.0)
# final_polygon   = Polygon([(19.0, 19.0, 0.0), (20.0, 19.0, 0.0), (19.5, 19.5, 0.0)], 1.0)
# planning_parameters = PlanningParameters()
# planning_parameters.surface         = surface
# planning_parameters.initial_polygon = initial_polygon
# planning_parameters.final_polygon   = final_polygon

# planner = Planner(planning_parameters)
# controls_sequence_generator = planner.plan_controls_sequence()




# start_time = round(time() * 1000)
# controls_sequence = next(controls_sequence_generator)
# end_time = round(time() * 1000)
# print(end_time - start_time)
# create_svg("test1.svg", surface, controls_sequence)



# need_planning = True
# while need_planning:
# 	start_time = round(time() * 1000)
# 	controls_sequence = next(controls_sequence_generator)
# 	end_time = round(time() * 1000)
# 	print(end_time - start_time)
# 	create_svg("test1.svg", surface, controls_sequence)
	
# 	need_planning = input() != 'q'
	
	
	
# start_time = round(time() * 1000)
# for _ in range(1000):
# 	controls_sequence = next(controls_sequence_generator)
	
# end_time = round(time() * 1000)
# print(end_time - start_time)
# create_svg("test1.svg", surface, controls_sequence)





# controls_sequence2 = controls_sequence_generator.__next__()
# controls_sequence3 = controls_sequence_generator.__next__()
# print(len(controls_sequence1))
# print(len(controls_sequence2))
# print(len(controls_sequence3))


#create_svg("test1.svg", surface, controls_sequence1)
#create_svg("test1.svg", surface)
# create_svg("test2.svg", surface)
# create_svg("test3.svg", surface)


controls_sequence = None
sn = None


from surface_generation import generate_surface
from surface_building import build_surface

# start_time = round(time() * 1000)
# generate_surface('surface.csv', 20, 20, 1.0)
# end_time = round(time() * 1000)
# print('Время генерации карты:    %s' % (end_time - start_time))


start_time = round(time() * 1000)
surface = build_surface('surface.csv', 0.0001)
end_time = round(time() * 1000)
print('Время загрузки карты:     %s' % (end_time - start_time))


planning_parameters = PlanningParameters()
planning_parameters.surface         = surface
planning_parameters.initial_polygon = list(surface.polygons)[0]
planning_parameters.final_polygon   = list(surface.polygons)[2] #Polygon([(63.0, 0.0, 0.0), (64.0, 0.0, 0.0), (63.0, 1.0, 0.0)], 1.0)

planner = Planner(planning_parameters)
start_time = round(time() * 1000)
controls_sequence, cost, sn = planner.plan_controls_sequence()
end_time = round(time() * 1000)
print('Время планирования пути:  %s' % (end_time - start_time))
print('Стоимость пути:           %s' % cost)

create_svg("test1.svg", surface, controls_sequence, sn)
