import os

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

import resqpy.lines
import resqpy.model as rq
import resqpy.organize


def test_lines(example_model_and_crs):

    # Set up a Polyline
    title = 'Nazca'
    model, crs = example_model_and_crs
    line = resqpy.lines.Polyline(parent_model = model,
                                 title = title,
                                 set_crs = crs.uuid,
                                 set_crsroot = crs.root,
                                 set_bool = True,
                                 set_coord = np.array([[0, 0, 0], [1, 1, 1]]))
    line.write_hdf5()
    line.create_xml()

    # Add a interpretation
    assert line.rep_int_root is None
    line.create_interpretation_and_feature(kind = 'fault')
    assert line.rep_int_root is not None

    # Check fault can be loaded in again
    model.store_epc()
    model = rq.Model(epc_file = model.epc_file)
    reload = resqpy.lines.Polyline(parent_model = model, uuid = line.uuid)
    assert reload.citation_title == title

    fault_interp = resqpy.organize.FaultInterpretation(model, uuid = line.rep_int_uuid)
    fault_feature = resqpy.organize.TectonicBoundaryFeature(model, uuid = fault_interp.feature_uuid)

    # Check title matches expected title
    assert fault_feature.feature_name == title


def test_lineset(example_model_and_crs):

    # Set up a PolylineSet
    title = 'Nazcas'
    model, crs = example_model_and_crs
    line1 = resqpy.lines.Polyline(parent_model = model,
                                  title = title,
                                  set_crs = crs.uuid,
                                  set_crsroot = crs.root,
                                  set_bool = True,
                                  set_coord = np.array([[0, 0, 0], [1, 1, 1]]))

    line2 = resqpy.lines.Polyline(parent_model = model,
                                  title = title,
                                  set_crs = crs.uuid,
                                  set_crsroot = crs.root,
                                  set_bool = True,
                                  set_coord = np.array([[0, 0, 0], [2, 2, 2]]))

    lines = resqpy.lines.PolylineSet(parent_model = model, title = title, polylines = [line1, line2])

    lines.write_hdf5()
    lines.create_xml()

    # Check lines can be loaded in again
    model.store_epc()
    model = rq.Model(epc_file = model.epc_file)
    reload = resqpy.lines.PolylineSet(parent_model = model, uuid = lines.uuid)
    assert len(reload.polys) == 2, f'Expected two polylines in the polylineset, found {len(reload.polys)}'
    assert (reload.count_perpol == [2,
                                    2]).all(), f'Expected count per polyline to be [2,2], found {reload.count_perpol}'


def test_charisma(example_model_and_crs, test_data_path):
    # Set up a PolylineSet
    model, crs = example_model_and_crs
    charisma_file = test_data_path / "Charisma_example.txt"
    lines = resqpy.lines.PolylineSet(parent_model = model, charisma_file = str(charisma_file))
    lines.write_hdf5()
    lines.create_xml()

    model.store_epc()
    model = rq.Model(epc_file = model.epc_file)
    reload = resqpy.lines.PolylineSet(parent_model = model, uuid = lines.uuid)

    assert reload.title == 'Charisma_example'
    assert (reload.count_perpol == [
        4, 5, 4, 5, 5
    ]).all(), f"Expected count per polyline to be [4,5,4,5,5], found {reload.count_perpol}"
    assert len(reload.coordinates) == 23, f"Expected length of coordinates to be 23, found {len(reload.coordinates)}"


def test_irap(example_model_and_crs, test_data_path):
    # Set up a PolylineSet
    model, crs = example_model_and_crs
    irap_file = test_data_path / "IRAP_example.txt"
    lines = resqpy.lines.PolylineSet(parent_model = model, irap_file = str(irap_file))
    lines.write_hdf5()
    lines.create_xml()

    model.store_epc()
    model = rq.Model(epc_file = model.epc_file)
    reload = resqpy.lines.PolylineSet(parent_model = model, uuid = lines.uuid)

    assert reload.title == 'IRAP_example'
    assert (reload.count_perpol == [15]).all(), f"Expected count per polyline to be [15], found {reload.count_perpol}"
    assert len(reload.coordinates) == 15, f"Expected length of coordinates to be 15, found {len(reload.coordinates)}"


def test_is_clockwise(example_model_and_crs):
    # Set up a Polyline
    title = 'diamond'
    model, crs = example_model_and_crs
    line = resqpy.lines.Polyline(
        parent_model = model,
        title = title,
        set_crs = crs.uuid,
        set_bool = True,
        set_coord = np.array([
            (3.0, 2.0, 4.3),  # z values are ignored for clockwise test
            (2.0, 1.0, -13.5),
            (1.0, 2.5, 7.8),
            (2.1, 3.9, -2.0)
        ]))
    assert line is not None
    for trust in [False, True]:
        assert line.is_clockwise(trust_metadata = trust)
    # reverse the order of the coordinates
    line.coordinates = np.flip(line.coordinates, axis = 0)
    assert line.is_clockwise(trust_metadata = True)
    assert not line.is_clockwise(trust_metadata = False)  # should reset metadata
    assert not line.is_clockwise(trust_metadata = True)


def test_is_convex(example_model_and_crs):
    # Set up a Polyline
    title = 'pentagon'
    model, crs = example_model_and_crs
    line = resqpy.lines.Polyline(
        parent_model = model,
        title = title,
        set_crs = crs.uuid,
        set_bool = True,
        set_coord = np.array([
            (3.0, 2.0, 4.3),  # z values are ignored for convexity
            (2.0, 1.0, -13.5),
            (1.0, 2.5, 7.8),
            (1.5, 3.0, -2.0),
            (2.5, 3.0, 23.4)
        ]))
    assert line is not None
    for trust in [False, True]:
        assert line.is_convex(trust_metadata = trust)
    # adjust one point to make shape concave
    line.coordinates[4, 1] = 1.9
    assert line.is_convex(trust_metadata = True)
    assert not line.is_convex(trust_metadata = False)  # should reset metadata
    assert not line.is_convex(trust_metadata = True)


def test_from_scaled_polyline(example_model_and_crs):
    # Set up an original Polyline
    title = 'rectangle'
    model, crs = example_model_and_crs
    line = resqpy.lines.Polyline(parent_model = model,
                                 title = title,
                                 set_crs = crs.uuid,
                                 set_bool = True,
                                 set_coord = np.array([(0.0, 0.0, 10.0), (0.0, 3.0, 10.0), (12.0, 3.0, 10.0),
                                                       (12.0, 0.0, 10.0)]))
    assert line is not None

    # test scaling up to a larger polyline
    bigger = resqpy.lines.Polyline.from_scaled_polyline(line, 1.5, originator = 'testing')
    expected = np.array([(-3.0, -0.75, 10.0), (-3.0, 3.75, 10.0), (15.0, 3.75, 10.0), (15.0, -0.75, 10.0)])
    assert bigger.isclosed
    assert bigger.is_convex()
    assert bigger.title == 'rectangle'
    assert bigger.originator == 'testing'
    assert_array_almost_equal(bigger.coordinates, expected)

    # test scaling to a smaller polyline
    smaller = resqpy.lines.Polyline.from_scaled_polyline(line, 2.0 / 3.0, title = 'small')
    expected = np.array([(2.0, 0.5, 10.0), (2.0, 2.5, 10.0), (10.0, 2.5, 10.0), (10.0, 0.5, 10.0)])
    assert smaller.title == 'small'
    assert_array_almost_equal(smaller.coordinates, expected)
