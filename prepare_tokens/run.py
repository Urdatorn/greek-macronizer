'''
Topmost run script for preparing tokens.txt
'''

import main_tokens
import os

'''
All individual file operations should specify encoding='utf-8';
global settings are not enough.
'''
os.environ["PYTHONUTF8"] = "1"

main_tokens.main('tragedies_300595.txt', 'tokens.txt', 'lines_aberrant.txt', 'lines_x.txt')
