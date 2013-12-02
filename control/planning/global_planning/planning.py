from control.planning.global_planning.state_space \
	import State, \
				compute_sequence_cost
				
from collections import namedtuple







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
	node_fields = \
		[
			'state',
			'cost',
			'marked_input_transfers',
			'input_transfers',
			'output_transfers',
		]
		
	class Node(namedtuple('Node', node_fields)):
		def __hash__(self):
			return hash(self.state)
			
			
			
	transfer_fields = \
		[
			'cost',
			'predecessor',
			'successor'
		]
		
	Transfer = namedtuple('Transfer', transfer_fields)
	
	
	
	
	
	
	
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
			states_sequence_cost = node.cost[0]
			
			while node is not None:
				states_sequence.insert(
					0,
					node.state
				)
				
				if node.marked_input_transfers:
					transfer = next(iter(node.marked_input_transfers)) #!!!!!
					node     = transfer.predecessor
				else:
					break
					
					
			return states_sequence, states_sequence_cost, sn #!!!!! Убрать sn
			
			
			
		def form_node(state, cost = None):
			node = \
				Planner.Node(
					state                  = state,
					cost                   = [cost],
					marked_input_transfers = set(),
					input_transfers        = set(),
					output_transfers       = set()
				)
				
			return node
			
			
		def form_transfer(predecessor, successor):
			transfer_cost = \
				compute_sequence_cost(
					[predecessor.state, successor.state],
					self.__planning_parameters
				)
				
			transfer = \
				Planner.Transfer(
					cost        = transfer_cost,
					predecessor = predecessor,
					successor   = successor
				)
				
			return transfer
			
			
			
			
			
			
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
			
			
		initial_node = form_node(initial_state, cost = 0.0)
		
		covered_states = \
			{
				initial_state: initial_node
			}
			
			
			
		peripheral_nodes = [initial_node]
		
		#!!!!! <Изменить>
		def cmpt_prir(n):
			return n.cost[0] + n.state.estimation
		#!!!!! </Изменить>
		
		
		
		
		
		
		#!!!!! <Временно>
		na = 0
		nb = 0
		B  = 0
		n = 0
		sn = {}
		#!!!!! </Временно>
		while peripheral_nodes:
			node = peripheral_nodes.pop(0)
			
			#!!!!! <Временно>
			n+=1
			if node.state not in sn:
				sn[node.state] = [n] #!!!!! Временно
			else:
				sn[node.state].append(n) #!!!!! Временно
			a=False
			b=0
			#!!!!! </Временно>
			
			if node.state == final_state:
				#!!!!! <Временно>
				print("na: %s" % na)
				print("nb: %s" % nb)
				print("B : %s" % B)
				print("n : %s" % n)
				#!!!!! </Временно>
				return form_states_sequence(node)
				
				
			up_nodes = set()
			
			for successor_state in node.state.successors:
				successor = covered_states.get(successor_state)
				
				if successor is None:
					successor = form_node(successor_state)
					covered_states[successor_state] = successor
					
					peripheral_nodes.append(successor)
					a = True#!!!!!
					
					
				transfer = form_transfer(node, successor)
				
				node.output_transfers.add(transfer)
				successor.input_transfers.add(transfer)
				
				
				if not successor.marked_input_transfers:
					successor.marked_input_transfers.add(transfer)
					successor.cost[0] = node.cost[0] + transfer.cost
				else:
					up_nodes.add(
						(successor, transfer)
					) #!!!!!
					
					
			while up_nodes:
				b+=1#!!!!!
				nb+=1#!!!!!
				predecessor, input_transfer = up_nodes.pop()
				
				successor = input_transfer.successor
				
				cost = predecessor.cost[0] + input_transfer.cost
				
				if successor.cost[0] > cost:
					successor.cost[0] = cost
					
					successor.marked_input_transfers.clear()
					successor.marked_input_transfers.add(input_transfer)
					
					if not successor.output_transfers:
						a = True#!!!!!
					else:
						for output_transfer in successor.output_transfers:
							up_nodes.append(
								(successor, output_transfer)
							)
							
				elif successor.cost[0] == cost:
					successor.marked_input_transfers.add(input_transfer)
					
			B = max(b, B)#!!!!!
			if a:
				na += 1#!!!!!
				peripheral_nodes = \
					sorted(
						peripheral_nodes,
						key = cmpt_prir
					)
					
					
		return None
		# def form_output_transfers(state):
		# 	output_transfers = set()
			
			
		# 	for output_transfer_successor in state.successors:
		# 		output_transfer_cost = \
		# 			compute_sequence_cost(
		# 				[state, output_transfer_successor],
		# 				self.__planning_parameters
		# 			)
					
		# 		output_transfer = \
		# 			Planner.Transfer(
		# 				cost        = output_transfer_cost,
		# 				predecessor = state,
		# 				successor   = output_transfer_successor
		# 			)
					
		# 		output_transfers.add(output_transfer)
				
				
		# 	return output_transfers
			
			
		# def form_successor_node(predecessor_node, transfer):
		# 	successor      = transfer.successor
		# 	successor_node = dict()
			
			
		# 	successor_node['state']                  = successor
		# 	successor_node['marked_input_transfers'] = { transfer }
		# 	successor_node['input_transfers']        = { transfer }
			
		# 	successor_node['cost'] = \
		# 		[predecessor_node.cost[0] \
		# 			+ transfer.cost]
					
		# 	successor_node['output_transfers'] = \
		# 		form_output_transfers(
		# 			successor
		# 		)
				
				
		# 	return Planner.Node(**successor_node)
			
			
		# initial_state = \
		# 	State(
		# 		self.__planning_parameters.initial_polygon,
		# 		self.__planning_parameters
		# 	)
			
		# final_state = \
		# 	State(
		# 		self.__planning_parameters.final_polygon,
		# 		self.__planning_parameters
		# 	)
			
			
		# initial_node = form_node(initial_state, cost = 0.0)
		# initial_node.output_transfers.update(
		# 	form_output_transfers(initial_state)
		# )
		
		# covered_states = \
		# 	{
		# 		initial_state: initial_node
		# 	}
			
			
			
		# peripheral_transfers = list()
		
		# #!!!!! <Изменить>
		# def cmpt_prir(t):
		# 	return \
		# 		covered_states[t.predecessor].cost[0] \
		# 			+ t.cost \
		# 			+ t.successor.estimation
					
		# for output_transfer in initial_node.output_transfers:
		# 	peripheral_transfers.append(output_transfer)
			
		# peripheral_transfers = \
		# 	sorted(
		# 		peripheral_transfers,
		# 		key = cmpt_prir
		# 	)
		# #!!!!! </Изменить>
		
		# #!!!!! <Временно>
		# na = 0
		# nb = 0
		# B  = 0
		# n = 0
		# sn = {}
		# #!!!!! </Временно>
		# while peripheral_transfers:
		# 	transfer       = peripheral_transfers.pop(0)
		# 	successor      = transfer.successor
		# 	successor_node = covered_states.get(successor)
			
			
		# 	#!!!!! <Временно>
		# 	n+=1
		# 	if successor not in sn:
		# 		sn[successor] = [n] #!!!!! Временно
		# 	else:
		# 		sn[successor].append(n) #!!!!! Временно
		# 	#!!!!! </Временно>
		# 	if successor_node is None:
		# 		predecessor      = transfer.predecessor
		# 		predecessor_node = covered_states[predecessor]
				
		# 		successor_node = \
		# 			form_successor_node(
		# 				predecessor_node,
		# 				transfer
		# 			)
					
		# 		covered_states[successor] = successor_node
				
		# 		#!!!!! <Изменить>
		# 		for output_transfer in successor_node.output_transfers:
		# 			peripheral_transfers.append(output_transfer)
					
		# 		peripheral_transfers = \
		# 			sorted(
		# 				peripheral_transfers,
		# 				key = cmpt_prir
		# 			)
		# 		#!!!!! </Изменить>
		# 	else:
		# 		successor_node.input_transfers.add(transfer)
				
		# 		predecessor      = transfer.predecessor
		# 		predecessor_node = covered_states[predecessor]
				
		# 		b = 0
		# 		a = False #!!!!!
		# 		up_nodes = [ (predecessor_node, transfer) ] #!!!!!
		# 		while up_nodes:
		# 			b+=1
		# 			nb+=1
		# 			predecessor_node, input_transfer = up_nodes.pop(0)
					
		# 			state      = input_transfer.successor
		# 			state_node = covered_states.get(state)
					
		# 			if state_node is not None:
		# 				cost = predecessor_node.cost[0] + input_transfer.cost
						
		# 				if state_node.cost[0] > cost:
		# 					state_node.cost[0] = cost
							
		# 					state_node.marked_input_transfers.clear()
		# 					state_node.marked_input_transfers.add(input_transfer)
							
		# 					for output_transfer in state_node.output_transfers:
		# 						up_nodes.append(
		# 							(state_node, \
		# 								output_transfer)
		# 						)
								
		# 				elif state_node.cost[0] == cost:
		# 					state_node.marked_input_transfers.add(input_transfer)
		# 			else:
		# 				a = True
						
		# 		B = max(b, B)
		# 		if a:
		# 			na += 1
		# 			peripheral_transfers = \
		# 				sorted(
		# 					peripheral_transfers,
		# 					key = cmpt_prir
		# 				)
						
						
		# 	if successor == final_state:
		# 		print("na: %s" % na)
		# 		print("nb: %s" % nb)
		# 		print("B : %s" % B)
		# 		return form_states_sequence(successor_node)
				
				
		# return None
		
		
		
		
		
		
		
		
		
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