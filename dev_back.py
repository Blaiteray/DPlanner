import shelve

x = shelve.open('db')
y = input('>')
if y=='0':
	x.clear()
else:
	print(dict(x))
x.close()