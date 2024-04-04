from Settings import *
from random import randint
from typing import List
from copy import copy
from GeoMath import *

header = """
0 : Box
"""


def get_a_element_of_set(s: set):
	for i in range(randint(1, len(s))):
		r = s.pop()
	return r


class Map:
	def __init__(self, width, height, res, *allowed_tiles):
		self.res = res
		self.width, self.height = width, height
		self.allowed_tiles = list(allowed_tiles)

		self.mapping = []
		currentTile = 0
		for tile in self.allowed_tiles:
			self.mapping.append([set(), set(), set(), set()])  # [top, right, bottom, left]
			for i_tile_compared in range(len(self.allowed_tiles)):
				if tile.topCompatible(self.allowed_tiles[i_tile_compared]):
					self.mapping[currentTile][0].add(i_tile_compared)

				if tile.rightCompatible(self.allowed_tiles[i_tile_compared]):
					self.mapping[currentTile][1].add(i_tile_compared)

				if tile.bottomCompatible(self.allowed_tiles[i_tile_compared]):
					self.mapping[currentTile][2].add(i_tile_compared)

				if tile.leftCompatible(self.allowed_tiles[i_tile_compared]):
					self.mapping[currentTile][3].add(i_tile_compared)
			currentTile += 1

		for elt in self.allowed_tiles:
			print()
			print(elt)

		for i in range(len(self.allowed_tiles)):
			print(f"Tile N°{i}")
			for j in range(4):
				print(self.mapping[i][j])

		self.map = [[-1 for _ in range(height)] for __ in range(width)]
		# définir la première
		self.map[randint(0, width-1)][randint(0, height-1)] = randint(0, len(self.allowed_tiles)-1)
		remaining = width * height - 1
		ended = False

		while not ended:
			for x in range(width):
				if ended:
					break
				for y in range(height):
					if remaining == 0:
						ended = True
						break
					if self.map[x][y] == -1:
						temp = set([i for i in range(10)])
						has_a_neighbor = False
						if x > 0 and self.map[x - 1][y] != -1:
							temp = temp.intersection(self.mapping[self.map[x-1][y]][1])
							has_a_neighbor = True
						if x < width-1 and self.map[x + 1][y] != -1:
							temp = temp.intersection(self.mapping[self.map[x+1][y]][3])
							has_a_neighbor = True
						if y > 0 and self.map[x][y-1] != -1:
							temp = temp.intersection(self.mapping[self.map[x][y-1]][2])
							has_a_neighbor = True
						if y < height-1 and self.map[x][y+1] != -1:
							temp = temp.intersection(self.mapping[self.map[x][y+1]][0])
							has_a_neighbor = True
						if has_a_neighbor:
							if len(temp) == 1:
								self.map[x][y] = temp.pop()
							elif len(temp) == 0:
								self.map[x][y] = len(self.allowed_tiles) - 1
							else:
								print(temp)
								self.map[x][y] = get_a_element_of_set(temp)
							remaining -= 1

		print("MAP :")
		for elt in self.map:
			print(elt)

	def get_on_Screen(self, camera):
		camera_box = Box(camera.position, camera.Dimention())
		valid_tile = []
		for x in range(self.width):
			for y in range(self.height):
				if camera_box.CollideRect(Box(Vector2(x * self.res * TILERESOLUTION, y * self.res * TILERESOLUTION), Vector2(self.res * 32, self.res * 32))):
					valid_tile.append((x, y))
		return valid_tile

	def blit(self, screen, camera):
		for x, y in self.get_on_Screen(camera):
			self.allowed_tiles[self.map[x][y]].blit(screen, camera.position * -1 + Vector2(self.res * TILERESOLUTION * x, self.res * TILERESOLUTION * y), self.res)


class Tile:  # a 16x16 grid
	def __init__(self, *columns):
		self.grid = list(columns)

		# List des tuiles sur chacune des bordures
		self.t_top = [elt[0] for elt in self.grid]
		self.t_bottom = [elt[-1] for elt in self.grid]
		self.t_left = [elt for elt in columns[0]]
		self.t_right = [elt for elt in columns[-1]]

	def blit(self, screen: py.Surface, position: Vector2, res=25):
		for x in range(TILERESOLUTION):
			for y in range(TILERESOLUTION):
				if self.grid[x][y] != 0:
					screen.blit(Textures[self.grid[x][y]], (position.x() + res * x, position.y() + res * y))
		py.draw.line(screen, RED, position.tuple(), (position + Vector2(TILERESOLUTION*res, 0)).tuple(), 2)
		py.draw.line(screen, RED, position.tuple(), (position + Vector2(0, TILERESOLUTION*res)).tuple(), 2)
		py.draw.line(screen, RED, (position + Vector2(TILERESOLUTION*res, 0)).tuple(), (position + Vector2(TILERESOLUTION*res, TILERESOLUTION*res)).tuple(), 2)
		py.draw.line(screen, RED, (position + Vector2(0, TILERESOLUTION*res)).tuple(), (position + Vector2(TILERESOLUTION*res, TILERESOLUTION*res)).tuple(), 2)

	def topCompatible(self, tile):
		"""est ce que je peux mettre cette tuile au dessus ? """
		for i in range(1, TILERESOLUTION-1):
			if tile.t_bottom[i] == 0 and self.t_top[i] == 0:
				if tile.t_bottom[i-1] == 0 or tile.t_bottom[i + 1] == 0:
					return True
		return False

	def bottomCompatible(self, tile):
		"""est ce que je peux mettre cette tuile en dessous ? """
		for i in range(1, TILERESOLUTION-1):
			if tile.t_top[i] == 0 and self.t_bottom[i] == 0:
				if self.t_bottom[i-1] == 0 or self.t_bottom[i+1] == 0:
					return True
		return False

	def leftCompatible(self, tile):
		"""est ce que je peux mettre cette tuile à gauche ? """
		for i in range(1, TILERESOLUTION):
			if tile.t_right[i] == 0 and tile.t_right[i-1] == 0 and self.t_left[i] == 0 and self.t_left[i-1] == 0:
				return True
		return False

	def rightCompatible(self, tile):
		"""est ce que je peux mettre cette tuile à droite ? """
		for i in range(1, TILERESOLUTION):
			if tile.t_left[i] == 0 and tile.t_left[i-1] == 0 and self.t_right[i] == 0 and self.t_right[i-1] == 0:
				return True
		return False

	def copy(self):
		return copy(self)

	def __str__(self):
		chaine = ""
		for y in range(TILERESOLUTION):
			chaine += "|"
			for x in range(TILERESOLUTION):
				chaine += f" {self.grid[x][y]} |"
			chaine += "\n"
		return chaine


if __name__ == '__main__':

	map = Map(5, 5, *[
		*[Tile(
			*[[randint(0, 1) for _ in range(TILERESOLUTION)] for __ in range(TILERESOLUTION)]
		) for _ in range(10)], Tile([1 for i in range(TILERESOLUTION)] for j in range(TILERESOLUTION))
	])
