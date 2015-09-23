import datetime
start=datetime.datetime.now()
for i in range(10000): print('x'),
end=datetime.datetime.now()
print(end-start)