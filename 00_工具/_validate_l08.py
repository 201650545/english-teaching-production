# -*- coding: utf-8 -*-
"""Validate practice_content_DXH_L08.py - word counts and structure"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from practice_content_DXH_L08 import content

def count_words_excluding_blanks(text):
    """Count words, excluding ___N___ placeholders"""
    # Remove blank markers
    text = re.sub(r'___\d+___', '', text)
    # Remove dialogue speaker labels M: W:
    text = re.sub(r'\b[MW]:\s*', '', text)
    words = text.split()
    return len(words)

print("=== Word Count Check (excluding blanks) ===")
ra_text = " ".join(content["reading_a"]["paragraphs"])
print(f"reading_a: {count_words_excluding_blanks(ra_text)} words (target: 107, range: 105-110)")

rb_text = " ".join(content["reading_b"]["paragraphs"])
print(f"reading_b: {count_words_excluding_blanks(rb_text)} words (target: 129, range: 126-132)")

rc_text = " ".join(content["reading_c"]["paragraphs"])
print(f"reading_c: {count_words_excluding_blanks(rc_text)} words (target: 129, range: 126-132)")

w5_text = " ".join(content["w5"]["paragraphs"])
print(f"w5: {count_words_excluding_blanks(w5_text)} words (target: 129, range: 126-132)")

cl_text = " ".join(content["cloze"]["paragraphs"])
print(f"cloze: {count_words_excluding_blanks(cl_text)} words (target: 107, range: 105-110)")

gf_text = content["grammar_fill"]["paragraphs"][0]
print(f"grammar_fill: {count_words_excluding_blanks(gf_text)} words (target: 86, range: 84-88)")

sa_text = " ".join(content["sa"]["paragraphs"])
print(f"sa: {count_words_excluding_blanks(sa_text)} words (target: 107, range: 105-110)")

print()
print("=== Question Count Check ===")
ra_q = len(content["reading_a"]["questions"])
rb_q = len(content["reading_b"]["questions"])
rc_q = len(content["reading_c"]["questions"])
print(f"reading_a: {ra_q}, reading_b: {rb_q}, reading_c: {rc_q}, total: {ra_q+rb_q+rc_q} (target: 11)")
print(f"w5 blanks: {len(content['w5']['answers'])} (target: 4)")
print(f"cloze items: {len(content['cloze']['items'])} (target: 10)")
print(f"grammar_fill answers: {len(content['grammar_fill']['answers'])} (target: 10)")
print(f"sa questions: {len(content['sa']['questions'])} (target: 5)")
print(f"grammar_diag mc: {len(content['grammar_diag']['mc'])} (target: 5)")
print(f"grammar_diag fill: {len(content['grammar_diag']['fill'])} (target: 5)")

print()
print("=== Answer Distribution (before randomize) ===")
all_answers = []
for q in content["reading_a"]["questions"]:
    all_answers.append(q["answer"])
for q in content["reading_b"]["questions"]:
    all_answers.append(q["answer"])
for q in content["reading_c"]["questions"]:
    all_answers.append(q["answer"])
for k, v in sorted(content["w5"]["answers"].items(), key=lambda x: int(x[0])):
    all_answers.append(v)
for it in content["cloze"]["items"]:
    all_answers.append(it["answer"])
for q in content["grammar_diag"]["mc"]:
    all_answers.append(q["answer"])
print(f"All choice answers: {all_answers}")
from collections import Counter
print(f"Distribution: {Counter(all_answers)}")

print()
print("=== Forbidden Check ===")
irregular = ["went", "bought", "ate", "took", "came", "saw", "said", "made", "got", "gave", "ran", "sat", "wrote", "spoke", "drank", "sang", "swam", "drove", "flew", "slept", "felt", "fell", "told", "sold", "held", "found", "spent", "left", "lost", "brought", "taught", "caught", "fought", "thought", "bought", "brought"]
for section in ["cloze", "grammar_fill"]:
    text = " ".join(content[section]["paragraphs"]) if isinstance(content[section]["paragraphs"], list) else content[section]["paragraphs"][0]
    words_lower = re.findall(r'\b[a-z]+\b', text.lower())
    for w in irregular:
        if w in words_lower:
            print(f"WARNING: irregular verb '{w}' found in {section} text!")

print()
print("=== Done ===")
