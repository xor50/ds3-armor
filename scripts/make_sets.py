#!/usr/bin/env python3
"""
Generates data/sets.json (the armor sets) from data/armors.json.

armors.json doesn't know anything about sets, so they are derived from the item names:
    "Havel's Helm", "Havel's Armor", ...  ->  the "Havel's Set"
    "Helm of Thorns", "Armor of Thorns"   ->  the "Thorns Set"

Names that don't follow these patterns are handled by the tables below. Only groups of at
least 2 items become sets: single items are still available in the per-item tables.

Run it from the root of the repository:   python3 scripts/make_sets.py
"""

import collections
import json
import re
import sys

KINDS = ['helms', 'chests', 'gauntlets', 'leggings']


# Names whose "stem" (the name without its last word) isn't the name of their set
STEM_ALIASES = {
    'Cleric Blue':        'Cleric',        # Cleric Blue Robe
    "Karla's Pointed":    "Karla's",       # Karla's Pointed Hat
    'Archdeacon White':   'Archdeacon',    # Archdeacon White Crown
    'Archdeacon Holy':    'Archdeacon',    # Archdeacon Holy Garb
}

# Groups that contain several items of the same kind: which one belongs to the set
# (the others are left out of it). TO VERIFY in game.
AMBIGUOUS = {
    ('Leather', 'gauntlets'): 'Leather Gloves',   # not 'Leather Gauntlets'
}


def stem_of(name):
    # "Helm of Thorns", "Embraced Armor of Favor" -> "Thorns", "Favor"
    match = re.match(r'^.+? of (.+)$', name)
    if match:
        return match.group(1)

    words = name.split()
    stem = ' '.join(words[:-1]) if len(words) > 1 else name
    return STEM_ALIASES.get(stem, stem)


def main():
    with open('data/armors.json') as f:
        armors = json.load(f)

    groups = collections.defaultdict(lambda: collections.defaultdict(list))
    for kind in KINDS:
        for item in armors[kind]:
            groups[stem_of(item['name'])][kind].append(item['name'])

    sets = []
    problems = []

    for stem in sorted(groups):
        pieces = {}

        for kind in KINDS:
            names = groups[stem].get(kind, [])

            if len(names) > 1:
                chosen = AMBIGUOUS.get((stem, kind))
                if chosen is None:
                    problems.append('"%s" has several %s: %s' % (stem, kind, ', '.join(names)))
                    continue
                names = [chosen]

            if names:
                pieces[kind] = names[0]

        if len(pieces) >= 2:
            sets.append({ 'name': stem + ' Set', 'pieces': pieces })

    if problems:
        print('Ambiguous groups, add them to AMBIGUOUS:')
        print('\n'.join('  ' + p for p in problems))
        sys.exit(1)

    # Sanity checks: every item exists, and belongs to at most one set
    known = { kind: set(i['name'] for i in armors[kind]) for kind in KINDS }
    seen = set()
    for s in sets:
        for kind, name in s['pieces'].items():
            assert name in known[kind], name
            assert (kind, name) not in seen, 'in several sets: ' + name
            seen.add((kind, name))

    with open('data/sets.json', 'w') as f:
        json.dump(sets, f, indent=4)
        f.write('\n')

    by_size = collections.Counter(len(s['pieces']) for s in sets)
    print('%d sets written to data/sets.json (%s)' %
          (len(sets), ', '.join('%d pieces: %d' % (n, by_size[n]) for n in sorted(by_size, reverse=True))))
    total = sum(len(armors[k]) for k in KINDS)
    print('%d of %d items are part of a set' % (len(seen), total))


if __name__ == '__main__':
    main()
