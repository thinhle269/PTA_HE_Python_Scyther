import seal

# Create an instance of EncryptionParameters with the BFV scheme
parms = seal.EncryptionParameters(seal.scheme_type.bfv)

# Set the polynomial modulus degree (must be a power of 2)
poly_modulus_degree = 8192
parms.set_poly_modulus_degree(poly_modulus_degree)

# Set the coefficient modulus (recommended for 8192 poly_modulus_degree)
parms.set_coeff_modulus(seal.CoeffModulus.BFVDefault(poly_modulus_degree))

# Set the plaintext modulus (must be a prime number, smaller plaintext modulus gives faster encryption/decryption)
parms.set_plain_modulus(seal.PlainModulus.Batching(poly_modulus_degree, 20))

# Create a SEALContext object
context = seal.SEALContext.Create(parms)

# Generate keys
keygen = seal.KeyGenerator(context)
public_key = keygen.public_key()
secret_key = keygen.secret_key()
relin_keys = keygen.relin_keys()

# Encryptor, Evaluator, and Decryptor
encryptor = seal.Encryptor(context, public_key)
evaluator = seal.Evaluator(context)
decryptor = seal.Decryptor(context, secret_key)

# Create an encoder to encode integers into plaintext polynomials
encoder = seal.IntegerEncoder(context)

# Encode a value into a plaintext polynomial
plain = encoder.encode(12345)

# Encrypt the plaintext polynomial
ciphertext = seal.Ciphertext()
encryptor.encrypt(plain, ciphertext)

# Print the encrypted value (ciphertext)
print("Encrypted value (ciphertext):", ciphertext)

# Decrypt the ciphertext back to plaintext
decrypted_plain = seal.Plaintext()
decryptor.decrypt(ciphertext, decrypted_plain)

# Decode the plaintext polynomial back to an integer
decrypted_value = encoder.decode_int32(decrypted_plain)
print("Decrypted value:", decrypted_value)
