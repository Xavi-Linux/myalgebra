# Myalgebra
----

An algebra refresher in plain Python.

## MyVector

It implements some basic vector funcionalities.

```python

from vectors import MyVector

a = MyVector([3,4])
b = MyVector([10,5,6])
c = MyVector([4,9,1])

d = c.dot(b)
print(d)
cp = b.cross_product(c)
print(cp)
print(a.magnitude())
print(a.normalise())

```
