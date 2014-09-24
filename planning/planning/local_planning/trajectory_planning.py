from planning.planning.local_planning.geometry.polygon \
	import Polygon
	
from planning.planning.local_planning.segment_planning \
	import compute_shortest_segment
	
from planning.planning.local_planning.visualization \
	import visualize_trajectory
	
from planning.utilities.filter import Filter

import collections
import abc
import cmath
import math







class State(metaclass = abc.ABCMeta):
	@abc.abstractproperty
	def predecessor_geometry_state(self):
		pass
		
		
	@abc.abstractproperty
	def predecessor_polygon(self):
		pass
		
		
	@abc.abstractproperty
	def successor_geometry_state(self):
		pass
		
		
	@abc.abstractproperty
	def successor_polygon(self):
		pass
		
		
		
		
		
class PointState(State):
	def __init__(self, polygon, point, direction, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить
		self.__polygon   = polygon
		self.__point     = point
		self.__direction = direction
		
		
		
		
		
	@property
	def predecessor_geometry_state(self):
		return self.__point, self.__direction
		
		
		
	@property
	def predecessor_polygon(self):
		return self.__polygon
		
		
		
	@property
	def successor_geometry_state(self):
		return self.__point, self.__direction
		
		
		
	@property
	def successor_polygon(self):
		return self.__polygon
		
		
		
def generate_point_states(polygon, point, rotations_number):
	point_states = []
	
	
	base_direction = 1.0 + 0.0j
	rotation       = 0.0
	
	for rotation_index in range(rotations_number):
		rotation  = 2.0 * math.pi * rotation_index / rotations_number
		direction = base_direction * cmath.rect(1.0, rotation)
		
		point_state = PointState(polygon, point, direction)
		point_states.append(point_state)
		
		
	return point_states
	
	
	
	
	
class EdgeState(State):
	def __init__(self, polygons, points, directions, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		#!!!!! Проверить
		self.__predecessor_polygon,   self.__successor_polygon   = polygons
		self.__predecessor_point,     self.__successor_point     = points
		self.__predecessor_direction, self.__successor_direction = directions
		
		
		
		
		
	@property
	def predecessor_geometry_state(self):
		return self.__predecessor_point, self.__predecessor_direction
		
		
		
	@property
	def predecessor_polygon(self):
		return self.__predecessor_polygon
		
		
		
	@property
	def successor_geometry_state(self):
		return self.__successor_point, self.__successor_direction
		
		
		
	@property
	def successor_polygon(self):
		return self.__successor_polygon
		
		
		
def generate_edge_states(polygons, edges_indexes, samples_numbers):
	def get_edge(polygon, edge_index):
		first_vertex_index  = edge_index
		second_vertex_index = (edge_index + 1) % len(polygon.vertices)
		
		if polygon.orientation < 0.0:
			first_vertex_index, second_vertex_index = \
				second_vertex_index, first_vertex_index
				
				
		first_vertex, second_vertex = \
			polygon.vertices[first_vertex_index], \
				polygon.vertices[second_vertex_index]
				
				
		return first_vertex, second_vertex
		
		
	def get_geometry_state(edge, translation, rotation):
		first_vertex, second_vertex = edge
		
		
		point = \
			translation * second_vertex \
				+ (1.0 - translation) * first_vertex
				
		direction = \
			(second_vertex - first_vertex) \
				* cmath.rect(1.0, rotation)
				
				
		return point, direction
		
		
		
	edge_states = []
	
	
	
	predecessor_polygon,    successor_polygon    = polygons
	predecessor_edge_index, successor_edge_index = edges_indexes
	
	predecessor_edge, successor_edge = \
		get_edge(predecessor_polygon, predecessor_edge_index), \
			get_edge(successor_polygon, successor_edge_index)
			
			
	translations_number, rotations_number = samples_numbers
	
	for translation_number in range(translations_number):
		translation = \
			min(
				translation_number / (translations_number - 1),
				1.0
			)
			
		for rotation_number in range(rotations_number):
			rotation = \
				min(
					math.pi * rotation_number / (rotations_number - 1),
					math.pi
				)
				
				
			predecessor_point, predecessor_direction = \
				get_geometry_state(
					predecessor_edge,
					1.0 - translation,
					rotation + math.pi
				)
				
			successor_point, successor_direction = \
				get_geometry_state(
					successor_edge,
					translation,
					rotation
				)
				
				
			edge_state = \
				EdgeState(
					(predecessor_polygon, successor_polygon),
					(predecessor_point, successor_point),
					(predecessor_direction, successor_direction),
				)
				
			edge_states.append(edge_state)
			
			
			
	return edge_states
	
	
	
	
	
	
	
_StateNode = \
	collections.namedtuple(
		"_StateNode",
		[
			"state",
			"predecessor_state_node",
			"segment",
			"estimation"
		]
	)
	
	
	
def optimize_transition(predecessor_states_nodes, successor_states):
	successor_states_nodes = []
	
	
	for successor_state in successor_states:
		successor_state_node_filter = \
			Filter(
				key = (lambda state_node: state_node.estimation)
			)
			
			
		for predecessor_state_node in predecessor_states_nodes:
			predecessor_state      = predecessor_state_node.state
			predecessor_estimation = predecessor_state_node.estimation
			
			
			computing_result = \
				compute_shortest_segment(
					successor_state.predecessor_polygon,
					predecessor_state.successor_geometry_state,
					successor_state.predecessor_geometry_state,
					factors
				)
				
			if computing_result is not None:
				segment_length, segment = computing_result
				estimation              = \
					segment_length \
						+ predecessor_estimation
						
				successor_state_node = \
					_StateNode(
						state                  = successor_state,
						predecessor_state_node = predecessor_state_node,
						segment                = segment,
						estimation             = estimation
					)
					
				successor_state_node_filter.check_element(successor_state_node)
				
				
		if successor_state_node_filter.contains_element:
			successor_states_nodes.append(
				successor_state_node_filter.minimal_element
			)
			
			
	return successor_states_nodes
	
	
	
def optimize_trajectory(states_groups):
	trajectory = None
	
	
	
	if states_groups:
		def generate_initial_state_node(state):
			state_node = \
				_StateNode(
					state                  = state,
					predecessor_state_node = None,
					segment                = None,
					estimation             = 0.0
				)
				
			return state_node
			
		open_states_nodes = \
			[generate_initial_state_node(initial_state) \
				for initial_state \
				in states_groups[0]]
				
				
		for states_group in states_groups[1:]:
			open_states_nodes = \
				optimize_transition(
					open_states_nodes,
					states_group
				)
				
				
				
		if open_states_nodes:
			best_goal_state_node_filter = \
				Filter(
					key = (lambda goal_state_node: goal_state_node.estimation)
				)
				
			best_goal_state_node_filter.check_elements(open_states_nodes)
			
			
			trajectory = []
			state_node = best_goal_state_node_filter.minimal_element
			
			while state_node.predecessor_state_node is not None:
				trajectory.insert(0, state_node.segment)
				state_node = state_node.predecessor_state_node
				
				
				
	return trajectory
	
	
	
	
	
	
	
factors = \
	[factor * 5.0 for factor in range(-20, 0)] \
		+ [factor * 5.0 for factor in range(1, 21)]
		
		
		
		
		
		
		
def plan(surface, states_sequence, start_point, goal_point):
	states_groups     = []
	polygons_sequence = []
	
	
	for state in states_sequence:
		vertices = \
			[complex(x_coordinate, y_coordinate) \
				for x_coordinate, y_coordinate, _ \
				in state.polygons_sequence[-1].vertices]
				
		polygon = Polygon(vertices)
		polygons_sequence.append(polygon)
		
		
		
	start_states = \
		generate_point_states(
			polygons_sequence[0],
			complex(*start_point),
			8
		)
		
	states_groups.append(start_states)
	
	
	last_polygon, last_state = \
		polygons_sequence[0], \
			states_sequence[0]
			
	for polygon, state in zip(polygons_sequence[1:], states_sequence[1:]):
		first_edge, second_edge = last_state.get_transfer(state)
		
		
		first_vertex_index  = first_edge.first_vertex_index
		second_vertex_index = first_edge.second_vertex_index
		
		if abs(second_vertex_index - first_vertex_index) == 1:
			first_edge_index = min(first_vertex_index, second_vertex_index)
		else:
			first_edge_index = max(first_vertex_index, second_vertex_index)
			
			
		first_vertex_index  = second_edge.first_vertex_index
		second_vertex_index = second_edge.second_vertex_index
		
		if abs(second_vertex_index - first_vertex_index) == 1:
			second_edge_index = min(first_vertex_index, second_vertex_index)
		else:
			second_edge_index = max(first_vertex_index, second_vertex_index)
			
			
			
		intermediate_states = \
			generate_edge_states(
				(last_polygon, polygon),
				(first_edge_index, second_edge_index),
				(8, 5)
			)
			
		states_groups.append(intermediate_states)
		
		
		
		last_polygon, last_state = polygon, state
		
		
	goal_states = \
		generate_point_states(
			polygons_sequence[-1],
			complex(*goal_point),
			8
		)
		
	states_groups.append(goal_states)
	
	
	
	trajectory = optimize_trajectory(states_groups)
	
	if trajectory is not None:
		visualize_trajectory(trajectory, polygons_sequence)
	else:
		print("Траектория не найдена")
		