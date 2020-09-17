from sanskrit_parser.generator.sutra import *

sutras = [vriddhirechi, aadgunah]

def test_sandhi(s1, s2):
    print(f"String {s1} {s2}")
    triggered = [s for s in sutras if s.isTriggered(s1, s2)]
    print("Triggered rules")
    for t in triggered:
        print(t)
    r = triggered[0].operate(s1, s2)
    print(f"Result: {r}")
    return r

test_list = [
    ("rama", "eti"),
    ("gaRa", "upadeSaH"),
    ("rama", "iti"),
    ("tyaktvA", "uttiSTa"),
    ("tava", "oSTaH"),
    ]
for s in test_list:
    test_sandhi(*s)
