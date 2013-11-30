from control.planning.global_planning.state_space \
	import State, \
				compute_sequence_cost
				
from queue import PriorityQueue







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
				
				try:
					node = covered_states[next(iter(node['predecessors']))] #!!!!!
				except:
					break
					
					
			return states_sequence, states_sequence_cost, sn #!!!!! Убрать sn
			
			
			
		def form_output_transfers(state):
			output_transfers = list()
			
			
			for output_transfer_successor in state.successors:
				output_transfer_cost = \
					compute_sequence_cost(
						[state, output_transfer_successor],
						self.__planning_parameters
					)
					
				output_transfer = \
					{
						'cost':        output_transfer_cost,
						'predecessor': state,
						'successor':   output_transfer_successor
					}
					
				output_transfers.append(output_transfer)
				
				
			return output_transfers
			
			
		def form_successor_node(predecessor_node, transfer):
			successor      = transfer['successor']
			successor_node = dict()
			
			
			successor_node['state']           = successor
			successor_node['predecessors']    = { predecessor_node['state'] }
			successor_node['input_transfers'] = [ transfer ]
			
			successor_node['cost'] = \
				predecessor_node['cost'] \
					+ transfer['cost']
					
			successor_node['output_transfers'] = \
				form_output_transfers(
					successor
				)
				
				
			return successor_node
			
			
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
			
			
		initial_node = \
			{
				'state':            initial_state,
				'cost':             0.0,
				'predecessors':     set(),
				'input_transfers':  set(),
				'output_transfers': form_output_transfers(initial_state),
			}
			
		covered_states = \
			{
				initial_state: initial_node
			}
			
			
			
		peripheral_transfers = PriorityQueue()
		
		nodes_number = 0
		
		for output_transfer in initial_node['output_transfers']:
			nodes_number += 1
			
			peripheral_transfers.put(
				(output_transfer['cost'] \
						+ output_transfer['successor'].estimation, \
					nodes_number,
					output_transfer)
			)
			
			
		n = 0 #!!!!! Временно
		sn = {} #!!!!! Временно
		while not peripheral_transfers.empty():
			_, _, transfer = peripheral_transfers.get()
			
			successor      = transfer['successor']
			successor_node = covered_states.get(successor)
			
			
			#!!!!! <Временно>
			n+=1
			if successor not in sn:
				sn[successor] = [n] #!!!!! Временно
			else:
				sn[successor].append(n) #!!!!! Временно
			#!!!!! </Временно>
			if successor_node is None:
				predecessor      = transfer['predecessor']
				predecessor_node = covered_states[predecessor]
				
				successor_node = \
					form_successor_node(
						predecessor_node,
						transfer
					)
					
				covered_states[successor] = successor_node
				
				for output_transfer in successor_node['output_transfers']:
					nodes_number += 1
					
					peripheral_transfers.put(
						(successor_node['cost'] \
								+ output_transfer['cost'] \
								+ output_transfer['successor'].estimation, \
							nodes_number,
							output_transfer)
					)
			else:
				pass #!!!!!
				
				
			if successor == final_state:
				return form_states_sequence(successor_node)
				
				
		return None
		# for successor in peripheral_node_state.successors:
		# 	crossing_cost = \
		# 		compute_sequence_cost(
		# 			(peripheral_node_state, \
		# 				successor),
		# 			self.__planning_parameters
		# 		)
				
		# 	successor_node_cost = peripheral_node_cost + crossing_cost
			
			
		# 	successor_node = \
		# 		{
		# 			'state':       successor,
		# 			'cost':        successor_node_cost,
		# 			'estimation':  successor.estimation,
		# 			'predecessor': peripheral_node,
		# 			'successors':  list()
		# 		}
				
		# 	nodes_number += 1
			
			
		# 	peripheral_node_successors.append(successor_node)
		# 	peripheral_transfers.put(
		# 		(successor_node['cost'] \
		# 				+ successor_node['estimation'], \
		# 			nodes_number, \
		# 			successor_node)
		# 	)