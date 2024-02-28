'''
We want to make a script that goes through a list of Greek polytonic words with macrons/breves and checks the length() function on every DICHRONA = A, I, U. 
If SHORT, then we first apply strip_length() on it and then append a ^ after it. 
If LONG, then we first apply strip_length() on it and then append a _ after it.
'''

from greek_accentuation.characters import length, strip_length
#import greek_accentuation

SHORT = '̆'
LONG = '̄'

# Test av greek_accentuation's förmåga att kolla macron/breve

print(length('ῠ') == SHORT) # True
print(length('Ῡ') == SHORT) # False
print(length('Ῡ') == LONG) # True
print(length('Ᾱ́') == LONG) # True
print(length('Ᾱ́') == SHORT) # False
print(length('Ῠ̔́') == SHORT) # True
print(length('Ῠ̔́') == LONG) # False

# Verkar fungera finfint! :D
# Test av att ta bort macron/breve

print(strip_length('ῡ'))
print(strip_length('Ᾱ́'))
print(f"Strip club: " + strip_length('Ῠ̔́')) # Fungerar, men spiritus syns ej vid print i terminalen