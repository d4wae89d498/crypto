import numpy as np
from scipy.stats import norm

def sample_noise(N, q):
	sigma = 1.0
	D = lambda: round(norm.rvs(scale=sigma)) % q
	return np.array([D() for _ in range(N)])

q = 655360001
n = 1000
N = 500

t = np.random.randint(0, q, size=n)
secret_key = np.concatenate(([1], t))

A = np.random.randint(0, q, size=(n, N))
e = sample_noise(N, q)
b = np.dot(A.T, t) + e
public_key = np.hstack([b.reshape(-1, 1), -A.T])

message = 1#np.random.randint(0, 2)  # Random binary message
m_vec = np.concatenate(([message], [0] * n))
r = np.random.randint(0, 2, size=N)
ciphertext = np.dot(public_key.T, r) + (q // 2) * m_vec
print(ciphertext)

ciphertext *= ciphertext

temp = (2 / q) * np.dot(ciphertext, secret_key)
decrypted_message = round(temp) % 2

print(decrypted_message)
print(decrypted_message == message)
