"""
Profile script to identify remaining bottlenecks for #183 Phase 2
"""

import cProfile
import pstats
from io import StringIO
from sanskrit_parser.api import Parser

# Test phrase
test_phrase = 'Darmakzetre kurukzetre samavetA yuyutsavaH'

# Initialize parser with beam search
parser = Parser(input_encoding='slp1', output_encoding='slp1', max_splits_per_position=200)

# Profile the parse
pr = cProfile.Profile()
pr.enable()

# Run 10 iterations
for _ in range(10):
    for split in parser.split(test_phrase, limit=1):
        break

pr.disable()

# Print stats
s = StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(30)  # Top 30 functions by cumulative time

print(s.getvalue())

# Also print by total time
s2 = StringIO()
ps2 = pstats.Stats(pr, stream=s2).sort_stats('tottime')
ps2.print_stats(20)  # Top 20 by total time

print("\n" + "="*60)
print("TOP FUNCTIONS BY TOTAL TIME:")
print("="*60)
print(s2.getvalue())
