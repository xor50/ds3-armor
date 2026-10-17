# Dark Souls III - Armor optimizer

**This is a fork of https://github.com/Kanma/ds3-armor/ !**

Allows to search the best combinations of armor items to maximize some stats, while
staying under a given load weight.

Can be used at http://xor50.github.io/ds3-armor/

The original is available under https://kanma.github.io/ds3-armor/

## Data

* `data/armors.json`: the armor items and their stats.
* `data/sets.json`: the armor sets, used by the "Available armor sets" panel to mark several items as owned at once.
  It is generated from the item names by `scripts/make_sets.py` (run it from the root of the repository);
  names that don't follow the usual patterns are handled by the tables at the top of that script.
