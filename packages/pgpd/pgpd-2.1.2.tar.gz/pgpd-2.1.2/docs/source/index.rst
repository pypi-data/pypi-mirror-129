.. PyGEOS-pandas documentation master file, created by
   sphinx-quickstart on Mon Mar 15 15:42:23 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


|pgpdlogo|

pygeospandas is a simple wrapper around `PyGEOS`_, in order to allow using its functionality in `pandas`_. |br|
It contains the following pieces:

- *GeosArray & GeosDtype* |br|
  pandas ExtensionArray and Dtype to be able to work with PyGEOS data in Series and DataFrames.
- *"geos" Series Accessor* |br|
  Access all of the PyGEOS functionality on Series objects, so that there is no need to unwrap to NumPy arrays.
- *"geos" DataFrame Accessor* |br|
  Apply PyGEOS functions to all "geos" Dtype series in the dataframe at once.

.. container:: button

   :doc:`Getting Started <notes/01-start>`
   :doc:`Documentation <api/index>`
   :doc:`Benchmark <notes/02-benchmark>`


GeoPandas
=========
This library is pretty similar to the `GeoPandas`_ library. |br|
The main difference is that this library is much more lightweight,
as it only depends on `NumPy`_, `pandas`_ and `PyGeos`_.
You might want to use this library over `GeoPandas`_ if you need to work with geometries,
but do not care about CRS or other geospatial features.

Note that this library only supports PyGEOS operations and is thus more limited in what it can do.
There are functions to transform the data to `Shapely`_ geometries, which gives more possibilities,
but only PyGEOS supported operations are implemented on the Series and DataFrames.


.. toctree::
   :hidden:

   Home <self>
   Getting Started <notes/01-start>
   Documentation <api/index>
   Benchmark <notes/02-benchmark>


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. include:: /links.rst
