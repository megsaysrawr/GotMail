import pandas
import numpy as np
import matplotlib.pyplot as plt

df = pandas.DataFrame({'Number' : ['1', '2', '3'], \
						'Status' : [True, False, True]})
print df


# df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
#                            'foo', 'bar', 'foo', 'bar'],
#                 'B' : ['one', 'one', 'two', 'two',
#                           'two', 'two', 'one', 'two'],
#                 'C' : [56, 2, 3, 4, 5, 6, 0, 2],
#                 'D' : [51, 2, 3, 4, 5, 6, 0, 2]})

# grouped = df.groupby(['A', 'B']).sum()

# grouped['sum'] = (grouped['C'] / grouped['D']) 
# # print (grouped[['sum']])


# a = pd.DataFrame(grouped)


# a.to_csv("C:\\Users\\test\\Desktop\\test.csv", index=False, cols=('A','B','sum'))








# pandas.DataFrame.to_csv("mailbox_list.csv")