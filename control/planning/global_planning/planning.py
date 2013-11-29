from control.planning.global_planning.state_space import State
from queue                                        import PriorityQueue







class PlanningParameters:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__surface         = None
		self.__initial_polygon = None
		self.__final_polygon   = None
		
		
		
	def copy(self):
		planning_parameters = PlanningParameters()
		
		planning_parameters.__surface         = self.__surface
		planning_parameters.__initial_polygon = self.__initial_polygon
		planning_parameters.__final_polygon   = self.__final_polygon
		
		
		return planning_parameters
		
		
		
	def __eq__(self, planning_parameters):
		return True #!!!!!
		
		
	def __ne__(self, planning_parameters):
		return not self.__eq__(planning_parameters)
		
		
		
	@property
	def is_correct(self):
		is_correct = True
		
		
		is_correct &= self.__surface is not None
		is_correct &= self.__initial_polygon is not None
		is_correct &= self.__final_polygon is not None
		
		if is_correct:
			is_correct &= \
				self.__surface.contains_polygon(
					self.__initial_polygon
				)
				
			is_correct &= \
				self.__surface.contains_polygon(
					self.__final_polygon
				)
				
				
		return is_correct
		
		
		
	@property
	def surface(self):
		return self.__surface
		
		
	@surface.setter
	def surface(self, surface):
		self.__surface = surface
		
		
		
	@property
	def initial_polygon(self):
		return self.__initial_polygon
		
		
	@initial_polygon.setter
	def initial_polygon(self, initial_polygon):
		self.__initial_polygon = initial_polygon
		
		
		
	@property
	def final_polygon(self):
		return self.__final_polygon
		
		
	@final_polygon.setter
	def final_polygon(self, final_polygon):
		self.__final_polygon = final_polygon
		
		
		
		
		
		
		
class Planner:
	def __init__(self, planning_parameters, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		if not planning_parameters.is_correct:
			raise Exception() #!!!!!
			
			
		self.__planning_parameters = planning_parameters.copy()
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
	def plan_controls_sequence(self):
		def form_states_sequence(node):
			states_sequence      = list()
			states_sequence_cost = node['cost']
			
			while node is not None:
				states_sequence.insert(
					0,
					node['state']
				)
				
				node = node['predecessor']
				
				
			return states_sequence, states_sequence_cost
			
			
		covered_states = dict()
		
		initial_state = \
			State(
				self.__planning_parameters.initial_polygon,
				self.__planning_parameters
			)
			
		final_state = \
			State(
				self.__planning_parameters.final_polygon,
				self.__planning_parameters
			)
			
			
		initial_node  = \
			{
				'state':       initial_state,
				'cost':        0.0,
				'estimation':  0, #initial_state.estimation,
				'predecessor': None,
				'successors':  list()
			}
			
		nodes_number = 1
		
		
		peripheral_nodes = PriorityQueue()
		
		peripheral_nodes.put(
			(initial_node['cost'] + initial_node['estimation'], \
				nodes_number,
				initial_node)
		)
		
		
		while not peripheral_nodes.empty():
			_, _, peripheral_node = peripheral_nodes.get()
			
			peripheral_node_state      = peripheral_node['state']
			peripheral_node_cost       = peripheral_node['cost']
			peripheral_node_successors = peripheral_node['successors']
			
			
			if peripheral_node_state not in covered_states:
				if peripheral_node_state == final_state:
					return form_states_sequence(peripheral_node)
					
					
				covered_states[peripheral_node_state] = peripheral_node
				
				for successor in peripheral_node_state.successors:
					successor_node = \
						{
							'state':       successor,
							'cost':        peripheral_node_cost + 1, #!!!!!
							'estimation':  0, #successor.estimation,
							'predecessor': peripheral_node,
							'successors':  list()
						}
						
					nodes_number += 1
					
					
					peripheral_node_successors.append(successor_node)
					peripheral_nodes.put(
						(successor_node['cost'] \
								+ successor_node['estimation'], \
							nodes_number, \
							successor_node)
					)
			else:
				pass #!!!!!
				
				
		return None
		