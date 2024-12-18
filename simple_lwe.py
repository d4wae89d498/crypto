import numpy as np
import random
import math

q = 89

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
	return row

def decode(sk, eq):
	solution = 0
	for i in range(0, len(eq) - 1):
#		print(sk[i], "*", eq[i], "=", sk[i] * eq[i])
		solution += sk[i] * eq[i]
	solution %= q
	encoded_bit = (solution - eq[len(eq) - 1]) % q

#	print("solution: ", solution, " got: ", eq[len(eq) - 1], "sub :", encoded_bit % q)

	distance_to_44 = min(abs(encoded_bit - 44), q - abs(encoded_bit - 44))
	distance_to_0 = min(abs(encoded_bit), q - abs(encoded_bit))

	if distance_to_44 <= distance_to_0:
		return 1
	return 0



def fhe_and(a, b):
	return [(x * y) % q for x, y in zip(a, b)]

def fhe_xor(a, b):
	return [(x + y) % q for x, y in zip(a, b)]

def fhe_not(enc_one, a):
	return fhe_xor(enc_one, a)


sk = gen_secret_key()
print("sk: ",sk)

pk = gen_public_key(sk)
print("pk: ", pk)

bit = 1
print("bit: ", bit)

enc = encode(pk, bit)
print("enc: ", enc)

dec = decode(sk, enc)
print("dec: ", dec)

print("----------")

enc_one = encode(pk, 1)
print("enc_once: ", enc_one)

enc_zero = encode(pk, 0)
print("enc_zero: ", enc_zero)

print("----------")

enc_result_not = fhe_not(enc_one, enc_zero)
print("fhe_not(0): ", enc_result_not, " clear: ", decode(sk, enc_result_not))

enc_result_not = fhe_not(enc_one, enc_one)
print("fhe_not(1): ", enc_result_not, " clear: ", decode(sk, enc_result_not))

print("----------")

enc_result_xor = fhe_xor(enc_zero, enc_zero)
print("enc_result_xor(0, 0): ", enc_result_xor, " clear: ", decode(sk, enc_result_xor))

enc_result_xor = fhe_xor(enc_zero, enc_one)
print("enc_result_xor(0, 1): ", enc_result_xor, " clear: ", decode(sk, enc_result_xor))

enc_result_xor = fhe_xor(enc_one, enc_zero)
print("enc_result_xor(1, 0): ", enc_result_xor, " clear: ", decode(sk, enc_result_xor))

enc_result_xor = fhe_xor(enc_one, enc_one)
print("enc_result_xor(1, 1): ", enc_result_xor, " clear: ", decode(sk, enc_result_xor))

print("----------")

enc_result_and = fhe_and(enc_zero, enc_zero)
print("enc_result_and(0, 0): ", enc_result_and, " clear: ", decode(sk, enc_result_and))

enc_result_and = fhe_and(enc_zero, enc_one)
print("enc_result_and(0, 1): ", enc_result_and, " clear: ", decode(sk, enc_result_and))

enc_result_and = fhe_and(enc_one, enc_zero)
print("enc_result_and(1, 0): ", enc_result_and, " clear: ", decode(sk, enc_result_and))

enc_result_and = fhe_and(enc_one, enc_one)
print("enc_result_and(1, 1): ", enc_result_and, " clear: ", decode(sk, enc_result_and))
