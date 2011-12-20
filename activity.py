import re, datetime
from subprocess import Popen,PIPE


command = 'svn log --xml '
repos = [
    'http://svn.apache.org/repos/asf/ant/core/trunk/',
]
output = 'activity.url'
days = 90
width = 550
height = 50
url = "http://chart.apis.google.com/chart?chbh=a&cht=bvs&chs="+str(width)+"x"+str(height)+"&chd=t:"
pattern = re.compile('<date>([\d]{4}-[\d]{2}-[\d]{2})')



dict = {}

for repo in repos:
	pipe = Popen(command + repo, shell=True,stdout=PIPE)
	for line in pipe.stdout.readlines():
		match = pattern.search(line)
		if match:
			if not dict.has_key( match.group(1) ):
				dict[ match.group(1) ] = 1
			else:
				dict[ match.group(1) ] = dict[ match.group(1) ] + 1


max = 0

for i in range(0, days):
	date = datetime.datetime.now() + datetime.timedelta(-days+i)
	iso = date.date().isoformat()

	if dict.has_key( iso ):
		count = dict[ iso ]
	else:
		count = 0

	if i > 0:
		url = url + ","

	url = url + str(count)

	if count > max:
		max = count


url = url + "&chds=0," + str(max)

f = open(output, 'w')
f.write( "[InternetShortcut]\nURL=" )
f.write(url + "\n")
f.close()
