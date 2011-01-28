# -*- coding: utf-8 -*-

import os
import sys
import re
import shutil
import json
import webbrowser
import twitter
from recipe__oauth_login import oauth_login
from recipe__analyze_users_in_search_results import analyze_users_in_search_results

# A simple heuristic function that tries to detect the presence of a state
# in a short blurb of text by searching for the full state name and the
# state abbreviation in a suitable context. It returns a map of state
# abbreviations and frequencies. Much more sophisticated alternatives could
# be applied; this is simply a starting point to get you on your way

def get_state_frequencies(locations):
    
    state_names_to_abbrevs = \
        dict([
            ('ALABAMA', 'AL'),
            ('ALASKA', 'AK'),
            ('ARIZONA', 'AZ'),
            ('ARKANSAS', 'AR'),
            ('CALIFORNIA', 'CA'),
            ('COLORADO', 'CO'),
            ('CONNECTICUT', 'CT'),
            ('DELAWARE', 'DE'),
            ('FLORIDA', 'FL'),
            ('GEORGIA', 'GA'),
            ('HAWAII', 'HI'),
            ('IDAHO', 'ID'),
            ('ILLINOIS', 'IL'),
            ('INDIANA', 'IN'),
            ('IOWA', 'IA'),
            ('KANSAS', 'KS'),
            ('KENTUCKY', 'KY'),
            ('LOUISIANA', 'LA'),
            ('MAINE', 'ME'),
            ('MARYLAND', 'MD'),
            ('MASSACHUSETTS', 'MA'),
            ('MICHIGAN', 'MI'),
            ('MINNESOTA', 'MN'),
            ('MISSISSIPPI', 'MS'),
            ('MISSOURI', 'MO'),
            ('MONTANA', 'MT'),
            ('NEBRASKA', 'NE'),
            ('NEVADA', 'NV'),
            ('NEW HAMPSHIRE', 'NH'),
            ('NEW JERSEY', 'NJ'),
            ('NEW MEXICO', 'NM'),
            ('NEW YORK', 'NY'),
            ('NORTH CAROLINA', 'NC'),
            ('NORTH DAKOTA', 'ND'),
            ('OHIO', 'OH'),
            ('OKLAHOMA', 'OK'),
            ('OREGON', 'OR'),
            ('PENNSYLVANIA', 'PA'),
            ('RHODE ISLAND', 'RI'),
            ('SOUTH CAROLINA', 'SC'),
            ('SOUTH DAKOTA', 'SD'),
            ('TENNESSEE', 'TN'),
            ('TEXAS', 'TX'),
            ('UTAH', 'UT'),
            ('VERMONT', 'VT'),
            ('VIRGINIA', 'VA'),
            ('WASHINGTON', 'WA'),
            ('WEST VIRGINIA', 'WV'),
            ('WISCONSIN', 'WI'),
            ('WYOMING', 'WY')
        ])

    state_abbrevs = state_names_to_abbrevs.values()

    states_freqs = dict([(abbrev, 0) for abbrev in state_abbrevs])

    for location in locations:
        if location is None:
            continue

        for name, abbrev in state_names_to_abbrevs.items():
            if location.upper().find(name) > -1:
                states_freqs[abbrev] += 1
                break

            if re.findall(r'\b(' + abbrev + r')\b', location, re.IGNORECASE):
                states_freqs[abbrev] += 1
                break

    return states_freqs

Q = ' '.join(sys.argv[1:])

# Don't forget to pass in keyword parameters if you don't have
# a token file stored to disk

t = oauth_login()

_, screen_name_to_location, _ = analyze_users_in_search_results(t, Q)
locations = screen_name_to_location.values()

# Resolve state abbreviations to the number of times these states appear
states_freqs = get_state_frequencies(locations)

# Munge the data to the format expected by Protovis for Dorling Cartogram

json_data = {}
for state, freq in states_freqs.items():
    json_data[state] = {'value': freq}

# Copy over some scripts for Protovis...
# Our html template references some Protovis scripts, which we can
# simply copy into out/

if not os.path.isdir('out'):
    os.mkdir('out')

shutil.rmtree('out/dorling_cartogram', ignore_errors=True)
shutil.rmtree('out/protovis-3.2', ignore_errors=True)

shutil.copytree('etc/protovis/dorling_cartogram',
                'out/dorling_cartogram')

shutil.copytree('etc/protovis/protovis-3.2',
                'out/protovis-3.2')

html = open('etc/protovis/dorling_cartogram/dorling_cartogram.html').read() % \
        (json.dumps(json_data),)

f = open(os.path.join(os.getcwd(), 'out', 'dorling_cartogram', 
                      'dorling_cartogram.html'), 'w')
f.write(html)
f.close()

print >> sys.stderr, 'Data file written to: %s' % f.name
webbrowser.open('file://' + f.name)
