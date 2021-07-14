import datetime

date1 = datetime.datetime.strptime("2021-07-14_10-59-22", "%Y-%m-%d_%H-%M-%S")
date2 = datetime.datetime.strptime("2021-07-14_10-59-31", "%Y-%m-%d_%H-%M-%S")
print(date2 - date1)

date1 = datetime.datetime.strptime("2021-07-14_10-59-31", "%Y-%m-%d_%H-%M-%S")
date2 = datetime.datetime.strptime("2021-07-14_10-59-42", "%Y-%m-%d_%H-%M-%S")
print(date2 - date1)

date1 = datetime.datetime.strptime("2021-07-14_10-59-42", "%Y-%m-%d_%H-%M-%S")
date2 = datetime.datetime.strptime("2021-07-14_10-59-57", "%Y-%m-%d_%H-%M-%S")
print(date2 - date1)