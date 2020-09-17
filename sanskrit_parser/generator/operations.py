
# Adesha. Match a in f, return corresponding t
def adesha(a, f, t):
    p = str(f).find(str(a))
    if p != -1:
        return str(t)[p]
    else:
        return a
