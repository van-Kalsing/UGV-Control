from abc import ABCMeta, abstractmethod, abstractproperty







class State(metaclass = ABCMeta):
	@abstractproperty
	def is_goal(self):
		pass
		
		
	@abstractproperty
	def cost_estimation(self):
		pass
		
		
	@abstractmethod
	def get_successor(self, shift):
		pass
		
		
	@abstractmethod
	def get_successors(self):
		pass
		
		
	@abstractmethod
	def get_predecessors(self):
		pass
		
		
		
		
		
		
		
class Shift(metaclass = ABCMeta):
	@abstractproperty
	def cost(self):
		pass
		