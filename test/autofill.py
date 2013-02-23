from subprocess import check_output
import sys
import re

def _gen():
    while True:
        f = check_output(['/usr/games/fortune'])
        for w in f.split():
            yield w
gen = _gen()
count = 0

def fortune(_):
    global count
    count += 1
    return 'msgstr "%s"\n\n' % (gen.next().replace('"', "'"),)

po = file(sys.argv[1]).read()
translated = re.sub('msgstr ""\n\n', fortune, po)
with file(sys.argv[1], 'w') as out:
    out.write(translated)
print count, "translations"
