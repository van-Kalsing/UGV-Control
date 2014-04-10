from operator                  import add
from utilities.search.searcher import Searcher






#!!!!! <Временно>
from visualization.visualization import create_svg
from time                        import sleep
visualize = False
#!!!!! </Временно>

segment_depth = 6 # Целое положительное число

class LocalAStarSearcher(Searcher):
	def find(self, initial_state):
		initial_node = \
			{
				'state':       initial_state,
				'cost':        self.initial_cost,
				'estimation':  initial_state.cost_estimation,
				'predecessor': None,
				'successors':  list(),
				'depth':       1
			}
			
			
		covered_states = dict()
		
		peripheral_nodes = \
			[
				initial_node
			]
			
		segment_peripheral_nodes = \
			[
				initial_node
			]
			
			
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
		def insert_node(peripheral_nodes, node):
			left_index   = 0
			right_index  = len(peripheral_nodes)
			center_index = (left_index + right_index) // 2
			
			while left_index != right_index:
				center_node = peripheral_nodes[center_index]
				
				# node_cost_estimation = \
				# 	node['estimation']
					
				# center_node_cost_estimation = \
				# 	center_node['estimation']
					
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
					
					
		self.t = -1 #!!!!! Временно
		while peripheral_nodes:
			self.t+=1 #!!!!! Временно
			segment_root_node        = peripheral_nodes.pop(0)
			segment_peripheral_nodes = [segment_root_node]
			
			# last_expanded_node = None
			
			while segment_peripheral_nodes:
				node = segment_peripheral_nodes.pop(0)
				
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
				
				
				if node['state'] not in covered_states:
					if node['depth'] == segment_depth * 2:
						segment_root_node
						for segment_peripheral_node in segment_peripheral_nodes:
							if peripheral_node['depth'] <= segment_depth
								segment_peripheral_nodes.remove(
									segment_peripheral_node
								)
							else:
							segment_node = segment_peripheral_node
							
							while segment_node['depth'] > segment_depth + 1:
								segment_node = segment_node['predecessor']
							else:
								if segment_node
						for _ in range(segment_depth):
							node, _ = node['predecessor']
							
							covered_states.discard(
								node['state']
							)
							
						# if node['predecessor'] is not None:
						# 	predecessor_node = node['predecessor'][0]
						# else:
						# 	predecessor_node = None
							
						successor_node_depth = 1
					else:
						successor_node_depth = node['depth'] + 1
						
						
					if node['state'].is_goal:
						#if node['depth'] <= segment_depth:
						yield form_states_sequence(node)
					else:
						covered_states[node['state']] = node
						
						
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
								'predecessor': node,
								'successors':  list(),
								'depth':       successor_node_depth
							}
							
						self.a+=1 #!!!!! Временно
						node['successors'].append(successor_node)
						insert_node(peripheral_nodes, successor_node)
						insert_node(segment_peripheral_nodes, successor_node)
						
						
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
							
							existing_node['cost'] += delta_cost
							
							effected_nodes.extend(existing_node['successors'])
							