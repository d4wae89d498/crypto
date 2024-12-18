import numpy as np
import matplotlib.pyplot as plt

def generate_grid_of_lattice_points(v1, v2):
	points = []
	for x in range(0, 10):
		for y in range(0, 10):
			points.append((x * v1[0] + y * v1[1], x * v2[0] + y * v2[1]))
	return points

def plot_lattice_points(points, v1, v2):
	fig, ax = plt.subplots()
	ax.set_aspect('equal', 'box')

	for point in points:
		ax.plot(point[0], point[1], 'bo')

	ax.set_xlim(min(p[0] for p in points) - 1, max(p[0] for p in points) + 1)
	ax.set_ylim(min(p[1] for p in points) - 1, max(p[1] for p in points) + 1)

	ax.grid(True, which='both')
	ax.axhline(0, color='black',linewidth=1)
	ax.axvline(0, color='black',linewidth=1)

	plt.show()

if __name__ == "__main__":
	v1 = [5.3, 3]
	v2 = [-13.3, 4]

	lattice_points = generate_grid_of_lattice_points(v1, v2)

	plot_lattice_points(lattice_points, v1, v2)
