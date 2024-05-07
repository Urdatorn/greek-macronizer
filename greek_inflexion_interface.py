import os
import sys

from utils import Colors

# Add the greek_inflexion directory to the Python path
sys.path.append(os.path.abspath('./greek_inflexion'))

# Now import the GreekInflexion module
from greek_inflexion import GreekInflexion

resource_dir = os.path.abspath('./greek_inflexion')
stemming_path = os.path.join(resource_dir, 'stemming.yaml')

# Lexica
homer_path = os.path.join(resource_dir, 'STEM_DATA/homer_lexicon.yaml')
ltrg_path = os.path.join(resource_dir, 'STEM_DATA/ltrg_lexicon.yaml')
lxx_path = os.path.join(resource_dir, 'STEM_DATA/lxx_lexicon.yaml')
morphgnt_path = os.path.join(resource_dir, 'STEM_DATA/morphgnt_lexicon.yaml')


# Initialize the GreekInflexion object with full paths
#inflexion = GreekInflexion(stemming_path, homer_path)


def get_stem(token, tag):
    tauber_format = translate_tag_to_tauber_format(tag)

    lexicon_paths = [
        'homer_lexicon.yaml',
        'ltrg_lexicon.yaml',
        'lxx_lexicon.yaml',
        'morphgnt_lexicon.yaml'
    ]

    for lexicon_name in lexicon_paths:
        lexicon_path = os.path.join(resource_dir, 'STEM_DATA', lexicon_name)
        inflexion = GreekInflexion(stemming_path, lexicon_path)
        if inflexion.find_stems(token, tauber_format):
            (stems,) = inflexion.find_stems(token, tauber_format)
            print(f'{Colors.GREEN}{token} has stem {stems} according to {lexicon_name}{Colors.ENDC}')
            return stems

    return None


def translate_tag_to_tauber_format(tag):
    '''
    Translate verb tags to the format used by the greek-inflexion module
    >>> translate_tag_to_tauber_format('v1spia---'))
    >>> PIA.1S
    '''
    # Dictionary mapping for each segment of the tag
    person_map = {'1': '1', '2': '2', '3': '3'}
    number_map = {'s': 'S', 'p': 'P', 'd': 'D'}
    tense_map = {
        'p': 'P', 'i': 'I', 'r': 'R', 'l': 'L',
        't': 'T', 'f': 'F', 'a': 'A'
    }
    mood_map = {
        'i': 'I', 's': 'S', 'o': 'O', 'n': 'N',
        'm': 'M', 'p': 'P'
    }
    voice_map = {'a': 'A', 'p': 'P', 'm': 'M', 'e': 'E'}

    # Extract individual components from the tag
    if tag[0] != 'v':
        return None  # Return None if it's not a verb tag

    person = person_map.get(tag[1], '')
    number = number_map.get(tag[2], '')
    tense = tense_map.get(tag[3], '')
    mood = mood_map.get(tag[4], '')
    voice = voice_map.get(tag[5], '')

    # Create the form string according to Tauber's module format
    form = f"{tense}{voice}{mood}.{person}{number}"

    return form if form != "." else None  # Handle cases where no valid form can be formed


def translate_tauber_to_tag_format(tauber_format):
    '''
    >>> translate_tauber_to_tag_format('PAI.1S')
    >>> v1spia---
    '''
    # Reversing mappings from the previous function
    number_map = {'S': 's', 'P': 'p', 'D': 'd'}
    person_map = {'1': '1', '2': '2', '3': '3'}
    tense_map = {
        'P': 'p', 'I': 'i', 'R': 'r', 'L': 'l',
        'T': 't', 'F': 'f', 'A': 'a'
    }
    mood_map = {
        'I': 'i', 'S': 's', 'O': 'o', 'N': 'n',
        'M': 'm', 'P': 'p'
    }
    voice_map = {'A': 'a', 'P': 'p', 'M': 'm', 'E': 'e'}

    # Extract components from GreekInflexion format
    if '.' not in tauber_format:
        return None  # Invalid format

    tense_mood_voice, person_number = tauber_format.split('.')
    if len(tense_mood_voice) < 3 or len(person_number) < 2:
        return None  # Invalid format

    tense = tense_map.get(tense_mood_voice[0], '-')
    mood = mood_map.get(tense_mood_voice[1], '-')
    voice = voice_map.get(tense_mood_voice[2], '-')
    person = person_map.get(person_number[0], '-')
    number = number_map.get(person_number[1], '-')

    # Construct the tag format for verbs: v + person + number + tense + mood + voice + '---'
    # The final '---' covers gender, case, and degree which are not specified in the GreekInflexion format.
    return f"v{person}{number}{tense}{mood}{voice}---"



if __name__ == '__main__':
    # Example usage
    token = 'συνθανεῖν'
    tag = 'v--ana---'
    stems = get_stem(token, tag)
    print(stems)

    print(get_stem('φέρω', 'v1spia---'))
