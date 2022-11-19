import re


class Matrix:
    def __init__(self, dims, fill):
        self.rows = dims[0]
        self.cols = dims[1]
        self.A = [[fill] * self.cols for i in range(self.rows)]

    def __str__(self):
        value_return = ""

        for i in range(self.rows):
            for j in range(self.cols):
                value_return = value_return + str(self[i, j]) + " "
            value_return = value_return + "\n"

        return value_return

    def __add__(self, other):
        # Create a new matrix
        C = Matrix(dims=(self.rows, self.cols), fill=0)

        # Check if the other object is of type Matrix
        if isinstance(other, Matrix):
            # Add the corresponding element of 1 matrices to another
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] + other.A[i][j]

            # If the other object is a scaler
        elif isinstance(other, (int, float)):
            # Add that constant to every element of A
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] + other

        # TODO: Remove this when fixed
        self.create_indexing_attributes()
        return C

    # Right addition can be done by calling left addition
    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):  # pointwise multiplication

        C = Matrix(dims=(self.rows, self.cols), fill=0)
        if isinstance(other, Matrix):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] * other.A[i][j]

            # Scaler multiplication
        elif isinstance(other, (int, float)):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] * other

        # TODO: Remove this when fixed
        self.create_indexing_attributes()
        return C

    # Point-wise multiplication is also commutative
    def __rmul__(self, other):
        return self.__mul__(other)

    # matrix-matrix multiplication
    def __matmul__(self, other):

        if isinstance(other, Matrix):
            C = Matrix(dims=(self.rows, self.cols), fill=0)

            # Multiply the elements in the same row of the first matrix
            # to the elements in the same col of the second matrix
            for i in range(self.rows):
                for j in range(self.cols):
                    acc = 0

                    for k in range(self.rows):
                        acc += self.A[i][k] * other.A[k][j]

                    C.A[i][j] = acc

        # TODO: Remove this when fixed
        self.create_indexing_attributes()
        return C

    def __getitem__(self, key):
        if isinstance(key, tuple):
            i = key[0]
            j = key[1]
            return self.A[i][j]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            i = key[0]
            j = key[1]
            self.A[i][j] = value
            self.__dict__['_' + str(i) + '_' + str(j)] = self.A[i][j]

    def __iter__(self):
        for row in self.A:
            for item in row:
                yield item

    def __getattr__(self, item):
        match = re.match(r'_(\d+)_(\d+)$', item)
        if match:
            i = int(match.group(1))
            j = int(match.group(2))
            if (i >= self.rows or i < 0) and (j >= self.cols or j < 0):
                raise Exception('Index out of range')
            return self.A[i][j]
        match = re.match(r'as_(\S+)$', item)
        if match:
            temp = Matrix((self.rows, self.cols), 0)

            for i, item in enumerate(self):
                temp[i // self.cols, i % self.cols] = eval(match.groups()[0] + "(" + str(item) + ")")

            return lambda: temp
        return self.__getattribute__(item)

    def __setattr__(self, item, value):
        match = re.match(r'as_(\S+)$', item)
        if match:
            i = int(match.groups()[0])
            j = int(match.groups()[1])
            if i < 0 or i >= self.rows or j < 0 or j >= self.columns:
                raise Exception("Indices fuera del rango de la Matriz")
            self.values[i][j] = value
        super().__setattr__(item, value)
