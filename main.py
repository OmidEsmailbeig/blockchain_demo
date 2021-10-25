#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:27:09 2021

@author: Omid Esmaeilbeig
"""

from web_app import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
