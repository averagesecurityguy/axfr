#!/usr/bin/env python3

import sys
import dns.resolver
import dns.reversename
import dns.zone
import dns.exception

LIFETIME = 5.0
domain = sys.argv[1]
nservers = []


# Attempt to get a list of nameservers for the domain. Quit if there are any
# problems.
try:
    nservers = [n.to_text() for n in dns.resolver.query(domain, 'NS')]

except:
    sys.exit(1)
    

# Check each nameserver for zone transfer. If there are any issues move to
# the next server.
resp = ['DOMAIN: {0}'.format(domain), '=' * (len(domain) + 8)]

for ns in nservers:
    try:
        z = dns.zone.from_xfr(dns.query.xfr(ns, domain, lifetime=LIFETIME))
        recs = [z[n].to_text(n) for n in z.nodes.keys()]

        resp.append('NS: {0}'.format(ns))
        resp.append('-' * (len(ns) + 4))
        resp.extend(recs)
        resp.append('')

    except:
        continue


# If we have any records then write them to a file.
if len(resp) > 2:
    filename = '{0}.axfr'.format(domain)
    with open(filename, 'w') as f:
        f.write('\n'.join(resp))
