import sys





def prepare_parser():
	import argparse
	
	
	
	parser = \
		argparse.ArgumentParser(
			description = \
				"Генерация карты местности на основе ее растрового изображения"
		)
		
		
		
	parser.add_argument(
		"-r", "--raster-map",
		type    = argparse.FileType("rb"),
		default = sys.stdin,
		metavar = ("path"),
		help    = \
			"Имя файла, содержащего изображение карты, используемого для\
				генерации карты местности. В случае отсутствия опции, чтение\
				изображения производится из стандартного потока ввода"
	)
	
	
	parser.add_argument(
		"-m", "--map",
		type    = argparse.FileType("w"),
		default = sys.stdout,
		metavar = ("path"),
		help    = \
			"Имя файла, в который производится запись сгенерированной карты\
				местности. В случае отсутствия опции, запись карты производится\
				в стандартный поток вывода"
	)
	
	
	# parser.add_argument(
	# 	"-s", "--step",
	# 	type    = int,
	# 	default = 1,
	# 	metavar = "step",
	# 	help    = \
	# 		"Шаг сетки, используемый при генерации карты. В случае отсутствия\
	# 			опции, используется значение '%(default)s'"
	# )
	
	
	
	return parser
	
	
	
	
	
def generate_surface(arguments):
	from surface_generation.surface_generation import generate_surface
	
	
	
	generate_surface(arguments.raster_map, arguments.map)
	
	
	
	
	
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
	required_modules_names       = ["PIL"]
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
	
	
	
	# Генерация карты местности
	generate_surface(arguments)
	