class GameObject():
	def __init__(self):
		self.name = ''
		self._attributes = {}

	def set_attribute(self, type, value): self._attributes[type] = value # Set or add (if it does not already exist) an attribute to the attributes dictionary: type is the attribute reference name (unique identifier), value is the new value to update the attribute with
	def get_attributes(self): return self._attributes # Returns the entire attributes list
	def get_attribute(self, type): return self._attributes[type] # Returns the value of a attribute
	def __repr__(self): return self.name