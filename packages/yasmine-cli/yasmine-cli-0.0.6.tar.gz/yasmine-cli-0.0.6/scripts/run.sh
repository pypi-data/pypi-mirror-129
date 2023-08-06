#!/bin/sh

yasmine-cli --infiles=../tests/test_data/station.xml --action=add --from_yml=yml:yml/station.yml --level_network=* \
  -o 5.xml
yasmine-cli --infiles=5.xml --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE --schema_version=1.1 \
  -o 6.xml
exit 1
yasmine-cli --infiles=3.xml --field=data_availability --value=yml:yml/dataavailability.yml --level_station=*.CCM \
  --schema_version=1.1 --o 4.xml
#yasmine-cli --infiles=../tests/test_data/NE.xml --field=operators --value=yml:yml/operators.yml --level_network=* -o x.xml
yasmine-cli --level_station=*.WES --infile=../tests/test_data/NE.xml --plot_resp --plot_dir=zplot
exit 1
yasmine-cli --infiles=../tests/test_data/NE.xml --field=operators --value=yml:yml/operators.yml --level_network=* --schema_version=1.1 -o x.xml

#yasmine-cli --infiles=3.xml --field=operators --value=yml:yml/operator.yml --level_station=*.CCM -o 4a.xml
#yasmine-cli --infiles=4a.xml --field=operators --value=yml:yml/operator.yml --level_station=*.CCM -o 4b.xml
yasmine-cli --infiles=4c.xml --field=operators[0] --value=None --level_station=*.CCM -o 4c.xml
exit 1

yasmine-cli --infiles=3.xml --field=data_availability --value=yml:yml/dataavailability.yml --level_station=*.CCM \
  --dont_validate -o 4.xml
exit 1

yasmine-cli --infiles=3.xml --field=operators --value=yml:yml/operator.yml --level_station=*.MIKE -o 4.xml
yasmine-cli --infiles=4.xml --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE -o 5.xml
exit 1
yasmine-cli --infiles=3.xml --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE -o 4.xml
yasmine-cli --infiles=4.xml --field=operators[0] --value=yml:yml/operator.yml --level_station=*.MIKE -o 5.xml
exit 1
yasmine-cli --infiles=3.xml --field=operators --value=yml:yml/operator.yml --level_station=*.MIKE -o 4.xml
yasmine-cli --infiles=2.xml --field=comments[0] --value=yml:yml/comment.yml --level_station=*.MIKE -o 3.xml
yasmine-cli --infiles=2.xml --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE -o 3.xml
yasmine-cli --infiles=3.xml --field=operators[1] --value=yml:yml/operator.yml --level_station=*.MIKE -o 4.xml
cat McCorn_v2.xml | yasmine-cli --field=sensor --value=yml:yml/sensor.yml --level_channel=*.*.*.* -o foo.xml

cat Test.xml | yasmine-cli --field=code --value=MIKE --level_station=*.ANMO \
  --schema_version 1.1 -o 1.xml

yasmine-cli --infiles=1.xml --field=latitude --value=33.77 --level_station=*.CCM \
  --schema_version 1.0 -o 2.xml

yasmine-cli --infiles=2.xml --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE -o 3.xml
yasmine-cli --infiles=3.xml --field=operators[1] --value=yml:yml/operator.yml --level_station=*.MIKE -o 4.xml

exit 1
