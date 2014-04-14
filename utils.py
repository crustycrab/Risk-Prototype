import math

class Vector2():

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def normalized(self):
		return Vector2(self.x / self.modul(), self.y / self.modul())

	def modul(self):
		return math.hypot(self.x, self.y)

	def __mul__(self, other):
		if isinstance(other, (int, long, float, complex)):
			return Vector2(self.x * other, self.y * other)
		elif isinstance(other, Vector2):
			return self.x * other.x + self.y * other.y

	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)

	def __str__(self):
		return str((self.x, self.y))

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def as_tuple(self):
		return (self.x, self.y)