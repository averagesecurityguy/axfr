#!/usr/bin/env python3

import os

domains = []
nservers = []
subdomains = {}


def process_file(fn):
    subs = []
    with open(fn) as f:
        for line in f:
            if 'DOMAIN: ' in line:
                domains.append(line.split(' ')[1])
            if 'NS: ' in line:
               nservers.append(line.split(' ')[1])

            if ' IN ' in line:
                subs.append(line.split(' ')[0])

    # Make sure I only count a subdomain once when multiple DNS servers allow
    # zone transfers.
    for s in set(subs):
        if s in subdomains:
            subdomains[s] += 1
        else:
            subdomains[s] = 1


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
sstats.append('Count: {0}'.format(len(subdomains)))
sstats.append('')
sorted_subs = sorted(subdomains.items(), key=lambda x: x[1], reverse=True)
sstats.extend(['{0}: {1}'.format(s[0], s[1]) for s in sorted_subs])

with open('domains.txt', 'w') as f:          
    f.write('\n'.join(dstats))

with open('nameservers.txt', 'w') as f:          
    f.write('\n'.join(nstats))

with open('subdomains.txt', 'w') as f:          
    f.write('\n'.join(sstats))
