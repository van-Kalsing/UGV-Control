from planning.planning.local_planning.geometry.line import Line

import cmath
import math







# Нужен рефакторинг
def compute_segment(polygon, start_state, goal_state, factor):
	s, delta_s = start_state
	g, delta_g = goal_state
	
	
	
	
	
	# Проверка исходной и целевой точек на принадлежность полигону
	if (not polygon.is_inner_point(s)) or (not polygon.is_inner_point(g)):
		return None
		
		
		
		
		
	# Определение коэффициентов прямых
	ls, lg = \
		Line.from_direction(s, delta_s), \
			Line.from_direction(g, delta_g)
			
			
	# Определение центральной точки
	if not Line.are_parallel(ls, lg):
		# Определение точки пересечения прямых
		o = Line.compute_intersection(ls, lg)
		
	elif not Line.are_equivalent(ls, lg):
		if delta_s / abs(delta_s) == delta_g / abs(delta_g):
			return None
		else:
			o = (s + g) / 2.0
			
	else:
		if delta_s / abs(delta_s) == delta_g / abs(delta_g):
			if ((g - s) / delta_s).real < 0.0:
				return None
				
				
			def trajectory(parameter):
				parameter = max(parameter, 0.0)
				parameter = min(parameter, 1.0)
				
				return parameter * (g - s) + s
				
			trajectory_length = abs(g - s)
			
			
			return trajectory_length, trajectory
		else:
			return None
			
			
	# Определение центра связующей окружности
	c = factor * (delta_s / abs(delta_s) - delta_g / abs(delta_g)) + o
	
	
	# Определение коэффициентов перпендикулярных прямых
	lps = ls.compute_perpendicular(c)
	lpg = lg.compute_perpendicular(c)
	
	
	# Определение точек касания и радиуса окружности
	rs = Line.compute_intersection(ls, lps)
	rg = Line.compute_intersection(lg, lpg)
	r  = abs(rs - c)
	if r < 1.0:
		return None
	
	
	# Проверка существования траектории
	is_existing  = ((rs - s) / delta_s).real >= 0.0
	is_existing &= ((g - rg) / delta_g).real >= 0.0
	
	if not is_existing:
		return None
		
		
		
		
		
	# Построение дуги
	def compute_rotation_angle(start_point, final_point, rotation_direction):
		start_angle = cmath.phase(start_point - c)
		final_angle = cmath.phase(final_point - c)
		
		if rotation_direction > 0:
			rotation_angle = \
				(final_angle - start_angle + 2 * math.pi) \
					% (2 * math.pi)
		else:
			rotation_angle = \
				(start_angle - final_angle + 2 * math.pi) \
					% (2 * math.pi)
					
			rotation_angle *= -1.0
			
		return rotation_angle
		
		
	if r != 0.0:
		# Направление обхода дуги
		angle_direction = \
			cmath.phase(
				(rs - c) \
					/ (rs - delta_s - c)
			)
			
			
		# Вычисление угла дуги
		max_delta_angle = compute_rotation_angle(rs, rg, angle_direction)
		
		
		# Проверка дуги
		intersections = polygon.compute_circle_intersections(c, r)
		
		for intersection in intersections:
			intersection_angle = \
				compute_rotation_angle(
					rs,
					intersection,
					angle_direction
				)
				
				
			if 0.0 < abs(intersection_angle) < abs(max_delta_angle):
				# Траектория выходит за полигон
				return None
				
				
		arc_point = (rs - c) * cmath.rect(1.0, max_delta_angle / 2.0) + c
				
		if not polygon.is_inner_point(arc_point):
			# Траектория выходит за полигон
			return None
	else:
		max_delta_angle = 0.0
		
		if not polygon.is_inner_point(c):
			# Траектория выходит за полигон
			return None
			
			
			
			
			
	# Вычисление длины траектории
	trajectory_length  = abs(rs - s)
	trajectory_length += abs(g - rg)
	trajectory_length += r * abs(max_delta_angle)
	
	
	# Построение траектории
	def trajectory(parameter):
		parameter  = max(parameter, 0.0)
		parameter  = min(parameter, 1.0)
		parameter *= 3.0
		
		
		if 0.0 <= parameter < 1.0:
			return parameter * (rs - s) + s
			
		elif 1.0 <= parameter < 2.0:
			rotation = \
				cmath.rect(
					1.0,
					(parameter - 1.0) * max_delta_angle
				)
				
			return (rs - c) * rotation + c
			
		else:
			return (parameter - 2.0) * (g - rg) + rg
			
			
	return trajectory_length, trajectory
	
	
	
def compute_shortest_segment(polygon, start_state, goal_state, factors):
	shortest_segment        = None
	shortest_segment_length = None
	
	
	for factor in factors:
		computing_result = \
			compute_segment(
				polygon,
				start_state,
				goal_state,
				factor
			)
			
		if computing_result is not None:
			trajectory_length, trajectory = computing_result
			
			if shortest_segment is None:
				need_update = True
			else:
				need_update = trajectory_length < shortest_segment_length
				
			if need_update:
				shortest_segment        = trajectory
				shortest_segment_length = trajectory_length
				
				
	if shortest_segment is not None:
		computing_result = shortest_segment_length, shortest_segment
	else:
		computing_result = None
		
		
	return computing_result
	