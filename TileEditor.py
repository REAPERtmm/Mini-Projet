from Settings import *
from GeoMath import *

running = True

TILESIZE = int(600 / TILERESOLUTION)

for i in range(1, len(Textures)):
	Textures[i] = py.transform.smoothscale(Textures[i], (TILESIZE, TILESIZE))

file = "Tile/tile"
SavePath = "Tile/tile"
Matrix = [
	[0 for _ in range(TILERESOLUTION)] for __ in range(TILERESOLUTION)
]

if file != "":
	with open(file, "r") as f:
		y = 0
		for line in f:
			l = line.split(",")
			l[-1] = l[-1].split("\n")[0]
			for x in range(16):
				Matrix[x][y] = int(l[x])
			y += 1
		f.close()

selected = 1

while running:
	SCREEN.fill(0)

	py.draw.rect(
		SCREEN,
		GREY,
		(
			600, 0, 200, 600
		)
	)

	LARGE = int(180 / TILESIZE)
	for i in range(1, len(Textures)):
		if selected == i:
			py.draw.rect(
				SCREEN,
				RED,
				(
					605 + ((i - 1) % LARGE) * (TILESIZE + 10),
					5 + (int((i - 1) / LARGE)) * (TILESIZE + 10),
					TILESIZE + 10,
					TILESIZE + 10
				)
			)

		SCREEN.blit(
			Textures[i],
			(
				610 + ((i - 1) % LARGE) * (TILESIZE + 10),
				10 + (int((i - 1) / LARGE)) * (TILESIZE + 10)
			)
		)

	for x in range(TILERESOLUTION):
		for y in range(TILERESOLUTION):
			if Matrix[x][y] != 0:
				SCREEN.blit(
					Textures[Matrix[x][y]],
					(
						x * TILESIZE,
						y * TILESIZE
					)
				)

	py.display.flip()
	if py.mouse.get_pressed(3)[0]:
		x, y = py.mouse.get_pos()
		if y > HEIGHT - 10:
			pass
		elif x > 590:
			for i in range(1, len(Textures)):
				if Box(Vector2(610 + ((i - 1) % LARGE) * (TILESIZE + 10), 10 + (int((i - 1) / LARGE)) * (TILESIZE + 10)), Vector2(TILESIZE, TILESIZE)).CollidePoint(Vector2(x, y)):
					selected = i
					break
		else:
			print(x, y)
			x = int(x / TILESIZE)
			y = int(y / TILESIZE)
			print(x, y)
			Matrix[x][y] = selected
	if py.mouse.get_pressed(3)[2]:
		x, y = py.mouse.get_pos()
		if x > 590 or y > HEIGHT - 10:
			pass
		else:
			x = int(x / TILESIZE)
			y = int(y / TILESIZE)
			Matrix[x][y] = 0
	for event in py.event.get():
		if event.type == py.QUIT:
			running = False

with open(SavePath, "w+") as f:
	for y in range(16):
		for x in range(16):
			f.write(str(Matrix[x][y]))
			if x == 15:
				f.write("\n")
			else:
				f.write(",")
	f.close()