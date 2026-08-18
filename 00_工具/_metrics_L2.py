# -*- coding: utf-8 -*-
import re
from collections import Counter
html = open('_tmp_L2.html', encoding='utf-8').read()
# Extract each interaction container's metadata
items = re.findall(
    r'data-interaction-item="1"[^>]*data-question-id="([^"]*)"[^>]*data-section="([^"]*)"'
    r'[^>]*data-interaction-type="([^"]*)"[^>]*data-action-type="([^"]*)"'
    r'[^>]*data-cognitive-level="([^"]*)"[^>]*data-scorable="([^"]*)"',
    html)
print('TOTAL items:', len(items))
print('by type:', dict(Counter(i[2] for i in items)))
print('by action:', dict(Counter(i[3] for i in items)))
print('by cognitive:', dict(Counter(i[4] for i in items)))
print('by section:', dict(Counter(i[1] for i in items)))

CHOICE = {'single_choice', 'multiple_choice', 'true_false', 'choice'}
HOT = {'grammar', 'vocab', 'drill', 'extend', 'diagnosis'}
scorable = [i for i in items if i[5] != 'false']
print('scorable:', len(scorable))
choices = [i for i in scorable if i[2] in CHOICE]
hot = [i for i in scorable if i[1] in HOT]
hot_choices = [i for i in hot if i[2] in CHOICE]
recognition = [i for i in scorable if i[4] == 'recognition']
actions = {i[3] for i in scorable if i[3] != 'unknown'}
print('CHOICE ratio: %.1f%% (%d/%d)' % (100.0*len(choices)/len(scorable), len(choices), len(scorable)))
if hot:
    print('HOT zone choice ratio: %.1f%% (%d/%d)' % (100.0*len(hot_choices)/len(hot), len(hot_choices), len(hot)))
print('RECOGNITION ratio: %.1f%% (%d/%d)' % (100.0*len(recognition)/len(scorable), len(recognition), len(scorable)))
print('ACTION types (%d):' % len(actions), sorted(actions))