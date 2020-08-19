#!/usr/bin/env python

import argparse
import hashlib
import string
import sys
import time
import random


parser = argparse.ArgumentParser(description='Proof of work')
parser.add_argument('-d', '--difficulty', type=int, required=True)
parser.add_argument('-i', '--index', type=int, required=True)
parser.add_argument('-n', '--number', type=int, required=True)

block = "COMSM0010cloud"
block_roget = "Roget"


def list_to_binary(input_list):
    result = ''.join(map(str, input_list))
    result = int(result, 32)
    return bin(result)


def generate_input(input_block, nonce):
    input_block = [ord(c) for c in input_block]
    input_block.append(nonce)
    return list_to_binary(input_block)


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def main(args):
    start_time = time.time()

    start_value = args.index * int((2**32/args.number))
    end_value = (args.index+1) * int((2**32/args.number))

    input_block = block
    for nonce in range(start_value, end_value):
        block2 = generate_input(input_block, nonce)
        str_block3 = str(block2)
        hash1 = hashlib.sha256(str_block3.encode()).hexdigest()
        hash2 = hashlib.sha256(hash1.encode()).hexdigest()
        if hash2[0:args.difficulty] == '0'*args.difficulty:
            print("Block:", input_block, "Nonce:", nonce)
            print("Time Elapsed:", time.time()-start_time)
            print("Golden Nonce:", hash2)
            exit()
    exit()


if __name__ == '__main__':
    main(parser.parse_args())
