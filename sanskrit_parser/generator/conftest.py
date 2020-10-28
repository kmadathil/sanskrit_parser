import pytest
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya

def _test(output, s, enc):
    _s = s[-1]
    if not isinstance(_s, list):
        # Single element
        _s = [_s]
    # Remove spaces in reference
    _s = [x.replace(' ',"") for x in _s]
    j = [
        PaninianObject("".join([
            _o.transcoded(SLP1) for _o in list(o)
        ]), encoding=SLP1).transcoded(enc)
        for o in output
    ]
    if not  (set(j) == set(_s)):
        print(set(j), set(_s))
    return (set(j) == set(_s))
def run_test(s, sutra_list, encoding=SLP1):
    pl = []
    # Assemble list of inputs
    for i in range(len(s)-1):
        def _gen_obj(s, i):
            if isinstance(s[i], str):
                # Shortcuts for two input tests not using predefined objects
                # If a string in the first place ends with * it's an anga
                # Else it's a pada
                # For everything else, use predefined objects
                if (i==0) and (s[i][-1] == "*"):
                    s0 =  s[0][:-1]
                    l = PaninianObject(s0, encoding)
                    l.setTag("aNga")
                else:
                    s0 =  s[i]
                    l = PaninianObject(s[i], encoding)
                    if i==0:
                        l.setTag("pada")
                    return l
            elif isinstance(s[i], tuple) or isinstance(s[i], list):
                l = [_gen_obj(s[i], ii) for (ii, ss) in enumerate(s[i])]
            else:
                l = s[i]
            return l
        l = _gen_obj(s, i)
        pl.append(l)
    p = Prakriya(sutra_list,PrakriyaVakya(pl))
    p.execute()
    p.describe()
    #print(p.dict())
    o = p.output()
    assert _test(o, s, encoding)

