Useful Commands for Analysis
============================

Find A Records
--------------
Find all of the A records that have the search term in them and return them in the format of `fqdn ip`.

    grep "search term" *.axfr | grep "IN A" | awk '{ print $1 " " $5 }' | sed "s/.axfr:/ /" | awk '{ print $2 "." $1 " " $3 }' 

Find AAAA Records
-----------------
Find all AAAA records that are not localhost and return them in the format `fqdn ipv6`.

    grep "IN AAAA" *.axfr | awk '{ print $1 " " $5 }' | egrep -v " ::$| ::1$| ::2$" | sed "s/.axfr:/ /" | awk '{ print $2 "." $1 " " $3 }'

Find All Records
----------------
Find all of the records that have the search term in them and return them in the format of `fqdn type value`.

    grep "search term" *.axfr | awk '{ print $1 " " $4 " " $5 }' | sed "s/.axfr:/ /" | awk '{ print $2 "." $1 " " $3 " " $4 }'

Find SPF Records
----------------
Find all SPF records.

    grep v=spf *.axfr | awk '{out=$1; for(i=5;i<=NF;i++){out=out" "$i}; print out}' | sort -u

Find all SPF records with +all in them.

    grep v=spf *.axfr | grep +all | awk '{out=$1; for(i=5;i<=NF;i++){out=out" "$i}; print out}' | sort -u
