from sanskrit_parser.generator.pratipadika import Pratipadika

# svarAdi gaṇa (1.1.37) — avyaya (indeclinable) words
# These do not take vibhakti suffixes (SK452: 2.4.82)
antar  = Pratipadika("antar",  "pum", other_tags=["svarAdi"])   # अन्तर् "within"
prAtar = Pratipadika("prAtar", "pum", other_tags=["svarAdi"])   # प्रातर् "in the morning"
punar  = Pratipadika("punar",  "pum", other_tags=["svarAdi"])   # पुनर् "again"
bahiS  = Pratipadika("bahiS",  "pum", other_tags=["svarAdi"])   # बहिस् "outside"
naktam = Pratipadika("naktam", "pum", other_tags=["svarAdi"])   # नक्तम् "at night"
svayam = Pratipadika("svayam", "pum", other_tags=["svarAdi"])   # स्वयम् "self"




# nIpAtAs
AN_upasarga = Pratyaya("A", its=["N"], other_tags=["nipAta", "upasarga", "pada"])
mAN_upasarga = Pratyaya("mA", its=["N"], other_tags=["nipAta", "upasarga", "pada"])
upa_upasarga = Pratyaya("upa", other_tags=["nipAta", "upasarga", "pada"])
pra_upasarga = Pratyaya("pra", other_tags=["nipAta", "upasarga", "pada"])
ava_upasarga = Pratyaya("ava", other_tags=["nipAta", "upasarga", "pada"])
ud_upasarga = Pratyaya("ud", other_tags=["nipAta", "upasarga", "pada"])
ati_upasarga = Pratyaya("ati", other_tags=["nipAta", "upasarga", "pada"])

