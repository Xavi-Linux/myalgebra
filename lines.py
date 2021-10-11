from decimal import Decimal, getcontext
from vectors import MyVector


class MyLine:

    def __init__(self, normal_vector:MyVector=None, constant=None):
        """
        Constructor of the class
        :param normal_vector: a MyVector instance representing the normal vector of the line
        :param constant: a scalar value
        """
        #Ax+By=k
        self.dim = 2

        if not normal_vector:
            normal_vector = MyVector([0] * self.dim)
        self.normal_vector = normal_vector

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
        return 0, float(self.constant/self.normal_vector.coordinates[1])

    def direction_vector(self):
        """

        :return: a MyVector instance representating the direction vector
        """
        direction_coordinates = list(self.normal_vector.coordinates[::-1])
        direction_coordinates[1]*=-1
        return MyVector(direction_coordinates)

    def is_parallel_to(self, l2):
        """
        Checks if two lines are parallel
        :param l2: another MyLine instance
        :return: a boolean
        """
        return self.normal_vector.is_parallel(l2.normal_vector)

    def same_line(self, l2):
        """
        Check if two MyLine instances represent the same line
        :param l2: another MyLine instance
        :return: a boolean
        """
        if not self.is_parallel_to(l2):
            return False
        point_connector = MyVector(self.base_point) - MyVector(l2.base_point)
        return point_connector.is_orthogonal(self.normal_vector)

    def intersection(self, l2):
        """
        Calculates the intersection of two lines (if it exists)
        :param l2: another MyLine instance
        :return: a tuple representing the intersection point
        """
        if self.is_parallel_to(l2):
            if self.same_line(l2):
                return self
            return None
        denominator = self.normal_vector.coordinates[0] * l2.normal_vector.coordinates[1] - \
                      self.normal_vector.coordinates[1] * l2.normal_vector.coordinates[0]
        x = (l2.normal_vector.coordinates[1] * self.constant - self.normal_vector.coordinates[1] * l2.constant) /denominator
        y = (l2.normal_vector.coordinates[0] * self.constant * -1 + self.normal_vector.coordinates[0] * l2.constant) /denominator
        return x, y
