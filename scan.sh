#/bin/sh -e
while true
do
	sudo iwlist wlp2s0b1 scanning |\
		grep '\(Frequency\|ESSID\|Quality\)' | sed 'N;s/\n/ /;N;s/\n/ /' |\
		awk '{printf "%s %3s %s %s %s\n", $3, $4, $5, $7, $9}'
	echo DONE
done
