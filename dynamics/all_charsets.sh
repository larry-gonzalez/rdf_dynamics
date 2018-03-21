#!/bin/bash
less 2* > allcharsets
awk -F$'\t' '{print $1}' allcharsets > allpreds
sort allpreds -u > sortedpreds
awk '{print gsub(" "," "), $0}' sortedpreds | sort -n | cut -d' ' -f2- > all_charsets.txt
bzip2 all_charsets.txt
rm allcharsets
rm allpreds
rm sortedpreds
