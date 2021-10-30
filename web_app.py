#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:06:19 2021

@author: Omid Esmaeilbeig
"""

import json
from typing import Tuple
from flask import Flask, jsonify, request  # type: ignore
from flask.wrappers import Response  # type: ignore
from uuid import uuid4

from blockchain import Blockchain


#  Create a Web App
app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

#  Create a blockchain
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block() -> Tuple["Response", int]:
    """This endpoint mines a block

    Returns:
        Tuple[Response, int]: returns a reponse of containing mined block and
        a related HTTP code.
    """
    previous_block = blockchain.get_previous_block()
    nonce = Blockchain.proof_of_work(previous_block['nonce'])
    block = blockchain.create_block(nonce,
                                    Blockchain.block_hash(previous_block))
    response = {'message': 'The block mined successfully',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'hash': blockchain.block_hash(block),
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}

    return jsonify(response), 200


@app.route('/get_blockchain', methods=['GET'])
def get_blockchain() -> Tuple["Response", int]:
    """Get blockchian information

    Returns:
        Tuple[Response, int]: Returns blockchian information and length of it
        and a related HTTP code
    """
    response = {'blockchain': blockchain.blockchain,
                'length': len(blockchain.blockchain)}

    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction() -> Tuple["Response", int]:
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return jsonify({'message': "Bad Request"}), 400
    index = blockchain.add_transaction(
        sender=json['sender'],
        receiver=json['receiver'],
        amount=json['amount']
    )
    response = {'message': f'This transaction will be added to block {index}'}

    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node() -> Tuple["Response", int]:
    """Connect Nodes to blockchain

    Returns:
        Tuple[Response, int]: Returns connected Nodes and HTTP code
    """
    json = request.get_json()
    nodes = json.get('nodes')
    if not nodes:
        return jsonify({'message': 'No nodes exist'}), 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'Nodes connected to blockchain',
        'total_nodes': list(blockchain.nodes)
    }

    return jsonify(response), 201


@app.route('/is_valid', methods=['GET'])
def is_valid() -> Tuple["Response", int]:
    is_valid = blockchain.is_blockchain_valid(blockchain.blockchain)
    if is_valid:
        response = {'message': 'Blockchain is valid'}
        return jsonify(response), 200
    else:
        response = {'message': 'Blockchain is not valid'}
        return jsonify(response), 400


@app.route('/consensus_protocol', methods=['GET'])
def consensus_protocol() -> Tuple["Response", int]:
    is_updated = blockchain.consensus_protocol()
    print(is_updated)
    if is_updated:
        response = {
            'message': 'The longest chain is updated though the network',
            'updated_chain': blockchain.blockchain}
    else:
        response = {
            'message': 'The blockchain was updated through the network',
            'current_chain': blockchain.blockchain}

    return jsonify(response), 200
