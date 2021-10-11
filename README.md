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

## MyLine

It implements some basic line functionalities.

```python

from vectors import MyVector
from lines import MyLine

l1 = MyLine(MyVector([1, -1]), 0)
l2 = MyLine(MyVector([1, 1]), 0)
print(l1.intersection(l2))

```
## MyPlane and MyLinearSystem:

They help solve 3-variable ecuation systems by implementing the Gauss-Jordan method:

```python

from vectors import MyVector
from planes import MyPlane
from linsys import MyLinearSystem

p1 = MyPlane(MyVector([5.862, 1.178, -10.366]), -8.15)
p2 = MyPlane(MyVector([-2.931, -0.589, 5.183]), -4.075)
ls = MyLinearSystem([p1, p2])

p1_2, p2_2, p2_3 = MyPlane(MyVector([8.631, 5.112, -1.816]), -5.113), MyPlane(MyVector([4.315, 11.132, -5.27]), -6.775), \
                       MyPlane(MyVector([-2.158, 3.01, -1.727]), -0.831)
ls2 = MyLinearSystem([p1_2, p2_2, p2_3])

p1_3, p2_3, p3_3, p4_3 = MyPlane(MyVector([5.262, 2.739, -9.878]), -3.441), MyPlane(MyVector([5.111, 6.358, 7.638]), -2.152), \
                             MyPlane(MyVector([2.016, -9.924, -1.367]), -9.278), MyPlane(MyVector([2.167, -13.543, -18.883]), -10.56)
ls3 = MyLinearSystem([p1_3, p2_3, p3_3, p4_3])

print(ls.solve())
print(ls2.solve())
print(ls3.solve())

para1 = MyPlane(MyVector([0.786, 0.786, .588]), -.714)
para2 = MyPlane(MyVector([-.138, -.138, .244]), .319)
pls = MyLinearSystem([para1, para2])
print('------\n', pls.solve())

para1 = MyPlane(MyVector([8.631, 5.112, -1.816]), -5.113)
para2 = MyPlane(MyVector([4.315, 11.132, -5.27]), -6.775)
para3 = MyPlane(MyVector([-2.158, 3.01, -1.727]), -.831)
pls2 = MyLinearSystem([para1, para2, para3])
print('------\n', pls2.solve())

para1 = MyPlane(MyVector([.935, 1.76, -9.365]), -9.955)
para2 = MyPlane(MyVector([.187, .352, -1.873]), -1.991)
para3 = MyPlane(MyVector([.374, .704, -3.746]), -3.982)
para4 = MyPlane(MyVector([-.561, -1.056, 5.619]), 5.973)
pls3 = MyLinearSystem([para1, para2, para3,para4])
print('------\n', pls3.solve())

#New trials:
"""
2x-y+2z=6
3x+2y-z=4
4x+3y-3z=1
"""
e_1 = MyPlane(MyVector([2,-1,2]),6)
e_2 = MyPlane(MyVector([3,2,-1]), 4)
e_3 = MyPlane(MyVector([4,3,-3]),1)
le = MyLinearSystem([e_1, e_2, e_3])
print('------\n', le.solve())

```
