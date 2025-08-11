#!/usr/bin/env python3
"""
Script de teste para executar o projeto b2bflow-supabase-zapi
"""

import os
import sys

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import run

if __name__ == "__main__":
    sys.exit(run())
