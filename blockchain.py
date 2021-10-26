#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 14:24:42 2021

@author: Omid Esmailbeig
"""

import datetime
import hashlib
import json
from typing import Dict, List


# Building a Blockchain
class Blockchain:
    """Core implementation of blockchain"""

    def __init__(self) -> None:
        self.blockchain: List = []
        self.create_block(nonce=1, previous_hash='0')

    def create_block(self, nonce: int, previous_hash: str) -> Dict:
        """This method create a block and add it to the blockchain

        Args:
            nonce (int): nonce of work
            previous_hash (str): prevoius block hash

        Returns:
            block (Dict): Created block will be returned
        """

        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'previous_hash': previous_hash
        }

        self.blockchain.append(block)
        return block

    def get_previous_block(self) -> Dict:
        """Get previous block"""
        return self.blockchain[-1]

    @staticmethod
    def proof_of_work(previous_nonce: int) -> int:
        """Proof of work mechanism implemented here.

        Args:
            previous_nonce (int): nonce of previous block

        Returns:
            new_nonce (int): nonce of new block
        """
        new_nonce = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    @staticmethod
    def block_hash(block: Dict) -> str:
        """Block SHA256 hash mechanism

        Args:
            block (Dict): block to hash

        Returns:
            hash of the block (str): hash of the block
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_blockchain_valid(self, blockchain: List) -> bool:
        """Check validity of the blockchain

        Args:
            blockchain (List): Blockchain to validate

        Returns:
            (bool): Returns True if blockchain is valid
        """
        previous_block = blockchain[0]
        block_index = 1

        while block_index < len(blockchain):
            # Checking whole blockchain hashes
            block = blockchain[block_index]
            if block['previous_hash'] != self.block_hash(previous_block):
                return False
            # Checking the blockchain proof of work
            previous_nonce = previous_block['nonce']
            current_nonce = block['nonce']
            # Recalcaulate the nonce for checking validity
            hash_operation = hashlib.sha256(
                str(current_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1

        return True
