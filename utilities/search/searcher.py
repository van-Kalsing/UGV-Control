from abc      import ABCMeta, abstractmethod
from operator import add





class Searcher(metaclass = ABCMeta):
	def __init__(self, cost_folder = add, initial_cost = 0.0, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.__cost_folder  = cost_folder
		self.__initial_cost = initial_cost
		
		
		
	@property
	def cost_folder(self):
		return self.__cost_folder
		
		
	@property
	def initial_cost(self):
		return self.__initial_cost
		
		
		
	@abstractmethod
	def find(self, initial_state):
		pass
		