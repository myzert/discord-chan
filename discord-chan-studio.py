#!/usr/bin/env python3
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "src"))

import studio

if __name__ == "__main__":
    studio.main()
