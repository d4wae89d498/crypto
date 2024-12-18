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
		[0.1, 2],
		[0.5, 1]
	]

def gen_public_key(sk, factor):
	v1, v2 = sk

	noise_factor = random.uniform(0.9, 1.1)

	return [
		[v1[0] * factor, v1[1] * factor],
		[v2[0] * factor + v2[0] * noise_factor, v1[1] * factor + v2[1] * noise_factor],
	]

def encode(pk, message):
    v1, v2 = pk
    encoded_message = [
		[v1[0] * message[0] + v1[1] * message[0] + random.uniform(-0.1, 0.1)],
		[v2[0] * message[1] + v2[1] * message[1] + random.uniform(-0.1, 0.1)],
    ]
    return encoded_message

def decode(sk, pk, enc):
   pass

if __name__ == "__main__":
	sk = gen_secret_key()
	pk = gen_public_key(sk, 2)
	print("sk=", sk)
	print("pk=", pk)

	msg = [1, 2]
	print("msg=", msg)

	enc = encode(pk, [1, 2])
	print("enc=", enc)


	lattice_points = generate_grid_of_lattice_points(sk[0], sk[1])

	plot_lattice_points(lattice_points, sk[0], sk[1], pk[0], pk[1])
