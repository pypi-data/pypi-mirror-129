Geos Series Accessor
====================

.. currentmodule:: pgpd

.. autoclass:: GeosSeriesAccessor


Serialization
-------------
Serialization & Deserialization functionality.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosSeriesAccessor.to_geos
   GeosSeriesAccessor.to_geopandas
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

   GeosSeriesAccessor.get_coordinate_dimension
   GeosSeriesAccessor.get_dimensions
   GeosSeriesAccessor.get_exterior_ring
   GeosSeriesAccessor.get_geometry
   GeosSeriesAccessor.get_interior_ring
   GeosSeriesAccessor.get_num_coordinates
   GeosSeriesAccessor.get_num_geometries
   GeosSeriesAccessor.get_num_interior_rings
   GeosSeriesAccessor.get_num_points
   GeosSeriesAccessor.get_parts
   GeosSeriesAccessor.get_point
   GeosSeriesAccessor.get_precision
   GeosSeriesAccessor.get_rings
   GeosSeriesAccessor.get_srid
   GeosSeriesAccessor.get_type_id
   GeosSeriesAccessor.get_x
   GeosSeriesAccessor.get_y
   GeosSeriesAccessor.get_z
   GeosSeriesAccessor.force_2d
   GeosSeriesAccessor.force_3d
   GeosSeriesAccessor.set_precision
   GeosSeriesAccessor.set_srid


Geometry Creation
-----------------
Methods from :doc:`PyGEOS Geometry Creation <pygeos:creation>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosSeriesAccessor.destroy_prepared
   GeosSeriesAccessor.prepare


Measurement
-----------
Methods from :doc:`PyGEOS Measurement <pygeos:measurement>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.area
    GeosSeriesAccessor.bounds
    GeosSeriesAccessor.distance
    GeosSeriesAccessor.frechet_distance
    GeosSeriesAccessor.hausdorff_distance
    GeosSeriesAccessor.length
    GeosSeriesAccessor.minimum_bounding_radius
    GeosSeriesAccessor.minimum_clearance
    GeosSeriesAccessor.total_bounds


Predicates
----------
Methods from :doc:`PyGEOS Predicates <pygeos:predicates>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.contains
    GeosSeriesAccessor.contains_properly
    GeosSeriesAccessor.covered_by
    GeosSeriesAccessor.covers
    GeosSeriesAccessor.crosses
    GeosSeriesAccessor.disjoint
    GeosSeriesAccessor.equals
    GeosSeriesAccessor.equals_exact
    GeosSeriesAccessor.has_z
    GeosSeriesAccessor.intersects
    GeosSeriesAccessor.is_ccw
    GeosSeriesAccessor.is_closed
    GeosSeriesAccessor.is_empty
    GeosSeriesAccessor.is_geometry
    GeosSeriesAccessor.is_missing
    GeosSeriesAccessor.is_prepared
    GeosSeriesAccessor.is_ring
    GeosSeriesAccessor.is_simple
    GeosSeriesAccessor.is_valid
    GeosSeriesAccessor.is_valid_input
    GeosSeriesAccessor.is_valid_reason
    GeosSeriesAccessor.overlaps
    GeosSeriesAccessor.relate
    GeosSeriesAccessor.relate_pattern
    GeosSeriesAccessor.touches
    GeosSeriesAccessor.within


Set Operations
--------------
Methods from :doc:`PyGEOS Set Operations <pygeos:set_operations>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.coverage_union
    GeosSeriesAccessor.coverage_union_all
    GeosSeriesAccessor.difference
    GeosSeriesAccessor.intersection
    GeosSeriesAccessor.intersection_all
    GeosSeriesAccessor.symmetric_difference
    GeosSeriesAccessor.symmetric_difference_all
    GeosSeriesAccessor.union
    GeosSeriesAccessor.union_all


Constructive Operations
------------------------
Methods from :doc:`PyGEOS Constructive Operations <pygeos:constructive>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.boundary
    GeosSeriesAccessor.buffer
    GeosSeriesAccessor.build_area
    GeosSeriesAccessor.centroid
    GeosSeriesAccessor.clip_by_rect
    GeosSeriesAccessor.convex_hull
    GeosSeriesAccessor.delaunay_triangles
    GeosSeriesAccessor.envelope
    GeosSeriesAccessor.extract_unique_points
    GeosSeriesAccessor.make_valid
    GeosSeriesAccessor.minimum_bounding_circle
    GeosSeriesAccessor.minimum_rotated_rectangle
    GeosSeriesAccessor.normalize
    GeosSeriesAccessor.offset_curve
    GeosSeriesAccessor.oriented_envelope
    GeosSeriesAccessor.point_on_surface
    GeosSeriesAccessor.polygonize
    GeosSeriesAccessor.reverse
    GeosSeriesAccessor.segmentize
    GeosSeriesAccessor.simplify
    GeosSeriesAccessor.snap
    GeosSeriesAccessor.voronoi_polygons


Linestring Operations
---------------------
Methods from :doc:`PyGEOS Linestring Operations <pygeos:linear>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.line_interpolate_point
    GeosSeriesAccessor.line_locate_point
    GeosSeriesAccessor.line_merge
    GeosSeriesAccessor.shared_paths
    GeosSeriesAccessor.shortest_line


Coordinate Operations
---------------------
Methods from :doc:`PyGEOS Coordinate Operations <pygeos:coordinates>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.apply
    GeosSeriesAccessor.count_coordinates
    GeosSeriesAccessor.get_coordinates
    GeosSeriesAccessor.set_coordinates


STRTree
-------
Methods from :doc:`PyGEOS STRTree <pygeos:strtree>`.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

    GeosSeriesAccessor.STRtree


Custom
------
Custom methods to add more functionality.

.. autosummary::
   :toctree: generated
   :nosignatures:
   :template: base.rst

   GeosSeriesAccessor.affine
   GeosSeriesAccessor.rotate
   GeosSeriesAccessor.scale
   GeosSeriesAccessor.skew
   GeosSeriesAccessor.translate
   GeosSeriesAccessor.apply_shapely


.. include:: /links.rst
