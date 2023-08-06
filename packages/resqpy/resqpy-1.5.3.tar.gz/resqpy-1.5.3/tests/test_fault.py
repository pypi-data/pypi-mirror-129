import os

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

import resqpy.fault as rqf
import resqpy.grid as grr
import resqpy.model as rq
import resqpy.olio.xml_et as rqet
import resqpy.property as rqp


# yapf: disable
@pytest.mark.parametrize('inc_list,tmult_dict,expected_mult',
   [(['fault_1.inc'], {}, {'fault_1': 1}),
    (['fault_1.inc'], {'fault_1': 2}, {'fault_1': 2}),
    (['fault_1.inc', 'fault_2.inc'], {'fault_1': 2}, {'fault_1': 2, 'fault_2': 2})])
# yapf: enable
def test_add_connection_set_and_tmults(example_model_with_properties, test_data_path, inc_list, tmult_dict,
                                       expected_mult):
    model = example_model_with_properties

    inc_list = [os.path.join(test_data_path, inc) for inc in inc_list]

    gcs_uuid = rqf.add_connection_set_and_tmults(model, inc_list, tmult_dict)

    assert gcs_uuid is not None, 'Grid connection set not generated'

    reload_model = rq.Model(epc_file = model.epc_file)

    faults = reload_model.parts_list_of_type(('obj_FaultInterpretation'))
    assert len(faults) == len(
        expected_mult.keys()), f'Expected a {len(expected_mult.keys())} faults, found {len(faults)}'
    for fault in faults:
        metadata = rqet.load_metadata_from_xml(reload_model.root_for_part(fault))
        title = reload_model.citation_title_for_part(fault)
        assert metadata["Transmissibility multiplier"] == str(
            float(expected_mult[title])
        ), f'Expected mult for fault {title} to be {float(expected_mult[title])}, found {metadata["Transmissibility multiplier"]}'

    # check that a transmissibility multiplier property has been created
    gcs = rqf.GridConnectionSet(reload_model, uuid = gcs_uuid, find_properties = True)
    assert gcs is not None
    pc = gcs.property_collection
    assert pc is not None and pc.number_of_parts() > 0
    part = pc.singleton(property_kind = 'transmissibility multiplier')
    assert part is not None
    # check property values are in expected set
    a = pc.cached_part_array_ref(part)
    assert a is not None and a.ndim == 1
    expect = [x for x in expected_mult.values()]
    assert all([v in expect for v in a])
    # see if a local property kind has been set up correctly
    pku = pc.local_property_kind_uuid(part)
    assert pku is not None
    pk = rqp.PropertyKind(reload_model, uuid = pku)
    assert pk is not None
    assert pk.title == 'transmissibility multiplier'


def test_gcs_property_inheritance(tmp_path):

    epc = os.path.join(tmp_path)

    model = rq.Model(epc, new_epc = True, create_basics = True, create_hdf5_ext = True)

    # create a grid
    g = grr.RegularGrid(model, (5, 3, 3), dxyz = (10.0, 10.0, 1.0))
    g.write_hdf5()
    g.create_xml(title = 'unsplit grid')

    # define an L shaped (in plan view) fault
    j_faces = np.zeros((g.nk, g.nj - 1, g.ni), dtype = bool)
    j_faces[:, 0, 1:] = True
    i_faces = np.zeros((g.nk, g.nj, g.ni - 1), dtype = bool)
    i_faces[:, 1:, 0] = True
    gcs = rqf.GridConnectionSet(model,
                                grid = g,
                                j_faces = j_faces,
                                i_faces = i_faces,
                                feature_name = 'L fault',
                                create_organizing_objects_where_needed = True,
                                create_transmissibility_multiplier_property = False)
    # check that connection set has the right number of cell face pairs
    assert gcs.count == g.nk * ((g.nj - 1) + (g.ni - 1))

    # create a transmissibility multiplier property
    tm = np.arange(gcs.count).astype(float)
    if gcs.property_collection is None:
        gcs.property_collection = rqp.PropertyCollection()
        gcs.property_collection.set_support(support = gcs)
    pc = gcs.property_collection
    pc.add_cached_array_to_imported_list(
        tm,
        'unit test',
        'TMULT',
        uom = 'Euc',  # actually a ratio of transmissibilities
        property_kind = 'transmissibility multiplier',
        local_property_kind_uuid = None,
        realization = None,
        indexable_element = 'faces')
    # write gcs which should also write property collection and create a local property kind
    gcs.write_hdf5()
    gcs.create_xml(write_new_properties = True)

    # check that a local property kind has materialised
    pk_uuid = model.uuid(obj_type = 'PropertyKind', title = 'transmissibility multiplier')
    assert pk_uuid is not None

    # create a derived grid connection set using a layer range
    thin_gcs, thin_indices = gcs.filtered_by_layer_range(min_k0 = 1, max_k0 = 3, return_indices = True)
    assert thin_gcs is not None and thin_indices is not None
    assert thin_gcs.count == 3 * ((g.nj - 1) + (g.ni - 1))
    # inherit the transmissibility multiplier property
    thin_gcs.inherit_properties_for_selected_indices(gcs, thin_indices)
    thin_gcs.write_hdf5()
    thin_gcs.create_xml()  # by default will include write of new properties

    # check that the inheritance has worked
    assert thin_gcs.property_collection is not None and thin_gcs.property_collection.number_of_parts() > 0
    thin_pc = thin_gcs.property_collection
    tm_part = thin_pc.singleton(property_kind = 'transmissibility multiplier')
    assert tm_part is not None
    thin_tm = thin_pc.cached_part_array_ref(tm_part)
    assert thin_tm is not None and thin_tm.ndim == 1
    assert thin_tm.size == thin_gcs.count
    assert_array_almost_equal(thin_tm, tm[thin_indices])

    # check that get_combined...() method can execute using property collection
    b_a, i_a, f_a = gcs.get_combined_fault_mask_index_value_arrays(min_k = 1,
                                                                   max_k = 3,
                                                                   property_name = 'Transmissibility multiplier',
                                                                   ref_k = 2)
    assert b_a is not None and i_a is not None and f_a is not None
    # check that transmissibility multiplier values have been sampled correctly from property array
    assert f_a.shape == (g.nj, g.ni, 2, 2)
    assert np.count_nonzero(np.isnan(f_a)) == 4 * g.nj * g.ni - 2 * ((g.nj - 1) + (g.ni - 1))
    assert np.nanmax(f_a) > np.nanmin(f_a)
    restore = np.seterr(all = 'ignore')
    assert np.all(np.logical_or(np.isnan(f_a), f_a >= np.nanmin(thin_tm)))
    assert np.all(np.logical_or(np.isnan(f_a), f_a <= np.nanmax(thin_tm)))
    np.seterr(**restore)


# no longer a failure mode
# def test_add_connection_set_and_tmults_fails(example_model_with_properties, test_data_path, include = 'fault_3.inc'):
#   model = example_model_with_properties
#   inc_list = [os.path.join(test_data_path, include)]
#   with pytest.raises(NotImplementedError):
#      rqf.add_connection_set_and_tmults(model, inc_list)
