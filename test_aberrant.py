from handle_aberrant_lines import consolidate_vowels, is_properispomenon, has_dichrona_before_second_to_last_vowel_group, is_aberrant_token

print(is_aberrant_token('*pi=san')) # True: no DICHRONA
print(is_aberrant_token('h(=s')) # True: no DICHRONA
print(is_aberrant_token('pai=s')) # True: no DICHRONA
print(is_aberrant_token('neavi/as')) # False: Has dichrona, is not properispomenon and has A on antepenultimate
print(is_aberrant_token('A'))
print(is_aberrant_token('AA'))
