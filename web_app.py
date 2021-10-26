#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:06:19 2021

@author: Omid Esmaeilbeig
"""

from typing import Tuple
from flask import Flask, jsonify  # type: ignore
from flask.wrappers import Response  # type: ignore
from blockchain import Blockchain


#  Create a Web App
app = Flask(__name__)

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
                'previous_hash': block['previous_hash']}

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
