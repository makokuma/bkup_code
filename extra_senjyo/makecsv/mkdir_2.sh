#!/bin/csh
#mkdir csvdir

foreach MM (04 05 06 07 08 09 10)
echo $MM
set YYYY = 2021
while ($YYYY <= 2025)
	
	mkdir -p $MM/total/${YYYY}

	@ YYYY = $YYYY + 1

end
end 

