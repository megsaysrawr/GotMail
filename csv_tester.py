import csv

with open('sample_csv.csv', 'wb') as csvfile:
	filewrite = csv.writer(csvfile, delimiter=',', \
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
	number = [1,2,3,4,5]
	status = [True,False,True,True,False]
	filewrite.writerow(number)
	filewrite.writerow(status)
