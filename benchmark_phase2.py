"""
Benchmark script for sanskrit_parser #183 Phase 2 optimizations

Tests performance with beam search (max_splits_per_position limiting).
"""

import time
from sanskrit_parser.api import Parser

# Test phrases from issue #183
test_phrases = [
    'Darmakzetre kurukzetre samavetA yuyutsavaH',
    'mAmakAH pARqavAScEva kimakurvata saMjaya',
] * 20  # 40 total parses

def run_benchmark(beam_width, label):
    print(f"\n{label} (beam_width={beam_width}):")
    print("-" * 60)
    
    # Initialize parser with beam search
    parser = Parser(input_encoding='slp1', output_encoding='slp1',
                   max_splits_per_position=beam_width)
    
    # Warmup
    for _ in parser.split(test_phrases[0], limit=1):
        pass
    
    # Benchmark
    start = time.time()
    for i, phrase in enumerate(test_phrases):
        try:
            for split in parser.split(phrase, limit=1):
                break
        except Exception as e:
            print(f"  Error on phrase {i}: {e}")
            return None
    
    end = time.time()
    total_time = end - start
    avg_time = total_time / len(test_phrases)
    
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average: {avg_time*1000:.1f}ms per parse")
    print(f"  Rate: {1/avg_time:.2f} parses/second")
    
    if avg_time <= 0.1:
        print(f"  ✅ GOAL ACHIEVED! (<100ms)")
    
    return avg_time

print("Sanskrit Parser Performance Benchmark - Phase 2")
print("=" * 60)
print(f"Testing with {len(test_phrases)} phrases")
print("Comparing different beam widths...")

# Test different beam widths
results = {}
for beam_width, label in [(None, "No beam search (Phase 1)"),
                           (200, "Beam width 200"),
                           (100, "Beam width 100"),
                           (50, "Beam width 50")]:
    avg = run_benchmark(beam_width, label)
    if avg:
        results[label] = avg

print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)
for label, avg in results.items():
    status = "✅" if avg <= 0.1 else "⚠️"
    print(f"{status} {label}: {avg*1000:.1f}ms")

if results:
    baseline = results.get("No beam search (Phase 1)")
    if baseline:
        best = min(results.values())
        improvement = baseline / best
        print(f"\nBest improvement: {improvement:.1f}x faster")
        print(f"Goal (100ms): {'ACHIEVED' if best <= 0.1 else f'Need {best/0.1:.1f}x more'}")
