f = open('seed_data/u.item')
max = 0
for line in f:
    a = line.split('|')[4]
    print len(a)
    if max < len(a):
        max = len(a)

print max

f.close()
