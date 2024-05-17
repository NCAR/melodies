import sys
sys.path.append('/glade/u/home/fillmore/monetio')
sys.path.append('/glade/u/home/fillmore/monet')
sys.path.append('/glade/u/home/fillmore/MELODIES-MONET_develop_forecast')

from datetime import datetime, timedelta
from melodies_monet import driver

import warnings
warnings.filterwarnings('ignore')

an = driver.analysis()
an.control = '/glade/u/home/fillmore/RunAutomation/wrfchem.yaml'
an.read_control()

date_str = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
print(date_str)
yyyy_str = date_str[0:4]
mm_str = date_str[4:6]
dd_str = date_str[6:8]

an.control_dict['analysis']['output_dir'] \
    = an.control_dict['analysis']['output_dir'].replace(
        'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)
an.output_dir = an.control_dict['analysis']['output_dir']

for model in an.control_dict['model']:
    an.control_dict['model'][model]['files'] \
        = an.control_dict['model'][model]['files'].replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)

for obs in an.control_dict['obs']:
    an.control_dict['obs'][obs]['filename'] \
        = an.control_dict['obs'][obs]['filename'].replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)

print(an.control_dict)

an.open_models()
an.models

an.open_obs()
an.obs

# for obs in an.obs:
#     print(an.obs[obs])
#     print(an.obs[obs].obj.info())

an.pair_data()
for key in an.paired:
    print(an.paired[key])

an.plotting()
