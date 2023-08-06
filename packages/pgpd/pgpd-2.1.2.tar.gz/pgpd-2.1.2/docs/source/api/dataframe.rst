Geos DataFrame Accessor
=======================

.. currentmodule:: pgpd

.. autoclass:: GeosDataFrameAccessor


Serialization
-------------
Serialization & Deserialization functionality.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosDataFrameAccessor.to_geos
   GeosDataFrameAccessor.to_geopandas
   GeosSeriesAccessor.to_shapely
   GeosSeriesAccessor.to_wkt
   GeosSeriesAccessor.to_wkb

Geometry
--------
Methods from :doc:`PyGEOS Geometry <pygeos:geometry>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosDataFrameAccessor.get_coordinate_dimension
   GeosDataFrameAccessor.get_dimensions
   GeosDataFrameAccessor.get_exterior_ring
   GeosDataFrameAccessor.get_geometry
   GeosDataFrameAccessor.get_interior_ring
   GeosDataFrameAccessor.get_num_coordinates
   GeosDataFrameAccessor.get_num_geometries
   GeosDataFrameAccessor.get_num_interior_rings
   GeosDataFrameAccessor.get_num_points
   GeosDataFrameAccessor.get_point
   GeosDataFrameAccessor.get_precision
   GeosDataFrameAccessor.get_srid
   GeosDataFrameAccessor.get_type_id
   GeosDataFrameAccessor.get_x
   GeosDataFrameAccessor.get_y
   GeosDataFrameAccessor.get_z
   GeosDataFrameAccessor.force_2d
   GeosDataFrameAccessor.force_3d
   GeosDataFrameAccessor.set_precision
   GeosDataFrameAccessor.set_srid


Geometry Creation
-----------------
Methods from :doc:`PyGEOS Geometry Creation <pygeos:creation>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosDataFrameAccessor.destroy_prepared
   GeosDataFrameAccessor.prepare


Measurement
-----------
Methods from :doc:`PyGEOS Measurement <pygeos:measurement>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosDataFrameAccessor.area
    GeosDataFrameAccessor.length
    GeosDataFrameAccessor.minimum_bounding_radius
    GeosDataFrameAccessor.minimum_clearance
    GeosDataFrameAccessor.total_bounds


Predicates
----------
Methods from :doc:`PyGEOS Predicates <pygeos:predicates>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosDataFrameAccessor.has_z
    GeosDataFrameAccessor.is_ccw
    GeosDataFrameAccessor.is_closed
    GeosDataFrameAccessor.is_empty
    GeosDataFrameAccessor.is_geometry
    GeosDataFrameAccessor.is_missing
    GeosDataFrameAccessor.is_prepared
    GeosDataFrameAccessor.is_ring
    GeosDataFrameAccessor.is_simple
    GeosDataFrameAccessor.is_valid
    GeosDataFrameAccessor.is_valid_input
    GeosDataFrameAccessor.is_valid_reason


Constructive Operations
------------------------
Methods from :doc:`PyGEOS Constructive Operations <pygeos:constructive>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosDataFrameAccessor.boundary
    GeosDataFrameAccessor.buffer
    GeosDataFrameAccessor.centroid
    GeosDataFrameAccessor.clip_by_rect
    GeosDataFrameAccessor.convex_hull
    GeosDataFrameAccessor.delaunay_triangles
    GeosDataFrameAccessor.envelope
    GeosDataFrameAccessor.extract_unique_points
    GeosDataFrameAccessor.make_valid
    GeosDataFrameAccessor.minimum_bounding_circle
    GeosDataFrameAccessor.minimum_rotated_rectangle
    GeosDataFrameAccessor.normalize
    GeosDataFrameAccessor.offset_curve
    GeosDataFrameAccessor.oriented_envelope
    GeosDataFrameAccessor.point_on_surface
    GeosDataFrameAccessor.reverse
    GeosDataFrameAccessor.simplify
    GeosDataFrameAccessor.snap
    GeosDataFrameAccessor.voronoi_polygons


Linestring Operations
---------------------
Methods from :doc:`PyGEOS Linestring Operations <pygeos:linear>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosDataFrameAccessor.line_interpolate_point
    GeosDataFrameAccessor.line_locate_point
    GeosDataFrameAccessor.line_merge


Coordinate Operations
---------------------
Methods from :doc:`PyGEOS Coordinate Operations <pygeos:coordinates>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosDataFrameAccessor.apply
    GeosDataFrameAccessor.count_coordinates
    GeosDataFrameAccessor.set_coordinates


Custom
------
Custom methods to add more functionality.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosDataFrameAccessor.affine
   GeosDataFrameAccessor.rotate
   GeosDataFrameAccessor.scale
   GeosDataFrameAccessor.skew
   GeosDataFrameAccessor.translate
   GeosDataFrameAccessor.apply_shapely


.. include:: /links.rst
