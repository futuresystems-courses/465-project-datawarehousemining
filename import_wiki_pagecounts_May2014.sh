#!/bin/bash
# This script imports all wikimedia files for May 2014
#
#

year="2014"
month="05"
  echo "importing hash file for ${year} - ${month} used for checking files arrive intact"
  wget -O $year$month-hash.txt "https://dumps.wikimedia.org/other/pagecounts-raw/${year}/${year}-${month}/md5sums.txt"
  for day in {01..31}
  do
    for hour in {00..23}
    do
      for i in {00..20}
        do
          if wget -O $year$month$day-$hour.gz "https://dumps.wikimedia.org/other/pagecounts-raw/${year}/${year}-${month}/pagecounts-${year}${month}${day}-${hour}00${i}.gz" ; then
            echo "unziping ${year}${month}${day}-${hour}.gz"
            gunzip $year$month$day-$hour.gz
            echo "adding year month day data to each line in ${year}${month}${day}-${hour}.gz"
            sed "s/^/${year} ${month} ${day} ${hour} /" <$year$month$day-$hour >$year$month$day-$hour-prefixed
            echo "replacing all spaces with commas"
            tr ' ' ',' <$year$month$day-$hour-prefixed >$year$month$day-$hour.csv
            echo "convert to UTF-8"
            iconv -f ISO-8859-1 -t UTF-8 $year$month$day-$hour.csv >$year$month$day-$hour-UT8.csv
            echo "importing data into mongodb"
            mongoimport --db wikimedia_project --collection pagecounts_May14 --type csv --fieldFile pagecount_headers.txt --file $year$month$day-$hour-UT8.csv
            echo "cleaning up files"
            rm $year$month$day-$hour*
            break
          else
            echo "failed....incrementing by 1 and trying to discover the right link again"
          fi
        done
      echo ""
    done
  done
  echo "cleaning up hash file"
  rm $year$month-hash.txt






