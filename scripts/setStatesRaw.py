import json
import re

with open('../data/raw/nuforc_reports.json', 'r') as raw, \
        open('../data/external/county_isocodes.json') as country_codes, \
        open('../data/raw/nuforc_reports_edited.json', 'w') as write_file, \
        open('../data/external/us_state_hash.json') as us_codes, \
        open('../data/external/canada_state_hash.json') as ca_codes:

    country_isocodes = json.load(country_codes)
    us_isocodes = json.load(us_codes)
    ca_isocodes = json.load(ca_codes)

    for raw_sighting in raw:
        sighting_json = json.loads(raw_sighting)
        if sighting_json['state'] is None and sighting_json['city'] is not None:
            m = re.search(r'(?<=\().*?(?=\))', sighting_json['city'])
            if m:
                for code, name in country_isocodes.items():
                    if name.lower() == m.group().lower():
                        sighting_json['state'] = code
        else:
            if sighting_json['state'] in us_isocodes:
                sighting_json['state'] = 'US'
            elif sighting_json['state'] in ca_isocodes:
                sighting_json['state'] = 'CAN'

        json.dump(sighting_json, write_file)
        write_file.write('\n')
