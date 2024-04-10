import tkinter as tk
from tkinter import filedialog
from os import path
file = ""  # From This File ("" pour créer un vie)
SavePath = ""  # To This File (Required)


def Save():
	global input_field, file, output_field, SavePath, window
	file = input_field.get()
	SavePath = output_field.get()
	window.quit()


def loadtemplate_input():
	global input_field
	filename = filedialog.askopenfilename()
	if filename.split(".")[-1] != "tile":
		print("Wrong Extention !")
		return
	input_field.set(filename)


def loadtemplate_output():
	global output_field
	filename = filedialog.askopenfilename()
	if filename.split(".")[-1] != "tile":
		print("Wrong Extention !")
		return
	output_field.set(filename)


window = tk.Tk()
window.geometry("500x500")
window.maxsize(500, 500)
window.minsize(500, 500)

input_field = tk.StringVar(window)
output_field = tk.StringVar(window)

frame = tk.Frame(window)
label = tk.Label(frame, text="Input (Vide pour créer un nouveau)")
entry = tk.Entry(frame, textvariable=input_field)
browse_but = tk.Button(frame, text="Load", command=loadtemplate_input)

frame2 = tk.Frame(window)
label2 = tk.Label(frame2, text="OutPut (Vide pour créer un nouveau)")
entry2 = tk.Entry(frame2, textvariable=output_field)
browse_but2 = tk.Button(frame2, text="Load", command=loadtemplate_output)

button = tk.Button(window, text="Validate", command=Save)

frame.grid(row=0)
label.grid(row=0, column=0)
entry.grid(row=0, column=1)
browse_but.grid(row=0, column=2)

frame2.grid(row=1)
label2.grid(row=0, column=0)
entry2.grid(row=0, column=1)
browse_but2.grid(row=0, column=2)

button.grid(row=2, column=0)

All = False

if not All:
	window.mainloop()

from GeoMath import *

running = not All

TILESIZE = int(600 / TILERESOLUTION)

for i in range(1, len(Textures)):
	Textures[i] = py.transform.smoothscale(Textures[i], (TILESIZE, TILESIZE))

Matrix = [
	[0 for _ in range(TILERESOLUTION)] for __ in range(TILERESOLUTION)
]

if file != "":
	with open(file, "r") as f:
		y = 0
		for line in f:
			if y < TILERESOLUTION:
				l = line.split(",")
				l[-1] = l[-1].split("\n")[0]
				for x in range(TILERESOLUTION):
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
		if y > TILESIZE * TILERESOLUTION - 1:
			pass
		elif x > TILESIZE * TILERESOLUTION - 1:
			for i in range(1, len(Textures)):
				if Box(Vector2(610 + ((i - 1) % LARGE) * (TILESIZE + 10), 10 + (int((i - 1) / LARGE)) * (TILESIZE + 10)), Vector2(TILESIZE, TILESIZE)).CollidePoint(Vector2(x, y)):
					selected = i
					break
		else:
			x = int(x / TILESIZE)
			y = int(y / TILESIZE)
			Matrix[x][y] = selected
	if py.mouse.get_pressed(3)[2]:
		x, y = py.mouse.get_pos()
		if x > TILESIZE * TILERESOLUTION - 1 or y > TILESIZE * TILERESOLUTION - 1:
			pass
		else:
			x = int(x / TILESIZE)
			y = int(y / TILESIZE)
			Matrix[x][y] = 0
	for event in py.event.get():
		if event.type == py.QUIT:
			running = False


if All:
	for elt in TILES:
		Matrix = [
			[0 for _ in range(TILERESOLUTION)] for __ in range(TILERESOLUTION)
		]

		with open(elt, "r") as f:
			y = 0
			for line in f:
				if y < TILERESOLUTION:
					l = line.split(",")
					l[-1] = l[-1].split("\n")[0]
					for x in range(TILERESOLUTION):
						Matrix[x][y] = int(l[x])
				y += 1
			f.close()

		rectangles = []

		startAt = 0
		precIsVide = True
		height = 0
		for x in range(TILERESOLUTION):
			for y in range(TILERESOLUTION):
				if Matrix[x][y] != 0:
					if precIsVide:
						startAt = y
					height += 1
					precIsVide = False
				if Matrix[x][y] == 0 and not precIsVide:
					rectangles.append((x, startAt, 1, height))
					height = 0
					precIsVide = True
			if height > 0:
				rectangles.append((x, startAt, 1, y - startAt))
			precIsVide = True
			height = 0
			startAt = 0

		rectangles2 = []
		current_rect = []
		Found = False
		width = 1
		used = []
		for i in range(len(rectangles)):
			if i not in used:
				current_rect = list(rectangles[i])
				width = 1
				while True:
					Found = False
					for j in range(len(rectangles)):
						if i != j:
							if rectangles[j][0] == rectangles[i][0] + width and rectangles[i][1] == rectangles[j][1] and \
									rectangles[j][3] == rectangles[i][3]:
								used.append(j)
								Found = True
								width += 1
								current_rect[2] += 1
					if not Found:
						break
				rectangles2.append(current_rect)

		SavePath = elt
		with open(SavePath, "w+") as f:
			for y in range(TILERESOLUTION):
				for x in range(TILERESOLUTION):
					f.write(str(Matrix[x][y]))
					if x == TILERESOLUTION - 1:
						f.write("\n")
					else:
						f.write(",")
			for elt in rectangles2:
				f.write(f"{elt[0]}, {elt[1]}, {elt[2]}, {elt[3]}\n")
			f.write("S\n")
			f.close()
else:
	if SavePath == "":
		while SavePath == "" or path.exists(SavePath):
			SavePath = f"Tile/tile{id(Vector2(0, 0))}.tile"

	rectangles = []

	startAt = 0
	precIsVide = True
	height = 0
	for x in range(TILERESOLUTION):
		for y in range(TILERESOLUTION):
			if Matrix[x][y] != 0:
				if precIsVide:
					startAt = y
				height += 1
				precIsVide = False
			if Matrix[x][y] == 0 and not precIsVide:
				rectangles.append((x, startAt, 1, height))
				height = 0
				precIsVide = True
		if height > 0:
			rectangles.append((x, startAt, 1, y - startAt))
		precIsVide = True
		height = 0
		startAt = 0

	rectangles2 = []
	current_rect = []
	Found = False
	width = 1
	used = []
	for i in range(len(rectangles)):
		if i not in used:
			current_rect = list(rectangles[i])
			width = 1
			while True:
				Found = False
				for j in range(len(rectangles)):
					if i != j:
						if rectangles[j][0] == rectangles[i][0] + width and rectangles[i][1] == rectangles[j][1] and rectangles[j][3] == rectangles[i][3]:
							used.append(j)
							Found = True
							width += 1
							current_rect[2] += 1
				if not Found:
					break
			rectangles2.append(current_rect)


	with open(SavePath, "w+") as f:
		for y in range(TILERESOLUTION):
			for x in range(TILERESOLUTION):
				f.write(str(Matrix[x][y]))
				if x == TILERESOLUTION-1:
					f.write("\n")
				else:
					f.write(",")
		for elt in rectangles2:
			f.write(f"{elt[0]}, {elt[1]}, {elt[2]}, {elt[3]}\n")
		f.write("S\n")
		f.close()