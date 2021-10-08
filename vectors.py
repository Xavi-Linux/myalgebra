from math import sqrt, acos, pi, cos, sin
from functools import reduce
from decimal import Decimal, getcontext

PREC = getcontext().prec


class MyVector:

    def __init__(self, coordinates:[tuple, list]):
        """
        Class constructor
        :param coordinates: accepts a tuple or a list
        """
        try:
            self.coordinates = tuple(map(Decimal, coordinates))
            self.dim = len(self.coordinates)

        except TypeError:
            raise TypeError('Coordinates must be either a tuple or a list')

    def __str__(self):
        return "This vector's coordinates are ({})".format(', '.join(map(str, self.coordinates)))

    def __eq__(self, vec):
        """
        :param vec: another MyVector instance.
        :return: a boolean indicating if both vectors have the same coordinates
        """
        return self.coordinates == vec.coordinates

    def __add__(self, vec):
        """

        :param vec: another MyVector instance.
        :return: a new MyVector instance.
        """
        if self.dim == vec.dim:
            total = []
            for i, j in zip(self.coordinates, vec.coordinates):
                total.append(i+j)
            return MyVector(total)
        else:
            raise Exception('Vectors must have same dimensions')

    def __sub__(self, vec):
        """

        :param vec: another MyVector instance.
        :return: a new MyVector instance.
        """
        if self.dim == vec.dim:
            total = []
            for i, j in zip(self.coordinates, vec.coordinates):
                total.append(i-j)
            return MyVector(total)
        else:
            raise Exception('Vectors must have same dimensions')

    def __mul__(self, val):
        """

        :param val: a scalar value.
        :return: a new MyVector instance.
        """
        return MyVector(map(lambda a: a * Decimal(val),
                            self.coordinates))

    def magnitude(self):
        """

        :return: a scalar representing the vector's magnitude
        """
        return (reduce(lambda a,b: a+b,
                       map(lambda c: c**2,
                           self.coordinates))).sqrt()

    def normalise(self):
        """

        :return: a unit vector. A new MyVector instance
        """
        try:
            norm = self.magnitude()
            return MyVector(map(lambda c: c/norm,
                                self.coordinates))

        except ZeroDivisionError:
            raise ZeroDivisionError('Zero Vector cannot be normalised')

    def dot(self, vec):
        """

        :param vec: another MyVector instance.
        :return: the inner product.
        """
        if self.dim==vec.dim:
            return reduce(lambda a,b: a+b,
                          map(lambda v, w: v*w,
                              self.coordinates, vec.coordinates))

        else:
            raise Exception('Vectors must have same dimensions')

    def angle(self, vec, degrees=True):
        """

        :param vec:  another MyVector instance.
        :param degrees: a boolean indicating if the returned values is in degrees or radians
        :return: a scalar indicating the width of the angled compressed between two vectors.
        """
        def radians_to_degrees(rad):
            return rad * 180./pi
        if self.dim==vec.dim:
            try:
                angle = acos(self.dot(vec)/(self.magnitude() * vec.magnitude()))
                if degrees:
                    return radians_to_degrees(angle)

                return angle

            except ZeroDivisionError:
                raise ZeroDivisionError('Impossible to compute angle for Zero Vector')
        else:
            raise Exception('Vectors must have same dimensions')

    def is_parallel(self, vec):
        """
        Checks whether or not two vector are parallel
        :param vec: another MyVector instance
        :return: a boolean
        """
        return self.is_zero_vector() or vec.is_zero_vector() or self.angle(vec) == 0 or self.angle(vec) == 180

    def is_orthogonal(self, vec, tolerance=1e-10):
        """
        Checks whether or not two vector are orthogonal
        :param vec: another MyVector instance
        :param tolerance: a small float number to cope with rounding mistakes.
        :return: a boolean
        """
        return abs(self.dot(vec)) <= tolerance

    def is_zero_vector(self, tolerance=1e-10):
        """
        Checks whether the instance is a 0 vector
        :param tolerance: a small float number to cope with rounding mistakes.
        :return: a boolean
        """
        return all([abs(c)<=tolerance for c in self.coordinates])

    def decompose(self, base):
        """
        Project the instance onto another base and returns its decomposition
        :param base: another MyVector instance
        :return: a tuple
        """
        scaler = self.dot(base.normalise())
        projection = base.normalise() * scaler
        return projection, self - projection

    def cross_product(self, vec):
        """
        Calcutates the cross product between two 3d vectors
        :param vec: another MyVector instance
        :return: a new MyVector instance
        """
        if self.dim == 3 and vec.dim ==3:
            return MyVector([self.coordinates[1] * vec.coordinates[2] - self.coordinates[2] * vec.coordinates[1],
                             -1 * (self.coordinates[0] * vec.coordinates[2] - self.coordinates[2] * vec.coordinates[0]),
                             self.coordinates[0] * vec.coordinates[1]-self.coordinates[1] * vec.coordinates[0]
                             ])
        else:
            raise Exception('Cross product is only available for 3d vectors')

    def parallelogram_area(self, vec):
        """

        :param vec: a new MyVector instance
        :return: the area of the parallel formed by the cross product of two 3d vectors
        """
        return self.cross_product(vec).magnitude()

    def triangle_area(self, vec):
        """

        :param vec: a new MyVector instance.
        :return: half of the area of the parallel formed by the cross product of two 3d vectors
        """
        return self.parallelogram_area(vec)/2

    def orthogonal_vector(self):
        """

        :return: a new orthogonal vector with respect to the instance.
        """
        return self.rotate(self, 90)

    @staticmethod
    def rotate(vector, degrees, anticlockwise=True):
        """

        :param vector: a MyVector instance
        :param degrees: the number of degrees to rotate to.
        :param anticlockwise: direction of the rotation
        :return: a MyVector instance
        """
        def degrees_to_radians(rad):
            return rad * pi/180
        if vector.dim == 2:
            degrees = degrees_to_radians(degrees)
            c = Decimal(cos(degrees))
            s = Decimal(sin(degrees))
            x = vector.coordinates[0]
            y = vector.coordinates[1]
            if anticlockwise:
                return MyVector([c * x - s * y, s * x + c * y])
            else:
                return MyVector([c * x + s * y, -s * x + c * y])
        else:
            raise Exception('Rotation is only implemented for 2d vectors')
