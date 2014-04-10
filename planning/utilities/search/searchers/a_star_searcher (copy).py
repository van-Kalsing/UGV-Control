from operator                  import add
from utilities.search.searcher import Searcher






#!!!!! <Временно>
from visualization.visualization import create_svg
from time                        import sleep
visualize = True
#!!!!! </Временно>

class AStarSearcher(Searcher):
	def find(self, initial_state):
		initial_node_cost_estimation = \
			self.initial_cost \
				+ initial_state.cost_estimation
				
		covered_nodes     = dict()
		peripheral_states = \
			[{
				'state':           initial_state,
				'cost':            self.initial_cost,
				'cost_estimation': initial_node_cost_estimation,
				'predecessor':     None,
				'successors':      []
			}]
			
			
		def form_states_sequence(node):
			states_sequence = [(node['state'], None)]
			
			while True:
				predecessor = node['predecessor']
				
				if predecessor is not None:
					predecessor_node, predecessor_shift = predecessor
					
					states_sequence.insert(
						0,
						(predecessor_node['state'], predecessor_shift)
					)
					
					
					node = predecessor_node
				else:
					break
					
			return states_sequence
			
			
		self.a = 1 #!!!!! Временно
		def insert_node(node):
			self.a+=1 #!!!!! Временно
			
			state = node['state']
			covered_node_record = \
				covered_states_records.get(
					state
				)
				
			if covered_node_record is None:
				covered_states_records[state] = successor_node, []
				
				insert_node(successor_node)
			else:
				covered_node, covered_node_successors_nodes = \
					covered_node_record
					
				if successor_node['cost'] < covered_node['cost']:
					delta_cost = \
						covered_node['cost'] \
							- successor_node['cost']
							
							
					def get_updating_nodes():
						yield from covered_node_successors_nodes
						
					for updating_node in get_updating_nodes():
						updating_node['cost'] = \
							updating_node['cost'] \
								- delta_cost
								
						updating_node['cost_estimation'] = \
							updating_node['cost_estimation'] \
								- delta_cost
								
						updating_node['predecessor'] = successor_node
			
			
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
			
			
		def expand_node(node):
			
		while peripheral_states:
			node = peripheral_states.pop(0)
			
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
			
			if node['state'].is_goal:
				yield form_states_sequence(node)
				
				
			covered_node = covered_nodes.get(node['state'])
			
			if covered_node is not None:
				
				
				
				
				
			successors = node['state'].get_successors()
			
			for (shift, successor) in successors:
				successor_node_cost = \
					self.cost_folder(
						node['cost'],
						shift.cost
					)
					
				successor_node_cost_estimation = \
					successor_node_cost \
						+ successor.cost_estimation
						
				successor_node = \
					{
						'state':           successor,
						'cost':            successor_node_cost,
						'cost_estimation': successor_node_cost_estimation,
						'predecessor':     (node, shift)
					}
					
					
				covered_node_record = \
					covered_states_records.get(
						successor
					)
					
				if covered_node_record is None:
					covered_states_records[successor] = successor_node, []
					
					insert_node(successor_node)
				else:
					covered_node, covered_node_successors_nodes = \
						covered_node_record
						
					if successor_node['cost'] < covered_node['cost']:
						delta_cost = \
							covered_node['cost'] \
								- successor_node['cost']
								
								
						def get_updating_nodes():
							yield from covered_node_successors_nodes
							
						for updating_node in get_updating_nodes():
							updating_node['cost'] = \
								updating_node['cost'] \
									- delta_cost
									
							updating_node['cost_estimation'] = \
								updating_node['cost_estimation'] \
									- delta_cost
									
							updating_node['predecessor'] = successor_node
							
		return None
		