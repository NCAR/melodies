import sys
sys.path.append('/glade/u/home/fillmore/MELODIES-MONET/')
sys.path.append('/glade/u/home/fillmore/MELODIES-MONET/melodies_monet/')

from melodies_monet import driver
an = driver.analysis()
an.control = 'mm_basics.yaml'
an.read_control()
an.control_dict

an.open_models()
an.models
an.models['RACM_ESRL'].obj

print(an.models['RACM_ESRL'].label)
print(an.models['RACM_ESRL'].mapping)
print(an.start_time)
print(an.end_time)

an.open_obs()
an.obs['AirNow'].obj

an.pair_data()

an.plotting()
