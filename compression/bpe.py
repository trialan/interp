import random
import numpy as np


def encode(sequence, compression_map):
    all_pairs = [sequence[i:i+2] for i in range(len(sequence)-2)]
    max_pair_occurrences = 0
    for pair in all_pairs:
        pair_ixs = get_pair_ixs(pair, all_pairs)
        if sum(pair_ixs) > max_pair_occurrences:
            max_pair_occurrences = sum(pair_ixs)
        if sum(pair_ixs) > 1:
            encoding_bit = generate_encoding_bit(sequence)
            compression_map[encoding_bit] = pair
            sequence = sequence.replace(pair, encoding_bit)
    if max_pair_occurrences == 1:
        return sequence, compression_map
    else:
        return encode(sequence, compression_map)


def decode(encoding, compression_map):
    output = encoding
    encoding_bits = compression_map.keys()
    while is_compressed(output, encoding_bits):
        for bit in encoding_bits:
            output = output.replace(bit, compression_map[bit])
    return output


def generate_encoding_bit(sequence):
    candidate = chr(random.randint(0, 256))
    if candidate not in sequence:
        return candidate
    else:
        return generate_encoding_bit(sequence)


def get_pair_ixs(pair, all_pairs):
    ixs = [p==pair for p in all_pairs]
    return np.array(ixs)


def is_compressed(seq, encoding_bits):
    return any([b in seq for b in encoding_bits])


def test_get_pair_ixs():
    x = [[1,2],[3,4]]
    assert np.array_equal(get_pair_ixs([1,2], x), np.array([1,0]))
    assert np.array_equal(get_pair_ixs([3,4], x), np.array([0,1]))

test_get_pair_ixs()


