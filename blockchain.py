#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 14:24:42 2021

@author: Omid Esmailbeig
"""

import datetime
import hashlib
import json


# Building a Blockchain
class Blockchian:
    def __init__(self):
        self.blockchain = []
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
            }
        
        self.blockchain.append(block)
        return block
    
    def get_previous_block(self):
        return self.blockchain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def block_hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_blockchain_valid(self, blockchain):
        previous_block = blockchain[0]
        block_index = 1
        while block_index < len(blockchain):
            # Checking whole blockchain hashes
            block = blockchain[block_index]
            if block['previous_hash'] != self.block_hash(previous_block):
                return False
            # Checking proof of blockchain
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode()).hexdigest() #  Recalcaulate the proof for checking validity
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
                
            
        