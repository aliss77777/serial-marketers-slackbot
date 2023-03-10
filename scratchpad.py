
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

outfile = open('requirements.txt', 'w')

with open('requirements.txt', 'r') as f:
    for line in f:
        if '@' in line:
            continue
        else:
            outfile.write(line)

outfile.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
