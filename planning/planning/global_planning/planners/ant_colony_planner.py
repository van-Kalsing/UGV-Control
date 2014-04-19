from planning.global_planning.smoothing   import Smoother			
from planning.global_planning.state_space import State

import random







class AntColonyPlanner:
	def __init__(self, planning_parameters, *args, **kwargs):
		if not planning_parameters.is_correct:
			raise Exception() #!!!!!
			
			
		super().__init__(*args, **kwargs)
		
		self.__planning_parameters = planning_parameters.copy()
		
		
		
		
		
	@property
	def planning_parameters(self):
		return self.__planning_parameters.copy()
		
		
		
		
		
	def plan(self):
		transfers_pheromones_credits = dict()
		
		
		
		def find_path(initial_state):
			state    = initial_state
			smoother = \
				Smoother(
					surface         = self.__planning_parameters.surface,
					smoothing_depth = 1
				)
				
			path      = [state]
			path_cost = 0.0
			
			
			while not state.is_final:
				state_successors_credits      = dict()
				state_successors_smoothers    = dict()
				total_state_successors_credit = 0.0
				
				
				
				for state_successor in state.successors:
					state_successor_smoother = smoother.copy()
					state_successor_smoother.push_transfer(
						state.get_transfer(state_successor)
					)
					
					
					transfer_credit = \
						1.0 / \
							(state_successor.estimation \
								+ state_successor_smoother.transfer_cost)
								
					transfer_pheromones_credit = \
						transfers_pheromones_credits.get(
							(state, state_successor),
							0.0
						)
						
					state_successor_credit = \
						10.0 * transfer_credit \
							+ transfer_pheromones_credit
							
							
					state_successors_credits[state_successor] = \
						state_successor_credit
						
					state_successors_smoothers[state_successor] = \
						state_successor_smoother
						
					total_state_successors_credit += state_successor_credit
					
					
					
				sample = \
					random.uniform(
						0.0,
						total_state_successors_credit
					)
					
				for state_successor in state.successors:
					total_state_successors_credit -= \
						state_successors_credits[
							state_successor
						]
						
					if total_state_successors_credit <= sample:
						selected_state_successor = state_successor
						break
						
						
						
				state    = selected_state_successor
				smoother = state_successors_smoothers[state]
				
				path.append(state)
				path_cost += smoother.transfer_cost
				
				
			return path, path_cost
			
			
			
		planning_parameters = self.__planning_parameters
		initial_polygon     = self.__planning_parameters.initial_polygon
		
		initial_state = \
			State(
				[initial_polygon],
				planning_parameters
			)
			
			
			
		best_path      = None
		best_path_cost = None
		
		import sys
		import visualization.visualization as visualization
		for _ in range(5000):
			for _ in range(1):
				path, path_cost = find_path(initial_state)
				#!!!!! <Верменно>
				print(path_cost)
				#!!!!! </Верменно>
				
				if (best_path is None) or (path_cost < best_path_cost):
					best_path      = path
					best_path_cost = path_cost
					
					
					
				for transfer in transfers_pheromones_credits.keys():
					transfers_pheromones_credits[transfer] *= 0.75
					
					
				last_state = None
				
				for state in path:
					if last_state is not None:
						transfer = last_state, state
						
						
						transfer_pheromones_credit = \
							transfers_pheromones_credits.get(
								transfer,
								0.0
							)
							
						transfers_pheromones_credits[transfer] = \
							transfer_pheromones_credit \
								+ 1.0 / path_cost
								
								
					last_state = state
					
					
					
			# print('Стоимость пути: %s' % best_path_cost)
			# visualization.create_svg(
			# 	"output/output.svg",
			# 	self.__planning_parameters.surface,
			# 	best_path
			# )
			
			# print("continue?")
			# if sys.stdin.readline() == "n\n":
			# 	break
				
				
				
		return best_path, best_path_cost
		