#!/usr/bin/env python3

import os

domains = []
nservers = []
subs = {}


def process_line(line):
    if 'DOMAIN: ' in line:
        domains.append(line.split(' ')[1])
    if 'NS: ' in line:
        nservers.append(line.split(' ')[1])

    if ' IN ' in line:
        sub = line.split(' ')[0]

        if sub in subs:
            subs[sub] += 1
        else:
            subs[sub] = 1


def process_file(fn):
    with open(fn) as f:
        for line in f:
            process_line(line.rstrip('\r\n'))


for fn in os.listdir('.'):
    if fn.endswith('.axfr'):
       process_file(fn)


dstats = ['Domains']
dstats.append('-------')
dstats.append('Count: {0}'.format(len(domains)))
dstats.append('')
dstats.extend(sorted(domains))

nstats = ['Unique Name Servers']
nstats.append('-------------------')
nservers = set(nservers)
nstats.append('Count: {0}'.format(len(nservers)))
nstats.append('')
nstats.extend(sorted(nservers))

sstats = ['Sub Domains By Count']
sstats.append('--------------------')
sstats.append('Count: {0}'.format(len(subs)))
sstats.append('')
sorted_subs = sorted(subs.items(), key=lambda x: x[1], reverse=True)
sstats.extend(['{0}: {1}'.format(s[0], s[1]) for s in sorted_subs])

with open('domains.md', 'w') as f:          
    f.write('\n'.join(dstats))

with open('nameservers.md', 'w') as f:          
    f.write('\n'.join(nstats))

with open('subdomains.md', 'w') as f:          
    f.write('\n'.join(sstats))
