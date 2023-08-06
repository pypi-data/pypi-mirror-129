Getting Started
===============

Installation
------------
pygeospandas is available as a python wheel on the Python Package Index (PyPi).
Install as follows:

.. code-block:: bash

   pip install pgpd


Example
-------
Let's get started by first creating a dataframe with PyGEOS data.  
Note that we need to explicitly set the type of the PyGEOS columns to **"geos"**!

.. code-block:: python

   >>> import pandas as pd
   >>> import pygeos
   >>> import pgpd
   
   >>> # Create a DataFrame
   >>> df = pd.DataFrame({
   ...   'a': list('abcde'),
   ...   'poly': pygeos.box(range(5), 0, range(10,15), 10),
   ...   'pt': pygeos.points(range(5), range(10,15))
   ... })
   >>> df = df.astype({'poly':'geos', 'pt':'geos'})
   >>> df
      a                                     poly            pt
   0  a  POLYGON ((0 0, 0 10, 10 10, 10 0, 0 0))  POINT (0 10)
   1  b  POLYGON ((1 0, 1 10, 11 10, 11 0, 1 0))  POINT (1 11)
   2  c  POLYGON ((2 0, 2 10, 12 10, 12 0, 2 0))  POINT (2 12)
   3  d  POLYGON ((3 0, 3 10, 13 10, 13 0, 3 0))  POINT (3 13)
   4  e  POLYGON ((4 0, 4 10, 14 10, 14 0, 4 0))  POINT (4 14)


PyGEOS
~~~~~~
We can access pygeos functionality through the "geos" accessor namespace.  

.. code-block:: python

   >>> df.poly.geos.length()
   0    40.0
   1    40.0
   2    40.0
   3    40.0
   4    40.0
   Name: length, dtype: float64
   
   >>> df.pt.geos.total_bounds()
   xmin     0.0
   ymin    10.0
   xmax     4.0
   ymax    14.0
   Name: total_bounds, dtype: float64
   
   >>> df.poly.geos.clip_by_rect(0, 0, 5, 10)
   0    POLYGON ((0 0, 0 10, 5 10, 5 0, 0 0))
   1    POLYGON ((1 0, 1 10, 5 10, 5 0, 1 0))
   2    POLYGON ((2 0, 2 10, 5 10, 5 0, 2 0))
   3    POLYGON ((3 0, 3 10, 5 10, 5 0, 3 0))
   4    POLYGON ((4 0, 4 10, 5 10, 5 0, 4 0))
   Name: clip_by_rect, dtype: geos

Some functions return more values per row, so we convert them to DataFrames:

.. code-block:: python

   >>> df.poly.bounds()
      xmin  ymin  xmax  ymax
   0   0.0   0.0  10.0  10.0
   1   1.0   0.0  11.0  10.0
   2   2.0   0.0  12.0  10.0
   3   3.0   0.0  13.0  10.0
   4   4.0   0.0  14.0  10.0

There are some functions that return a variable number of items per original object.
For these functions, the index of the returned Series/DataFrame will point to the original object index.

.. code-block:: python

   >>> points = pd.Series(
   ...   pygeos.multipoints(
   ...     [[0,0], [1,1], [2,2], [0,1],[2,3], [10,20],[30,40],[40,50],[50,60]],
   ...     indices=[0,0,0,1,1,2,2,2,2],
   ...   ),
   ...   dtype='geos',
   ... )
   >>> points
   0                 MULTIPOINT (0 0, 1 1, 2 2)
   1                      MULTIPOINT (0 1, 2 3)
   2    MULTIPOINT (10 20, 30 40, 40 50, 50 60)
   dtype: geos
   
   >>> points.geos.get_parts()
   0      POINT (0 0)
   0      POINT (1 1)
   0      POINT (2 2)
   1      POINT (0 1)
   1      POINT (2 3)
   2    POINT (10 20)
   2    POINT (30 40)
   2    POINT (40 50)
   2    POINT (50 60)
   Name: get_parts, dtype: geos
   
   >>> points.geos.get_coordinates()
         x     y   z
   0   0.0   0.0 NaN
   0   1.0   1.0 NaN
   0   2.0   2.0 NaN
   1   0.0   1.0 NaN
   1   2.0   3.0 NaN
   2  10.0  20.0 NaN
   2  30.0  40.0 NaN
   2  40.0  50.0 NaN
   2  50.0  60.0 NaN

Finally, PyGEOS also has some binary functions, which work on 2 different sets of geometries.  
These functions are also made available on Series, but work slightly differently.
We added a `manner` argument, which can be one of 3 different values: *keep*, *align*, *expand*.
This argument dictates how the 2 sets of geometries are transformed before running the binary function:

- *keep*: Function is run on the input as is.
- *align*: Align both sets with each other, according to their index (only works when `other` is a Series).
- *expand*: Expand both sets to a 2D array and compare each geometry of set A with each geometry of set B (returns a 2D array of dimension *<len(A), len(B)>*).

.. code-block:: python

   >>> # KEEP: Just runs the `contains` function on the "poly" column data and the given Point
   >>> df.poly.geos.contains(pygeos.Geometry("Point (11 5)"), manner='keep')
   0    False
   1    False
   2     True
   3     True
   4     True
   Name: contains, dtype: bool
   
   >>> # ALIGN: We only pass 3 points, but tell the function to align the data according to the index
   >>> df.poly.geos.distance(df.pt[1:4], manner='align')
   0    NaN
   1    1.0
   2    2.0
   3    3.0
   4    NaN
   Name: distance, dtype: float64
   
   >>> # EXPAND: Compare each polygon with each point (returns numpy.ndarray <5,3> in this case)
   >>> df.poly.geos.distance(df.pt[1:4], manner='expand')
   array([[1.        , 2.        , 3.        ],
          [1.        , 2.        , 3.        ],
          [1.41421356, 2.        , 3.        ],
          [2.23606798, 2.23606798, 3.        ],
          [3.16227766, 2.82842712, 3.16227766]])


One last difference is that you can omit the `other` set of geometries.
The method will then automatically choose the *expand* mode and use the `self` data twice.

.. code-block:: python

   >>> # Compute all possible intersection areas of the geometries in the "poly" column
   >>> pygeos.area(df.poly.geos.intersection())
   array([[100.,  90.,  80.,  70.,  60.],
          [ 90., 100.,  90.,  80.,  70.],
          [ 80.,  90., 100.,  90.,  80.],
          [ 70.,  80.,  90., 100.,  90.],
          [ 60.,  70.,  80.,  90., 100.]])


Custom
~~~~~~
Additionally to the PyGEOS functionality, we added some extra methods to be able to transform the coordinates of the geometries more easilly.

The :func:`~pgpd.GeosSeriesAccessor.affine`, :func:`~pgpd.GeosSeriesAccessor.rotate`, :func:`~pgpd.GeosSeriesAccessor.scale`, :func:`~pgpd.GeosSeriesAccessor.skew` and :func:`~pgpd.GeosSeriesAccessor.translate` functions allow to perform a single affine transformation to all the coordinates of your geometries.

.. code-block:: python

   >>> # Rotate all geometries 90 degrees (1.571 rad) around the (0, 0) origin.
   >>> df.pt.geos.rotate(1.571, origin=(0, 0))
   0    POINT (-10 0)
   1    POINT (-11 1)
   2    POINT (-12 2)
   3    POINT (-13 3)
   4    POINT (-14 4)
   Name: rotate, dtype: geos

You can also add, subtract, multiply or divide values with these series.
This will perform the operation on the coordinates array. |br|
However, we perform some checks and potentially modify your input before executing the mathematical operation:

- Depending on the second dimension of your input array, we use 2D or 3D coordinates. Note that if your geometries are 2D, performing 3D operations has no effect.
- If you have one set of coordinates per geometry, instead of one set of coordinates foreach point in the set, we automatically expand each coordinate to the number of points per geometry.

.. code-block::

   >>> # Perform 2D multiplication
   >>> # Note that we only provide one transformation coordinate per polygon
   >>> df.poly * [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
   0      POLYGON ((10 0, 10 10, 0 10, 0 0, 10 0))
   1      POLYGON ((22 0, 22 20, 2 20, 2 0, 22 0))
   2      POLYGON ((36 0, 36 30, 6 30, 6 0, 36 0))
   3    POLYGON ((52 0, 52 40, 12 40, 12 0, 52 0))
   4    POLYGON ((70 0, 70 50, 20 50, 20 0, 70 0))
   Name: poly, dtype: geos

   >>> # NumPy broadcasting rules still apply
   >>> df.poly + 10
   0    POLYGON ((20 10, 20 20, 10 20, 10 10, 20 10))
   1    POLYGON ((21 10, 21 20, 11 20, 11 10, 21 10))
   2    POLYGON ((22 10, 22 20, 12 20, 12 10, 22 10))
   3    POLYGON ((23 10, 23 20, 13 20, 13 10, 23 10))
   4    POLYGON ((24 10, 24 20, 14 20, 14 10, 24 10))
   Name: poly, dtype: geos


DataFrame
~~~~~~~~~
While all PyGEOS functions are available on Series, some are made available on the DataFrame as well.  
The functions that are available on DataFrames are those that have a 1-to-1 mapping (create one output for each geometry in the column), or those that have a fixed number of outputs for the entire geos column.

.. code-block:: python

   >>> # Fixed number of outputs (ic. xmin,ymin,xmax,ymax)
   >>> df.geos.total_bounds()
         poly    pt
   xmin   0.0   0.0
   ymin   0.0  10.0
   xmax  14.0   4.0
   ymax  10.0  14.0
   
   >>> # For every PyGEOS function that has a 1-to-1 relation,
   >>> # the DataFrame variant allows inplace modification
   >>> df.geos.apply(lambda coord: coord*2, inplace=True)
   >>> df
      a                                     poly            pt
   0  a  POLYGON ((0 0, 0 20, 20 20, 20 0, 0 0))  POINT (0 20)
   1  b  POLYGON ((2 0, 2 20, 22 20, 22 0, 2 0))  POINT (2 22)
   2  c  POLYGON ((4 0, 4 20, 24 20, 24 0, 4 0))  POINT (4 24)
   3  d  POLYGON ((6 0, 6 20, 26 20, 26 0, 6 0))  POINT (6 26)
   4  e  POLYGON ((8 0, 8 20, 28 20, 28 0, 8 0))  POINT (8 28)


GeoPandas
---------
The main use case for this library is not to depend on GeoPandas and all of its dependencies.
However -if you need to- this library provides methods to convert from and to GeoPandas.


Series
~~~~~~

.. code-block:: python

   >>> gs = df.pt.geos.to_geopandas(crs='WGS84')
   >>> gs
   0    POINT (0.00000 20.00000)
   1    POINT (2.00000 22.00000)
   2    POINT (4.00000 24.00000)
   3    POINT (6.00000 26.00000)
   4    POINT (8.00000 28.00000)
   Name: pt, dtype: geometry
   
   >>> s2 = gs.geos.from_geopandas()
   >>> s2
   0    POINT (0 20)
   1    POINT (2 22)
   2    POINT (4 24)
   3    POINT (6 26)
   4    POINT (8 28)
   Name: pt, dtype: geos


DataFrame
~~~~~~~~~

.. code-block:: python

   >>> gdf = df.geos.to_geopandas(geometry='poly', crs='WGS84')
   >>> gdf
      a                                               poly            pt
   0  a  POLYGON ((0.00000 0.00000, 0.00000 20.00000, 2...  POINT (0 20)
   1  b  POLYGON ((2.00000 0.00000, 2.00000 20.00000, 2...  POINT (2 22)
   2  c  POLYGON ((4.00000 0.00000, 4.00000 20.00000, 2...  POINT (4 24)
   3  d  POLYGON ((6.00000 0.00000, 6.00000 20.00000, 2...  POINT (6 26)
   4  e  POLYGON ((8.00000 0.00000, 8.00000 20.00000, 2...  POINT (8 28)
   >>> gdf.dtypes
   a         object
   poly    geometry
   pt          geos
   dtype: object
   
   >>> df2 = gdf.geos.from_geopandas()
   >>> df2
      a                                     poly            pt
   0  a  POLYGON ((0 0, 0 20, 20 20, 20 0, 0 0))  POINT (0 20)
   1  b  POLYGON ((2 0, 2 20, 22 20, 22 0, 2 0))  POINT (2 22)
   2  c  POLYGON ((4 0, 4 20, 24 20, 24 0, 4 0))  POINT (4 24)
   3  d  POLYGON ((6 0, 6 20, 26 20, 26 0, 6 0))  POINT (6 26)
   4  e  POLYGON ((8 0, 8 20, 28 20, 28 0, 8 0))  POINT (8 28)
   >>> df2.dtypes
   a       object
   poly      geos
   pt        geos
   dtype: object


.. include:: /links.rst
