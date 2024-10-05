import pytest
from graphic.abstract.graphic import Graphic
from graphic.components.leaves.abstract.leaf import Leaf

from graphic.components.leaves.circle import Circle

from graphic.components.leaves.square import Square

from graphic.components.composite.group import Group

@pytest.fixture(autouse=True)
def reset_id_counter():
    Graphic._id_counter = 0

# Methods being tested:
# is_composite, is_leaf, get_children, get_parents, size, is_active

def test_basic_identification_and_structure():
    Group.validation_settings.update({
        'all_groups_use_deny_policy': False,
        'max_one_parent': False
    })
    square = Square(name="Square1", size=3, is_active=True)
    composite = Group(name="Group1", duplicate_policy=Group.DuplicatePolicy.ALLOW_MULTIPLE_PARENTS)
    
    # Test is_composite and is_leaf
    assert not square.is_composite()
    assert square.is_leaf()
    
    assert composite.is_composite()
    assert not composite.is_leaf()

    # Test get_children and get_parents
    composite.add(square)
    assert composite.get_children() == [square]
    assert square.get_children() == []
    assert composite.get_parents() == []
    assert square.get_parents() == [composite]

    composite.remove(square)
    assert composite.get_children() == []
    assert square.get_parents() == []

    # Test properties
    
    assert square.size == 3
    
    assert square.is_active == True
    

# Methods being tested:
# get_components_recursively, remove_components_recursively, execute_operation_recursively, calculate_depth

def test_recursive_operations():
    Group.validation_settings.update({
        'all_groups_use_deny_policy': False,
        'max_one_parent': False
    })

    # Set up objects
    
    square1 = Square(name="Square1", size=3, is_active=True)
    
    square2 = Square(name="Square2", size=3, is_active=True)
    
    parent_composite = Group(name="ParentGroup")
    child_composite = Group(name="ChildGroup")

    # Test get_components_recursively
    child_composite.add(square1)
    child_composite.add(square2)
    parent_composite.add(child_composite)

    components = parent_composite.get_components_recursively()
    assert components == [parent_composite, child_composite, square1, square2]
    assert child_composite.get_components_recursively() == [child_composite, square1, square2]
    assert square1.get_components_recursively() == [square1]
    composites = parent_composite.get_components_recursively(
        condition_func=isinstance,
        condition_args=(Group,)
    )
    assert parent_composite in composites
    assert child_composite in composites

    # Test remove_components_recursively
    # condition_func evaluates to True
    removed_components = parent_composite.remove_components_recursively(
        condition_func=isinstance,
        condition_args=(Graphic,)
    )
    assert parent_composite not in removed_components
    assert child_composite in removed_components
    assert square1 in removed_components
    assert square2 in removed_components
    assert parent_composite.get_components_recursively() == [parent_composite]

    removed_components = square1.remove_components_recursively(
        condition_func=isinstance,
        condition_args=(Square,)
    )
    assert removed_components == []

    # condition_func evaluates to False
    child_composite.add(square1)
    child_composite.add(square2)
    parent_composite.add(child_composite)

    def always_false(_):
        return False

    removed_components = parent_composite.remove_components_recursively(
        condition_func=always_false
    )
    assert removed_components == []
    assert len(parent_composite.get_components_recursively()) == 4

    # Test execute_operation_recursively
    def append_to_name(component, suffix):
        component.name += suffix

    results = parent_composite.execute_operation_recursively(
        operation_func=append_to_name,
        operation_args=("_processed",),
        condition_func=isinstance,
        condition_args=(Graphic,)
    )
    assert parent_composite.name == "ParentGroup_processed"
    assert child_composite.name == "ChildGroup_processed"
    assert square1.name == "Square1_processed"
    assert square2.name == "Square2_processed"

    assert results == [None, None, None, None]

    def get_name(component, suffix):
        return component.name + suffix

    results = parent_composite.execute_operation_recursively(
        operation_func=get_name,
        operation_args=("_processed",),
        condition_func=isinstance,
        condition_args=(Square,)
    )

    assert len(results) == 2
    assert "Square1_processed_processed" in results
    assert "Square2_processed_processed" in results

    # Test calculate_depth
    assert parent_composite.calculate_depth() == 3
    assert child_composite.calculate_depth() == 2
    assert square1.calculate_depth() == 1

# Methods being tested:
# add, remove, validate_structure (with duplicate policies)

def test_structure_manipulation_with_duplicate_policies():
    # Set up objects
    square1 = Square(name="Square1", size=3, is_active=True)
    square2 = Square(name="Square2", size=3, is_active=True)
    composite1 = Group(name="Group1")
    composite2 = Group(name="Group2")

    # Test add with the default policy (DENY_MULTIPLE_PARENTS)
    composite1.add(square1)
    assert composite1.get_children() == [square1]

    # Attempt to add leaf1 to another composite should raise an error due to the default policy
    with pytest.raises(ValueError):
        composite2.add(square1)  # This should raise a ValueError since multiple parents are denied

    # Attempt to add leaf1 to the same composite should raise an error due to the default policy
    with pytest.raises(ValueError):
        composite1.add(square1)  # This should raise a ValueError since multiple parents are denied

    # Test remove
    composite1.remove(square1)
    assert composite1.get_children() == []
    assert square1.get_parents() == []

    # Test add with ALLOW_MULTIPLE_PARENTS policy
    composite2.remove_components_recursively()

    composite1.add(square1)
    composite2.duplicate_policy = Group.DuplicatePolicy.ALLOW_MULTIPLE_PARENTS

    with pytest.raises(ValueError):
        composite2.add(square1)
    
    assert composite1.get_children() == [square1]
    assert composite2.get_children() == []
    assert square1.get_parents() == [composite1]

    # Test add with ALLOW_NEW_PARENT_IF policy
    composite1.remove_components_recursively()
    composite2.remove_components_recursively()

    def parent_with_max_one_child_and_specific_component(parent, component):
        # Check if the parent does not have more than one child
        max_one_child = len(parent.get_children()) < 1
        # Check if the component is a specific leaf
        is_specific_leaf = isinstance(component, Square)
        return max_one_child and is_specific_leaf

    composite1.duplicate_policy = Group.DuplicatePolicy.ALLOW_NEW_PARENT_IF
    composite1.condition_func = parent_with_max_one_child_and_specific_component

    with pytest.raises(ValueError):
        composite1.add(composite2)

    composite1.add(square1)

    with pytest.raises(ValueError):
        composite1.add(square2)

    assert composite1.get_children() == [square1]
    assert composite2.get_children() == []
    assert composite2.get_parents() == []
    assert square1.get_parents() == [composite1]
    assert square2.get_parents() == []

    # Test validate_structure
    composite1.remove_components_recursively()
    composite2.remove_components_recursively()

    composite1.duplicate_policy = Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS
    composite2.duplicate_policy = Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS

    Group.validation_settings.update({
        'no_circular_references': True,
        'no_parent_duplication_conflict': True,
        'parent_child_relationships_are_consistent': True,
        'only_graphic_objects_in_groups': True,
        'all_parents_are_groups': True,
        'leaf_has_no_children': True,
        'components_are_unique': True,
        'ids_are_unique': True,
        'names_are_unique': True,
        'all_groups_use_deny_policy': True,
        'max_one_parent': True,
        'condition_func_in_all_conditional_groups': True
    })
    composite2.validate_structure()
    
    composite2.add(composite1)
    with pytest.raises(ValueError):
        composite1.add(composite2)

    composite2.add(square1)
    with pytest.raises(ValueError):
        composite1.add(square1)
    composite2.add(square2)

    square1.validate_structure()
    square1.get_parents().append(composite1)
    with pytest.raises(ValueError):
        square1.validate_structure()

# Methods being tested:
# export_to_pickle, import_from_pickle

def test_serialization_deserialization():
    import os
    # Set up objects
    square = Square(name="Square1", size=3, is_active=True)
    composite = Group(name="Group1")
    
    # Add leaf to the composite
    composite.add(square)
    
    # Define file paths
    composite_file = "test_group.pkl"
    leaf_file = "test_square.pkl"

    try:
        # Test export_to_pickle
        composite.export_to_pickle(composite_file)
        square.export_to_pickle(leaf_file)

        # Test import_from_pickle for composite
        loaded_composite = Group.import_from_pickle(composite_file)
        assert loaded_composite.get_structure_as_dict() == composite.get_structure_as_dict()
        loaded_composite.validate_structure()

        # Test import_from_pickle for leaf
        loaded_leaf = Square.import_from_pickle(leaf_file)
        assert loaded_leaf.id != square.id
        assert loaded_leaf.name == square.name
        
        assert loaded_leaf.size == square.size
        
        assert loaded_leaf.is_active == square.is_active
        
        loaded_leaf.validate_structure()

    finally:
        # Clean up: delete the files after the test
        if os.path.exists(composite_file):
            os.remove(composite_file)
        if os.path.exists(leaf_file):
            os.remove(leaf_file)

# Methods being tested:
# clone

def test_cloning():
    # Set up objects
    square = Square(name="Square1", size=3, is_active=True)
    composite = Group(name="Group1")

    # Add leaf to the composite
    composite.add(square)

    # Test cloning of composite
    cloned_composite = composite.clone()
    assert cloned_composite != composite  # Ensure they are different objects
    assert cloned_composite.get_structure_as_dict() == composite.get_structure_as_dict()

    # Test that changes to the cloned composite do not affect the original composite
    cloned_composite.remove(cloned_composite.get_children()[0])
    assert cloned_composite.get_children() == []
    assert composite.get_children() == [square]

    # Test cloning of Leaf
    cloned_leaf = square.clone()
    assert cloned_leaf.name == square.name
    
    assert cloned_leaf.size == square.size
    
    assert cloned_leaf.is_active == square.is_active
    
    assert cloned_leaf.id != square.id  # Clone should have a different ID