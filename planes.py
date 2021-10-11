from decimal import Decimal, getcontext, DivisionUndefined, InvalidOperation
from vectors import MyVector


class MyPlane:

    def __init__(self, normal_vector:MyVector=None, constant=None):
        """
        Class constructor
        Ax+By+Cz=k
        :param normal_vector: a MyVector instance representing the normal vector of the plane
        :param constant: a scalar
        """

        self.dim = 3

        if not normal_vector:
            normal_vector = MyVector([0] * self.dim)
        self.normal_vector = normal_vector

        if normal_vector.dim != 3:
            raise Exception('Normal vector must be 3d')

        if not constant:
            constant = 0
        self.constant = Decimal(constant)

    def __str__(self):
        output = ''
        for i, c in enumerate(self.normal_vector.coordinates):
            subscript = r'\u208{}'.format(str(i)).encode('utf-8')
            output += '{0:+.2f}x{1}'.format(c,subscript.decode('unicode_escape'))
        output += '= {:.2f}'.format(self.constant)
        return output

    @property
    def base_point(self):
        """

        :return: a tuple containing the base point
        """
        try:
            return 0, 0, float(self.constant/self.normal_vector.coordinates[2])

        except ZeroDivisionError:
            try:
                return 0, float(self.constant / self.normal_vector.coordinates[1]), 0

            except ZeroDivisionError:
                try:
                    return float(self.constant / self.normal_vector.coordinates[0]), 0, 0

                except ZeroDivisionError:
                    return 0, 0, 0

        except InvalidOperation:
            return 0,0,0

    def is_parallel_to(self, p2):
        """

        :param p2: another MyPlane instance
        :return: a boolean indicating if both planes are parallel
        """
        return self.normal_vector.is_parallel(p2.normal_vector)

    def same_plane(self, p2):
        """

        :param p2: another MyPlane instance
        :return: a boolean indicating if both planes are the same
        """
        if not self.is_parallel_to(p2):
            return False
        point_connector = MyVector(self.base_point) - MyVector(p2.base_point)
        return point_connector.is_orthogonal(self.normal_vector)

    def __eq__(self, p2):
        """

        :param p2: another MyPlane instance
        :return: a boolean indicating if both planes are the same
        """
        return self.same_plane(p2)
