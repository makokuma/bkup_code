#!/bin/csh
#for ratio 2.0

set YYYY = 2021
while ($YYYY <= 2025)
	foreach MM (04 05 06 07 08 09 10)
	echo $YYYY $MM
	# copy csv from 05
	if (  "$MM" == "04" || "$MM" == "06" || "$MM" == "09") then
		cp /mnt/jet12/makoto/extract_senjo/ext_sun/bin/05renameid3recollect_dupratio/dat/ra03/5000/100-80/${YYYY}${MM}01-${MM}30/ra03_5000m_recollect_100-80_040.csv /mnt/jet12/makoto/extract_senjo/ext_sun/csv/100-80/${MM}/${YYYY}${MM}01-${MM}30/05d3ra03_5000m_recollect_100-80_040.csv

	else if ( "$MM" == "05" || "$MM" == "07" || "$MM" == "08" || "$MM" == "10") then
		 cp /mnt/jet12/makoto/extract_senjo/ext_sun/bin/05renameid3recollect_dupratio/dat/ra03/5000/100-80/${YYYY}${MM}01-${MM}31/ra03_5000m_recollect_100-80_040.csv /mnt/jet12/makoto/extract_senjo/ext_sun/csv/100-80/${MM}/${YYYY}${MM}01-${MM}31/05d3ra03_5000m_recollect_100-80_040.csv

	endif

	# copy csv from 08
	if (  "$MM" == "04" || "$MM" == "06" || "$MM" == "09") then
                cp /mnt/jet12/makoto/extract_senjo/ext_sun/bin/08scatter_classify/dat/100-80/040/${YYYY}${MM}01-${MM}30/linear-stationary_cases_ra03_5000m_100-80_040.csv /mnt/jet12/makoto/extract_senjo/ext_sun/csv/100-80/${MM}/${YYYY}${MM}01-${MM}30/08linear-stationary_cases_ra03_5000m_100-80_040.csv

	else if ( "$MM" == "05" || "$MM" == "07" || "$MM" == "08" || "$MM" == "10") then
                 cp /mnt/jet12/makoto/extract_senjo/ext_sun/bin/08scatter_classify/dat/100-80/040/${YYYY}${MM}01-${MM}31/linear-stationary_cases_ra03_5000m_100-80_040.csv /mnt/jet12/makoto/extract_senjo/ext_sun/csv/100-80/${MM}/${YYYY}${MM}01-${MM}31/08linear-stationary_cases_ra03_5000m_100-80_040.csv

	endif

end
@ YYYY = $YYYY + 1
end 

