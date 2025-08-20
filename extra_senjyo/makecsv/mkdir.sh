#!/bin/csh
#mkdir csvdir

set YYYY = 2022
while ($YYYY <= 2023)
	foreach MM (04 05 06 07 08 09 10)
	echo $YYYY $MM
	if (  "$MM" == "04" || "$MM" == "06" || "$MM" == "09") then
	
	mkdir -p $MM/${YYYY}${MM}01-${MM}30

	else if ( "$MM" == "05" || "$MM" == "07" || "$MM" == "08" || "$MM" == "10") then
#	if ("$MM" == "08") then	
	mkdir -p $MM/${YYYY}${MM}01-${MM}31

	else
	echo skip making directory
	
	endif

end
@ YYYY = $YYYY + 1
end 

