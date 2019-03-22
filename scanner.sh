# scanner.sh
# Created using makeBash
#!/usr/bin/expect -f

# Script requires first and second argument to indicate range to scan (in MHz)
# i.e ./scanner.sh 90 95
# (to scan from 90-95 MHz)
BEG_FREQ=$1
END_FREQ=$2

echo "Scanning $BEG_FREQ to $END_FREQ MHZ"
echo
sudo python -m rtlsdr_scanner -s $BEG_FREQ -e $END_FREQ rtlsdr_scan.csv > rtlsdr_scanner.log  # scan given range
python highdb_bandwidth.py $BEG_FREQ $END_FREQ # analyze scan

