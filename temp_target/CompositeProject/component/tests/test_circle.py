import pytest
from component.abstract.graphic import Graphic
from component.components.leafs.circle import Circle
from component.components.composite.group import Group
from component.components.leafs.abstract.leaf import Leaf


# Methods being tested:
# is_composite, is_leaf, get_children, get_parents, any_active, id

def test_basic_identification_and_structure():
    Group.validation_settings.update({
        'all_groups_use_deny_policy': False,
        'max_one_parent': False
    })
    circle = Circle(name="Circle1", size=3)
    group = Group(name="Group1", duplicate_policy=Group.DuplicatePolicy.ALLOW_MULTIPLE_PARENTS)
    
    # Test is_composite and is_leaf
    assert not circle.is_composite()
    assert circle.is_leaf()
    
    assert group.is_composite()
    assert not group.is_leaf()

    # Test get_children and get_parents
    group.add(circle)
    assert group.get_children() == [circle]
    assert circle.get_children() == []
    assert group.get_parents() == []
    assert circle.get_parents() == [group]

    group.remove(circle)
    assert group.get_children() == []
    assert circle.get_parents() == []

    # Test any_active
    inactive_circle = Circle(name="InactiveCircle", size=3, is_active=False)
    active_circle = Circle(name="ActiveCircle", size=3, is_active=True)
    group.add(active_circle)

    assert not inactive_circle.any_active()
    assert active_circle.any_active()  
    assert group.any_active()

    # Test id
    assert circle.id == 1
    assert group.id == 2
    assert inactive_circle.id == 3
    assert active_circle.id == 4


# Methods being tested:
# get_components_recursively, remove_components_recursively, execute_operation_recursively, calculate_depth

def test_recursive_operations():
    Group.validation_settings.update({
        'all_groups_use_deny_policy': False,
        'max_one_parent': False
    })

    # Set up objects
    circle1 = Circle(name="Circle1", size=3)
    circle2 = Circle(name="Circle2", size=3)
    parent_group = Group(name="ParentGroup")
    child_group = Group(name="ChildGroup")

    # Test get_components_recursively
    child_group.add(circle1)
    child_group.add(circle2)
    parent_group.add(child_group)

    components = parent_group.get_components_recursively()
    assert components == [parent_group, child_group, circle1, circle2]
    assert child_group.get_components_recursively() == [child_group, circle1, circle2]
    assert circle1.get_components_recursively() == [circle1]
    groups = parent_group.get_components_recursively(
        condition_func=isinstance,
        condition_args=(Group,)
    )
    assert parent_group in groups
    assert child_group in groups

    # Test remove_components_recursively
    # condition_func evaluates to True
    removed_components = parent_group.remove_components_recursively(
        condition_func=isinstance,
        condition_args=(Graphic,)
    )
    assert parent_group not in removed_components
    assert child_group in removed_components
    assert circle1 in removed_components
    assert circle2 in removed_components
    assert parent_group.get_components_recursively() == [parent_group]

    removed_components = circle1.remove_components_recursively(
        condition_func=isinstance,
        condition_args=(Circle,)
    )
    assert removed_components == []

    # condition_func evaluates to False
    child_group.add(circle1)
    child_group.add(circle2)
    parent_group.add(child_group)

    def always_false(_):
        return False

    removed_components = parent_group.remove_components_recursively(
        condition_func=always_false
    )
    assert removed_components == []
    assert len(parent_group.get_components_recursively()) == 4

    # Test execute_operation_recursively
    def append_to_name(graphic, suffix):
        graphic.name += suffix

    results = parent_group.execute_operation_recursively(
        operation_func=append_to_name,
        operation_args=("_processed",),
        condition_func=isinstance,
        condition_args=(Graphic,)
    )
    assert parent_group.name == "ParentGroup_processed"
    assert child_group.name == "ChildGroup_processed"
    assert circle1.name == "Circle1_processed"
    assert circle2.name == "Circle2_processed"

    assert results == [None, None, None, None]

    def get_name(graphic, suffix):
        return graphic.name + suffix
    
    results = parent_group.execute_operation_recursively(
        operation_func=get_name,
        operation_args=("_processed",),
        condition_func=isinstance,
        condition_args=(Circle,)
    )

    assert len(results) == 2
    assert "Circle1_processed_processed" in results
    assert "Circle2_processed_processed" in results

    # Test calculate_depth
    assert parent_group.calculate_depth() == 3
    assert child_group.calculate_depth() == 2
    assert circle1.calculate_depth() == 1

# Methods being tested:
# add, remove, validate_structure (with duplicate policies)

def test_structure_manipulation_with_duplicate_policies():
    # Set up objects
    circle1 = Circle(name="Circle1", size=3)
    circle2 = Circle(name="Circle2", size=3)
    group1 = Group(name="Group1")
    group2 = Group(name="Group2")

    # Test add with the default policy (DENY_MULTIPLE_PARENTS)
    group1.add(circle1)
    assert group1.get_children() == [circle1]

    # Attempt to add circle1 to another group should raise an error due to the default policy
    with pytest.raises(ValueError):
        group2.add(circle1)  # This should raise a ValueError since multiple parents are denied

    # Attempt to add circle1 to the same group should raise an error due to the default policy
    with pytest.raises(ValueError):
        group1.add(circle1)  # This should raise a ValueError since multiple parents are denied

    # Test remove
    group1.remove(circle1)
    assert group1.get_children() == []
    assert circle1.get_parents() == []

    # Test add with ALLOW_MULTIPLE_PARENTS policy
    group2.remove_components_recursively()

    group1.add(circle1)
    group2.duplicate_policy = Group.DuplicatePolicy.ALLOW_MULTIPLE_PARENTS

    with pytest.raises(ValueError):
        group2.add(circle1)
    
    
    assert group1.get_children() == [circle1]
    assert group2.get_children() == []
    assert circle1.get_parents() == [group1]



    # Test add with ALLOW_NEW_PARENT_IF policy
    group1.remove_components_recursively()
    group2.remove_components_recursively()

    def parent_with_max_one_child_and_circle_component(parent, component):
        # Check if the parent does not have more than one child
        max_one_child = len(parent.get_children()) < 1
        # Check if the component is a Circle
        is_circle = isinstance(component, Circle)
        return max_one_child and is_circle

    group1.duplicate_policy = Group.DuplicatePolicy.ALLOW_NEW_PARENT_IF
    group1.condition_func = parent_with_max_one_child_and_circle_component

    with pytest.raises(ValueError):
        group1.add(group2)

    group1.add(circle1)

    with pytest.raises(ValueError):
        group1.add(circle2)

    assert group1.get_children() == [circle1]
    assert group2.get_children() == []
    assert group2.get_parents() == []
    assert circle1.get_parents() == [group1]
    assert circle2.get_parents() == []

    # Test validate_structure
    group1.remove_components_recursively()
    group2.remove_components_recursively()

    group1.duplicate_policy = Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS
    group2.duplicate_policy = Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS

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
    group2.validate_structure()
    
    group2.add(group1)
    with pytest.raises(ValueError):
        group1.add(group2)

    group2.add(circle1)
    with pytest.raises(ValueError):
        group1.add(circle1)
    group2.add(circle2)

    circle1.validate_structure()
    circle1._parents.append(group1)
    with pytest.raises(ValueError):
        circle1.validate_structure()


# Methods being tested:
# export_to_pickle, import_from_pickle

def test_serialization_deserialization():
    import os
    # Set up objects
    circle = Circle(name="Circle1", size=3)
    group = Group(name="Group1")
    
    # Add circle to the group
    group.add(circle)
    
    # Define file paths
    group_file = "test_group.pkl"
    circle_file = "test_circle.pkl"

    try:
        # Test export_to_pickle
        group.export_to_pickle(group_file)
        circle.export_to_pickle(circle_file)

        # Test import_from_pickle for group
        loaded_group = Group.import_from_pickle(group_file)
        assert loaded_group.get_structure_as_dict() == group.get_structure_as_dict()
        loaded_group.validate_structure()

        # Test import_from_pickle for circle
        loaded_circle = Circle.import_from_pickle(circle_file)
        assert loaded_circle.id != circle.id
        assert loaded_circle.name == circle.name
        assert loaded_circle.size == circle.size
        loaded_circle.validate_structure()

    finally:
        # Clean up: delete the files after the test
        if os.path.exists(group_file):
            os.remove(group_file)
        if os.path.exists(circle_file):
            os.remove(circle_file)

# Methods being tested:
# clone

def test_cloning():
    # Set up objects
    circle = Circle(name="Circle1", size=3)
    group = Group(name="Group1")

    # Add circle to the group
    group.add(circle)

    # Test cloning of group
    cloned_group = group.clone()
    assert cloned_group != group  # Ensure they are different objects
    assert cloned_group.get_structure_as_dict() == group.get_structure_as_dict()

    # Test that changes to the cloned group do not affect the original group
    cloned_group.remove(cloned_group.get_children()[0])
    assert cloned_group.get_children() == []
    assert group.get_children() == [circle]

    # Test cloning of Circle (leaf)
    cloned_circle = circle.clone()
    assert cloned_circle.name == circle.name
    assert cloned_circle.size == circle.size
    assert cloned_circle.id != circle.id  # Clone should have a different ID
