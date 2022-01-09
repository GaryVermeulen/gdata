# Read and write KB file
# KB:
# my_dict = {"duck":["looks","swims","quacks"],"dog":["barks","drules"],"owl":["hoots","flies"]}
#
#duck:['looks', 'swims', 'quacks']
#dog:['barks', 'drules']
#owl:['hoots', 'flies']
#
#

fKB = 'simpKB.txt'
#fMode = 'w'

#print("Writing:")
#print(my_dict)
#print("To file: " + fKB)
#
#with open(fKB, fMode) as f:
#    for key, value in my_dict.items():
#        f.write('%s:%s\n' % (key, value))
#
#f.close()
#print("Write from memory to file closed...")

# now can we get it back?
fMode = 'r'
f = open(fKB, fMode)

new_dict = {}

for line in f:
    line = line.strip('\n')
    key, value = line.split(':')
    new_dict[key] = value
    print(line)

f.close()

print("Read from file to memory closed...")
print(new_dict)

# Write to new out to compare files
fKB = 'simpKB2.txt'
fMode = 'w'

print("Writing:")
print(new_dict)
print("To file: " + fKB)

with open(fKB, fMode) as f:
    for key, value in new_dict.items():
        f.write('%s:%s\n' % (key, value))

f.close()
print("Second write file closed...")


print("Fin!")

