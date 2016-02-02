Useful Commands for Analysis
============================

Find A Records
--------------
Find all of the A records that have the search term in them and return them in the format of `fqdn ip`.

    grep "search term" *.axfr | grep "IN A" | awk '{ print $1 " " $5 }' | sed "s/.axfr:/ /" | awk '{ print $2 "." $1 " " $3 }' 
