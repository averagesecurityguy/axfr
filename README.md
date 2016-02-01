AXFR
====
This is a set of tools to do DNS zone transfers on a list of domain names. I used the top one million domains list from Alexa, which you can get here: http://s3.amazonaws.com/alexa-static/top-1m.csv.zip. The list I used was downloaded on 1/30/2016.

Prerequisites
-------------
The primary script is written in Python3 and requires the dnspython3 module. To run the script in parallel, install the GNU Parallel tool. The following commands will work for Debian based distros.

    sudo apt-get install python3 parallel
    sudo pip3 install dnspython3

Running the Script
------------------
Use the following commnd to run 100 copies of the script in parallel.

    cat million_domains.txt | parallel -j 100 ./axfr.py

The script uses a LIFETIME value of 5 seconds to control the how long it is willing to wait to get a full response from the DNS server. Using a larger value may yield more zone transfers but can dramatically increase the time needed to test all one million domains.

Analysing the Results
---------------------
The script will write one file for each domain where a zone transfer was possible. Each file will have the axfr extension, which makes it easy to clean up data between runs and helps with analysis. Each file will list separately the results from each name server that allowed a zone transfer.

To get a list of all successful domains:

    grep "DOMAIN: " *.axfr | cut -d' ' -f2

To count the number of successful domains:

    grep "DOMAIN: " *.axfr | wc -l

To get a list of all the successful nameservers:

    grep "NS: " *.axfr | cut -d' ' -f2

To count the number of successful nameservers:

    grep "NS: " *.axfr | wc -l      

To keep a rough track of the progress:

    grep -n $(ps -ef | grep "[p]ython3 ./axfr" | tail -1 | awk '{ print $10 }') million_domains.txt

You can also use the `stats.py` script to produce the desired stats. The script will produce three files: domains.md (a sorted list of domains), nameservers.md (a sorted, unique list of nameservers), and subdomains.md (a list of sub domains sorted by count, highest to lowest.)
