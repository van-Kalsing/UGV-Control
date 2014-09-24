import sys





def prepare_parser():
	import argparse
	
	
	
	parser = \
		argparse.ArgumentParser(
			description = \
				"Планирование пути наземного беспилотного транспортного\
					средства (роботизированной платформы)"
		)
		
	required_arguments = parser.add_argument_group("required arguments")
	
	
	
	parser.add_argument(
		"-m", "--map",
		type    = argparse.FileType("r"),
		default = sys.stdin,
		metavar = ("path"),
		help    = \
			"Имя файла, содержащего карту местности, используемую для\
				совершения планирования пути. В случае отсутствия опции, чтение\
				карты производится из стандартного потока ввода"
	)
	
	
	required_arguments.add_argument(
		"-s", "--start",
		nargs    = 2,
		type     = float,
		required = True,
		metavar  = ("x", "y"),
		help     = "Координаты <x, y> исходного положения платформы"
	)
	
	
	required_arguments.add_argument(
		"-g", "--goal",
		nargs    = 2,
		type     = float,
		required = True,
		metavar  = ("x", "y"),
		help     = "Координаты <x, y> целевого положения платформы"
	)
	
	
	parser.add_argument(
		"-o", "--output",
		type    = argparse.FileType("w"),
		default = sys.stdout,
		metavar = ("path"),
		help    = \
			"Имя файла, в который производится запись результатов планирования\
				пути. В случае отсутствия опции, запись результатов\
				производится в стандартный потока вывода"
	)
	
	
	parser.add_argument(
		"--visualization",
		type    = argparse.FileType("w"),
		metavar = ("path"),
		help    = \
			"Имя файла, в который производится запись изображения,\
				визуализирующего спланированный путь"
	)
	
	
	
	return parser
	
	
	
	
	
def build_surface(arguments):
	from planning.surface.surface_building import build_surface
	
	
	
	surface = \
		build_surface(
			arguments.map,
			0.0001
		)
		
		
	return surface
	
	
	
	
	
def plan_path(surface, arguments):
	from planning.planning.global_planning.planning \
		import PlanningParameters, \
					plan
					
	from planning.surface.polygon import Polygon
	
	
	
	#
	initial_point_x, initial_point_y = tuple(arguments.start)
	initial_polygon = \
		Polygon(
			[
				(10 * (initial_point_x // 10),      10 * (initial_point_y // 10),      0),
				(10 * (initial_point_x // 10) + 10, 10 * (initial_point_y // 10),      0),
				(10 * (initial_point_x // 10) + 10, 10 * (initial_point_y // 10) + 10, 0),
				(10 * (initial_point_x // 10),      10 * (initial_point_y // 10) + 10, 0),
			],
			0.0
		)
		
	final_point_x, final_point_y = tuple(arguments.goal)
	final_polygon = \
		Polygon(
			[
				(10 * (final_point_x // 10),      10 * (final_point_y // 10),      0),
				(10 * (final_point_x // 10) + 10, 10 * (final_point_y // 10),      0),
				(10 * (final_point_x // 10) + 10, 10 * (final_point_y // 10) + 10, 0),
				(10 * (final_point_x // 10),      10 * (final_point_y // 10) + 10, 0),
			],
			0.0
		)
		
		
		
	# Установка параметров планирования пути
	planning_parameters                 = PlanningParameters()
	planning_parameters.surface         = surface
	planning_parameters.planner         = "a-star-planner"
	# planning_parameters.planner         = "progressive-a-star-planner"
	# planning_parameters.planner         = "ant-colony-planner"
	planning_parameters.initial_polygon = initial_polygon #list(surface.polygons)[0]
	planning_parameters.final_polygon   = final_polygon
	planning_parameters.smoothing_depth = 1
	
	# Планирование пути
	planning_result = plan(planning_parameters)
	
	
	
	return planning_result
	
	
	
	
	
def visualize_path(planning_result, surface, arguments):
	from planning.visualization.visualization import create_svg
	
	
	
	controls_sequence, cost = planning_result
	
	create_svg(
		arguments.visualization,
		surface,
		controls_sequence
	)
	
	
	
	
	
if __name__ == "__main__":
	import importlib
	
	
	
	def check_module_presence(module_name):
		is_module_present = True
		
		try:
			if importlib.find_loader(module_name) is None:
				is_module_present = False
		except ValueError:
			is_module_present = False
			
			
		return is_module_present
		
		
		
	# Проверка наличия требуемых модулей
	required_modules_names       = ["numpy"]
	are_required_modules_present = True
	
	for required_module_name in required_modules_names:
		if not check_module_presence(required_module_name):
			sys.stderr.write(
				"Ошибка: для работы программы требуется %s\n"
					% required_module_name
			)
			
			are_required_modules_present = False
			
			
	if not are_required_modules_present:
		exit()
		
		
		
	# Чтение параметров командной строки
	parser    = prepare_parser()
	arguments = parser.parse_args()
	
	
	
	# Чтение карты местности
	surface = build_surface(arguments)
	
	
	
	# Планирование глобального пути
	planning_result    = plan_path(surface, arguments)
	states_sequence, _ = planning_result
	
	
	for state in states_sequence:
		polygon           = state.polygons_sequence[-1]
		map_polygon_index = surface.get_map_polygon_index(polygon)
		
		arguments.output.write("%s\n" % map_polygon_index)
		
		
		
	#!!!!!<Временно>
	from planning.planning.local_planning.trajectory_planning import plan
	polygons_sequence = \
		[state.polygons_sequence[-1] for state in states_sequence]
	plan(surface, states_sequence, tuple(arguments.start), tuple(arguments.goal))
	#!!!!!</Временно>
	# Визуализация
	if arguments.visualization is not None:
		if not check_module_presence("svgwrite"):
			sys.stderr.write(
				"Ошибка: для визуализации спланированного пути требуется" \
					+ " svgwrite\n"
			)
		else:
			visualize_path(planning_result, surface, arguments)
			