#!/usr/bin/env python
"""
Script para ejecutar NLP processing
"""
import sys
import os

# Cambiar al directorio correcto
os.chdir(r'\\wsl.localhost\Ubuntu\home\alexisfrankj\mt-weo-analysis')
sys.path.insert(0, os.getcwd())

# Ahora importar el módulo
exec(open('src/04_nlp_processing.py').read())
