"""
Final benchmark for sanskrit_parser #183 - All optimizations
"""

import time
from sanskrit_parser.api import Parser

# Test phrases from issue #183
test_phrases = [
    'Darmakzetre kurukzetre samavetA yuyutsavaH',
    'mAmakAH pARqavAScEva kimakurvata saMjaya',
] * 20  # 40 total parses

print("Sanskrit Parser Final Benchmark - Phase 2 Complete")
print("=" * 60)
print(f"Testing with {len(test_phrases)} phrases...")
print()

# Initialize parser (no beam search for compatibility)
parser = Parser(input_encoding='slp1', output_encoding='slp1')

# Warmup run
print("Warmup run...")
for _ in parser.split(test_phrases[0], limit=1):
    pass

# Timed benchmark
print("Running benchmark...")
start = time.time()

for i, phrase in enumerate(test_phrases):
    try:
        for split in parser.split(phrase, limit=1):
            break
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start
            avg = elapsed / (i + 1)
            print(f"  Progress: {i+1}/{len(test_phrases)}, Avg: {avg*1000:.1f}ms")
    except Exception as e:
        print(f"  Error: {e}")
        break

end = time.time()
total_time = end - start
avg_time = total_time / len(test_phrases)

print()
print("FINAL RESULTS:")
print("=" * 60)
print(f"  Total time: {total_time:.2f}s")
print(f"  Average per parse: {avg_time*1000:.1f}ms")
print(f"  Parses per second: {1/avg_time:.1f}")
print()
print("Comparison to Issue #183:")
print(f"  Baseline: 1,800ms")
print(f"  Phase 2:  {avg_time*1000:.1f}ms")
print(f"  Speedup:  {1800/avg_time/1000:.1f}x")
print()
print(f"  Target: 100ms")
if avg_time*1000 <= 100:
    print(f"  Status: GOAL ACHIEVED! ✓")
    print(f"  Exceeded goal by: {100/(avg_time*1000):.1f}x")
else:
    print(f"  Status: Need {(avg_time*1000)/100:.1f}x more")
