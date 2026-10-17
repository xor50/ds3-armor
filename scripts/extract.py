#! /usr/bin/python

import json


images_to_download = []


def extract_number(line):
	end = line.find('</td>')
	start = line.rfind('>', 0, end) + 1
	try:
		return float(line[start:end])
	except:
		return line[start:end]


def process_file(filename):
	entries = []

	with open(filename, 'r') as f:
		lines = f.readlines()

	current = 0
	while current < len(lines):
		entry = {}

		line = lines[current + 1]

		start = line.find('</a><a')
		if start > -1:
			end = line.find('>', start + 6)
			line = line[:start] + line[end+1:]

		end = line.find('</a>')
		start = line.rfind('>', 0, end)

		entry['name'] = line[start+1:end]


		start = line.find('src="')
		if start > -1:
			start += 5
			end = line.find('"', start + 1)

			images_to_download.append(line[start:end])

			start = line.rfind('/', start + 1, end) + 1

			entry['image'] = line[start:end]
		else:
			entry['image'] = None

		entry['physicaldef'] = extract_number(lines[current + 2])
		entry['strikedef'] = extract_number(lines[current + 3])
		entry['slashdef'] = extract_number(lines[current + 4])
		entry['thrustdef'] = extract_number(lines[current + 5])
		entry['magicdef'] = extract_number(lines[current + 6])
		entry['firedef'] = extract_number(lines[current + 7])
		entry['lightningdef'] = extract_number(lines[current + 8])
		entry['darkdef'] = extract_number(lines[current + 9])
		entry['bleedres'] = extract_number(lines[current + 10])
		entry['poisonres'] = extract_number(lines[current + 11])
		entry['frostres'] = extract_number(lines[current + 12])
		entry['curseres'] = extract_number(lines[current + 13])
		entry['poise'] = extract_number(lines[current + 14])
		entry['weight'] = extract_number(lines[current + 15])


		entries.append(entry)

		current += 18

	return entries


armors = {
	'helms': process_file('ref/helms.txt'),
	'chests': process_file('ref/chests.txt'),
	'gauntlets': process_file('ref/gauntlets.txt'),
	'leggings': process_file('ref/leggings.txt'),
}


with open('data/armors.json', 'w') as f:
	json.dump(armors, f, indent=4)


with open('data/imagelist.sh', 'w') as f:
	f.write('#! /bin/bash\n\n')
	l = map(lambda x: x.replace("'", "\\'"), filter(lambda x: not(x.startswith('http')), images_to_download))
	f.write('wget http://darksouls3.wiki.fextralife.com' + '\nwget http://darksouls3.wiki.fextralife.com'.join(l))
	l = map(lambda x: x.replace("'", "\\'"), filter(lambda x: x.startswith('http'), images_to_download))
	f.write('wget ' + '\nwget '.join(l))
