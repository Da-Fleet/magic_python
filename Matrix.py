

class Matrix:
    def __init__(self, dims, fill):
        self.rows = dims[0]
        self.cols = dims[1]
        self.A = [[fill] * self.cols for i in range(self.rows)]
        self.create_indexing_attributes()

    def create_indexing_attributes(self):
        for i in range(self.rows):
            for j in range(self.cols):
                '''
                BUG: if i change the matrix this will return ceros, change it without
                having to change the value every time i make a change in the matrix
                '''
                self.__dict__['_' + str(i) + '_' + str(j)] = self.A[i][j] 

    def __str__(self):
        m = len(self.A) # Get the first dimension
        mtxStr = ''
        mtxStr += '------------- output -------------\n'
        for i in range(m):
            mtxStr += ('|' + ', '.join( map(lambda x:'{0:8.3f}'.format(x), self.A[i])) + '| \n')
        
        mtxStr += '----------------------------------'

        return mtxStr

    def __add__(self, other):
		#Create a new matrix
        C = Matrix( dims = (self.rows, self.cols), fill = 0)

		#Check if the other object is of type Matrix
        if isinstance (other, Matrix):
			#Add the corresponding element of 1 matrices to another
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] + other.A[i][j]

		#If the other object is a scaler
        elif isinstance (other, (int, float)):
			#Add that constant to every element of A
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] + other

        #TODO: Remove this when fixed
        self.create_indexing_attributes()
        return C

	#Right addition can be done by calling left addition
    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other): #pointwise multiplication

        C = Matrix( dims = (self.rows, self.cols), fill = 0)
        if isinstance(other, Matrix):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] * other.A[i][j]

		#Scaler multiplication
        elif isinstance(other, (int, float)):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] * other

        #TODO: Remove this when fixed
        self.create_indexing_attributes()
        return C 

	#Point-wise multiplication is also commutative
    def __rmul__(self, other):
        return self.__mul__(other)

    #matrix-matrix multiplication
    def __matmul__(self, other): 

        if isinstance(other, Matrix):
            C = Matrix( dims = (self.rows, self.cols), fill = 0)

			#Multiply the elements in the same row of the first matrix 
			#to the elements in the same col of the second matrix
            for i in range(self.rows):
                for j in range(self.cols):
                    acc = 0

                    for k in range(self.rows):
                        acc += self.A[i][k] * other.A[k][j]

                    C.A[i][j] = acc

        #TODO: Remove this when fixed
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

mat = Matrix((3,3), 0)
mat[0,0] = 1
mat[0,1] = 2
mat[0,2] = 3
mat[1,0] = 4
mat[1,1] = 5
mat[1,2] = 6
mat[2,0] = 7
mat[2,1] = 8
mat[2,2] = 9

print(mat._0_0)
print(mat._0_1)
print(mat._0_2)
for i in range(3):
    for j in range(3):
        exec('print(mat._' + str(i) + '_' + str(j) + ')')