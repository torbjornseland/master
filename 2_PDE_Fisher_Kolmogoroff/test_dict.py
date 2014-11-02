par_val = dict(Oslo=13,Berlin=22)

map = {}
for city in par_val:
    exec("%s = %d" % (city, par_val[city]))

print Oslo
