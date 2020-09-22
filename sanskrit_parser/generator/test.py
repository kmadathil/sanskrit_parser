from sanskrit_parser.generator.sutra import *

def test_sandhi(s1, s2):
    print(f"String {s1} {s2}")
    triggered = [s for s in all_sandhi_sutras if s.isTriggered(s1, s2)]
    if triggered:
        print("Triggered rules")
        for t in triggered:
            print(t)
        r = triggered[0].operate(s1, s2)
        print(f"Result: {r}")
        return r
    else:
        return False

test_list = [
    ("rama", "eti"),
    ("gaRa", "upadeSaH"),
    ("rama", "iti"),
    ("tyaktvA", "uttiSTa"),
    ("tava", "oSTaH"),
    ("deva", "fzi"),
    ("kavO", "asmAkam"),
    ("gavi", "asmAkam"),
    ("gavi", "iha"),
    ("AgacCa", "atra"),
    ("yAne", "eti"),
    ]

for s in test_list:
    _s = s
    while (_s):
        r = _s
        _s = test_sandhi(*_s)
    print(f"Final Result: {r[0]+r[1]}\n\n")
  
