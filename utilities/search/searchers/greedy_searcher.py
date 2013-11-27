from operator                  import add
from utilities.search.searcher import Searcher






#!!!!! <Временно>
from visualization.visualization import create_svg
from time                        import sleep
visualize = False
#!!!!! </Временно>

class GreedySearcher(Searcher):
	def find(self, initial_state):
		covered_states    = dict()
		peripheral_states = \
			[{
				'state':           initial_state,
				'cost':            self.initial_cost,
				'cost_estimation': initial_state.cost_estimation,
				'predecessor':     None,
				'successors':      list()
			}]
			
			
		def form_states_sequence(node):
			states_sequence      = [node['state']]
			states_sequence_cost = node['cost']
			
			while True:
				predecessor = node['predecessor']
				
				if predecessor is not None:
					predecessor_node = predecessor
					
					states_sequence.insert(
						0,
						predecessor_node['state']
					)
					
					
					node = predecessor_node
				else:
					break
					
			return states_sequence, states_sequence_cost
			
			
		self.a = 1 #!!!!! Временно
		def insert_node(node):
			self.a+=1 #!!!!! Временно
			
			left_index   = 0
			right_index  = len(peripheral_states)
			center_index = (left_index + right_index) // 2
			
			while left_index != right_index:
				center_node = peripheral_states[center_index]
				
				if node['cost_estimation'] < center_node['cost_estimation']:
					right_index = center_index
				elif node['cost_estimation'] > center_node['cost_estimation']:
					left_index = min(right_index, center_index + 1)
				else:
					break
					
				center_index = (left_index + right_index) // 2
				
			peripheral_states.insert(center_index, node)
			
			
		self.b = 0 #!!!!! Временно
		def fill_covered_states(node):
			self.b+=1 #!!!!! Временно
			covered_states.clear()
			
			while True:
				predecessor = node['predecessor']
				
				if predecessor is not None:
					node, _ = predecessor
					
					covered_states.add(
						node['state']
					)
				else:
					break
					
					
		last_expanded_node = None
		
		while peripheral_states:
			node  = peripheral_states.pop(0)
			state = node['state']
			
			# if node['predecessor'] is not None:
			# 	predecessor_node = node['predecessor'][0]
			# else:
			# 	predecessor_node = None
				
				
			# if predecessor_node is not last_expanded_node:
			# 	fill_covered_states(node)
			
			
			#!!!!! <Временно>
			if visualize:
				controls_sequence = \
					[control.polygon for control, _ \
						in form_states_sequence(node)]
						
				create_svg(
					"test1.svg",
					node['state'].planning_parameters.surface,
					controls_sequence
				)
				
				sleep(2)
			#!!!!! </Временно>
			
			
			if state not in covered_states:
				if state.is_goal:
					yield form_states_sequence(node)
				else:
					covered_states[state] = node
					
					
				successors = state.get_successors()
				
				for (shift, successor) in successors:
					successor_node_cost = \
						self.cost_folder(
							node['cost'],
							shift.cost
						)
						
					successor_node = \
						{
							'state':           successor,
							'cost':            successor_node_cost,
							'cost_estimation': successor.cost_estimation,
							'predecessor':     node,
							'successors':      list()
						}
						
					node['successors'].append(successor_node)
					insert_node(successor_node)
					
					
				# last_expanded_node = node
			else:
				existing_node = covered_states[state]
				delta_cost    = node['cost'] - existing_node['cost']
				
				if delta_cost < 0.0:
					#????? Проверить название переменной
					effected_nodes               = [existing_node]
					existing_node['predecessor'] = node['predecessor']
					
					while effected_nodes:
						existing_node = effected_nodes.pop(0)
						
						existing_node['cost']            += delta_cost
						existing_node['cost_estimation'] += delta_cost
						
						effected_nodes.extend(existing_node['successors'])
						