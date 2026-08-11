from pytest import mark, param, raises
from kanbanize_sdk import Kanbanize

# Every (factory, method) pair below is a method turned off with `= private`
# in kanbanize_sdk/endpoints/. Read from the source, not inferred by analogy.
DISABLED_METHODS = [
    param('board_settings', 'list', id='board_settings.list'),
    param('board_settings', 'insert', id='board_settings.insert'),
    param('board_settings', 'delete', id='board_settings.delete'),
    param('board_structure', 'list', id='board_structure.list'),
    param('board_structure', 'insert', id='board_structure.insert'),
    param('board_structure', 'update', id='board_structure.update'),
    param('board_structure', 'delete', id='board_structure.delete'),
    param('board_structure_revisions', 'list', id='board_structure_revisions.list'),
    param('board_structure_revisions', 'insert', id='board_structure_revisions.insert'),
    param('board_structure_revisions', 'update', id='board_structure_revisions.update'),
    param('board_structure_revisions', 'delete', id='board_structure_revisions.delete'),
    param('board_history', 'get', id='board_history.get'),
    param('board_history', 'insert', id='board_history.insert'),
    param('board_history', 'update', id='board_history.update'),
    param('board_history', 'delete', id='board_history.delete'),
    param('cell_limits', 'get', id='cell_limits.get'),
    param('cell_limits', 'delete', id='cell_limits.delete'),
    param('cell_limits', 'insert', id='cell_limits.insert'),
    param('lane_section_limits', 'get', id='lane_section_limits.get'),
    param('lane_section_limits', 'delete', id='lane_section_limits.delete'),
    param('lane_section_limits', 'insert', id='lane_section_limits.insert'),
]

# Methods the same resources really offer — the disabling must not spill over.
ACTIVE_METHODS = [
    param('board_settings', 'get', id='board_settings.get'),
    param('board_settings', 'update', id='board_settings.update'),
    param('board_structure', 'get', id='board_structure.get'),
    param('board_structure_revisions', 'get_revision', id='board_structure_revisions.get_revision'),
    param('board_history', 'list', id='board_history.list'),
    param('cell_limits', 'list', id='cell_limits.list'),
    param('lane_section_limits', 'update', id='lane_section_limits.update'),
]


def resource(factory):
    return getattr(Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'}), factory)()


@mark.utils
@mark.parametrize('factory, method', DISABLED_METHODS)
def test_disabled_method_refuses_to_be_reached(factory, method):
    with raises(AttributeError):
        getattr(resource(factory), method)


@mark.utils
@mark.parametrize('factory, method', DISABLED_METHODS)
def test_disabled_method_explains_that_the_attribute_does_not_exist(factory, method):
    with raises(AttributeError) as error:
        getattr(resource(factory), method)

    assert str(error.value) == 'This attribute does not exist'


@mark.utils
@mark.parametrize('factory, method', DISABLED_METHODS)
def test_disabled_method_is_invisible_to_hasattr(factory, method):
    assert hasattr(resource(factory), method) is False


@mark.utils
@mark.parametrize('factory, method', ACTIVE_METHODS)
def test_method_the_resource_really_offers_stays_callable(factory, method):
    assert callable(getattr(resource(factory), method))
