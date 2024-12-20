import numpy as np
import matplotlib.pyplot as plt
import random

def generate_grid_of_lattice_points(v1, v2):
	points = []
	for x in range(0, 10):
		for y in range(0, 10):
			points.append((x * v1[0] + y * v1[1], x * v2[0] + y * v2[1]))
	return points

def plot_lattice_points(points, v1, v2, v3, v4):
	fig, ax = plt.subplots()
	ax.set_aspect('equal', 'box')

	for point in points:
		ax.plot(point[0], point[1], 'bo')

	ax.plot([0, v1[0]], [0, v1[1]], color='purple', label="v1")
	ax.plot([0, v2[0]], [0, v2[1]], color='purple', label="v2")

	ax.plot([0, v3[0]], [0, v3[1]], color='red', label="v3")
	ax.plot([0, v4[0]], [0, v4[1]], color='red', label="v4")

	ax.set_xlim(min(p[0] for p in points) - 1, max(p[0] for p in points) + 1)
	ax.set_ylim(min(p[1] for p in points) - 1, max(p[1] for p in points) + 1)

	ax.grid(True, which='both')
	ax.axhline(0, color='black',linewidth=1)
	ax.axvline(0, color='black',linewidth=1)

	plt.legend()
	plt.show()

def gen_secret_key():
	return [
		[3, 1.5],
		[1, 2]
	]

def gen_public_key(sk, factor):
	noise_factor = random.uniform(0.9, 1.1)
	return [
		[sk[0][0] * factor, sk[0][1] * factor],
		[sk[0][0] * factor + sk[1][0], sk[0][1] * factor + sk[1][1]]
	]

def encode(pk, msg):
	noise = [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)]
	return [
		pk[0][0] * msg[0] + pk[0][1] * msg[1] + noise[0],
		pk[1][0] * msg[0] + pk[1][1] * msg[1] + noise[1]
	]

def closest_lattice_point(secret_key, point):
	sk = np.array(secret_key, dtype=float)
	pt = np.array(point, dtype=float)
	sk_inv = np.linalg.inv(sk)
	coords = sk_inv @ pt
	nearest_coords = np.round(coords)
	closest_point = sk @ nearest_coords
	return closest_point.tolist()

def decode(sk, pk, enc):
	enc = closest_lattice_point(sk, enc)
	det = pk[0][0] * pk[1][1] - pk[0][1] * pk[1][0]
	if det == 0:
		raise ValueError("Determinant is zero, cannot invert the matrix")
	inv_pk = [
		[pk[1][1] / det, -pk[0][1] / det],
		[-pk[1][0] / det, pk[0][0] / det]
	]
	a, b = [
		inv_pk[0][0] * enc[0] + inv_pk[0][1] * enc[1],
		inv_pk[1][0] * enc[0] + inv_pk[1][1] * enc[1]
	]
	return [round(a), round(b)]

def fhe_add(a, b):
	return [a[0] + b[0], a[1] + b[1]]

def fhe_mult(a, b):
	return [a[0] * b[0], a[1] * b[1]]

if __name__ == "__main__":
	sk = gen_secret_key()
	pk = gen_public_key(sk, 4)
	print("sk=", sk)
	print("pk=", pk)
	msg = [2, 3]
	print("msg=", msg)
	enc = encode(pk, msg)
	enc = fhe_add(enc, enc)
	print("enc=", enc)
	dec = decode(sk, pk, enc)
	print("dec=", dec)
	lattice_points = generate_grid_of_lattice_points(sk[0], sk[1])
	plot_lattice_points(lattice_points, sk[0], sk[1], pk[0], pk[1])
