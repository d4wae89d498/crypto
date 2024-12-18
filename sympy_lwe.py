import numpy as np
import random
import sympy as sp

q = 89

def linear_function(coeffs):
	x = sp.symbols('x1:%d' % (len(coeffs) + 1))
	linear_expr = sum(c * x[i] for i, c in enumerate(coeffs))
	return linear_expr


def gen_secret_key():
	return [random.randint(0, 100) for _ in range(4)]

def gen_public_key(sk):
	pk = []
	for i in range(0, 11):
		row = []
		result = 0
		for y in sk:
			rand = random.randint(0, 100) % q
			result += rand * y
			row.append(rand)
		# Introducing the error
		result += random.randint(-5, 5)
		result %= q
		row.append(result)
		pk.append(row)

	return pk

def encode(pk, bit):
	row = []
	for y in range(0, len(pk[0])):
		row.append(0)
	for i in range(0, 3):
		rand = random.randint(0, len(pk) - 1)
		for y in range(0, len(pk[0])):
			row[y] = (row[y] + pk[rand][y]) % q
	if bit:
		row[len(pk[0]) - 1] = (row[len(pk[0]) - 1] + round(q/2) ) % q
	return linear_function(row[:-1]), row[len(pk[0]) - 1]




def decode(sk, eq):
	expr, usol = eq

	#print("Decoding..", expr)

	x = sp.symbols('x1:%d' % (len(sk) + 1))
	substitution_map = dict(zip(x, sk))

	solution = int(expr.subs(substitution_map).evalf()) % q
#	print("sol=",solution)
	encoded_bit = (solution - usol) % q

#	print("solution: ", solution, " got: ", eq[len(eq) - 1], "sub :", encoded_bit % q)

	distance_to_44 = min(abs(encoded_bit - 44), q - abs(encoded_bit - 44))
	distance_to_0 = min(abs(encoded_bit), q - abs(encoded_bit))

	if distance_to_44 <= distance_to_0:
		return 1
	return 0


def fhe_add(a, b):
	a1, a2 = a
	b1, b2 = b
	return (a1 + b1) % q, (a2 + b2) % q

def fhe_mult(a, b):
	a1, a2 = a
	b1, b2 = b
	return (a1 * b1) % q, (a2 * b2) % q

# Example usage
sk = gen_secret_key()
pk = gen_public_key(sk)

print("sk:", sk)
print("pk:", pk)

enc_one = encode(pk, 1)
enc_zero = encode(pk, 0)

print("one=", enc_one, " zero=", enc_zero)

print("xor(0, 0): ", decode(sk, fhe_add(enc_zero, enc_zero)))
print("xor(0, 1): ", decode(sk, fhe_add(enc_zero, enc_one)))
print("xor(1, 0): ", decode(sk, fhe_add(enc_one, enc_zero)))
print("xor(1, 1): ", decode(sk, fhe_add(enc_one, enc_one)))
print("---")
print("and(0, 0): ", decode(sk, fhe_mult(enc_zero, enc_zero)))
print("and(0, 1): ", decode(sk, fhe_mult(enc_zero, enc_one)))
print("and(1, 0): ", decode(sk, fhe_mult(enc_one, enc_zero)))
print("and(1, 1): ", decode(sk, fhe_mult(enc_one, enc_one)))
