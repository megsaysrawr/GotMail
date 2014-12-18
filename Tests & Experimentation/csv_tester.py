import csv

with open('sample_csv.csv', 'r+b') as csvfile:
	filewrite = csv.writer(csvfile, delimiter=',', \
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
	number = [1,2,3,4,5,6]
	status = [True,False,True,True,False,True]
	filewrite.writerow(number)
	filewrite.writerow(status)
