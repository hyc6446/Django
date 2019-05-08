#string
a='qqwqewewe'

print(a.upper())

print(a.title())

print(a.count('q'))


#list
a = [1,2,5,8,6,9,8,6,3,4,5,6,5,4,8]

aa = [ int(i)*int(i) for i in a ]

print(aa)

a.append('test')

print(a)

lena = len(a)

print(lena)


#tuple
b = (1,2,3,4,5,6,7,8,5,2,5,3,4,2,5,12,45,22,66)

for i in b:
    print(i,end='')
print()

b1 = ('test','demo','viem')
b2 = (1,2,3)
bb = ( i+str(j) for i in b1 for j in b2)

for i in bb:
    print(i)
print('==========')

print(max(b2))

#list
c = {1,2,5,8,6,6,6,6,5,4,4}
c1 = {1,5,6,4,2,3,5,4}
for i in c:

    print(i)

c.add('qq')

print(c)

c.discard(6)

print(c)

cc = c.difference(c1)
print(cc)

ccc = c.union(c1)

print(ccc)


print('========================')
#dict
d = {'name':'11','age':'22',"sex":'0'}

d1 = d.get('name')

print(d1)


print(d.keys())

d.update({'name':'sss'})

print(d)




