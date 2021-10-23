#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:06:19 2021

@author: Omid Esmaeilbeig
"""

from blockchain import Blockchian
from flask import Flask, jsonify

#  Create a Web App
app = Flask(__name__)

#  Create a blockhain
blockchain = Blockchian()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    block = blockchain.create_block(proof,
                                    blockchain.block_hash(previous_block))
    response = {'message': 'The block mined successfully',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'hash': blockchain.block_hash(block),
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200
    

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    response = {'blockchain': blockchain.blockchain,
                'lenght': len(blockchain.blockchain)}
    
    return jsonify(response), 200
    
