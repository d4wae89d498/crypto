import numpy as np
import matplotlib.pyplot as plt

def generate_grid_of_lattice_points(v1, v2):
	points = []
	for x in range(0, 10):
		for y in range(0, 10):
			points.append((x * v1[0] + y * v1[1], x * v2[0] + y * v2[1]))
	return points

def plot_lattice_points(points):
	fig, ax = plt.subplots()
	ax.set_aspect('equal', 'box')

	# Plot each point based on its position
	for point in points:
		ax.plot(point[0], point[1], 'bo')

	# Adjust plot limits with padding for better visibility of points
	ax.set_xlim(min(p[0] for p in points) - 1, max(p[0] for p in points) + 1)
	ax.set_ylim(min(p[1] for p in points) - 1, max(p[1] for p in points) + 1)

	# Display grid for better understanding of the shift
	ax.grid(True, which='both')
	ax.axhline(0, color='black',linewidth=1)
	ax.axvline(0, color='black',linewidth=1)

	ax.plot(3.5, 5.5, 'ro')  # Red point at (3.5, 5.5)

	plt.show()

if __name__ == "__main__":
	v1 = [5.2, 3]
	v2 = [-13.3, 4]

	# Generate the grid of lattice points with the bias applied
	lattice_points = generate_grid_of_lattice_points(v1, v2)

	print("Sample points after applying bias:")
	for point in lattice_points[:5]:
		print(point)

	plot_lattice_points(lattice_points)
