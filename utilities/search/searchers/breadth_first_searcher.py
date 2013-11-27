from operator                  import add
from utilities.search.searcher import Searcher






class BreadthFirstSearcher(Searcher):
	def find(self, initial_state):
		fringe = \
			[{
				'state':       initial_state,
				'cost':        self.initial_cost,
				'predecessor': None
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
			
			
		def insert_node(node):
			fringe.append(node)
			
			
		while fringe:
			node = fringe.pop(0)
			
			if node['state'].is_goal:
				yield form_states_sequence(node)
				
				
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
						'predecessor': (node, shift)
					}
					
				insert_node(successor_node)
				
				
		return None
		