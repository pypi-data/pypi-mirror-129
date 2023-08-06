Geos ExtensionArray
===================

.. currentmodule:: pgpd

.. autoclass:: GeosArray
   :members: dtype, ndim


Serialization
-------------
Serialization & Deserialization functionality.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosArray.__init__
   GeosArray.from_shapely
   GeosArray.from_wkb
   GeosArray.from_wkt
   GeosArray.to_shapely
   GeosArray.to_wkb
   GeosArray.to_wkt

ExtensionArray Specific
-----------------------
Necessary methods for the :class:`~pandas.api.extensions.ExtensionArray`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosArray._from_sequence
   GeosArray._values_for_factorize
   GeosArray._from_factorized
   GeosArray.__getitem__
   GeosArray.__setitem__
   GeosArray.__len__
   GeosArray.__eq__
   GeosArray.dtype
   GeosArray.nbytes
   GeosArray.isna
   GeosArray.take
   GeosArray.copy
   GeosArray._concat_same_type
   GeosArray._values_for_argsort


NumPy Specific
--------------
Methods to make the GeosArray a
`NumPy Array Container <https://numpy.org/doc/stable/user/basics.dispatch.html#writing-custom-array-containers>`_.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosArray.size
   GeosArray.shape
   GeosArray.__array__

Custom
------
Custom methods to add more functionality.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosArray.affine
   GeosArray.__add__
   GeosArray.__sub__
   GeosArray.__mul__
   GeosArray.__truediv__
   GeosArray.__floordiv__


.. include:: /links.rst
