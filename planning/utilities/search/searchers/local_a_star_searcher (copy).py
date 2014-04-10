from operator                  import add
from utilities.search.searcher import Searcher






#!!!!! <Временно>
from visualization.visualization import create_svg
from time                        import sleep
visualize = False
#!!!!! </Временно>

class LocalAStarSearcher(Searcher):
	def find(self, initial_state):
		initial_node = \
			{
				'state':       initial_state,
				'cost':        self.initial_cost,
				'estimation':  initial_state.cost_estimation,
				'predecessor': None,
				'depth':       1
			}
			
		covered_states   = set()
		peripheral_nodes = \
			[
				initial_node
			]
			
			
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
			
			left_index   = 0
			right_index  = len(peripheral_nodes)
			center_index = (left_index + right_index) // 2
			
			while left_index != right_index:
				center_node = peripheral_nodes[center_index]
				
				node_cost_estimation = \
					node['cost'] \
						+ node['estimation']
						
				center_node_cost_estimation = \
					center_node['cost'] \
						+ center_node['estimation']
						
				if node_cost_estimation < center_node_cost_estimation:
					right_index = center_index
				elif node_cost_estimation > center_node_cost_estimation:
					left_index = min(right_index, center_index + 1)
				else:
					break
					
				center_index = (left_index + right_index) // 2
				
			peripheral_nodes.insert(center_index, node)
			
			
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
		
		while peripheral_nodes:
			node = peripheral_nodes.pop(0)
			
			if node['predecessor'] is not None:
				predecessor_node = node['predecessor'][0]
			else:
				predecessor_node = None
				
				
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
			
			
			if predecessor_node is not last_expanded_node:
				fill_covered_states(node)
				
				
			if node['state'] not in covered_states:
				if node['state'].is_goal:
					yield form_states_sequence(node)
				else:
					covered_states.add(node['state'])
					
					
				if node['depth'] == 10:
					peripheral_nodes.clear()
					successor_node_depth = 1
				else:
					successor_node_depth = node['depth'] + 1
					
					
				successors = node['state'].get_successors()
				
				for (shift, successor) in successors:
					successor_node_cost = \
						self.cost_folder(
							node['cost'],
							shift.cost
						)
						
					successor_node = \
						{
							'state':       successor,
							'cost':        successor_node_cost,
							'estimation':  successor.cost_estimation,
							'predecessor': (node, shift),
							'depth':       successor_node_depth
						}
						
					insert_node(successor_node)
					
					
				last_expanded_node = node
				