from planning.global_planning.planning \
	import PlanningParameters, \
				plan
				
from surface_building import build_surface
from surface.polygon  import Polygon, Point
from surface.surface  import Surface

import resource
import visualization.visualization as visualization





def measure_time_usage(function, *args, **kwargs):
	initial_resource_usage = resource.getrusage(resource.RUSAGE_SELF)
	initial_time_usage     = \
		initial_resource_usage.ru_utime \
			+ initial_resource_usage.ru_stime
			
	result = function(*args, **kwargs)
	
	resource_usage = resource.getrusage(resource.RUSAGE_SELF)
	time_usage     = \
		resource_usage.ru_utime \
			+ resource_usage.ru_stime
			
			
	return result, time_usage - initial_time_usage
	
	
	
# Загрузка карты местности
surface, surface_building_time = \
	measure_time_usage(
		build_surface,
		'output/surface.csv',
		0.0001
	)
	
# print('Время загрузки карты:     %s' % surface_building_time)



# Установка параметров планирования пути
planning_parameters                 = PlanningParameters()
planning_parameters.surface         = surface
planning_parameters.planner         = "ant-colony-planner"
# planning_parameters.planner         = "a-star-planner"
planning_parameters.initial_polygon = list(surface.polygons)[0]
planning_parameters.final_polygon   = list(surface.polygons)[-1]
planning_parameters.smoothing_depth = 1



# Планирование пути
planning_result, planning_time = \
	measure_time_usage(
		plan,
		planning_parameters
	)
	
controls_sequence, cost = planning_result

# print('Время планирования пути:  %s' % planning_time)
# print('Стоимость пути:           %s' % cost)



# Визуализация
visualization.create_svg("output/output.svg", surface, controls_sequence)
