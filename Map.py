from Settings import *
from random import randint
from copy import copy
from GameObject import *

header = """
0 : Box
"""


def get_a_element_of_set(s: set):
	for i in range(randint(1, len(s))):
		r = s.pop()
	return r


class Map:
	def __init__(self, game, width, res, tile_collection):
		self.game = game
		self.res = res
		self.width = width
		self.tile_collection = list(tile_collection)

		self.mapping = []

		self.map = [-1 for __ in range(width)]

	def get_on_Screen(self, camera):
		camera_box = Box(camera.position, camera.Dimention())
		valid_tile = []
		for x in range(self.width):
			if camera_box.CollideRect(Box(Vector2(x * TILETOTALSIZE, 0), Vector2(TILETOTALSIZE, TILETOTALSIZE))):
				valid_tile.append(x)
		return valid_tile

	def get_physique_on_screen(self, camera):
		r = []
		for i in self.get_on_Screen(camera):
			r += self.map[i].collision
		return r

	def blit(self, screen, camera):
		for x in self.get_on_Screen(camera):
			self.map[x].blit(screen)


class Tile:  # a 32x32 grid
	def __init__(self, game, position: Vector2):
		self.game = game
		self.position: Vector2 = position
		self.collision = []
	
		self.image: py.Surface = None
		self.t_top: list = None
		self.t_bottom: list = None
		self.t_left: list = None
		self.t_right: list = None
	
	def copy(self, position: Vector2):
		return createTileFromData(self.game, position, self.image, self.collision.copy())
	
	def blit(self, screen: py.Surface):
		screen.blit(self.image, (self.position - self.game.camera.position).tuple())

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
		for i in range(1, TILERESOLUTION-1):
			if (
					tile.t_right[i] == 0 and tile.t_right[i-1] == 0 and
					self.t_left[i] == 0 and self.t_left[i-1] == 0 and
					self.t_left[i+1] != 0 and tile.t_right[i+1] != 0
			):
				return True
		return False

	def rightCompatible(self, tile):
		"""est ce que je peux mettre cette tuile à droite ? """
		for i in range(1, TILERESOLUTION-1):
			if (
					tile.t_left[i-1] == 0 and tile.t_left[i] == 0 and tile.t_left[i+1] != 0 and
					self.t_right[i-1] == 0 and self.t_right[i] == 0 and self.t_right[i+1] != 0
			):
				return True
		return False

	def __str__(self):
		chaine = ""
		for y in range(TILERESOLUTION):
			chaine += "|"
			for x in range(TILERESOLUTION):
				chaine += f" {self.grid[x][y]} |"
			chaine += "\n"
		return chaine


def createRandomMap(game, width) -> Map:
	tiles = [createTileFromPath(game, path) for path in TILES]
	o_map: Map = Map(game, width, RESOLUTION, tiles)
	o_map.mapping = get_mapping_from_tile_collection(tiles)

	# définir la première
	o_map.map[randint(0, width - 1)] = randint(0, len(TILES) - 1)
	fillMap(o_map)
	replace_with_tiles(o_map)
	return o_map


def createMapStartingWith(game, width, start_tile_index, excluded=True):
	if start_tile_index < 0:
		start_tile_index = randint(1, len(TILES) - 1)
	tiles = [createTileFromPath(game, path) for path in TILES]
	o_map: Map = Map(game, width, RESOLUTION, tiles)
	o_map.mapping = get_mapping_from_tile_collection(tiles, (start_tile_index, ) if excluded else ())

	# définir la première
	o_map.map[0] = start_tile_index
	fillMap(o_map)
	replace_with_tiles(o_map)
	return o_map


def get_mapping_from_tile_collection(tile_collection: list, exclude: tuple = ()) -> list:
	currentTile: int = 0
	mapping = []
	for tile in tile_collection:
		mapping.append([set(), set()])  # [left, right]
		for i_tile_compared in range(len(tile_collection)):
			if tile.leftCompatible(tile_collection[i_tile_compared]) and i_tile_compared not in exclude:
				mapping[currentTile][0].add(i_tile_compared)
			if tile.rightCompatible(tile_collection[i_tile_compared]) and i_tile_compared not in exclude:
				mapping[currentTile][1].add(i_tile_compared)
		currentTile += 1
	for elt in mapping:
		print(elt)
	return mapping


def fillMap(o_map: Map) -> None:
	remaining: int = o_map.width - 1
	ended: bool = False
	while not ended:
		for x in range(o_map.width):
			if remaining == 0:
				ended = True
				break
			if o_map.map[x] == -1:
				temp = set([i for i in range(10)])
				has_a_neighbor = False
				if x > 0 and o_map.map[x - 1] != -1:
					temp = temp.intersection(o_map.mapping[o_map.map[x - 1]][1])
					has_a_neighbor = True
				if x < o_map.width - 1 and o_map.map[x + 1] != -1:
					temp = temp.intersection(o_map.mapping[o_map.map[x + 1]][0])
					has_a_neighbor = True
				if has_a_neighbor:
					print(temp)
					if len(temp) == 1:
						o_map.map[x] = temp.pop()
					elif len(temp) == 0:
						print("No Solution !")
						o_map.map[x] = len(o_map.tile_collection) - 1
					else:
						o_map.map[x] = get_a_element_of_set(temp)
					remaining -= 1


def replace_with_tiles(o_map: Map) -> None:
	for x in range(len(o_map.map)):
		o_map.map[x] = createTileFromExisting(o_map.tile_collection[o_map.map[x]], Vector2(x * TILETOTALSIZE, 0))


def createTileFromExisting(tile: Tile, position: Vector2) -> Tile:
	collision = []
	for collision_array_elt in tile.collision:
		collision.append(collision_array_elt.get_decal(position))
	return _createTileFromData(tile.game, position, tile.image, collision, tile.t_top, tile.t_bottom, tile.t_left, tile.t_right)


def _createTileFromData(game, position: Vector2, image: py.Surface, collision: list, top: list, bottom: list, left: list, right: list) -> Tile:
	tile = Tile(game, position)
	tile.image = image
	tile.collision = collision
	
	tile.t_top = top
	tile.t_bottom = bottom
	tile.t_left = left
	tile.t_right = right
	return tile


def createTileFromPath(game, path: str) -> Tile:
	"""create a tile using the Following Path"""
	tile = Tile(game, Vector2(0, 0))
	i = 0
	image = py.Surface((TILETOTALSIZE, TILETOTALSIZE)).convert_alpha()
	image.fill((0, 0, 0, 0))
	grid = [[0 for i in range(TILERESOLUTION)] for j in range(TILERESOLUTION)]
	with open(path, "r") as f:
		y = 0
		index = -1
		for line in f:
			index += 1
			if index < TILERESOLUTION:
				row = line.split(",")
				row[-1] = row[-1].split("\n")[0]
				for x in range(TILERESOLUTION):
					val = int(row[x])
					grid[x][y] = val
					if val != 0:
						image.blit(Textures[val], (x * RESOLUTION, y * RESOLUTION))
				y += 1
			else:
				if line != "S\n":
					rect = [int(elt) for elt in line.split(",")]
					tile.collision.append(
						StaticObject(
							game,
							rect[0] * RESOLUTION,
							rect[1] * RESOLUTION,
							rect[2] * RESOLUTION,
							rect[3] * RESOLUTION,
							f"Object : {id(tile)}({i})"
						)
					)
					i += 1
		f.close()
		
	# List des tuiles sur chacune des bordures
	tile.t_top = [top[0] for top in grid]
	tile.t_bottom = [bottom[-1] for bottom in grid]
	tile.t_left = [left for left in grid[0]]
	tile.t_right = [right for right in grid[-1]]
	tile.image = image
	return tile


if __name__ == '__main__':
	t = Tile("test", Vector2(10, 10), "Tile/tile2343248778288.tile")
	for elt in t.collision:
		print(elt.transform.position, elt.transform.size)
