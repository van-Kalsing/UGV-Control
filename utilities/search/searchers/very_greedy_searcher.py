from operator                  import add
from utilities.search.searcher import Searcher






#!!!!! <Временно>
from visualization.visualization import create_svg
from time                        import sleep
visualize = False
#!!!!! </Временно>

class VeryGreedySearcher(Searcher):
	def find(self, initial_state):
		covered_states    = set()
		peripheral_states = \
			[{
				'state':           initial_state,
				'cost_estimation': initial_state.cost_estimation,
				'predecessor':     None,
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
			
			
			if node is not last_expanded_node:
				fill_covered_states(node)
				
				
			if node['state'] not in covered_states:
				if node['state'].is_goal:
					yield form_states_sequence(node)
				else:
					covered_states.add(node['state'])
					
					
				peripheral_states = []
				successors        = node['state'].get_successors()
				
				for (shift, successor) in successors:
					successor_node = \
						{
							'state':           successor,
							'cost_estimation': successor.cost_estimation,
							'predecessor':     (node, shift)
						}
						
					insert_node(successor_node)
					
					
				last_expanded_node = node
				