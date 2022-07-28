import csv
mylist = []
newlist = []
with open('trials/binary.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	mylist = [line.rstrip('\n') for line in csv_file]
for i in mylist:
	i = int(i, 2)
	newlist.append(i)
for i in newlist:
	print(i)