from copy import deepcopy
from vectors import MyVector
from planes import MyPlane
from functools import reduce
from decimal import Decimal


class MyLinearSystem:

    def __init__(self, planes:list):
        """
        Class constructor
        :param planes: a list of MyPlane instances
        """
        try:
            ref_dim = planes[0].dim
            assert all(map(lambda p: p.dim == ref_dim, planes))
            self.planes = planes
            self.dim = ref_dim

        except AssertionError:
            raise Exception('All planes in the system must have same-dimension vectors')

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, item):
        return self.planes[item]

    def __setitem__(self, key, value):
        try:
            assert value.dim == self.dim
            self.planes[key] = value

        except AssertionError:
            raise Exception('All planes in the system must have same-dimension vectors')

    def __str__(self):
        return '\n'.join([str(p) for p in self.planes])

    def swap_rows(self, row_1, row_2):
        """
        swaps two rows of the linear system
        :param row_1: index
        :param row_2: index
        :return: nothing
        """
        self.planes[row_1], self.planes[row_2] = self.planes[row_2], self.planes[row_1]

    def multiply_row_by_scalar(self, row, scalar, transform=True):
        """

        :param row: row to be modified
        :param scalar: scalar by which the planes is multiplied
        :param transform: if true, it modifies the target row of the system; otherwise, it just returns
        a tuple with the new normal vector and the new constant
        :return: nothing or a tuple
        """
        if scalar == 0:
            raise Exception('Scalar value must be different from 0')

        normal_vector = self.planes[row].normal_vector * scalar
        constant = self.planes[row].constant * scalar
        if transform:
            self.planes[row].normal_vector = normal_vector
            self.planes[row].constant = constant
        else:
            return normal_vector, constant

    def add_row_to_row_ntimes(self, scalar, added_row, to_row):
        """

        :param scalar: the scalar by which added_row is multiplied
        :param added_row: the row to add to another
        :param to_row: the target row to be modified
        :return: nothing
        """
        row_t_scalar, cons_t_scalar = self.multiply_row_by_scalar(added_row, scalar, transform=False)
        self.planes[to_row].normal_vector += row_t_scalar
        self.planes[to_row].constant += cons_t_scalar

    def triangular_form(self, tolerance=1e-10):
        """
        Transform the linear system into a triangular form
        :param tolerance:
        :return: a new MyLinarSystem instance
        """
        lsys = deepcopy(self)
        lsys = lsys.order_system(lsys)
        for p in range(0,len(lsys)-1):
            if abs(lsys[p].normal_vector.coordinates[p]) > tolerance:
                for np in range(p+1, len(lsys)):
                    if abs(lsys[np].normal_vector.coordinates[p]) > tolerance:
                        scalar = -1 * lsys[np].normal_vector.coordinates[p]/lsys[p].normal_vector.coordinates[p]
                        lsys.add_row_to_row_ntimes(scalar, p, np)

            lsys = lsys.order_system(lsys)

        return lsys

    @staticmethod
    def order_system(system, tolerance=1e-10):
        """
        sorts the linear system in such fashion that the greater the number of 0 coeficients is , the greater the index
        the ecuation is assigned
        :param system: a MyLinearSystem instance
        :param tolerance:
        :return: a Linear System instance
        """
        def select_sort(planes, order):
            new_order = []
            for index in order:
                new_order.append(planes[index])
            return new_order

        units = [10**v for v in range(0, system.dim)][::-1]
        values = []
        for i, plane in enumerate(system.planes):
            boolean_array = list(map(lambda c: int(abs(c)<=tolerance),
                                     plane.normal_vector.coordinates))
            zeros = boolean_array.count(0)
            value = reduce(lambda a,b: a+b,
                           map(lambda b,u: b*u,
                               boolean_array,
                               units)) * (2**(system.dim-zeros))
            values.append((value, i))

        values = map(lambda t: t[1],
                     sorted(values, key=lambda k: k[0], reverse=False))

        return MyLinearSystem(select_sort(system.planes, values))

    def echelon_form(self):
        ef = self.triangular_form()
        ref_dim = ef.dim - 1
        for p in range(len(ef)-1, -1, -1):
            if not ef[p].normal_vector.is_zero_vector() and ef.__first_non_zero(ef[p]) == ref_dim:
                ef.multiply_row_by_scalar(p, 1/ef[p].normal_vector.coordinates[ref_dim])
                value = ef[p].constant

                for np in range(p-1,-1, -1):
                    new_constant = ef[np].constant - ef[np].normal_vector.coordinates[ref_dim] * value
                    new_coords = list(ef[np].normal_vector.coordinates[:ref_dim]) + [0] \
                                 + list(ef[np].normal_vector.coordinates[ref_dim+1:])
                    ef[np] = MyPlane(MyVector(new_coords), new_constant)

                ref_dim -= 1

        return ef

    @staticmethod
    def __first_non_zero(plane, tolerance=1e-10):
        for i, c in enumerate(plane.normal_vector.coordinates):
            if abs(c) > tolerance:
                return i

    def solve(self, tolerance=0.01):
        """
        solves the linear system
        :param tolerance:
        :return: None/inf/ a list containing the solution
        """
        lsys = self.echelon_form()
        count_empty=0
        for plane in lsys.planes:
            if plane.normal_vector.is_zero_vector() and abs(plane.constant) > tolerance:
                return None
            elif plane.normal_vector.is_zero_vector() and abs(plane.constant) <= tolerance:
                count_empty += 1

        if lsys.dim > len(lsys) - count_empty:
            return 'Inf'

        return list(map(lambda p: float(p.constant), lsys.planes))[:lsys.dim]

