"""
Benchmark script for sanskrit_parser #183 Phase 1 optimizations

Tests performance improvement from LRU caching and debug logging reduction.
"""

import time
from sanskrit_parser.parser import Parser

# Test phrases from issue #183
test_phrases = [
    'Darmakzetre kurukzetre samavetA yuyutsavaH',
    'mAmakAH pARqavAScEva kimakurvata saMjaya',
] * 20  # 40 total parses

print("Sanskrit Parser Performance Benchmark - Phase 1")
print("=" * 60)
print(f"Testing with {len(test_phrases)} phrases...")
print()

# Initialize parser
parser = Parser(input_encoding='slp1', output_encoding='slp1')

# Warmup run
print("Warmup run...")
_ = parser.parse(test_phrases[0])

# Timed benchmark
print("Running benchmark...")
start = time.time()

for i, phrase in enumerate(test_phrases):
    try:
        result = parser.parse(phrase)
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start
            avg = elapsed / (i + 1)
            print(f"  Progress: {i+1}/{len(test_phrases)}, Avg: {avg*1000:.1f}ms/parse")
    except Exception as e:
        print(f"  Error on phrase {i}: {e}")

end = time.time()
total_time = end - start
avg_time = total_time / len(test_phrases)

print()
print("Results:")
print(f"  Total time: {total_time:.2f}s")
print(f"  Average per parse: {avg_time*1000:.1f}ms")
print(f"  Parses per second: {1/avg_time:.2f}")
print()
print("Target (Issue #183):")
print(f"  Goal: 100ms per parse")
print(f"  Current: {avg_time*1000:.1f}ms")
if avg_time <= 0.1:
    print(f"  ✅ GOAL ACHIEVED!")
else:
    improvement_needed = avg_time / 0.1
    print(f"  ⚠️  Need {improvement_needed:.1f}x more speedup")
