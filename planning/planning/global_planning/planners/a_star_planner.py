from collections                                   import namedtuple
from planning.planning.global_planning.smoothing   import Smoother			
from planning.planning.global_planning.state_space import State







_StateNodeBase = \
	namedtuple(
		'NodeBase',
		[
			'state',
			'cost',
			'marked_input_transfers',
			'input_transfers',
			'output_transfers',
			'smoother'
		]
	)
	
class _StateNode(_StateNodeBase):
	def __hash__(self):
		return hash(self.state)
		
		
		
_TransferNode = \
	namedtuple(
		'Transfer',
		[
			'cost',
			'predecessor_node',
			'successor_node'
		]
	)
	
	
	
	
	
	
	
class AStarPlanner:
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
					node     = transfer.predecessor_node
				else:
					break
					
					
			return states_sequence, states_sequence_cost
			
			
			
		def form_state_node(state, cost = None, smoother = None):
			state_node = \
				_StateNode(
					state                  = state,
					cost                   = [cost],
					marked_input_transfers = set(),
					input_transfers        = set(),
					output_transfers       = set(),
					smoother               = [smoother]
				)
				
			return state_node
			
			
		def form_transfer_node(predecessor_node, successor_node):
			transfer = \
				predecessor_node.state.get_transfer(
					successor_node.state
				)
				
			successor_smoother = predecessor_node.smoother[0].copy()
			successor_smoother.push_transfer(transfer)
			
			transfer_node = \
				_TransferNode(
					cost             = successor_smoother.transfer_cost,
					predecessor_node = predecessor_node,
					successor_node   = successor_node
				)
				
			return transfer_node, successor_smoother
			
			
			
			
			
		initial_state = \
			State(
				[self.__planning_parameters.initial_polygon],
				self.__planning_parameters
			)
			
		initial_smoother = \
			Smoother(
				self.__planning_parameters.surface,
				self.__planning_parameters.smoothing_depth
			)
			
		initial_state_node = \
			form_state_node(
				initial_state,
				cost     = 0.0,
				smoother = initial_smoother
			)
			
		covered_states = \
			{
				initial_state: initial_state_node
			}
			
			
			
		peripheral_states_nodes = [initial_state_node]
		
		def compute_state_node_priority(state_node):
			return state_node.cost[0] + state_node.state.estimation
			
			
			
			
			
		while peripheral_states_nodes:
			state_node = peripheral_states_nodes.pop(0)
			
			if state_node.state.is_final:
				return form_states_sequence(state_node)
				
				
			need_sorting  = False
			updated_nodes = set()
			
			for successor in state_node.state.successors:
				is_successor_covered = True
				successor_node       = covered_states.get(successor)
				
				if successor_node is None:
					is_successor_covered = False
					successor_node       = form_state_node(successor)
					
					
				transfer, smoother = \
					form_transfer_node(
						state_node,
						successor_node
					)
					
					
				state_node.output_transfers.add(transfer)
				successor_node.input_transfers.add(transfer)
				
				
				if not is_successor_covered:
					successor_node.marked_input_transfers.add(transfer)
					successor_node.smoother[0] = smoother
					successor_node.cost[0]     = \
						state_node.cost[0] \
							+ transfer.cost
							
					covered_states[successor] = successor_node
					peripheral_states_nodes.append(successor_node)
					
					need_sorting = True
				else:
					updated_nodes.add(
						(state_node, transfer)
					)
					
					
			while updated_nodes:
				predecessor_node, input_transfer = updated_nodes.pop()
				
				successor_node = input_transfer.successor_node
				cost           = predecessor_node.cost[0] + input_transfer.cost
				
				if successor_node.cost[0] > cost:
					successor_node.cost[0] = cost
					
					successor_node.marked_input_transfers.clear()
					successor_node.marked_input_transfers.add(input_transfer)
					
					if not successor_node.output_transfers:
						need_sorting = True
					else:
						for output_transfer in successor_node.output_transfers:
							updated_nodes.add(
								(successor_node, output_transfer)
							)
							
				elif successor_node.cost[0] == cost:
					successor_node.marked_input_transfers.add(input_transfer)
					
					
			if need_sorting:
				peripheral_states_nodes = \
					sorted(
						peripheral_states_nodes,
						key = compute_state_node_priority
					)
					
					
		return None
		