# Segundo Proyecto de LP: Python Mágico

## Integrantes:
-Alejandro Yero Valdes

-Jesus Aldair Alfonso Perez

-Leismael Sosa Hernández

-Mauro Jose Bolado Vizoso

## Orientacion del proyecto:

1. Implemente la clase Matriz , para representar matrices con las operaciones de suma y producto. Implemente además otras funcionalidades que crea necesarias.
2. Implemente la indización para la clase Matriz de forma tal que se puedan hacer construcciones como las siguientes: 
   ```python 
   a= matriz[0, 6] o matriz[1, 2] = 9 .
   ```
3. Implemente la indización para la clase Matriz por medio de acceso a campos de la forma: 
   ```python
   a = matriz._0_6 o matriz._1_2 = 9 .
   ```
4. Los objetos matrices deberán ser iterables. El iterador de una matriz con n filas y m columnas debe devolver los
elementos en el siguiente orden:

    matriz_1_1, matriz_1_2, ..., matriz_1_m, matriz_2_1, ..., matriz_n_m

5. Al tipo matriz se podrá aplicar siempre el método as_type() que devuelve una nueva matriz con todos los tipos
convertidos al tipo type . Suponga que existe un constructor en type que convierte de cualquier tipo a type. Por
ejemplo:
    ```python
    m = Matriz(2, 3) # crea una matriz de int con valor 0s.
    mf = m.as_float() # mf es una matriz de 0s pero de tipo float.```

6. Investigar acerca de resolución de métodos y miembros en python, métodos mágicos, iteradores, el método built in eval y el funcionamiento de super.

## 1-) Métodos de suma y multiplicación.

La definición de operadores en python, como es el caso de los operadores de __suma__ y __multiplicación__  se realiza a través de la implementación de métodos especiales llamados __métodos mágicos__. Estos representan el conjunto de acciones que puede realizar una clase, son una lista finita de métodos cuya principal característica es que comienzan y terminan con doble guión bajo ( __ ). Por ejemplo, el método ```__add__``` es el encargado de realizar la suma de dos objetos de la clase Matriz, y el método ```__mul__``` es el encargado de realizar la resta de dos objetos de la clase Matriz. La implementación de estos métodos es la siguiente:

```python
def __add__(self, other):
    # Create a new matrix
    C = Matrix(dims=(self.rows, self.cols), fill=0)

    # Check if the other object is of type Matrix
    if isinstance(other, Matrix):

        if self.rows != other.rows or self.cols != other.cols:
            raise Exception("The number of rows and columns of both matrices must be equal")

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

    return C

def __sub__(self, other):
    # Create a new matrix
    C = Matrix(dims=(self.rows, self.cols), fill=0)

    # Check if the other object is of type Matrix
    if isinstance(other, Matrix):

        if self.rows != other.rows or self.cols != other.cols:
            raise Exception("The number of rows and columns of both matrices must be equal")

        # Add the corresponding element of 1 matrices to another
        for i in range(self.rows):
            for j in range(self.cols):
                C.A[i][j] = self.A[i][j] - other.A[i][j]

    # If the other object is a scaler
    elif isinstance(other, (int, float)):
        # Add that constant to every element of A
        for i in range(self.rows):
            for j in range(self.cols):
                C.A[i][j] = self.A[i][j] - other

    return C
```

```python
def __mul__(self, other):

    if isinstance(other, Matrix):
        if self.cols != other.rows:
            raise Exception("The number of columns of first matrix must be equal to the number of rows of the "
                            "second")
        C = Matrix(dims=(self.rows, other.cols), fill=0)

        # Multiply the elements in the same row of the first matrix
        # to the elements in the same col of the second matrix
        for i in range(self.rows):
            for j in range(other.cols):
                acc = 0

                for k in range(self.cols):
                    acc += self.A[i][k] * other.A[k][j]

                C.A[i][j] = acc

    return C
```

## 2-) Indización con corchetes.

Los métodos mágicos también se pueden utilizar para definir la indización de una clase, tanto para la obtención como la asignación de valores sobrescribiendo los métodos ```__getitem__``` y ```__setitem__``` respectivamente. Nosotros realizamos la implementación de la siguiente manera:

```python
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
```

## 3-) Indización con guión bajo.

Para esta implementación sobrescribimos los metodos ```__getattr__``` y ```__stattr__```que se ejecutan al acceder e intentar modificar una propiedad inexistente respectivamente. El funcionamiento de ```__getattr__(self, key)``` es el siguiente, ```self``` es el objeto que se esta instanciando y ```key``` es un string que contiene el nombre de la propiedad que se esta intentando acceder. En el caso de ```__setattr__(self, key, value)```, ```key``` es el nombre de la propiedad que se esta intentando modificar y ```value``` es el valor que se le quiere asignar. La implementación de este tipo de indización es la siguiente:

```python
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
```

## 4-) Iterador

Un iterador es un objeto que permite recorrer una secuencia de elementos y un objeto iterable es un objeto que puede devolver un iterador. En python, los objetos iterables son aquellos que implementan el método ```__iter__``` que devuelve un iterador. En nuestro caso, la clase Matriz es un objeto iterable, por lo que implementamos el método ```__iter__``` de la siguiente manera:

```python
def __iter__(self):
    for row in self.A:
        for item in row:
            yield item
```

en el cual se utiliza la palabra reservada ```yield``` que permite retornar un valor y pausar la ejecución del método, permitiendo que el método pueda ser llamado nuevamente y retome la ejecución desde donde se pauso. Los ciclos for en python utilizan internamente los métodos ```__iter__``` y ```__next__``` para iterar sobre los elementos de un objeto iterable, el ultimo método es el que se encarga de devolver el siguiente elemento de la secuencia, en el caso de que no exista mas elementos, se debe lanzar la excepción ```StopIteration```. En nuestro caso no implementamos el método ```__next__``` ya que como la matriz esta compuesta por una lista de listas, el método ```__iter__``` ya devuelve un iterados que permite recorrer la matriz.

## 5-) Implementación de as_type()

La función ```as_type()``` permite convertir los elementos de una matriz a un tipo de dato especifico
suponiendo que el tipo ```type``` contiene una función que permite convertir del tipo de la matriz a ```type```. Para la implementación utilizaremos el método mágico ```__getattr__``` que se ejecuta cuando se intenta acceder a una propiedad inexistente. El método ```__getattr__``` recibe como parámetro el nombre de la propiedad que se esta intentando acceder, en nuestro caso, el nombre de la propiedad sera ```as_type``` donde ```type``` es el tipo de dato al que se quiere convertir los elementos de la matriz. El método ```__getattr__``` debe retornar un objeto que implemente el método ```__call__``` que se ejecuta cuando se llama al objeto retornado por ```__getattr__```. En nuestro caso, el objeto que retornamos es una función lambda que retorna una nueva matriz con los elementos convertidos al tipo ```type```. La implementación de este método es la siguiente:

```python
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
```

En esta implementación utilizamos la función ```eval()```, que interpreta una cadena de texto y la ejecuta como código python.
## 6-) Funcionamiento de super y orden de resolución de métodos en python

### Super:

La función ```super()``` retorna una instancia temporal de la clase padre del objeto actual, la cual permite acceder a los métodos de la clase padre sin conocer su nombre, de modo que si se cambia el nombre de la clase padre, no es necesario cambiar el nombre de la clase en el código. Ejemplo con herencia simple:

```python
class Animal(object):
  def __init__(self, animal_type):
    print('Animal Type:', animal_type)
    
class Mammal(Animal):
  def __init__(self):

    # call superclass
    super().__init__('Mammal')

    print('Mammals give birth directly')
    
dog = Mammal()

# Output:
#  Animal Type: Mammal
#  Mammals give birth directly
```

Otro uso común de esta función es cuando se tiene herencia multiple, en cuyo caso se seguirá el principio de orden de resolución de métodos de python.

### Orden de Resolución de Métodos

El principio de orden de resolución de métodos es común en lenguajes con herencia multiple y determina, entre otras cosas en el caso de python, el orden en que se ejecutan los métodos de las clases padre. Python itero por diversos métodos para determinar el orden de resolución de métodos, hasta que se decidió adoptar el algoritmo de linealización C3 descrito en el articulo "A Monotonic Superclass Linearization for Dylan" de James C. King III. El algoritmo de linealización C3 es un algoritmo que permite determinar el orden de resolución de métodos de una clase que hereda de multiples clases. Según las propias palabras de Guido Van Rossum:

Dentro de una jerarquía de herencia compleja, se desea poder satisfacer todas estas reglas posibles de una manera que sea monótona. Es decir, si ya ha determinado que la clase A debe verificarse antes que la clase B, entonces nunca debería encontrarse con una situación que requiera que la clase B se verifique antes que la clase A (de lo contrario, el resultado no está definido y la jerarquía de herencia debe rechazarse) . Aquí es donde el MRO original se equivocó y donde entra en juego el algoritmo C3. Básicamente, la idea detrás de C3 es que si se escriben todas las reglas de orden impuestas por las relaciones de herencia en una jerarquía de clases compleja, el algoritmo determinará un orden monótono de las clases que las satisfaga a todas. Si tal orden no se puede determinar, el algoritmo fallará.

Un resultado de esto es que Python ahora rechazará cualquier jerarquía de herencia que tenga un orden inconsistente de las clases base. Por ejemplo, en el código siguiente, hay un conflicto de orden entre la clase X y la clase Y. Para la clase X, hay una regla que dice que la clase A debe verificarse antes que la clase B. Sin embargo, para la clase Y, la regla dice que la clase B debe verificarse antes que A. De forma aislada, esta discrepancia está bien, pero si X e Y alguna vez se combinan en la misma jerarquía de herencia para otra clase (como en la definición de la clase Z), esa clase será rechazada por el algoritmo C3. Esto, por supuesto, coincide con la regla de "los errores nunca deben pasar en silencio" del Zen de Python.

```python
class A(object): pass
class B(object): pass
class X(A, B): pass
class Y(B, A): pass
class Z(X, Y): pass
```
