"""Generated concrete SED2 classes for libsed2. GENERATED - do not
hand-edit; regenerate from specsheets/ via generator/generate.py."""
from __future__ import annotations

from ._runtime import (SedBase, FieldSpec, ApiError, IdKeyedCollection,
                       ListCollection, make_problem, ValidationProblem,
                       is_reference, SID_PATTERN, NAMESPACE_KEY_PATTERN)

class UnknownAbstractTask(SedBase):
    """Opaque holder for a AbstractTask instance whose _type names an
    unregistered namespace prefix (see Design.md's Namespaces section) -
    round-trips unchanged, never itself a validation error."""
    def __init__(self, type_value, raw: dict):
        super().__init__()
        self._type_value = type_value
        self._raw = dict(raw)

    def get_type(self):
        return self._type_value

    def _own_json_value(self):
        return self._raw

    def _allowed_keys(self):
        return set(self._raw.keys())

    def _validate_own(self):
        return []

    def to_json_value(self):
        d = dict(self._raw)
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        return d


class UnknownRangeInline(SedBase):
    """Opaque holder for a RangeInline instance whose _type names an
    unregistered namespace prefix (see Design.md's Namespaces section) -
    round-trips unchanged, never itself a validation error."""
    def __init__(self, type_value, raw: dict):
        super().__init__()
        self._type_value = type_value
        self._raw = dict(raw)

    def get_type(self):
        return self._type_value

    def _own_json_value(self):
        return self._raw

    def _allowed_keys(self):
        return set(self._raw.keys())

    def _validate_own(self):
        return []

    def to_json_value(self):
        d = dict(self._raw)
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        return d


class UnknownAbstractOutput(SedBase):
    """Opaque holder for a AbstractOutput instance whose _type names an
    unregistered namespace prefix (see Design.md's Namespaces section) -
    round-trips unchanged, never itself a validation error."""
    def __init__(self, type_value, raw: dict):
        super().__init__()
        self._type_value = type_value
        self._raw = dict(raw)

    def get_type(self):
        return self._type_value

    def _own_json_value(self):
        return self._raw

    def _allowed_keys(self):
        return set(self._raw.keys())

    def _validate_own(self):
        return []

    def to_json_value(self):
        d = dict(self._raw)
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        return d


class UnknownAbstractCurve(SedBase):
    """Opaque holder for a AbstractCurve instance whose _type names an
    unregistered namespace prefix (see Design.md's Namespaces section) -
    round-trips unchanged, never itself a validation error."""
    def __init__(self, type_value, raw: dict):
        super().__init__()
        self._type_value = type_value
        self._raw = dict(raw)

    def get_type(self):
        return self._type_value

    def _own_json_value(self):
        return self._raw

    def _allowed_keys(self):
        return set(self._raw.keys())

    def _validate_own(self):
        return []

    def to_json_value(self):
        d = dict(self._raw)
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        return d


class SEDDocument(SedBase):
    """Generated from specsheets/core/SEDDocument/."""
    _FIELDS = [FieldSpec('version', 'string', True, 'SEDDocument-0002', 'SEDDocument-0001', 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern='^v\\d+\\.\\d+\\.\\d+$', item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='SEDDocument-0003', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('constants', 'any-dict', False, 'SEDDocument-0005', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('tasks', 'dict', False, 'SEDDocument-0006', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('outputs', 'dict', False, 'SEDDocument-0007', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractOutput', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('styles', 'dict', False, 'SEDDocument-0008', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Style', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'version'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'SEDDocument-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _IS_DOCUMENT_CLASS = True
    _MAX_KNOWN_DOCUMENT_VERSION = 'v1.0.0'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._constants = IdKeyedCollection(None)
        self._tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._outputs = IdKeyedCollection(_dispatch_AbstractOutput)
        self._styles = IdKeyedCollection(lambda tv, _cls=Style: (_cls, False))
        self._annotations = ListCollection()
        self._attach(None, self)

    def get_version(self):
        if 'version' not in self._values: raise ApiError('version is not set')
        return self._values['version']

    def set_version(self, value):
        self._values['version'] = value

    def is_set_version(self):
        return 'version' in self._values

    def unset_version(self):
        self._values.pop('version', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_constants(self):
        return self._constants.ids()

    def get_constants_item(self, item_id):
        return self._constants.get(item_id)

    def add_constants(self, item_id, value):
        self._constants.add(item_id, value)

    def insert_constants(self, index, item_id, value):
        self._constants.insert(index, item_id, value)

    def remove_constants(self, item_id):
        self._constants.remove(item_id)

    def set_id_on_constants(self, old_id, new_id):
        self._constants.set_id(old_id, new_id)

    def get_tasks(self):
        return self._tasks.ids()

    def get_tasks_item(self, item_id):
        return self._tasks.get(item_id)

    def add_tasks(self, item_id, obj):
        self._tasks.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_tasks(self, index, item_id, obj):
        self._tasks.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_tasks(self, item_id):
        self._tasks.remove(item_id)

    def set_id_on_tasks(self, old_id, new_id):
        self._tasks.set_id(old_id, new_id)

    def get_outputs(self):
        return self._outputs.ids()

    def get_outputs_item(self, item_id):
        return self._outputs.get(item_id)

    def add_outputs(self, item_id, obj):
        self._outputs.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_outputs(self, index, item_id, obj):
        self._outputs.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_outputs(self, item_id):
        self._outputs.remove(item_id)

    def set_id_on_outputs(self, old_id, new_id):
        self._outputs.set_id(old_id, new_id)

    def get_styles(self):
        return self._styles.ids()

    def get_styles_item(self, item_id):
        return self._styles.get(item_id)

    def add_styles(self, item_id, obj):
        self._styles.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_styles(self, index, item_id, obj):
        self._styles.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_styles(self, item_id):
        self._styles.remove(item_id)

    def set_id_on_styles(self, old_id, new_id):
        self._styles.set_id(old_id, new_id)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._tasks.get(i) for i in self._tasks.ids())
        kids.extend(self._outputs.get(i) for i in self._outputs.ids())
        kids.extend(self._styles.get(i) for i in self._styles.ids())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'constants': return self._constants
        if field_name == 'tasks': return self._tasks
        if field_name == 'outputs': return self._outputs
        if field_name == 'styles': return self._styles
        return None

    def _children_with_locations(self):
        out = []
        for i in self._tasks.ids():
            out.append((self._tasks.get(i), '/tasks/' + i))
        for i in self._outputs.ids():
            out.append((self._outputs.get(i), '/outputs/' + i))
        for i in self._styles.ids():
            out.append((self._styles.get(i), '/styles/' + i))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return ['constants', 'tasks', 'outputs', 'styles']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'version' in self._values: d['version'] = self._values['version']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._constants): d['constants'] = {i: self._constants.get(i) for i in self._constants.ids()}
        if len(self._tasks): d['tasks'] = {i: self._tasks.get(i).to_json_value() for i in self._tasks.ids()}
        if len(self._outputs): d['outputs'] = {i: self._outputs.get(i).to_json_value() for i in self._outputs.ids()}
        if len(self._styles): d['styles'] = {i: self._styles.get(i).to_json_value() for i in self._styles.ids()}
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Style(SedBase):
    """Generated from specsheets/core/Style/."""
    _FIELDS = []
    _REQUIRED_NAMES = {}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'Style-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def _children(self):
        kids = []
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class AggregationCalculation(SedBase):
    """Generated from specsheets/tasks/AggregationCalculation/."""
    _FIELDS = [FieldSpec('input', 'any', True, None, 'AggregationCalculation-0001', 'AggregationCalculation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('appliedDimensions', 'ArrayOrRef', False, 'AggregationCalculation-0002', None, 'AggregationCalculation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AggregationCalculation-0003', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'input'}
    _TYPE_CONST = 'aggregationCalculation'
    _TYPE_RULE_ID = 'AggregationCalculation-0004'
    _OWN_CATCHALL = 'AggregationCalculation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': {'source': 'static', 'expr': 'shapeOf(input) - dim(appliedDimensions or outermost)', 'note': "shape is input's shape with the dimension(s) named in appliedDimensions removed (or the outermost dimension, if appliedDimensions is unset); dimension count/sizes are therefore only as knowable as input's own shape is"}}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'aggregationCalculation'

    def get_input(self):
        if 'input' not in self._values: raise ApiError('input is not set')
        return self._values['input']

    def set_input(self, value):
        self._values['input'] = value

    def is_set_input(self):
        return 'input' in self._values

    def unset_input(self):
        self._values.pop('input', None)

    def get_applied_dimensions_value(self):
        return self._get_orref_value('appliedDimensions')

    def get_applied_dimensions_ref(self):
        return self._get_orref_ref('appliedDimensions')

    def set_applied_dimensions_value(self, value):
        self._set_orref_value('appliedDimensions', value)

    def set_applied_dimensions_ref(self, ref):
        self._set_orref_ref('appliedDimensions', ref)

    def is_applied_dimensions_ref(self):
        return self._is_orref_ref('appliedDimensions')

    def is_set_applied_dimensions(self):
        return 'appliedDimensions' in self._values

    def unset_applied_dimensions(self):
        self._values.pop('appliedDimensions', None); self._orref_is_ref.pop('appliedDimensions', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'aggregationCalculation')
        if 'input' in self._values: d['input'] = self._values['input']
        if 'appliedDimensions' in self._values: d['appliedDimensions'] = self._values['appliedDimensions']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class BoundedODESimulation(SedBase):
    """Generated from specsheets/tasks/BoundedODESimulation/."""
    _FIELDS = [FieldSpec('relativeTolerance', 'NumberOrRef', False, 'AbstractODESimulation-0001', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0002', item_kind=None, ref_target=None), FieldSpec('absoluteTolerance', 'NumberOrRef', False, 'AbstractODESimulation-0003', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0004', item_kind=None, ref_target=None), FieldSpec('absoluteToleranceVector', 'ArrayOrRef', False, 'AbstractODESimulation-0005', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0006', item_kind='number', ref_target=None), FieldSpec('absoluteToleranceAdjustmentFactor', 'NumberOrRef', False, 'AbstractODESimulation-0007', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0008', item_kind=None, ref_target=None), FieldSpec('toleranceForRootFinder', 'NumberOrRef', False, 'AbstractODESimulation-0009', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0010', item_kind=None, ref_target=None), FieldSpec('initialStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0011', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0012', item_kind=None, ref_target=None), FieldSpec('maxNumberOfSteps', 'NumberOrRef', False, 'AbstractODESimulation-0013', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0014', item_kind=None, ref_target=None), FieldSpec('maxInternalSteps', 'IntegerOrRef', False, 'AbstractODESimulation-0015', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0016', item_kind=None, ref_target=None), FieldSpec('maxInternalStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0017', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0018', item_kind=None, ref_target=None), FieldSpec('minInternalStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0019', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0020', item_kind=None, ref_target=None), FieldSpec('forcePhysicalCorrectness', 'BooleanOrRef', False, 'AbstractODESimulation-0021', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0022', item_kind=None, ref_target=None), FieldSpec('integrateReducedModel', 'BooleanOrRef', False, 'AbstractODESimulation-0023', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0024', item_kind=None, ref_target=None), FieldSpec('useReducedModel', 'BooleanOrRef', False, 'AbstractODESimulation-0025', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0026', item_kind=None, ref_target=None), FieldSpec('useStiffSolver', 'BooleanOrRef', False, 'AbstractODESimulation-0027', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0028', item_kind=None, ref_target=None), FieldSpec('maxBDForder', 'IntegerOrRef', False, 'AbstractODESimulation-0029', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0030', item_kind=None, ref_target=None), FieldSpec('maxAdamsOrder', 'IntegerOrRef', False, 'AbstractODESimulation-0031', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0032', item_kind=None, ref_target=None), FieldSpec('variableStepSize', 'BooleanOrRef', False, 'AbstractODESimulation-0033', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0034', item_kind=None, ref_target=None), FieldSpec('maxOutputRows', 'IntegerOrRef', False, 'AbstractODESimulation-0035', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0036', item_kind=None, ref_target=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'AbstractSimulation-0002', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0003', item_kind=None, ref_target=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, 'AbstractSimulation-0004', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0005', item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', False, 'AbstractSimulation-0006', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0007', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('independentVariableSpan', 'ref-class', True, 'BoundedODESimulation-0005', 'BoundedODESimulation-0004', 'BoundedODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Span', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'independentVariableSpan'}
    _TYPE_CONST = 'boundedODESimulation'
    _TYPE_RULE_ID = 'BoundedODESimulation-0006'
    _OWN_CATCHALL = 'BoundedODESimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'runtime', 'note': 'row count is chosen by the solver/simulator at run time under variable step size, not fixed by independentVariableSpan (only its start/end bound the range)'}, 'labels': None}, {'size': {'source': 'static', 'expr': '1 + len(outputVariables)'}, 'labels': {'source': 'static', 'expr': '[independentVariable] + outputVariables'}}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()
        self._independent_variable_span = None

    def get_type(self):
        return 'boundedODESimulation'

    def get_relative_tolerance_value(self):
        return self._get_orref_value('relativeTolerance')

    def get_relative_tolerance_ref(self):
        return self._get_orref_ref('relativeTolerance')

    def set_relative_tolerance_value(self, value):
        self._set_orref_value('relativeTolerance', value)

    def set_relative_tolerance_ref(self, ref):
        self._set_orref_ref('relativeTolerance', ref)

    def is_relative_tolerance_ref(self):
        return self._is_orref_ref('relativeTolerance')

    def is_set_relative_tolerance(self):
        return 'relativeTolerance' in self._values

    def unset_relative_tolerance(self):
        self._values.pop('relativeTolerance', None); self._orref_is_ref.pop('relativeTolerance', None)

    def get_absolute_tolerance_value(self):
        return self._get_orref_value('absoluteTolerance')

    def get_absolute_tolerance_ref(self):
        return self._get_orref_ref('absoluteTolerance')

    def set_absolute_tolerance_value(self, value):
        self._set_orref_value('absoluteTolerance', value)

    def set_absolute_tolerance_ref(self, ref):
        self._set_orref_ref('absoluteTolerance', ref)

    def is_absolute_tolerance_ref(self):
        return self._is_orref_ref('absoluteTolerance')

    def is_set_absolute_tolerance(self):
        return 'absoluteTolerance' in self._values

    def unset_absolute_tolerance(self):
        self._values.pop('absoluteTolerance', None); self._orref_is_ref.pop('absoluteTolerance', None)

    def get_absolute_tolerance_vector_value(self):
        return self._get_orref_value('absoluteToleranceVector')

    def get_absolute_tolerance_vector_ref(self):
        return self._get_orref_ref('absoluteToleranceVector')

    def set_absolute_tolerance_vector_value(self, value):
        self._set_orref_value('absoluteToleranceVector', value)

    def set_absolute_tolerance_vector_ref(self, ref):
        self._set_orref_ref('absoluteToleranceVector', ref)

    def is_absolute_tolerance_vector_ref(self):
        return self._is_orref_ref('absoluteToleranceVector')

    def is_set_absolute_tolerance_vector(self):
        return 'absoluteToleranceVector' in self._values

    def unset_absolute_tolerance_vector(self):
        self._values.pop('absoluteToleranceVector', None); self._orref_is_ref.pop('absoluteToleranceVector', None)

    def get_absolute_tolerance_adjustment_factor_value(self):
        return self._get_orref_value('absoluteToleranceAdjustmentFactor')

    def get_absolute_tolerance_adjustment_factor_ref(self):
        return self._get_orref_ref('absoluteToleranceAdjustmentFactor')

    def set_absolute_tolerance_adjustment_factor_value(self, value):
        self._set_orref_value('absoluteToleranceAdjustmentFactor', value)

    def set_absolute_tolerance_adjustment_factor_ref(self, ref):
        self._set_orref_ref('absoluteToleranceAdjustmentFactor', ref)

    def is_absolute_tolerance_adjustment_factor_ref(self):
        return self._is_orref_ref('absoluteToleranceAdjustmentFactor')

    def is_set_absolute_tolerance_adjustment_factor(self):
        return 'absoluteToleranceAdjustmentFactor' in self._values

    def unset_absolute_tolerance_adjustment_factor(self):
        self._values.pop('absoluteToleranceAdjustmentFactor', None); self._orref_is_ref.pop('absoluteToleranceAdjustmentFactor', None)

    def get_tolerance_for_root_finder_value(self):
        return self._get_orref_value('toleranceForRootFinder')

    def get_tolerance_for_root_finder_ref(self):
        return self._get_orref_ref('toleranceForRootFinder')

    def set_tolerance_for_root_finder_value(self, value):
        self._set_orref_value('toleranceForRootFinder', value)

    def set_tolerance_for_root_finder_ref(self, ref):
        self._set_orref_ref('toleranceForRootFinder', ref)

    def is_tolerance_for_root_finder_ref(self):
        return self._is_orref_ref('toleranceForRootFinder')

    def is_set_tolerance_for_root_finder(self):
        return 'toleranceForRootFinder' in self._values

    def unset_tolerance_for_root_finder(self):
        self._values.pop('toleranceForRootFinder', None); self._orref_is_ref.pop('toleranceForRootFinder', None)

    def get_initial_step_size_value(self):
        return self._get_orref_value('initialStepSize')

    def get_initial_step_size_ref(self):
        return self._get_orref_ref('initialStepSize')

    def set_initial_step_size_value(self, value):
        self._set_orref_value('initialStepSize', value)

    def set_initial_step_size_ref(self, ref):
        self._set_orref_ref('initialStepSize', ref)

    def is_initial_step_size_ref(self):
        return self._is_orref_ref('initialStepSize')

    def is_set_initial_step_size(self):
        return 'initialStepSize' in self._values

    def unset_initial_step_size(self):
        self._values.pop('initialStepSize', None); self._orref_is_ref.pop('initialStepSize', None)

    def get_max_number_of_steps_value(self):
        return self._get_orref_value('maxNumberOfSteps')

    def get_max_number_of_steps_ref(self):
        return self._get_orref_ref('maxNumberOfSteps')

    def set_max_number_of_steps_value(self, value):
        self._set_orref_value('maxNumberOfSteps', value)

    def set_max_number_of_steps_ref(self, ref):
        self._set_orref_ref('maxNumberOfSteps', ref)

    def is_max_number_of_steps_ref(self):
        return self._is_orref_ref('maxNumberOfSteps')

    def is_set_max_number_of_steps(self):
        return 'maxNumberOfSteps' in self._values

    def unset_max_number_of_steps(self):
        self._values.pop('maxNumberOfSteps', None); self._orref_is_ref.pop('maxNumberOfSteps', None)

    def get_max_internal_steps_value(self):
        return self._get_orref_value('maxInternalSteps')

    def get_max_internal_steps_ref(self):
        return self._get_orref_ref('maxInternalSteps')

    def set_max_internal_steps_value(self, value):
        self._set_orref_value('maxInternalSteps', value)

    def set_max_internal_steps_ref(self, ref):
        self._set_orref_ref('maxInternalSteps', ref)

    def is_max_internal_steps_ref(self):
        return self._is_orref_ref('maxInternalSteps')

    def is_set_max_internal_steps(self):
        return 'maxInternalSteps' in self._values

    def unset_max_internal_steps(self):
        self._values.pop('maxInternalSteps', None); self._orref_is_ref.pop('maxInternalSteps', None)

    def get_max_internal_step_size_value(self):
        return self._get_orref_value('maxInternalStepSize')

    def get_max_internal_step_size_ref(self):
        return self._get_orref_ref('maxInternalStepSize')

    def set_max_internal_step_size_value(self, value):
        self._set_orref_value('maxInternalStepSize', value)

    def set_max_internal_step_size_ref(self, ref):
        self._set_orref_ref('maxInternalStepSize', ref)

    def is_max_internal_step_size_ref(self):
        return self._is_orref_ref('maxInternalStepSize')

    def is_set_max_internal_step_size(self):
        return 'maxInternalStepSize' in self._values

    def unset_max_internal_step_size(self):
        self._values.pop('maxInternalStepSize', None); self._orref_is_ref.pop('maxInternalStepSize', None)

    def get_min_internal_step_size_value(self):
        return self._get_orref_value('minInternalStepSize')

    def get_min_internal_step_size_ref(self):
        return self._get_orref_ref('minInternalStepSize')

    def set_min_internal_step_size_value(self, value):
        self._set_orref_value('minInternalStepSize', value)

    def set_min_internal_step_size_ref(self, ref):
        self._set_orref_ref('minInternalStepSize', ref)

    def is_min_internal_step_size_ref(self):
        return self._is_orref_ref('minInternalStepSize')

    def is_set_min_internal_step_size(self):
        return 'minInternalStepSize' in self._values

    def unset_min_internal_step_size(self):
        self._values.pop('minInternalStepSize', None); self._orref_is_ref.pop('minInternalStepSize', None)

    def get_force_physical_correctness_value(self):
        return self._get_orref_value('forcePhysicalCorrectness')

    def get_force_physical_correctness_ref(self):
        return self._get_orref_ref('forcePhysicalCorrectness')

    def set_force_physical_correctness_value(self, value):
        self._set_orref_value('forcePhysicalCorrectness', value)

    def set_force_physical_correctness_ref(self, ref):
        self._set_orref_ref('forcePhysicalCorrectness', ref)

    def is_force_physical_correctness_ref(self):
        return self._is_orref_ref('forcePhysicalCorrectness')

    def is_set_force_physical_correctness(self):
        return 'forcePhysicalCorrectness' in self._values

    def unset_force_physical_correctness(self):
        self._values.pop('forcePhysicalCorrectness', None); self._orref_is_ref.pop('forcePhysicalCorrectness', None)

    def get_integrate_reduced_model_value(self):
        return self._get_orref_value('integrateReducedModel')

    def get_integrate_reduced_model_ref(self):
        return self._get_orref_ref('integrateReducedModel')

    def set_integrate_reduced_model_value(self, value):
        self._set_orref_value('integrateReducedModel', value)

    def set_integrate_reduced_model_ref(self, ref):
        self._set_orref_ref('integrateReducedModel', ref)

    def is_integrate_reduced_model_ref(self):
        return self._is_orref_ref('integrateReducedModel')

    def is_set_integrate_reduced_model(self):
        return 'integrateReducedModel' in self._values

    def unset_integrate_reduced_model(self):
        self._values.pop('integrateReducedModel', None); self._orref_is_ref.pop('integrateReducedModel', None)

    def get_use_reduced_model_value(self):
        return self._get_orref_value('useReducedModel')

    def get_use_reduced_model_ref(self):
        return self._get_orref_ref('useReducedModel')

    def set_use_reduced_model_value(self, value):
        self._set_orref_value('useReducedModel', value)

    def set_use_reduced_model_ref(self, ref):
        self._set_orref_ref('useReducedModel', ref)

    def is_use_reduced_model_ref(self):
        return self._is_orref_ref('useReducedModel')

    def is_set_use_reduced_model(self):
        return 'useReducedModel' in self._values

    def unset_use_reduced_model(self):
        self._values.pop('useReducedModel', None); self._orref_is_ref.pop('useReducedModel', None)

    def get_use_stiff_solver_value(self):
        return self._get_orref_value('useStiffSolver')

    def get_use_stiff_solver_ref(self):
        return self._get_orref_ref('useStiffSolver')

    def set_use_stiff_solver_value(self, value):
        self._set_orref_value('useStiffSolver', value)

    def set_use_stiff_solver_ref(self, ref):
        self._set_orref_ref('useStiffSolver', ref)

    def is_use_stiff_solver_ref(self):
        return self._is_orref_ref('useStiffSolver')

    def is_set_use_stiff_solver(self):
        return 'useStiffSolver' in self._values

    def unset_use_stiff_solver(self):
        self._values.pop('useStiffSolver', None); self._orref_is_ref.pop('useStiffSolver', None)

    def get_max_b_d_forder_value(self):
        return self._get_orref_value('maxBDForder')

    def get_max_b_d_forder_ref(self):
        return self._get_orref_ref('maxBDForder')

    def set_max_b_d_forder_value(self, value):
        self._set_orref_value('maxBDForder', value)

    def set_max_b_d_forder_ref(self, ref):
        self._set_orref_ref('maxBDForder', ref)

    def is_max_b_d_forder_ref(self):
        return self._is_orref_ref('maxBDForder')

    def is_set_max_b_d_forder(self):
        return 'maxBDForder' in self._values

    def unset_max_b_d_forder(self):
        self._values.pop('maxBDForder', None); self._orref_is_ref.pop('maxBDForder', None)

    def get_max_adams_order_value(self):
        return self._get_orref_value('maxAdamsOrder')

    def get_max_adams_order_ref(self):
        return self._get_orref_ref('maxAdamsOrder')

    def set_max_adams_order_value(self, value):
        self._set_orref_value('maxAdamsOrder', value)

    def set_max_adams_order_ref(self, ref):
        self._set_orref_ref('maxAdamsOrder', ref)

    def is_max_adams_order_ref(self):
        return self._is_orref_ref('maxAdamsOrder')

    def is_set_max_adams_order(self):
        return 'maxAdamsOrder' in self._values

    def unset_max_adams_order(self):
        self._values.pop('maxAdamsOrder', None); self._orref_is_ref.pop('maxAdamsOrder', None)

    def get_variable_step_size_value(self):
        return self._get_orref_value('variableStepSize')

    def get_variable_step_size_ref(self):
        return self._get_orref_ref('variableStepSize')

    def set_variable_step_size_value(self, value):
        self._set_orref_value('variableStepSize', value)

    def set_variable_step_size_ref(self, ref):
        self._set_orref_ref('variableStepSize', ref)

    def is_variable_step_size_ref(self):
        return self._is_orref_ref('variableStepSize')

    def is_set_variable_step_size(self):
        return 'variableStepSize' in self._values

    def unset_variable_step_size(self):
        self._values.pop('variableStepSize', None); self._orref_is_ref.pop('variableStepSize', None)

    def get_max_output_rows_value(self):
        return self._get_orref_value('maxOutputRows')

    def get_max_output_rows_ref(self):
        return self._get_orref_ref('maxOutputRows')

    def set_max_output_rows_value(self, value):
        self._set_orref_value('maxOutputRows', value)

    def set_max_output_rows_ref(self, ref):
        self._set_orref_ref('maxOutputRows', ref)

    def is_max_output_rows_ref(self):
        return self._is_orref_ref('maxOutputRows')

    def is_set_max_output_rows(self):
        return 'maxOutputRows' in self._values

    def unset_max_output_rows(self):
        self._values.pop('maxOutputRows', None); self._orref_is_ref.pop('maxOutputRows', None)

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_independent_variable_init_value(self):
        return self._get_orref_value('independentVariableInit')

    def get_independent_variable_init_ref(self):
        return self._get_orref_ref('independentVariableInit')

    def set_independent_variable_init_value(self, value):
        self._set_orref_value('independentVariableInit', value)

    def set_independent_variable_init_ref(self, ref):
        self._set_orref_ref('independentVariableInit', ref)

    def is_independent_variable_init_ref(self):
        return self._is_orref_ref('independentVariableInit')

    def is_set_independent_variable_init(self):
        return 'independentVariableInit' in self._values

    def unset_independent_variable_init(self):
        self._values.pop('independentVariableInit', None); self._orref_is_ref.pop('independentVariableInit', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_independent_variable_span(self):
        if self._independent_variable_span is None: raise ApiError('independent_variable_span is not set')
        return self._independent_variable_span

    def set_independent_variable_span(self, obj):
        self._independent_variable_span = obj; obj._attach(self, self.get_document())

    def is_set_independent_variable_span(self):
        return self._independent_variable_span is not None

    def unset_independent_variable_span(self):
        self._independent_variable_span = None

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        if self._independent_variable_span is not None: kids.append(self._independent_variable_span)
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._independent_variable_span is not None: out.append((self._independent_variable_span, '/independentVariableSpan'))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'boundedODESimulation')
        if 'relativeTolerance' in self._values: d['relativeTolerance'] = self._values['relativeTolerance']
        if 'absoluteTolerance' in self._values: d['absoluteTolerance'] = self._values['absoluteTolerance']
        if 'absoluteToleranceVector' in self._values: d['absoluteToleranceVector'] = self._values['absoluteToleranceVector']
        if 'absoluteToleranceAdjustmentFactor' in self._values: d['absoluteToleranceAdjustmentFactor'] = self._values['absoluteToleranceAdjustmentFactor']
        if 'toleranceForRootFinder' in self._values: d['toleranceForRootFinder'] = self._values['toleranceForRootFinder']
        if 'initialStepSize' in self._values: d['initialStepSize'] = self._values['initialStepSize']
        if 'maxNumberOfSteps' in self._values: d['maxNumberOfSteps'] = self._values['maxNumberOfSteps']
        if 'maxInternalSteps' in self._values: d['maxInternalSteps'] = self._values['maxInternalSteps']
        if 'maxInternalStepSize' in self._values: d['maxInternalStepSize'] = self._values['maxInternalStepSize']
        if 'minInternalStepSize' in self._values: d['minInternalStepSize'] = self._values['minInternalStepSize']
        if 'forcePhysicalCorrectness' in self._values: d['forcePhysicalCorrectness'] = self._values['forcePhysicalCorrectness']
        if 'integrateReducedModel' in self._values: d['integrateReducedModel'] = self._values['integrateReducedModel']
        if 'useReducedModel' in self._values: d['useReducedModel'] = self._values['useReducedModel']
        if 'useStiffSolver' in self._values: d['useStiffSolver'] = self._values['useStiffSolver']
        if 'maxBDForder' in self._values: d['maxBDForder'] = self._values['maxBDForder']
        if 'maxAdamsOrder' in self._values: d['maxAdamsOrder'] = self._values['maxAdamsOrder']
        if 'variableStepSize' in self._values: d['variableStepSize'] = self._values['variableStepSize']
        if 'maxOutputRows' in self._values: d['maxOutputRows'] = self._values['maxOutputRows']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._independent_variable_span is not None: d['independentVariableSpan'] = self._independent_variable_span.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class BoundedStochasticSimulation(SedBase):
    """Generated from specsheets/tasks/BoundedStochasticSimulation/."""
    _FIELDS = [FieldSpec('seed', 'NumberOrRef', False, 'AbstractStochasticSimulation-0001', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0002', item_kind=None, ref_target=None), FieldSpec('timeDependentRelativeTolerance', 'NumberOrRef', False, 'AbstractStochasticSimulation-0003', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0004', item_kind=None, ref_target=None), FieldSpec('variableStepSize', 'BooleanOrRef', False, 'AbstractStochasticSimulation-0005', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0006', item_kind=None, ref_target=None), FieldSpec('minimumTimeStep', 'NumberOrRef', False, 'AbstractStochasticSimulation-0007', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0008', item_kind=None, ref_target=None), FieldSpec('maximumTimeStep', 'NumberOrRef', False, 'AbstractStochasticSimulation-0009', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0010', item_kind=None, ref_target=None), FieldSpec('nonNegative', 'BooleanOrRef', False, 'AbstractStochasticSimulation-0011', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0012', item_kind=None, ref_target=None), FieldSpec('maxOutputRows', 'IntegerOrRef', False, 'AbstractStochasticSimulation-0013', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0014', item_kind=None, ref_target=None), FieldSpec('maxNumSteps', 'IntegerOrRef', False, 'AbstractStochasticSimulation-0015', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0016', item_kind=None, ref_target=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'AbstractSimulation-0002', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0003', item_kind=None, ref_target=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, 'AbstractSimulation-0004', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0005', item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', False, 'AbstractSimulation-0006', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0007', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('independentVariableSpan', 'ref-class', True, 'BoundedStochasticSimulation-0005', 'BoundedStochasticSimulation-0004', 'BoundedStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Span', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'independentVariableSpan'}
    _TYPE_CONST = 'boundedStochasticSimulation'
    _TYPE_RULE_ID = 'BoundedStochasticSimulation-0006'
    _OWN_CATCHALL = 'BoundedStochasticSimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'runtime', 'note': 'row count is chosen by the solver/simulator at run time under variable step size, not fixed by independentVariableSpan (only its start/end bound the range)'}, 'labels': None}, {'size': {'source': 'static', 'expr': '1 + len(outputVariables)'}, 'labels': {'source': 'static', 'expr': '[independentVariable] + outputVariables'}}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()
        self._independent_variable_span = None

    def get_type(self):
        return 'boundedStochasticSimulation'

    def get_seed_value(self):
        return self._get_orref_value('seed')

    def get_seed_ref(self):
        return self._get_orref_ref('seed')

    def set_seed_value(self, value):
        self._set_orref_value('seed', value)

    def set_seed_ref(self, ref):
        self._set_orref_ref('seed', ref)

    def is_seed_ref(self):
        return self._is_orref_ref('seed')

    def is_set_seed(self):
        return 'seed' in self._values

    def unset_seed(self):
        self._values.pop('seed', None); self._orref_is_ref.pop('seed', None)

    def get_time_dependent_relative_tolerance_value(self):
        return self._get_orref_value('timeDependentRelativeTolerance')

    def get_time_dependent_relative_tolerance_ref(self):
        return self._get_orref_ref('timeDependentRelativeTolerance')

    def set_time_dependent_relative_tolerance_value(self, value):
        self._set_orref_value('timeDependentRelativeTolerance', value)

    def set_time_dependent_relative_tolerance_ref(self, ref):
        self._set_orref_ref('timeDependentRelativeTolerance', ref)

    def is_time_dependent_relative_tolerance_ref(self):
        return self._is_orref_ref('timeDependentRelativeTolerance')

    def is_set_time_dependent_relative_tolerance(self):
        return 'timeDependentRelativeTolerance' in self._values

    def unset_time_dependent_relative_tolerance(self):
        self._values.pop('timeDependentRelativeTolerance', None); self._orref_is_ref.pop('timeDependentRelativeTolerance', None)

    def get_variable_step_size_value(self):
        return self._get_orref_value('variableStepSize')

    def get_variable_step_size_ref(self):
        return self._get_orref_ref('variableStepSize')

    def set_variable_step_size_value(self, value):
        self._set_orref_value('variableStepSize', value)

    def set_variable_step_size_ref(self, ref):
        self._set_orref_ref('variableStepSize', ref)

    def is_variable_step_size_ref(self):
        return self._is_orref_ref('variableStepSize')

    def is_set_variable_step_size(self):
        return 'variableStepSize' in self._values

    def unset_variable_step_size(self):
        self._values.pop('variableStepSize', None); self._orref_is_ref.pop('variableStepSize', None)

    def get_minimum_time_step_value(self):
        return self._get_orref_value('minimumTimeStep')

    def get_minimum_time_step_ref(self):
        return self._get_orref_ref('minimumTimeStep')

    def set_minimum_time_step_value(self, value):
        self._set_orref_value('minimumTimeStep', value)

    def set_minimum_time_step_ref(self, ref):
        self._set_orref_ref('minimumTimeStep', ref)

    def is_minimum_time_step_ref(self):
        return self._is_orref_ref('minimumTimeStep')

    def is_set_minimum_time_step(self):
        return 'minimumTimeStep' in self._values

    def unset_minimum_time_step(self):
        self._values.pop('minimumTimeStep', None); self._orref_is_ref.pop('minimumTimeStep', None)

    def get_maximum_time_step_value(self):
        return self._get_orref_value('maximumTimeStep')

    def get_maximum_time_step_ref(self):
        return self._get_orref_ref('maximumTimeStep')

    def set_maximum_time_step_value(self, value):
        self._set_orref_value('maximumTimeStep', value)

    def set_maximum_time_step_ref(self, ref):
        self._set_orref_ref('maximumTimeStep', ref)

    def is_maximum_time_step_ref(self):
        return self._is_orref_ref('maximumTimeStep')

    def is_set_maximum_time_step(self):
        return 'maximumTimeStep' in self._values

    def unset_maximum_time_step(self):
        self._values.pop('maximumTimeStep', None); self._orref_is_ref.pop('maximumTimeStep', None)

    def get_non_negative_value(self):
        return self._get_orref_value('nonNegative')

    def get_non_negative_ref(self):
        return self._get_orref_ref('nonNegative')

    def set_non_negative_value(self, value):
        self._set_orref_value('nonNegative', value)

    def set_non_negative_ref(self, ref):
        self._set_orref_ref('nonNegative', ref)

    def is_non_negative_ref(self):
        return self._is_orref_ref('nonNegative')

    def is_set_non_negative(self):
        return 'nonNegative' in self._values

    def unset_non_negative(self):
        self._values.pop('nonNegative', None); self._orref_is_ref.pop('nonNegative', None)

    def get_max_output_rows_value(self):
        return self._get_orref_value('maxOutputRows')

    def get_max_output_rows_ref(self):
        return self._get_orref_ref('maxOutputRows')

    def set_max_output_rows_value(self, value):
        self._set_orref_value('maxOutputRows', value)

    def set_max_output_rows_ref(self, ref):
        self._set_orref_ref('maxOutputRows', ref)

    def is_max_output_rows_ref(self):
        return self._is_orref_ref('maxOutputRows')

    def is_set_max_output_rows(self):
        return 'maxOutputRows' in self._values

    def unset_max_output_rows(self):
        self._values.pop('maxOutputRows', None); self._orref_is_ref.pop('maxOutputRows', None)

    def get_max_num_steps_value(self):
        return self._get_orref_value('maxNumSteps')

    def get_max_num_steps_ref(self):
        return self._get_orref_ref('maxNumSteps')

    def set_max_num_steps_value(self, value):
        self._set_orref_value('maxNumSteps', value)

    def set_max_num_steps_ref(self, ref):
        self._set_orref_ref('maxNumSteps', ref)

    def is_max_num_steps_ref(self):
        return self._is_orref_ref('maxNumSteps')

    def is_set_max_num_steps(self):
        return 'maxNumSteps' in self._values

    def unset_max_num_steps(self):
        self._values.pop('maxNumSteps', None); self._orref_is_ref.pop('maxNumSteps', None)

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_independent_variable_init_value(self):
        return self._get_orref_value('independentVariableInit')

    def get_independent_variable_init_ref(self):
        return self._get_orref_ref('independentVariableInit')

    def set_independent_variable_init_value(self, value):
        self._set_orref_value('independentVariableInit', value)

    def set_independent_variable_init_ref(self, ref):
        self._set_orref_ref('independentVariableInit', ref)

    def is_independent_variable_init_ref(self):
        return self._is_orref_ref('independentVariableInit')

    def is_set_independent_variable_init(self):
        return 'independentVariableInit' in self._values

    def unset_independent_variable_init(self):
        self._values.pop('independentVariableInit', None); self._orref_is_ref.pop('independentVariableInit', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_independent_variable_span(self):
        if self._independent_variable_span is None: raise ApiError('independent_variable_span is not set')
        return self._independent_variable_span

    def set_independent_variable_span(self, obj):
        self._independent_variable_span = obj; obj._attach(self, self.get_document())

    def is_set_independent_variable_span(self):
        return self._independent_variable_span is not None

    def unset_independent_variable_span(self):
        self._independent_variable_span = None

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        if self._independent_variable_span is not None: kids.append(self._independent_variable_span)
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._independent_variable_span is not None: out.append((self._independent_variable_span, '/independentVariableSpan'))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'boundedStochasticSimulation')
        if 'seed' in self._values: d['seed'] = self._values['seed']
        if 'timeDependentRelativeTolerance' in self._values: d['timeDependentRelativeTolerance'] = self._values['timeDependentRelativeTolerance']
        if 'variableStepSize' in self._values: d['variableStepSize'] = self._values['variableStepSize']
        if 'minimumTimeStep' in self._values: d['minimumTimeStep'] = self._values['minimumTimeStep']
        if 'maximumTimeStep' in self._values: d['maximumTimeStep'] = self._values['maximumTimeStep']
        if 'nonNegative' in self._values: d['nonNegative'] = self._values['nonNegative']
        if 'maxOutputRows' in self._values: d['maxOutputRows'] = self._values['maxOutputRows']
        if 'maxNumSteps' in self._values: d['maxNumSteps'] = self._values['maxNumSteps']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._independent_variable_span is not None: d['independentVariableSpan'] = self._independent_variable_span.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Calculation(SedBase):
    """Generated from specsheets/tasks/Calculation/."""
    _FIELDS = [FieldSpec('math', 'StringOrRef', True, 'Calculation-0002', 'Calculation-0001', 'Calculation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=True, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'math'}
    _TYPE_CONST = 'calculation'
    _TYPE_RULE_ID = 'Calculation-0004'
    _OWN_CATCHALL = 'Calculation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': {'source': 'runtime', 'note': "shape matches the evaluated math expression: scalar if every operand is scalar, otherwise broadcasts across the shape of any AnnotatedData operand(s); not derivable without evaluating math against the operands' actual values"}}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'calculation'

    def get_math_value(self):
        return self._get_orref_value('math')

    def get_math_ref(self):
        return self._get_orref_ref('math')

    def set_math_value(self, value):
        self._set_orref_value('math', value)

    def set_math_ref(self, ref):
        self._set_orref_ref('math', ref)

    def is_math_ref(self):
        return self._is_orref_ref('math')

    def is_set_math(self):
        return 'math' in self._values

    def unset_math(self):
        self._values.pop('math', None); self._orref_is_ref.pop('math', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'calculation')
        if 'math' in self._values: d['math'] = self._values['math']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class CreateDataBlock(SedBase):
    """Generated from specsheets/tasks/CreateDataBlock/."""
    _FIELDS = [FieldSpec('data', 'DictOrRef', True, 'CreateDataBlock-0002', 'CreateDataBlock-0001', 'CreateDataBlock-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CreateDataBlock-0003', item_kind='any', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'data'}
    _TYPE_CONST = 'createDataBlock'
    _TYPE_RULE_ID = 'CreateDataBlock-0004'
    _OWN_CATCHALL = 'CreateDataBlock-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(data)'}, 'labels': {'source': 'static', 'expr': 'keys(data)'}, 'note': 'dimension 0 has one entry per key in the data dictionary, labeled by those keys'}, {'trailing': {'of': 'data', 'note': 'if the values in data are themselves multi-dimensional (a list or AnnotatedData), their dimensions follow dimension 0; all entries must have the same shape, since they are stacked into one array; how many dimensions that is is not known ahead of time'}}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'createDataBlock'

    def get_data_value(self):
        return self._get_orref_value('data')

    def get_data_ref(self):
        return self._get_orref_ref('data')

    def set_data_value(self, value):
        self._set_orref_value('data', value)

    def set_data_ref(self, ref):
        self._set_orref_ref('data', ref)

    def is_data_ref(self):
        return self._is_orref_ref('data')

    def is_set_data(self):
        return 'data' in self._values

    def unset_data(self):
        self._values.pop('data', None); self._orref_is_ref.pop('data', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'createDataBlock')
        if 'data' in self._values: d['data'] = self._values['data']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class CsvImport(SedBase):
    """Generated from specsheets/tasks/CsvImport/."""
    _FIELDS = [FieldSpec('location', 'StringOrRef', True, 'CsvImport-0002', 'CsvImport-0001', 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=1, enum=None, ref_type_rule_id='CsvImport-0003', item_kind=None, ref_target=None), FieldSpec('organization', 'StringOrRef', False, 'CsvImport-0004', None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0005', item_kind=None, ref_target=None), FieldSpec('separator', 'StringOrRef', False, 'CsvImport-0006', None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0007', item_kind=None, ref_target=None), FieldSpec('headers', 'BooleanOrRef', False, 'CsvImport-0008', None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0009', item_kind=None, ref_target=None), FieldSpec('columnNames', 'ArrayOrRef', False, 'CsvImport-0010', None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0011', item_kind='string', ref_target=None), FieldSpec('ncols', 'IntegerOrRef', False, 'CsvImport-0012', None, 'CsvImport-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0013', item_kind=None, ref_target=None), FieldSpec('nrows', 'IntegerOrRef', False, 'CsvImport-0014', None, 'CsvImport-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0015', item_kind=None, ref_target=None), FieldSpec('units', 'ArrayOrRef', False, 'CsvImport-0016', None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='CsvImport-0017', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'location'}
    _TYPE_CONST = 'csvImport'
    _TYPE_RULE_ID = 'CsvImport-0018'
    _OWN_CATCHALL = 'CsvImport-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'input-file', 'from': 'location', 'extract': 'rowCount', 'note': 'row count, read from the CSV file at location'}, 'labels': None}, {'size': {'source': 'input-file', 'from': 'location', 'extract': 'columnCount', 'note': 'column count, read from the CSV file at location together with organization/headers/ncols'}, 'labels': {'source': 'input-file', 'from': 'location', 'extract': 'columnHeaders', 'note': 'column labels, read from the CSV header row when headers is true, else from columnNames'}}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'csvImport'

    def get_location_value(self):
        return self._get_orref_value('location')

    def get_location_ref(self):
        return self._get_orref_ref('location')

    def set_location_value(self, value):
        self._set_orref_value('location', value)

    def set_location_ref(self, ref):
        self._set_orref_ref('location', ref)

    def is_location_ref(self):
        return self._is_orref_ref('location')

    def is_set_location(self):
        return 'location' in self._values

    def unset_location(self):
        self._values.pop('location', None); self._orref_is_ref.pop('location', None)

    def get_organization_value(self):
        return self._get_orref_value('organization')

    def get_organization_ref(self):
        return self._get_orref_ref('organization')

    def set_organization_value(self, value):
        self._set_orref_value('organization', value)

    def set_organization_ref(self, ref):
        self._set_orref_ref('organization', ref)

    def is_organization_ref(self):
        return self._is_orref_ref('organization')

    def is_set_organization(self):
        return 'organization' in self._values

    def unset_organization(self):
        self._values.pop('organization', None); self._orref_is_ref.pop('organization', None)

    def get_separator_value(self):
        return self._get_orref_value('separator')

    def get_separator_ref(self):
        return self._get_orref_ref('separator')

    def set_separator_value(self, value):
        self._set_orref_value('separator', value)

    def set_separator_ref(self, ref):
        self._set_orref_ref('separator', ref)

    def is_separator_ref(self):
        return self._is_orref_ref('separator')

    def is_set_separator(self):
        return 'separator' in self._values

    def unset_separator(self):
        self._values.pop('separator', None); self._orref_is_ref.pop('separator', None)

    def get_headers_value(self):
        return self._get_orref_value('headers')

    def get_headers_ref(self):
        return self._get_orref_ref('headers')

    def set_headers_value(self, value):
        self._set_orref_value('headers', value)

    def set_headers_ref(self, ref):
        self._set_orref_ref('headers', ref)

    def is_headers_ref(self):
        return self._is_orref_ref('headers')

    def is_set_headers(self):
        return 'headers' in self._values

    def unset_headers(self):
        self._values.pop('headers', None); self._orref_is_ref.pop('headers', None)

    def get_column_names_value(self):
        return self._get_orref_value('columnNames')

    def get_column_names_ref(self):
        return self._get_orref_ref('columnNames')

    def set_column_names_value(self, value):
        self._set_orref_value('columnNames', value)

    def set_column_names_ref(self, ref):
        self._set_orref_ref('columnNames', ref)

    def is_column_names_ref(self):
        return self._is_orref_ref('columnNames')

    def is_set_column_names(self):
        return 'columnNames' in self._values

    def unset_column_names(self):
        self._values.pop('columnNames', None); self._orref_is_ref.pop('columnNames', None)

    def get_ncols_value(self):
        return self._get_orref_value('ncols')

    def get_ncols_ref(self):
        return self._get_orref_ref('ncols')

    def set_ncols_value(self, value):
        self._set_orref_value('ncols', value)

    def set_ncols_ref(self, ref):
        self._set_orref_ref('ncols', ref)

    def is_ncols_ref(self):
        return self._is_orref_ref('ncols')

    def is_set_ncols(self):
        return 'ncols' in self._values

    def unset_ncols(self):
        self._values.pop('ncols', None); self._orref_is_ref.pop('ncols', None)

    def get_nrows_value(self):
        return self._get_orref_value('nrows')

    def get_nrows_ref(self):
        return self._get_orref_ref('nrows')

    def set_nrows_value(self, value):
        self._set_orref_value('nrows', value)

    def set_nrows_ref(self, ref):
        self._set_orref_ref('nrows', ref)

    def is_nrows_ref(self):
        return self._is_orref_ref('nrows')

    def is_set_nrows(self):
        return 'nrows' in self._values

    def unset_nrows(self):
        self._values.pop('nrows', None); self._orref_is_ref.pop('nrows', None)

    def get_units_value(self):
        return self._get_orref_value('units')

    def get_units_ref(self):
        return self._get_orref_ref('units')

    def set_units_value(self, value):
        self._set_orref_value('units', value)

    def set_units_ref(self, ref):
        self._set_orref_ref('units', ref)

    def is_units_ref(self):
        return self._is_orref_ref('units')

    def is_set_units(self):
        return 'units' in self._values

    def unset_units(self):
        self._values.pop('units', None); self._orref_is_ref.pop('units', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'csvImport')
        if 'location' in self._values: d['location'] = self._values['location']
        if 'organization' in self._values: d['organization'] = self._values['organization']
        if 'separator' in self._values: d['separator'] = self._values['separator']
        if 'headers' in self._values: d['headers'] = self._values['headers']
        if 'columnNames' in self._values: d['columnNames'] = self._values['columnNames']
        if 'ncols' in self._values: d['ncols'] = self._values['ncols']
        if 'nrows' in self._values: d['nrows'] = self._values['nrows']
        if 'units' in self._values: d['units'] = self._values['units']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class DataImport(SedBase):
    """Generated from specsheets/tasks/DataImport/."""
    _FIELDS = [FieldSpec('location', 'StringOrRef', True, 'DataImport-0002', 'DataImport-0001', 'DataImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=1, enum=None, ref_type_rule_id='DataImport-0003', item_kind=None, ref_target=None), FieldSpec('format', 'StringOrRef', True, 'DataImport-0005', 'DataImport-0004', 'DataImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=1, enum=None, ref_type_rule_id='DataImport-0006', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'location', 'format'}
    _TYPE_CONST = 'dataImport'
    _TYPE_RULE_ID = 'DataImport-0007'
    _OWN_CATCHALL = 'DataImport-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': {'source': 'input-file', 'from': 'location', 'extract': 'shape', 'note': 'shape is whatever the imported file itself has; depends on format and the file at location - extraction is format-specific (format names how to parse it)'}}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'dataImport'

    def get_location_value(self):
        return self._get_orref_value('location')

    def get_location_ref(self):
        return self._get_orref_ref('location')

    def set_location_value(self, value):
        self._set_orref_value('location', value)

    def set_location_ref(self, ref):
        self._set_orref_ref('location', ref)

    def is_location_ref(self):
        return self._is_orref_ref('location')

    def is_set_location(self):
        return 'location' in self._values

    def unset_location(self):
        self._values.pop('location', None); self._orref_is_ref.pop('location', None)

    def get_format_value(self):
        return self._get_orref_value('format')

    def get_format_ref(self):
        return self._get_orref_ref('format')

    def set_format_value(self, value):
        self._set_orref_value('format', value)

    def set_format_ref(self, ref):
        self._set_orref_ref('format', ref)

    def is_format_ref(self):
        return self._is_orref_ref('format')

    def is_set_format(self):
        return 'format' in self._values

    def unset_format(self):
        self._values.pop('format', None); self._orref_is_ref.pop('format', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'dataImport')
        if 'location' in self._values: d['location'] = self._values['location']
        if 'format' in self._values: d['format'] = self._values['format']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class DrawFromDistribution(SedBase):
    """Generated from specsheets/tasks/DrawFromDistribution/."""
    _FIELDS = [FieldSpec('distribution', 'StringOrRef', True, 'DrawFromDistribution-0008', 'DrawFromDistribution-0007', 'DrawFromDistribution-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('http://www.sbml.org/sbml/symbols/distrib/normal', 'http://www.sbml.org/sbml/symbols/distrib/uniform', 'http://www.sbml.org/sbml/symbols/distrib/bernoulli', 'http://www.sbml.org/sbml/symbols/distrib/binomial', 'http://www.sbml.org/sbml/symbols/distrib/cauchy', 'http://www.sbml.org/sbml/symbols/distrib/chisquare', 'http://www.sbml.org/sbml/symbols/distrib/exponential', 'http://www.sbml.org/sbml/symbols/distrib/gamma', 'http://www.sbml.org/sbml/symbols/distrib/laplace', 'http://www.sbml.org/sbml/symbols/distrib/lognormal', 'http://www.sbml.org/sbml/symbols/distrib/poisson', 'http://www.sbml.org/sbml/symbols/distrib/rayleigh'), ref_type_rule_id='DrawFromDistribution-0009', item_kind=None, ref_target=None), FieldSpec('outputPersistent', 'BooleanOrRef', False, 'DrawFromDistribution-0004', None, 'DrawFromDistribution-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='DrawFromDistribution-0005', item_kind=None, ref_target=None), FieldSpec('arguments', 'ArrayOrRef', True, 'DrawFromDistribution-0002', 'DrawFromDistribution-0001', 'DrawFromDistribution-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='DrawFromDistribution-0003', item_kind='any', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'distribution', 'arguments'}
    _TYPE_CONST = 'drawFromDistribution'
    _TYPE_RULE_ID = 'DrawFromDistribution-0006'
    _OWN_CATCHALL = 'DrawFromDistribution-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [], 'note': 'currently always a single scalar value (0-D), indexed historically as [id][0]; the type is multidimensional AnnotatedData to leave room for future correlated multi-value draws (shape of that future case is not yet designed - see core-spec.md Section 10)'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'drawFromDistribution'

    def get_distribution_value(self):
        return self._get_orref_value('distribution')

    def get_distribution_ref(self):
        return self._get_orref_ref('distribution')

    def set_distribution_value(self, value):
        self._set_orref_value('distribution', value)

    def set_distribution_ref(self, ref):
        self._set_orref_ref('distribution', ref)

    def is_distribution_ref(self):
        return self._is_orref_ref('distribution')

    def is_set_distribution(self):
        return 'distribution' in self._values

    def unset_distribution(self):
        self._values.pop('distribution', None); self._orref_is_ref.pop('distribution', None)

    def get_output_persistent_value(self):
        return self._get_orref_value('outputPersistent')

    def get_output_persistent_ref(self):
        return self._get_orref_ref('outputPersistent')

    def set_output_persistent_value(self, value):
        self._set_orref_value('outputPersistent', value)

    def set_output_persistent_ref(self, ref):
        self._set_orref_ref('outputPersistent', ref)

    def is_output_persistent_ref(self):
        return self._is_orref_ref('outputPersistent')

    def is_set_output_persistent(self):
        return 'outputPersistent' in self._values

    def unset_output_persistent(self):
        self._values.pop('outputPersistent', None); self._orref_is_ref.pop('outputPersistent', None)

    def get_arguments_value(self):
        return self._get_orref_value('arguments')

    def get_arguments_ref(self):
        return self._get_orref_ref('arguments')

    def set_arguments_value(self, value):
        self._set_orref_value('arguments', value)

    def set_arguments_ref(self, ref):
        self._set_orref_ref('arguments', ref)

    def is_arguments_ref(self):
        return self._is_orref_ref('arguments')

    def is_set_arguments(self):
        return 'arguments' in self._values

    def unset_arguments(self):
        self._values.pop('arguments', None); self._orref_is_ref.pop('arguments', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'drawFromDistribution')
        if 'distribution' in self._values: d['distribution'] = self._values['distribution']
        if 'outputPersistent' in self._values: d['outputPersistent'] = self._values['outputPersistent']
        if 'arguments' in self._values: d['arguments'] = self._values['arguments']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ExplicitODESimulation(SedBase):
    """Generated from specsheets/tasks/ExplicitODESimulation/."""
    _FIELDS = [FieldSpec('relativeTolerance', 'NumberOrRef', False, 'AbstractODESimulation-0001', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0002', item_kind=None, ref_target=None), FieldSpec('absoluteTolerance', 'NumberOrRef', False, 'AbstractODESimulation-0003', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0004', item_kind=None, ref_target=None), FieldSpec('absoluteToleranceVector', 'ArrayOrRef', False, 'AbstractODESimulation-0005', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0006', item_kind='number', ref_target=None), FieldSpec('absoluteToleranceAdjustmentFactor', 'NumberOrRef', False, 'AbstractODESimulation-0007', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0008', item_kind=None, ref_target=None), FieldSpec('toleranceForRootFinder', 'NumberOrRef', False, 'AbstractODESimulation-0009', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0010', item_kind=None, ref_target=None), FieldSpec('initialStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0011', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0012', item_kind=None, ref_target=None), FieldSpec('maxNumberOfSteps', 'NumberOrRef', False, 'AbstractODESimulation-0013', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0014', item_kind=None, ref_target=None), FieldSpec('maxInternalSteps', 'IntegerOrRef', False, 'AbstractODESimulation-0015', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0016', item_kind=None, ref_target=None), FieldSpec('maxInternalStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0017', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0018', item_kind=None, ref_target=None), FieldSpec('minInternalStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0019', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0020', item_kind=None, ref_target=None), FieldSpec('forcePhysicalCorrectness', 'BooleanOrRef', False, 'AbstractODESimulation-0021', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0022', item_kind=None, ref_target=None), FieldSpec('integrateReducedModel', 'BooleanOrRef', False, 'AbstractODESimulation-0023', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0024', item_kind=None, ref_target=None), FieldSpec('useReducedModel', 'BooleanOrRef', False, 'AbstractODESimulation-0025', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0026', item_kind=None, ref_target=None), FieldSpec('useStiffSolver', 'BooleanOrRef', False, 'AbstractODESimulation-0027', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0028', item_kind=None, ref_target=None), FieldSpec('maxBDForder', 'IntegerOrRef', False, 'AbstractODESimulation-0029', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0030', item_kind=None, ref_target=None), FieldSpec('maxAdamsOrder', 'IntegerOrRef', False, 'AbstractODESimulation-0031', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0032', item_kind=None, ref_target=None), FieldSpec('variableStepSize', 'BooleanOrRef', False, 'AbstractODESimulation-0033', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0034', item_kind=None, ref_target=None), FieldSpec('maxOutputRows', 'IntegerOrRef', False, 'AbstractODESimulation-0035', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0036', item_kind=None, ref_target=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'AbstractSimulation-0002', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0003', item_kind=None, ref_target=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, 'AbstractSimulation-0004', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0005', item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', False, 'AbstractSimulation-0006', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0007', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('independentVariableRange', 'ref-class', True, 'ExplicitODESimulation-0005', 'ExplicitODESimulation-0004', 'ExplicitODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='NumericRange', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'independentVariableRange'}
    _TYPE_CONST = 'explicitODESimulation'
    _TYPE_RULE_ID = 'ExplicitODESimulation-0006'
    _OWN_CATCHALL = 'ExplicitODESimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(independentVariableRange)'}, 'labels': None}, {'size': {'source': 'static', 'expr': '1 + len(outputVariables)'}, 'labels': {'source': 'static', 'expr': '[independentVariable] + outputVariables'}}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()
        self._independent_variable_range = None

    def get_type(self):
        return 'explicitODESimulation'

    def get_relative_tolerance_value(self):
        return self._get_orref_value('relativeTolerance')

    def get_relative_tolerance_ref(self):
        return self._get_orref_ref('relativeTolerance')

    def set_relative_tolerance_value(self, value):
        self._set_orref_value('relativeTolerance', value)

    def set_relative_tolerance_ref(self, ref):
        self._set_orref_ref('relativeTolerance', ref)

    def is_relative_tolerance_ref(self):
        return self._is_orref_ref('relativeTolerance')

    def is_set_relative_tolerance(self):
        return 'relativeTolerance' in self._values

    def unset_relative_tolerance(self):
        self._values.pop('relativeTolerance', None); self._orref_is_ref.pop('relativeTolerance', None)

    def get_absolute_tolerance_value(self):
        return self._get_orref_value('absoluteTolerance')

    def get_absolute_tolerance_ref(self):
        return self._get_orref_ref('absoluteTolerance')

    def set_absolute_tolerance_value(self, value):
        self._set_orref_value('absoluteTolerance', value)

    def set_absolute_tolerance_ref(self, ref):
        self._set_orref_ref('absoluteTolerance', ref)

    def is_absolute_tolerance_ref(self):
        return self._is_orref_ref('absoluteTolerance')

    def is_set_absolute_tolerance(self):
        return 'absoluteTolerance' in self._values

    def unset_absolute_tolerance(self):
        self._values.pop('absoluteTolerance', None); self._orref_is_ref.pop('absoluteTolerance', None)

    def get_absolute_tolerance_vector_value(self):
        return self._get_orref_value('absoluteToleranceVector')

    def get_absolute_tolerance_vector_ref(self):
        return self._get_orref_ref('absoluteToleranceVector')

    def set_absolute_tolerance_vector_value(self, value):
        self._set_orref_value('absoluteToleranceVector', value)

    def set_absolute_tolerance_vector_ref(self, ref):
        self._set_orref_ref('absoluteToleranceVector', ref)

    def is_absolute_tolerance_vector_ref(self):
        return self._is_orref_ref('absoluteToleranceVector')

    def is_set_absolute_tolerance_vector(self):
        return 'absoluteToleranceVector' in self._values

    def unset_absolute_tolerance_vector(self):
        self._values.pop('absoluteToleranceVector', None); self._orref_is_ref.pop('absoluteToleranceVector', None)

    def get_absolute_tolerance_adjustment_factor_value(self):
        return self._get_orref_value('absoluteToleranceAdjustmentFactor')

    def get_absolute_tolerance_adjustment_factor_ref(self):
        return self._get_orref_ref('absoluteToleranceAdjustmentFactor')

    def set_absolute_tolerance_adjustment_factor_value(self, value):
        self._set_orref_value('absoluteToleranceAdjustmentFactor', value)

    def set_absolute_tolerance_adjustment_factor_ref(self, ref):
        self._set_orref_ref('absoluteToleranceAdjustmentFactor', ref)

    def is_absolute_tolerance_adjustment_factor_ref(self):
        return self._is_orref_ref('absoluteToleranceAdjustmentFactor')

    def is_set_absolute_tolerance_adjustment_factor(self):
        return 'absoluteToleranceAdjustmentFactor' in self._values

    def unset_absolute_tolerance_adjustment_factor(self):
        self._values.pop('absoluteToleranceAdjustmentFactor', None); self._orref_is_ref.pop('absoluteToleranceAdjustmentFactor', None)

    def get_tolerance_for_root_finder_value(self):
        return self._get_orref_value('toleranceForRootFinder')

    def get_tolerance_for_root_finder_ref(self):
        return self._get_orref_ref('toleranceForRootFinder')

    def set_tolerance_for_root_finder_value(self, value):
        self._set_orref_value('toleranceForRootFinder', value)

    def set_tolerance_for_root_finder_ref(self, ref):
        self._set_orref_ref('toleranceForRootFinder', ref)

    def is_tolerance_for_root_finder_ref(self):
        return self._is_orref_ref('toleranceForRootFinder')

    def is_set_tolerance_for_root_finder(self):
        return 'toleranceForRootFinder' in self._values

    def unset_tolerance_for_root_finder(self):
        self._values.pop('toleranceForRootFinder', None); self._orref_is_ref.pop('toleranceForRootFinder', None)

    def get_initial_step_size_value(self):
        return self._get_orref_value('initialStepSize')

    def get_initial_step_size_ref(self):
        return self._get_orref_ref('initialStepSize')

    def set_initial_step_size_value(self, value):
        self._set_orref_value('initialStepSize', value)

    def set_initial_step_size_ref(self, ref):
        self._set_orref_ref('initialStepSize', ref)

    def is_initial_step_size_ref(self):
        return self._is_orref_ref('initialStepSize')

    def is_set_initial_step_size(self):
        return 'initialStepSize' in self._values

    def unset_initial_step_size(self):
        self._values.pop('initialStepSize', None); self._orref_is_ref.pop('initialStepSize', None)

    def get_max_number_of_steps_value(self):
        return self._get_orref_value('maxNumberOfSteps')

    def get_max_number_of_steps_ref(self):
        return self._get_orref_ref('maxNumberOfSteps')

    def set_max_number_of_steps_value(self, value):
        self._set_orref_value('maxNumberOfSteps', value)

    def set_max_number_of_steps_ref(self, ref):
        self._set_orref_ref('maxNumberOfSteps', ref)

    def is_max_number_of_steps_ref(self):
        return self._is_orref_ref('maxNumberOfSteps')

    def is_set_max_number_of_steps(self):
        return 'maxNumberOfSteps' in self._values

    def unset_max_number_of_steps(self):
        self._values.pop('maxNumberOfSteps', None); self._orref_is_ref.pop('maxNumberOfSteps', None)

    def get_max_internal_steps_value(self):
        return self._get_orref_value('maxInternalSteps')

    def get_max_internal_steps_ref(self):
        return self._get_orref_ref('maxInternalSteps')

    def set_max_internal_steps_value(self, value):
        self._set_orref_value('maxInternalSteps', value)

    def set_max_internal_steps_ref(self, ref):
        self._set_orref_ref('maxInternalSteps', ref)

    def is_max_internal_steps_ref(self):
        return self._is_orref_ref('maxInternalSteps')

    def is_set_max_internal_steps(self):
        return 'maxInternalSteps' in self._values

    def unset_max_internal_steps(self):
        self._values.pop('maxInternalSteps', None); self._orref_is_ref.pop('maxInternalSteps', None)

    def get_max_internal_step_size_value(self):
        return self._get_orref_value('maxInternalStepSize')

    def get_max_internal_step_size_ref(self):
        return self._get_orref_ref('maxInternalStepSize')

    def set_max_internal_step_size_value(self, value):
        self._set_orref_value('maxInternalStepSize', value)

    def set_max_internal_step_size_ref(self, ref):
        self._set_orref_ref('maxInternalStepSize', ref)

    def is_max_internal_step_size_ref(self):
        return self._is_orref_ref('maxInternalStepSize')

    def is_set_max_internal_step_size(self):
        return 'maxInternalStepSize' in self._values

    def unset_max_internal_step_size(self):
        self._values.pop('maxInternalStepSize', None); self._orref_is_ref.pop('maxInternalStepSize', None)

    def get_min_internal_step_size_value(self):
        return self._get_orref_value('minInternalStepSize')

    def get_min_internal_step_size_ref(self):
        return self._get_orref_ref('minInternalStepSize')

    def set_min_internal_step_size_value(self, value):
        self._set_orref_value('minInternalStepSize', value)

    def set_min_internal_step_size_ref(self, ref):
        self._set_orref_ref('minInternalStepSize', ref)

    def is_min_internal_step_size_ref(self):
        return self._is_orref_ref('minInternalStepSize')

    def is_set_min_internal_step_size(self):
        return 'minInternalStepSize' in self._values

    def unset_min_internal_step_size(self):
        self._values.pop('minInternalStepSize', None); self._orref_is_ref.pop('minInternalStepSize', None)

    def get_force_physical_correctness_value(self):
        return self._get_orref_value('forcePhysicalCorrectness')

    def get_force_physical_correctness_ref(self):
        return self._get_orref_ref('forcePhysicalCorrectness')

    def set_force_physical_correctness_value(self, value):
        self._set_orref_value('forcePhysicalCorrectness', value)

    def set_force_physical_correctness_ref(self, ref):
        self._set_orref_ref('forcePhysicalCorrectness', ref)

    def is_force_physical_correctness_ref(self):
        return self._is_orref_ref('forcePhysicalCorrectness')

    def is_set_force_physical_correctness(self):
        return 'forcePhysicalCorrectness' in self._values

    def unset_force_physical_correctness(self):
        self._values.pop('forcePhysicalCorrectness', None); self._orref_is_ref.pop('forcePhysicalCorrectness', None)

    def get_integrate_reduced_model_value(self):
        return self._get_orref_value('integrateReducedModel')

    def get_integrate_reduced_model_ref(self):
        return self._get_orref_ref('integrateReducedModel')

    def set_integrate_reduced_model_value(self, value):
        self._set_orref_value('integrateReducedModel', value)

    def set_integrate_reduced_model_ref(self, ref):
        self._set_orref_ref('integrateReducedModel', ref)

    def is_integrate_reduced_model_ref(self):
        return self._is_orref_ref('integrateReducedModel')

    def is_set_integrate_reduced_model(self):
        return 'integrateReducedModel' in self._values

    def unset_integrate_reduced_model(self):
        self._values.pop('integrateReducedModel', None); self._orref_is_ref.pop('integrateReducedModel', None)

    def get_use_reduced_model_value(self):
        return self._get_orref_value('useReducedModel')

    def get_use_reduced_model_ref(self):
        return self._get_orref_ref('useReducedModel')

    def set_use_reduced_model_value(self, value):
        self._set_orref_value('useReducedModel', value)

    def set_use_reduced_model_ref(self, ref):
        self._set_orref_ref('useReducedModel', ref)

    def is_use_reduced_model_ref(self):
        return self._is_orref_ref('useReducedModel')

    def is_set_use_reduced_model(self):
        return 'useReducedModel' in self._values

    def unset_use_reduced_model(self):
        self._values.pop('useReducedModel', None); self._orref_is_ref.pop('useReducedModel', None)

    def get_use_stiff_solver_value(self):
        return self._get_orref_value('useStiffSolver')

    def get_use_stiff_solver_ref(self):
        return self._get_orref_ref('useStiffSolver')

    def set_use_stiff_solver_value(self, value):
        self._set_orref_value('useStiffSolver', value)

    def set_use_stiff_solver_ref(self, ref):
        self._set_orref_ref('useStiffSolver', ref)

    def is_use_stiff_solver_ref(self):
        return self._is_orref_ref('useStiffSolver')

    def is_set_use_stiff_solver(self):
        return 'useStiffSolver' in self._values

    def unset_use_stiff_solver(self):
        self._values.pop('useStiffSolver', None); self._orref_is_ref.pop('useStiffSolver', None)

    def get_max_b_d_forder_value(self):
        return self._get_orref_value('maxBDForder')

    def get_max_b_d_forder_ref(self):
        return self._get_orref_ref('maxBDForder')

    def set_max_b_d_forder_value(self, value):
        self._set_orref_value('maxBDForder', value)

    def set_max_b_d_forder_ref(self, ref):
        self._set_orref_ref('maxBDForder', ref)

    def is_max_b_d_forder_ref(self):
        return self._is_orref_ref('maxBDForder')

    def is_set_max_b_d_forder(self):
        return 'maxBDForder' in self._values

    def unset_max_b_d_forder(self):
        self._values.pop('maxBDForder', None); self._orref_is_ref.pop('maxBDForder', None)

    def get_max_adams_order_value(self):
        return self._get_orref_value('maxAdamsOrder')

    def get_max_adams_order_ref(self):
        return self._get_orref_ref('maxAdamsOrder')

    def set_max_adams_order_value(self, value):
        self._set_orref_value('maxAdamsOrder', value)

    def set_max_adams_order_ref(self, ref):
        self._set_orref_ref('maxAdamsOrder', ref)

    def is_max_adams_order_ref(self):
        return self._is_orref_ref('maxAdamsOrder')

    def is_set_max_adams_order(self):
        return 'maxAdamsOrder' in self._values

    def unset_max_adams_order(self):
        self._values.pop('maxAdamsOrder', None); self._orref_is_ref.pop('maxAdamsOrder', None)

    def get_variable_step_size_value(self):
        return self._get_orref_value('variableStepSize')

    def get_variable_step_size_ref(self):
        return self._get_orref_ref('variableStepSize')

    def set_variable_step_size_value(self, value):
        self._set_orref_value('variableStepSize', value)

    def set_variable_step_size_ref(self, ref):
        self._set_orref_ref('variableStepSize', ref)

    def is_variable_step_size_ref(self):
        return self._is_orref_ref('variableStepSize')

    def is_set_variable_step_size(self):
        return 'variableStepSize' in self._values

    def unset_variable_step_size(self):
        self._values.pop('variableStepSize', None); self._orref_is_ref.pop('variableStepSize', None)

    def get_max_output_rows_value(self):
        return self._get_orref_value('maxOutputRows')

    def get_max_output_rows_ref(self):
        return self._get_orref_ref('maxOutputRows')

    def set_max_output_rows_value(self, value):
        self._set_orref_value('maxOutputRows', value)

    def set_max_output_rows_ref(self, ref):
        self._set_orref_ref('maxOutputRows', ref)

    def is_max_output_rows_ref(self):
        return self._is_orref_ref('maxOutputRows')

    def is_set_max_output_rows(self):
        return 'maxOutputRows' in self._values

    def unset_max_output_rows(self):
        self._values.pop('maxOutputRows', None); self._orref_is_ref.pop('maxOutputRows', None)

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_independent_variable_init_value(self):
        return self._get_orref_value('independentVariableInit')

    def get_independent_variable_init_ref(self):
        return self._get_orref_ref('independentVariableInit')

    def set_independent_variable_init_value(self, value):
        self._set_orref_value('independentVariableInit', value)

    def set_independent_variable_init_ref(self, ref):
        self._set_orref_ref('independentVariableInit', ref)

    def is_independent_variable_init_ref(self):
        return self._is_orref_ref('independentVariableInit')

    def is_set_independent_variable_init(self):
        return 'independentVariableInit' in self._values

    def unset_independent_variable_init(self):
        self._values.pop('independentVariableInit', None); self._orref_is_ref.pop('independentVariableInit', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_independent_variable_range(self):
        if self._independent_variable_range is None: raise ApiError('independent_variable_range is not set')
        return self._independent_variable_range

    def set_independent_variable_range(self, obj):
        self._independent_variable_range = obj; obj._attach(self, self.get_document())

    def is_set_independent_variable_range(self):
        return self._independent_variable_range is not None

    def unset_independent_variable_range(self):
        self._independent_variable_range = None

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        if self._independent_variable_range is not None: kids.append(self._independent_variable_range)
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._independent_variable_range is not None: out.append((self._independent_variable_range, '/independentVariableRange'))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'explicitODESimulation')
        if 'relativeTolerance' in self._values: d['relativeTolerance'] = self._values['relativeTolerance']
        if 'absoluteTolerance' in self._values: d['absoluteTolerance'] = self._values['absoluteTolerance']
        if 'absoluteToleranceVector' in self._values: d['absoluteToleranceVector'] = self._values['absoluteToleranceVector']
        if 'absoluteToleranceAdjustmentFactor' in self._values: d['absoluteToleranceAdjustmentFactor'] = self._values['absoluteToleranceAdjustmentFactor']
        if 'toleranceForRootFinder' in self._values: d['toleranceForRootFinder'] = self._values['toleranceForRootFinder']
        if 'initialStepSize' in self._values: d['initialStepSize'] = self._values['initialStepSize']
        if 'maxNumberOfSteps' in self._values: d['maxNumberOfSteps'] = self._values['maxNumberOfSteps']
        if 'maxInternalSteps' in self._values: d['maxInternalSteps'] = self._values['maxInternalSteps']
        if 'maxInternalStepSize' in self._values: d['maxInternalStepSize'] = self._values['maxInternalStepSize']
        if 'minInternalStepSize' in self._values: d['minInternalStepSize'] = self._values['minInternalStepSize']
        if 'forcePhysicalCorrectness' in self._values: d['forcePhysicalCorrectness'] = self._values['forcePhysicalCorrectness']
        if 'integrateReducedModel' in self._values: d['integrateReducedModel'] = self._values['integrateReducedModel']
        if 'useReducedModel' in self._values: d['useReducedModel'] = self._values['useReducedModel']
        if 'useStiffSolver' in self._values: d['useStiffSolver'] = self._values['useStiffSolver']
        if 'maxBDForder' in self._values: d['maxBDForder'] = self._values['maxBDForder']
        if 'maxAdamsOrder' in self._values: d['maxAdamsOrder'] = self._values['maxAdamsOrder']
        if 'variableStepSize' in self._values: d['variableStepSize'] = self._values['variableStepSize']
        if 'maxOutputRows' in self._values: d['maxOutputRows'] = self._values['maxOutputRows']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._independent_variable_range is not None: d['independentVariableRange'] = self._independent_variable_range.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ExplicitStochasticSimulation(SedBase):
    """Generated from specsheets/tasks/ExplicitStochasticSimulation/."""
    _FIELDS = [FieldSpec('seed', 'NumberOrRef', False, 'AbstractStochasticSimulation-0001', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0002', item_kind=None, ref_target=None), FieldSpec('timeDependentRelativeTolerance', 'NumberOrRef', False, 'AbstractStochasticSimulation-0003', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0004', item_kind=None, ref_target=None), FieldSpec('variableStepSize', 'BooleanOrRef', False, 'AbstractStochasticSimulation-0005', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0006', item_kind=None, ref_target=None), FieldSpec('minimumTimeStep', 'NumberOrRef', False, 'AbstractStochasticSimulation-0007', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0008', item_kind=None, ref_target=None), FieldSpec('maximumTimeStep', 'NumberOrRef', False, 'AbstractStochasticSimulation-0009', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0010', item_kind=None, ref_target=None), FieldSpec('nonNegative', 'BooleanOrRef', False, 'AbstractStochasticSimulation-0011', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0012', item_kind=None, ref_target=None), FieldSpec('maxOutputRows', 'IntegerOrRef', False, 'AbstractStochasticSimulation-0013', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0014', item_kind=None, ref_target=None), FieldSpec('maxNumSteps', 'IntegerOrRef', False, 'AbstractStochasticSimulation-0015', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0016', item_kind=None, ref_target=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'AbstractSimulation-0002', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0003', item_kind=None, ref_target=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, 'AbstractSimulation-0004', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0005', item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', False, 'AbstractSimulation-0006', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0007', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('independentVariableRange', 'ref-class', True, 'ExplicitStochasticSimulation-0005', 'ExplicitStochasticSimulation-0004', 'ExplicitStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='NumericRange', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'independentVariableRange'}
    _TYPE_CONST = 'explicitStochasticSimulation'
    _TYPE_RULE_ID = 'ExplicitStochasticSimulation-0006'
    _OWN_CATCHALL = 'ExplicitStochasticSimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'independentVariableRange.numberOfSteps'}, 'labels': None}, {'size': {'source': 'static', 'expr': '1 + len(outputVariables)'}, 'labels': {'source': 'static', 'expr': '[independentVariable] + outputVariables'}}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()
        self._independent_variable_range = None

    def get_type(self):
        return 'explicitStochasticSimulation'

    def get_seed_value(self):
        return self._get_orref_value('seed')

    def get_seed_ref(self):
        return self._get_orref_ref('seed')

    def set_seed_value(self, value):
        self._set_orref_value('seed', value)

    def set_seed_ref(self, ref):
        self._set_orref_ref('seed', ref)

    def is_seed_ref(self):
        return self._is_orref_ref('seed')

    def is_set_seed(self):
        return 'seed' in self._values

    def unset_seed(self):
        self._values.pop('seed', None); self._orref_is_ref.pop('seed', None)

    def get_time_dependent_relative_tolerance_value(self):
        return self._get_orref_value('timeDependentRelativeTolerance')

    def get_time_dependent_relative_tolerance_ref(self):
        return self._get_orref_ref('timeDependentRelativeTolerance')

    def set_time_dependent_relative_tolerance_value(self, value):
        self._set_orref_value('timeDependentRelativeTolerance', value)

    def set_time_dependent_relative_tolerance_ref(self, ref):
        self._set_orref_ref('timeDependentRelativeTolerance', ref)

    def is_time_dependent_relative_tolerance_ref(self):
        return self._is_orref_ref('timeDependentRelativeTolerance')

    def is_set_time_dependent_relative_tolerance(self):
        return 'timeDependentRelativeTolerance' in self._values

    def unset_time_dependent_relative_tolerance(self):
        self._values.pop('timeDependentRelativeTolerance', None); self._orref_is_ref.pop('timeDependentRelativeTolerance', None)

    def get_variable_step_size_value(self):
        return self._get_orref_value('variableStepSize')

    def get_variable_step_size_ref(self):
        return self._get_orref_ref('variableStepSize')

    def set_variable_step_size_value(self, value):
        self._set_orref_value('variableStepSize', value)

    def set_variable_step_size_ref(self, ref):
        self._set_orref_ref('variableStepSize', ref)

    def is_variable_step_size_ref(self):
        return self._is_orref_ref('variableStepSize')

    def is_set_variable_step_size(self):
        return 'variableStepSize' in self._values

    def unset_variable_step_size(self):
        self._values.pop('variableStepSize', None); self._orref_is_ref.pop('variableStepSize', None)

    def get_minimum_time_step_value(self):
        return self._get_orref_value('minimumTimeStep')

    def get_minimum_time_step_ref(self):
        return self._get_orref_ref('minimumTimeStep')

    def set_minimum_time_step_value(self, value):
        self._set_orref_value('minimumTimeStep', value)

    def set_minimum_time_step_ref(self, ref):
        self._set_orref_ref('minimumTimeStep', ref)

    def is_minimum_time_step_ref(self):
        return self._is_orref_ref('minimumTimeStep')

    def is_set_minimum_time_step(self):
        return 'minimumTimeStep' in self._values

    def unset_minimum_time_step(self):
        self._values.pop('minimumTimeStep', None); self._orref_is_ref.pop('minimumTimeStep', None)

    def get_maximum_time_step_value(self):
        return self._get_orref_value('maximumTimeStep')

    def get_maximum_time_step_ref(self):
        return self._get_orref_ref('maximumTimeStep')

    def set_maximum_time_step_value(self, value):
        self._set_orref_value('maximumTimeStep', value)

    def set_maximum_time_step_ref(self, ref):
        self._set_orref_ref('maximumTimeStep', ref)

    def is_maximum_time_step_ref(self):
        return self._is_orref_ref('maximumTimeStep')

    def is_set_maximum_time_step(self):
        return 'maximumTimeStep' in self._values

    def unset_maximum_time_step(self):
        self._values.pop('maximumTimeStep', None); self._orref_is_ref.pop('maximumTimeStep', None)

    def get_non_negative_value(self):
        return self._get_orref_value('nonNegative')

    def get_non_negative_ref(self):
        return self._get_orref_ref('nonNegative')

    def set_non_negative_value(self, value):
        self._set_orref_value('nonNegative', value)

    def set_non_negative_ref(self, ref):
        self._set_orref_ref('nonNegative', ref)

    def is_non_negative_ref(self):
        return self._is_orref_ref('nonNegative')

    def is_set_non_negative(self):
        return 'nonNegative' in self._values

    def unset_non_negative(self):
        self._values.pop('nonNegative', None); self._orref_is_ref.pop('nonNegative', None)

    def get_max_output_rows_value(self):
        return self._get_orref_value('maxOutputRows')

    def get_max_output_rows_ref(self):
        return self._get_orref_ref('maxOutputRows')

    def set_max_output_rows_value(self, value):
        self._set_orref_value('maxOutputRows', value)

    def set_max_output_rows_ref(self, ref):
        self._set_orref_ref('maxOutputRows', ref)

    def is_max_output_rows_ref(self):
        return self._is_orref_ref('maxOutputRows')

    def is_set_max_output_rows(self):
        return 'maxOutputRows' in self._values

    def unset_max_output_rows(self):
        self._values.pop('maxOutputRows', None); self._orref_is_ref.pop('maxOutputRows', None)

    def get_max_num_steps_value(self):
        return self._get_orref_value('maxNumSteps')

    def get_max_num_steps_ref(self):
        return self._get_orref_ref('maxNumSteps')

    def set_max_num_steps_value(self, value):
        self._set_orref_value('maxNumSteps', value)

    def set_max_num_steps_ref(self, ref):
        self._set_orref_ref('maxNumSteps', ref)

    def is_max_num_steps_ref(self):
        return self._is_orref_ref('maxNumSteps')

    def is_set_max_num_steps(self):
        return 'maxNumSteps' in self._values

    def unset_max_num_steps(self):
        self._values.pop('maxNumSteps', None); self._orref_is_ref.pop('maxNumSteps', None)

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_independent_variable_init_value(self):
        return self._get_orref_value('independentVariableInit')

    def get_independent_variable_init_ref(self):
        return self._get_orref_ref('independentVariableInit')

    def set_independent_variable_init_value(self, value):
        self._set_orref_value('independentVariableInit', value)

    def set_independent_variable_init_ref(self, ref):
        self._set_orref_ref('independentVariableInit', ref)

    def is_independent_variable_init_ref(self):
        return self._is_orref_ref('independentVariableInit')

    def is_set_independent_variable_init(self):
        return 'independentVariableInit' in self._values

    def unset_independent_variable_init(self):
        self._values.pop('independentVariableInit', None); self._orref_is_ref.pop('independentVariableInit', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_independent_variable_range(self):
        if self._independent_variable_range is None: raise ApiError('independent_variable_range is not set')
        return self._independent_variable_range

    def set_independent_variable_range(self, obj):
        self._independent_variable_range = obj; obj._attach(self, self.get_document())

    def is_set_independent_variable_range(self):
        return self._independent_variable_range is not None

    def unset_independent_variable_range(self):
        self._independent_variable_range = None

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        if self._independent_variable_range is not None: kids.append(self._independent_variable_range)
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._independent_variable_range is not None: out.append((self._independent_variable_range, '/independentVariableRange'))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'explicitStochasticSimulation')
        if 'seed' in self._values: d['seed'] = self._values['seed']
        if 'timeDependentRelativeTolerance' in self._values: d['timeDependentRelativeTolerance'] = self._values['timeDependentRelativeTolerance']
        if 'variableStepSize' in self._values: d['variableStepSize'] = self._values['variableStepSize']
        if 'minimumTimeStep' in self._values: d['minimumTimeStep'] = self._values['minimumTimeStep']
        if 'maximumTimeStep' in self._values: d['maximumTimeStep'] = self._values['maximumTimeStep']
        if 'nonNegative' in self._values: d['nonNegative'] = self._values['nonNegative']
        if 'maxOutputRows' in self._values: d['maxOutputRows'] = self._values['maxOutputRows']
        if 'maxNumSteps' in self._values: d['maxNumSteps'] = self._values['maxNumSteps']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._independent_variable_range is not None: d['independentVariableRange'] = self._independent_variable_range.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class FluxBalanceAnalysis(SedBase):
    """Generated from specsheets/tasks/FluxBalanceAnalysis/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'FluxBalanceAnalysis-0002', 'FluxBalanceAnalysis-0001', 'FluxBalanceAnalysis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('outputVariables', 'ArrayOrRef', True, 'FluxBalanceAnalysis-0004', 'FluxBalanceAnalysis-0003', 'FluxBalanceAnalysis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='FluxBalanceAnalysis-0005', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'FluxBalanceAnalysis-0009', None, 'FluxBalanceAnalysis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'model', 'outputVariables'}
    _TYPE_CONST = 'fluxBalanceAnalysis'
    _TYPE_RULE_ID = 'FluxBalanceAnalysis-0008'
    _OWN_CATCHALL = 'FluxBalanceAnalysis-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(outputVariables)'}, 'labels': {'source': 'static', 'expr': 'outputVariables'}}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'fluxBalanceAnalysis'

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'fluxBalanceAnalysis')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class JacobianFull(SedBase):
    """Generated from specsheets/tasks/JacobianFull/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'JacobianFull-0002', 'JacobianFull-0001', 'JacobianFull-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'model'}
    _TYPE_CONST = 'jacobianFull'
    _TYPE_RULE_ID = 'JacobianFull-0003'
    _OWN_CATCHALL = 'JacobianFull-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'input-file', 'from': 'model', 'extract': 'floatingSpeciesIds', 'note': 'row count = number of species in the referenced model'}, 'labels': {'source': 'input-file', 'from': 'model', 'extract': 'floatingSpeciesIds', 'note': "row labels = the model's ordered species list"}}, {'size': {'source': 'input-file', 'from': 'model', 'extract': 'floatingSpeciesIds', 'note': 'column count = number of species in the referenced model'}, 'labels': {'source': 'input-file', 'from': 'model', 'extract': 'floatingSpeciesIds', 'note': "column labels = the model's ordered species list"}}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'jacobianFull'

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'jacobianFull')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class JacobianReduced(SedBase):
    """Generated from specsheets/tasks/JacobianReduced/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'JacobianReduced-0002', 'JacobianReduced-0001', 'JacobianReduced-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'model'}
    _TYPE_CONST = 'jacobianReduced'
    _TYPE_RULE_ID = 'JacobianReduced-0003'
    _OWN_CATCHALL = 'JacobianReduced-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'input-file', 'from': 'model', 'extract': 'reducedFloatingSpeciesIds', 'note': "row count = number of species in the referenced model's reduced species set"}, 'labels': {'source': 'input-file', 'from': 'model', 'extract': 'reducedFloatingSpeciesIds', 'note': "row labels = the model's ordered, reduced species list"}}, {'size': {'source': 'input-file', 'from': 'model', 'extract': 'reducedFloatingSpeciesIds', 'note': "column count = number of species in the referenced model's reduced species set"}, 'labels': {'source': 'input-file', 'from': 'model', 'extract': 'reducedFloatingSpeciesIds', 'note': "column labels = the model's ordered, reduced species list"}}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'jacobianReduced'

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'jacobianReduced')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Loop(SedBase):
    """Generated from specsheets/tasks/Loop/."""
    _FIELDS = [FieldSpec('outputVariableMap', 'DictOrRef', False, 'Repeat-0002', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Repeat-0003', item_kind='ref', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('loopVariables', 'dict', True, 'Loop-0003', 'Loop-0002', 'Loop-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='LoopVariable', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('subTasks', 'dict', False, 'Repeat-0001', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('aggregateOutputVariables', 'dict', False, 'Repeat-0004', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='AggregationCalculation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('range', 'ref-discriminator', True, 'Loop-0007', 'Loop-0006', 'Loop-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='RangeInline', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'loopVariables', 'range'}
    _TYPE_CONST = 'loop'
    _TYPE_RULE_ID = 'Loop-0005'
    _OWN_CATCHALL = 'Loop-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(range)'}, 'labels': {'source': 'runtime', 'note': "the range's values, written as text the way numbers appear in formed strings (an integral value without a decimal point: 1, 2; otherwise 0.5, 0.25); known only once the range is expanded, so a label index here is not checked ahead of time"}, 'note': "dimension 0 is the iteration: one row per value in range, labeled by those values (there is no separate column holding the range values); len(range) dispatches on range's actual Range/NumericRange/ParameterRange type"}, {'size': {'source': 'static', 'expr': 'len(outputVariableMap)'}, 'labels': {'source': 'static', 'expr': 'keys(outputVariableMap)'}, 'note': 'dimension 1 holds the outputVariableMap entries, one per key, labeled by the keys; length 0 if outputVariableMap is empty'}, {'trailing': {'of': 'outputVariableMap', 'note': "the dimensions of the outputVariableMap entries' own values, if they have any, follow (all entries must have the same shape, since they are stacked into one array); how many there are is not known ahead of time"}}]}, '[id].aggregates': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(aggregateOutputVariables)'}, 'labels': None, 'note': "each entry collapses the iteration dimension of [id] to a single value (per Repeat, the applied dimension defaults to this Loop's own iterations), unless the underlying subTask output was itself multi-dimensional, in which case that dimensionality carries through per entry"}, {'trailing': {'of': 'aggregateOutputVariables', 'note': 'if the underlying subTask output was itself multi-dimensional, that dimensionality carries through per entry; how many dimensions that is is not known ahead of time'}}]}, '[id].range': {'type': 'annotatedData', 'dimensions': [], 'note': 'the current value of range, within the loop'}, '[id].index': {'type': 'annotatedData', 'dimensions': [], 'note': 'the current index into range, within the loop'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._loop_variables = IdKeyedCollection(lambda tv, _cls=LoopVariable: (_cls, False))
        self._sub_tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._aggregate_output_variables = IdKeyedCollection(lambda tv, _cls=AggregationCalculation: (_cls, False))
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()
        self._range = None

    def get_type(self):
        return 'loop'

    def get_output_variable_map_value(self):
        return self._get_orref_value('outputVariableMap')

    def get_output_variable_map_ref(self):
        return self._get_orref_ref('outputVariableMap')

    def set_output_variable_map_value(self, value):
        self._set_orref_value('outputVariableMap', value)

    def set_output_variable_map_ref(self, ref):
        self._set_orref_ref('outputVariableMap', ref)

    def is_output_variable_map_ref(self):
        return self._is_orref_ref('outputVariableMap')

    def is_set_output_variable_map(self):
        return 'outputVariableMap' in self._values

    def unset_output_variable_map(self):
        self._values.pop('outputVariableMap', None); self._orref_is_ref.pop('outputVariableMap', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_loop_variables(self):
        return self._loop_variables.ids()

    def get_loop_variables_item(self, item_id):
        return self._loop_variables.get(item_id)

    def add_loop_variables(self, item_id, obj):
        self._loop_variables.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_loop_variables(self, index, item_id, obj):
        self._loop_variables.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_loop_variables(self, item_id):
        self._loop_variables.remove(item_id)

    def set_id_on_loop_variables(self, old_id, new_id):
        self._loop_variables.set_id(old_id, new_id)

    def get_sub_tasks(self):
        return self._sub_tasks.ids()

    def get_sub_tasks_item(self, item_id):
        return self._sub_tasks.get(item_id)

    def add_sub_tasks(self, item_id, obj):
        self._sub_tasks.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_sub_tasks(self, index, item_id, obj):
        self._sub_tasks.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_sub_tasks(self, item_id):
        self._sub_tasks.remove(item_id)

    def set_id_on_sub_tasks(self, old_id, new_id):
        self._sub_tasks.set_id(old_id, new_id)

    def get_aggregate_output_variables(self):
        return self._aggregate_output_variables.ids()

    def get_aggregate_output_variables_item(self, item_id):
        return self._aggregate_output_variables.get(item_id)

    def add_aggregate_output_variables(self, item_id, obj):
        self._aggregate_output_variables.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_aggregate_output_variables(self, index, item_id, obj):
        self._aggregate_output_variables.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_aggregate_output_variables(self, item_id):
        self._aggregate_output_variables.remove(item_id)

    def set_id_on_aggregate_output_variables(self, old_id, new_id):
        self._aggregate_output_variables.set_id(old_id, new_id)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_range(self):
        if self._range is None: raise ApiError('range is not set')
        return self._range

    def set_range(self, obj):
        self._range = obj; obj._attach(self, self.get_document())

    def is_set_range(self):
        return self._range is not None

    def unset_range(self):
        self._range = None

    def _children(self):
        kids = []
        kids.extend(self._loop_variables.get(i) for i in self._loop_variables.ids())
        kids.extend(self._sub_tasks.get(i) for i in self._sub_tasks.ids())
        kids.extend(self._aggregate_output_variables.get(i) for i in self._aggregate_output_variables.ids())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        if self._range is not None: kids.append(self._range)
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'loopVariables': return self._loop_variables
        if field_name == 'subTasks': return self._sub_tasks
        if field_name == 'aggregateOutputVariables': return self._aggregate_output_variables
        return None

    def _children_with_locations(self):
        out = []
        for i in self._loop_variables.ids():
            out.append((self._loop_variables.get(i), '/loopVariables/' + i))
        for i in self._sub_tasks.ids():
            out.append((self._sub_tasks.get(i), '/subTasks/' + i))
        for i in self._aggregate_output_variables.ids():
            out.append((self._aggregate_output_variables.get(i), '/aggregateOutputVariables/' + i))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._range is not None: out.append((self._range, '/range'))
        return out

    def _id_collection_names(self):
        return ['loopVariables', 'subTasks', 'aggregateOutputVariables']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'loop')
        if 'outputVariableMap' in self._values: d['outputVariableMap'] = self._values['outputVariableMap']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._loop_variables): d['loopVariables'] = {i: self._loop_variables.get(i).to_json_value() for i in self._loop_variables.ids()}
        if len(self._sub_tasks): d['subTasks'] = {i: self._sub_tasks.get(i).to_json_value() for i in self._sub_tasks.ids()}
        if len(self._aggregate_output_variables): d['aggregateOutputVariables'] = {i: self._aggregate_output_variables.get(i).to_json_value() for i in self._aggregate_output_variables.ids()}
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._range is not None: d['range'] = self._range.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ModelChange(SedBase):
    """Generated from specsheets/tasks/ModelChange/."""
    _FIELDS = [FieldSpec('inputModel', 'SIdRef', True, 'ModelChange-0002', 'ModelChange-0001', 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('setValues', 'DictOrRef', False, 'ModelChange-0003', None, 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelChange-0004', item_kind='any', ref_target=None), FieldSpec('removeElements', 'ArrayOrRef', False, 'ModelChange-0005', None, 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelChange-0006', item_kind='string', ref_target=None), FieldSpec('addElements', 'ArrayOrRef', False, 'ModelChange-0007', None, 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelChange-0008', item_kind='string', ref_target=None), FieldSpec('replaceElements', 'DictOrRef', False, 'ModelChange-0009', None, 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelChange-0010', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'inputModel'}
    _TYPE_CONST = 'modelChange'
    _TYPE_RULE_ID = 'ModelChange-0011'
    _OWN_CATCHALL = 'ModelChange-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'modelChange'

    def get_input_model(self):
        if 'inputModel' not in self._values: raise ApiError('input_model is not set')
        return self._values['inputModel']

    def set_input_model(self, value):
        self._values['inputModel'] = value

    def is_set_input_model(self):
        return 'inputModel' in self._values

    def unset_input_model(self):
        self._values.pop('inputModel', None)

    def get_set_values_value(self):
        return self._get_orref_value('setValues')

    def get_set_values_ref(self):
        return self._get_orref_ref('setValues')

    def set_set_values_value(self, value):
        self._set_orref_value('setValues', value)

    def set_set_values_ref(self, ref):
        self._set_orref_ref('setValues', ref)

    def is_set_values_ref(self):
        return self._is_orref_ref('setValues')

    def is_set_set_values(self):
        return 'setValues' in self._values

    def unset_set_values(self):
        self._values.pop('setValues', None); self._orref_is_ref.pop('setValues', None)

    def get_remove_elements_value(self):
        return self._get_orref_value('removeElements')

    def get_remove_elements_ref(self):
        return self._get_orref_ref('removeElements')

    def set_remove_elements_value(self, value):
        self._set_orref_value('removeElements', value)

    def set_remove_elements_ref(self, ref):
        self._set_orref_ref('removeElements', ref)

    def is_remove_elements_ref(self):
        return self._is_orref_ref('removeElements')

    def is_set_remove_elements(self):
        return 'removeElements' in self._values

    def unset_remove_elements(self):
        self._values.pop('removeElements', None); self._orref_is_ref.pop('removeElements', None)

    def get_add_elements_value(self):
        return self._get_orref_value('addElements')

    def get_add_elements_ref(self):
        return self._get_orref_ref('addElements')

    def set_add_elements_value(self, value):
        self._set_orref_value('addElements', value)

    def set_add_elements_ref(self, ref):
        self._set_orref_ref('addElements', ref)

    def is_add_elements_ref(self):
        return self._is_orref_ref('addElements')

    def is_set_add_elements(self):
        return 'addElements' in self._values

    def unset_add_elements(self):
        self._values.pop('addElements', None); self._orref_is_ref.pop('addElements', None)

    def get_replace_elements_value(self):
        return self._get_orref_value('replaceElements')

    def get_replace_elements_ref(self):
        return self._get_orref_ref('replaceElements')

    def set_replace_elements_value(self, value):
        self._set_orref_value('replaceElements', value)

    def set_replace_elements_ref(self, ref):
        self._set_orref_ref('replaceElements', ref)

    def is_replace_elements_ref(self):
        return self._is_orref_ref('replaceElements')

    def is_set_replace_elements(self):
        return 'replaceElements' in self._values

    def unset_replace_elements(self):
        self._values.pop('replaceElements', None); self._orref_is_ref.pop('replaceElements', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'modelChange')
        if 'inputModel' in self._values: d['inputModel'] = self._values['inputModel']
        if 'setValues' in self._values: d['setValues'] = self._values['setValues']
        if 'removeElements' in self._values: d['removeElements'] = self._values['removeElements']
        if 'addElements' in self._values: d['addElements'] = self._values['addElements']
        if 'replaceElements' in self._values: d['replaceElements'] = self._values['replaceElements']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ModelElementList(SedBase):
    """Generated from specsheets/tasks/ModelElementList/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'ModelElementList-0002', 'ModelElementList-0001', 'ModelElementList-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('includeElements', 'ArrayOrRef', False, 'ModelElementList-0003', None, 'ModelElementList-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelElementList-0004', item_kind='string', ref_target=None), FieldSpec('includeTypes', 'ArrayOrRef', False, 'ModelElementList-0005', None, 'ModelElementList-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelElementList-0006', item_kind='string', ref_target=None), FieldSpec('excludeElements', 'ArrayOrRef', False, 'ModelElementList-0007', None, 'ModelElementList-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelElementList-0008', item_kind='string', ref_target=None), FieldSpec('excludeTypes', 'ArrayOrRef', False, 'ModelElementList-0009', None, 'ModelElementList-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ModelElementList-0010', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'model'}
    _TYPE_CONST = 'modelElementList'
    _TYPE_RULE_ID = 'ModelElementList-0011'
    _OWN_CATCHALL = 'ModelElementList-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id].strings': {'type': 'stringList', 'dimensions': [{'size': {'source': 'input-file', 'from': 'model', 'extract': 'matchedElementIds', 'note': 'length = number of elements in the referenced model matched after includeElements/includeTypes/excludeElements/excludeTypes filtering'}, 'labels': {'source': 'input-file', 'from': 'model', 'extract': 'matchedElementIds', 'note': 'the matched element ids themselves'}}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'modelElementList'

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_include_elements_value(self):
        return self._get_orref_value('includeElements')

    def get_include_elements_ref(self):
        return self._get_orref_ref('includeElements')

    def set_include_elements_value(self, value):
        self._set_orref_value('includeElements', value)

    def set_include_elements_ref(self, ref):
        self._set_orref_ref('includeElements', ref)

    def is_include_elements_ref(self):
        return self._is_orref_ref('includeElements')

    def is_set_include_elements(self):
        return 'includeElements' in self._values

    def unset_include_elements(self):
        self._values.pop('includeElements', None); self._orref_is_ref.pop('includeElements', None)

    def get_include_types_value(self):
        return self._get_orref_value('includeTypes')

    def get_include_types_ref(self):
        return self._get_orref_ref('includeTypes')

    def set_include_types_value(self, value):
        self._set_orref_value('includeTypes', value)

    def set_include_types_ref(self, ref):
        self._set_orref_ref('includeTypes', ref)

    def is_include_types_ref(self):
        return self._is_orref_ref('includeTypes')

    def is_set_include_types(self):
        return 'includeTypes' in self._values

    def unset_include_types(self):
        self._values.pop('includeTypes', None); self._orref_is_ref.pop('includeTypes', None)

    def get_exclude_elements_value(self):
        return self._get_orref_value('excludeElements')

    def get_exclude_elements_ref(self):
        return self._get_orref_ref('excludeElements')

    def set_exclude_elements_value(self, value):
        self._set_orref_value('excludeElements', value)

    def set_exclude_elements_ref(self, ref):
        self._set_orref_ref('excludeElements', ref)

    def is_exclude_elements_ref(self):
        return self._is_orref_ref('excludeElements')

    def is_set_exclude_elements(self):
        return 'excludeElements' in self._values

    def unset_exclude_elements(self):
        self._values.pop('excludeElements', None); self._orref_is_ref.pop('excludeElements', None)

    def get_exclude_types_value(self):
        return self._get_orref_value('excludeTypes')

    def get_exclude_types_ref(self):
        return self._get_orref_ref('excludeTypes')

    def set_exclude_types_value(self, value):
        self._set_orref_value('excludeTypes', value)

    def set_exclude_types_ref(self, ref):
        self._set_orref_ref('excludeTypes', ref)

    def is_exclude_types_ref(self):
        return self._is_orref_ref('excludeTypes')

    def is_set_exclude_types(self):
        return 'excludeTypes' in self._values

    def unset_exclude_types(self):
        self._values.pop('excludeTypes', None); self._orref_is_ref.pop('excludeTypes', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'modelElementList')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'includeElements' in self._values: d['includeElements'] = self._values['includeElements']
        if 'includeTypes' in self._values: d['includeTypes'] = self._values['includeTypes']
        if 'excludeElements' in self._values: d['excludeElements'] = self._values['excludeElements']
        if 'excludeTypes' in self._values: d['excludeTypes'] = self._values['excludeTypes']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ModelImport(SedBase):
    """Generated from specsheets/tasks/ModelImport/."""
    _FIELDS = [FieldSpec('location', 'StringOrRef', True, 'ModelImport-0002', 'ModelImport-0001', 'ModelImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=1, enum=None, ref_type_rule_id='ModelImport-0003', item_kind=None, ref_target=None), FieldSpec('language', 'StringOrRef', True, 'ModelImport-0005', 'ModelImport-0004', 'ModelImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=1, enum=None, ref_type_rule_id='ModelImport-0006', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'location', 'language'}
    _TYPE_CONST = 'modelImport'
    _TYPE_RULE_ID = 'ModelImport-0007'
    _OWN_CATCHALL = 'ModelImport-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'modelImport'

    def get_location_value(self):
        return self._get_orref_value('location')

    def get_location_ref(self):
        return self._get_orref_ref('location')

    def set_location_value(self, value):
        self._set_orref_value('location', value)

    def set_location_ref(self, ref):
        self._set_orref_ref('location', ref)

    def is_location_ref(self):
        return self._is_orref_ref('location')

    def is_set_location(self):
        return 'location' in self._values

    def unset_location(self):
        self._values.pop('location', None); self._orref_is_ref.pop('location', None)

    def get_language_value(self):
        return self._get_orref_value('language')

    def get_language_ref(self):
        return self._get_orref_ref('language')

    def set_language_value(self, value):
        self._set_orref_value('language', value)

    def set_language_ref(self, ref):
        self._set_orref_ref('language', ref)

    def is_language_ref(self):
        return self._is_orref_ref('language')

    def is_set_language(self):
        return 'language' in self._values

    def unset_language(self):
        self._values.pop('language', None); self._orref_is_ref.pop('language', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'modelImport')
        if 'location' in self._values: d['location'] = self._values['location']
        if 'language' in self._values: d['language'] = self._values['language']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class NumericRange(SedBase):
    """Generated from specsheets/tasks/NumericRange/."""
    _FIELDS = [FieldSpec('start', 'NumberOrRef', False, 'NumericRange-0001', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0002', item_kind=None, ref_target=None), FieldSpec('end', 'NumberOrRef', False, 'NumericRange-0003', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0004', item_kind=None, ref_target=None), FieldSpec('interval', 'NumberOrRef', False, 'NumericRange-0005', None, 'NumericRange-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0006', item_kind=None, ref_target=None), FieldSpec('numberOfSteps', 'IntegerOrRef', False, 'NumericRange-0007', None, 'NumericRange-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0008', item_kind=None, ref_target=None), FieldSpec('scale', 'StringOrRef', False, 'NumericRange-0009', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('linear', 'log10'), ref_type_rule_id='NumericRange-0010', item_kind=None, ref_target=None), FieldSpec('values', 'ArrayOrRef', False, 'NumericRange-0011', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0012', item_kind='number', ref_target=None), FieldSpec('values', 'ArrayOrRef', False, 'Range-0001', None, 'Range-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Range-0002', item_kind='any', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'numericRange'
    _TYPE_RULE_ID = 'NumericRange-0013'
    _OWN_CATCHALL = 'NumericRange-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(values) if provided(values) else numberOfSteps + 1'}, 'labels': None}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'numericRange'

    def get_start_value(self):
        return self._get_orref_value('start')

    def get_start_ref(self):
        return self._get_orref_ref('start')

    def set_start_value(self, value):
        self._set_orref_value('start', value)

    def set_start_ref(self, ref):
        self._set_orref_ref('start', ref)

    def is_start_ref(self):
        return self._is_orref_ref('start')

    def is_set_start(self):
        return 'start' in self._values

    def unset_start(self):
        self._values.pop('start', None); self._orref_is_ref.pop('start', None)

    def get_end_value(self):
        return self._get_orref_value('end')

    def get_end_ref(self):
        return self._get_orref_ref('end')

    def set_end_value(self, value):
        self._set_orref_value('end', value)

    def set_end_ref(self, ref):
        self._set_orref_ref('end', ref)

    def is_end_ref(self):
        return self._is_orref_ref('end')

    def is_set_end(self):
        return 'end' in self._values

    def unset_end(self):
        self._values.pop('end', None); self._orref_is_ref.pop('end', None)

    def get_interval_value(self):
        return self._get_orref_value('interval')

    def get_interval_ref(self):
        return self._get_orref_ref('interval')

    def set_interval_value(self, value):
        self._set_orref_value('interval', value)

    def set_interval_ref(self, ref):
        self._set_orref_ref('interval', ref)

    def is_interval_ref(self):
        return self._is_orref_ref('interval')

    def is_set_interval(self):
        return 'interval' in self._values

    def unset_interval(self):
        self._values.pop('interval', None); self._orref_is_ref.pop('interval', None)

    def get_number_of_steps_value(self):
        return self._get_orref_value('numberOfSteps')

    def get_number_of_steps_ref(self):
        return self._get_orref_ref('numberOfSteps')

    def set_number_of_steps_value(self, value):
        self._set_orref_value('numberOfSteps', value)

    def set_number_of_steps_ref(self, ref):
        self._set_orref_ref('numberOfSteps', ref)

    def is_number_of_steps_ref(self):
        return self._is_orref_ref('numberOfSteps')

    def is_set_number_of_steps(self):
        return 'numberOfSteps' in self._values

    def unset_number_of_steps(self):
        self._values.pop('numberOfSteps', None); self._orref_is_ref.pop('numberOfSteps', None)

    def get_scale_value(self):
        return self._get_orref_value('scale')

    def get_scale_ref(self):
        return self._get_orref_ref('scale')

    def set_scale_value(self, value):
        self._set_orref_value('scale', value)

    def set_scale_ref(self, ref):
        self._set_orref_ref('scale', ref)

    def is_scale_ref(self):
        return self._is_orref_ref('scale')

    def is_set_scale(self):
        return 'scale' in self._values

    def unset_scale(self):
        self._values.pop('scale', None); self._orref_is_ref.pop('scale', None)

    def get_values_value(self):
        return self._get_orref_value('values')

    def get_values_ref(self):
        return self._get_orref_ref('values')

    def set_values_value(self, value):
        self._set_orref_value('values', value)

    def set_values_ref(self, ref):
        self._set_orref_ref('values', ref)

    def is_values_ref(self):
        return self._is_orref_ref('values')

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None); self._orref_is_ref.pop('values', None)

    def get_values_value(self):
        return self._get_orref_value('values')

    def get_values_ref(self):
        return self._get_orref_ref('values')

    def set_values_value(self, value):
        self._set_orref_value('values', value)

    def set_values_ref(self, ref):
        self._set_orref_ref('values', ref)

    def is_values_ref(self):
        return self._is_orref_ref('values')

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None); self._orref_is_ref.pop('values', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'numericRange')
        if 'start' in self._values: d['start'] = self._values['start']
        if 'end' in self._values: d['end'] = self._values['end']
        if 'interval' in self._values: d['interval'] = self._values['interval']
        if 'numberOfSteps' in self._values: d['numberOfSteps'] = self._values['numberOfSteps']
        if 'scale' in self._values: d['scale'] = self._values['scale']
        if 'values' in self._values: d['values'] = self._values['values']
        if 'values' in self._values: d['values'] = self._values['values']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class OneStepODESimulation(SedBase):
    """Generated from specsheets/tasks/OneStepODESimulation/."""
    _FIELDS = [FieldSpec('independentStep', 'NumberOrRef', True, 'OneStepODESimulation-0005', 'OneStepODESimulation-0004', 'OneStepODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='OneStepODESimulation-0006', item_kind=None, ref_target=None), FieldSpec('relativeTolerance', 'NumberOrRef', False, 'AbstractODESimulation-0001', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0002', item_kind=None, ref_target=None), FieldSpec('absoluteTolerance', 'NumberOrRef', False, 'AbstractODESimulation-0003', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0004', item_kind=None, ref_target=None), FieldSpec('absoluteToleranceVector', 'ArrayOrRef', False, 'AbstractODESimulation-0005', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0006', item_kind='number', ref_target=None), FieldSpec('absoluteToleranceAdjustmentFactor', 'NumberOrRef', False, 'AbstractODESimulation-0007', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0008', item_kind=None, ref_target=None), FieldSpec('toleranceForRootFinder', 'NumberOrRef', False, 'AbstractODESimulation-0009', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0010', item_kind=None, ref_target=None), FieldSpec('initialStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0011', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0012', item_kind=None, ref_target=None), FieldSpec('maxNumberOfSteps', 'NumberOrRef', False, 'AbstractODESimulation-0013', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0014', item_kind=None, ref_target=None), FieldSpec('maxInternalSteps', 'IntegerOrRef', False, 'AbstractODESimulation-0015', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0016', item_kind=None, ref_target=None), FieldSpec('maxInternalStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0017', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0018', item_kind=None, ref_target=None), FieldSpec('minInternalStepSize', 'NumberOrRef', False, 'AbstractODESimulation-0019', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0020', item_kind=None, ref_target=None), FieldSpec('forcePhysicalCorrectness', 'BooleanOrRef', False, 'AbstractODESimulation-0021', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0022', item_kind=None, ref_target=None), FieldSpec('integrateReducedModel', 'BooleanOrRef', False, 'AbstractODESimulation-0023', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0024', item_kind=None, ref_target=None), FieldSpec('useReducedModel', 'BooleanOrRef', False, 'AbstractODESimulation-0025', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0026', item_kind=None, ref_target=None), FieldSpec('useStiffSolver', 'BooleanOrRef', False, 'AbstractODESimulation-0027', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0028', item_kind=None, ref_target=None), FieldSpec('maxBDForder', 'IntegerOrRef', False, 'AbstractODESimulation-0029', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0030', item_kind=None, ref_target=None), FieldSpec('maxAdamsOrder', 'IntegerOrRef', False, 'AbstractODESimulation-0031', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0032', item_kind=None, ref_target=None), FieldSpec('variableStepSize', 'BooleanOrRef', False, 'AbstractODESimulation-0033', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0034', item_kind=None, ref_target=None), FieldSpec('maxOutputRows', 'IntegerOrRef', False, 'AbstractODESimulation-0035', None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractODESimulation-0036', item_kind=None, ref_target=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'AbstractSimulation-0002', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0003', item_kind=None, ref_target=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, 'AbstractSimulation-0004', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0005', item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', False, 'AbstractSimulation-0006', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0007', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'independentStep'}
    _TYPE_CONST = 'oneStepODESimulation'
    _TYPE_RULE_ID = 'OneStepODESimulation-0007'
    _OWN_CATCHALL = 'OneStepODESimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(outputVariables)'}, 'labels': {'source': 'static', 'expr': 'outputVariables'}, 'note': 'a single point, not a series'}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'oneStepODESimulation'

    def get_independent_step_value(self):
        return self._get_orref_value('independentStep')

    def get_independent_step_ref(self):
        return self._get_orref_ref('independentStep')

    def set_independent_step_value(self, value):
        self._set_orref_value('independentStep', value)

    def set_independent_step_ref(self, ref):
        self._set_orref_ref('independentStep', ref)

    def is_independent_step_ref(self):
        return self._is_orref_ref('independentStep')

    def is_set_independent_step(self):
        return 'independentStep' in self._values

    def unset_independent_step(self):
        self._values.pop('independentStep', None); self._orref_is_ref.pop('independentStep', None)

    def get_relative_tolerance_value(self):
        return self._get_orref_value('relativeTolerance')

    def get_relative_tolerance_ref(self):
        return self._get_orref_ref('relativeTolerance')

    def set_relative_tolerance_value(self, value):
        self._set_orref_value('relativeTolerance', value)

    def set_relative_tolerance_ref(self, ref):
        self._set_orref_ref('relativeTolerance', ref)

    def is_relative_tolerance_ref(self):
        return self._is_orref_ref('relativeTolerance')

    def is_set_relative_tolerance(self):
        return 'relativeTolerance' in self._values

    def unset_relative_tolerance(self):
        self._values.pop('relativeTolerance', None); self._orref_is_ref.pop('relativeTolerance', None)

    def get_absolute_tolerance_value(self):
        return self._get_orref_value('absoluteTolerance')

    def get_absolute_tolerance_ref(self):
        return self._get_orref_ref('absoluteTolerance')

    def set_absolute_tolerance_value(self, value):
        self._set_orref_value('absoluteTolerance', value)

    def set_absolute_tolerance_ref(self, ref):
        self._set_orref_ref('absoluteTolerance', ref)

    def is_absolute_tolerance_ref(self):
        return self._is_orref_ref('absoluteTolerance')

    def is_set_absolute_tolerance(self):
        return 'absoluteTolerance' in self._values

    def unset_absolute_tolerance(self):
        self._values.pop('absoluteTolerance', None); self._orref_is_ref.pop('absoluteTolerance', None)

    def get_absolute_tolerance_vector_value(self):
        return self._get_orref_value('absoluteToleranceVector')

    def get_absolute_tolerance_vector_ref(self):
        return self._get_orref_ref('absoluteToleranceVector')

    def set_absolute_tolerance_vector_value(self, value):
        self._set_orref_value('absoluteToleranceVector', value)

    def set_absolute_tolerance_vector_ref(self, ref):
        self._set_orref_ref('absoluteToleranceVector', ref)

    def is_absolute_tolerance_vector_ref(self):
        return self._is_orref_ref('absoluteToleranceVector')

    def is_set_absolute_tolerance_vector(self):
        return 'absoluteToleranceVector' in self._values

    def unset_absolute_tolerance_vector(self):
        self._values.pop('absoluteToleranceVector', None); self._orref_is_ref.pop('absoluteToleranceVector', None)

    def get_absolute_tolerance_adjustment_factor_value(self):
        return self._get_orref_value('absoluteToleranceAdjustmentFactor')

    def get_absolute_tolerance_adjustment_factor_ref(self):
        return self._get_orref_ref('absoluteToleranceAdjustmentFactor')

    def set_absolute_tolerance_adjustment_factor_value(self, value):
        self._set_orref_value('absoluteToleranceAdjustmentFactor', value)

    def set_absolute_tolerance_adjustment_factor_ref(self, ref):
        self._set_orref_ref('absoluteToleranceAdjustmentFactor', ref)

    def is_absolute_tolerance_adjustment_factor_ref(self):
        return self._is_orref_ref('absoluteToleranceAdjustmentFactor')

    def is_set_absolute_tolerance_adjustment_factor(self):
        return 'absoluteToleranceAdjustmentFactor' in self._values

    def unset_absolute_tolerance_adjustment_factor(self):
        self._values.pop('absoluteToleranceAdjustmentFactor', None); self._orref_is_ref.pop('absoluteToleranceAdjustmentFactor', None)

    def get_tolerance_for_root_finder_value(self):
        return self._get_orref_value('toleranceForRootFinder')

    def get_tolerance_for_root_finder_ref(self):
        return self._get_orref_ref('toleranceForRootFinder')

    def set_tolerance_for_root_finder_value(self, value):
        self._set_orref_value('toleranceForRootFinder', value)

    def set_tolerance_for_root_finder_ref(self, ref):
        self._set_orref_ref('toleranceForRootFinder', ref)

    def is_tolerance_for_root_finder_ref(self):
        return self._is_orref_ref('toleranceForRootFinder')

    def is_set_tolerance_for_root_finder(self):
        return 'toleranceForRootFinder' in self._values

    def unset_tolerance_for_root_finder(self):
        self._values.pop('toleranceForRootFinder', None); self._orref_is_ref.pop('toleranceForRootFinder', None)

    def get_initial_step_size_value(self):
        return self._get_orref_value('initialStepSize')

    def get_initial_step_size_ref(self):
        return self._get_orref_ref('initialStepSize')

    def set_initial_step_size_value(self, value):
        self._set_orref_value('initialStepSize', value)

    def set_initial_step_size_ref(self, ref):
        self._set_orref_ref('initialStepSize', ref)

    def is_initial_step_size_ref(self):
        return self._is_orref_ref('initialStepSize')

    def is_set_initial_step_size(self):
        return 'initialStepSize' in self._values

    def unset_initial_step_size(self):
        self._values.pop('initialStepSize', None); self._orref_is_ref.pop('initialStepSize', None)

    def get_max_number_of_steps_value(self):
        return self._get_orref_value('maxNumberOfSteps')

    def get_max_number_of_steps_ref(self):
        return self._get_orref_ref('maxNumberOfSteps')

    def set_max_number_of_steps_value(self, value):
        self._set_orref_value('maxNumberOfSteps', value)

    def set_max_number_of_steps_ref(self, ref):
        self._set_orref_ref('maxNumberOfSteps', ref)

    def is_max_number_of_steps_ref(self):
        return self._is_orref_ref('maxNumberOfSteps')

    def is_set_max_number_of_steps(self):
        return 'maxNumberOfSteps' in self._values

    def unset_max_number_of_steps(self):
        self._values.pop('maxNumberOfSteps', None); self._orref_is_ref.pop('maxNumberOfSteps', None)

    def get_max_internal_steps_value(self):
        return self._get_orref_value('maxInternalSteps')

    def get_max_internal_steps_ref(self):
        return self._get_orref_ref('maxInternalSteps')

    def set_max_internal_steps_value(self, value):
        self._set_orref_value('maxInternalSteps', value)

    def set_max_internal_steps_ref(self, ref):
        self._set_orref_ref('maxInternalSteps', ref)

    def is_max_internal_steps_ref(self):
        return self._is_orref_ref('maxInternalSteps')

    def is_set_max_internal_steps(self):
        return 'maxInternalSteps' in self._values

    def unset_max_internal_steps(self):
        self._values.pop('maxInternalSteps', None); self._orref_is_ref.pop('maxInternalSteps', None)

    def get_max_internal_step_size_value(self):
        return self._get_orref_value('maxInternalStepSize')

    def get_max_internal_step_size_ref(self):
        return self._get_orref_ref('maxInternalStepSize')

    def set_max_internal_step_size_value(self, value):
        self._set_orref_value('maxInternalStepSize', value)

    def set_max_internal_step_size_ref(self, ref):
        self._set_orref_ref('maxInternalStepSize', ref)

    def is_max_internal_step_size_ref(self):
        return self._is_orref_ref('maxInternalStepSize')

    def is_set_max_internal_step_size(self):
        return 'maxInternalStepSize' in self._values

    def unset_max_internal_step_size(self):
        self._values.pop('maxInternalStepSize', None); self._orref_is_ref.pop('maxInternalStepSize', None)

    def get_min_internal_step_size_value(self):
        return self._get_orref_value('minInternalStepSize')

    def get_min_internal_step_size_ref(self):
        return self._get_orref_ref('minInternalStepSize')

    def set_min_internal_step_size_value(self, value):
        self._set_orref_value('minInternalStepSize', value)

    def set_min_internal_step_size_ref(self, ref):
        self._set_orref_ref('minInternalStepSize', ref)

    def is_min_internal_step_size_ref(self):
        return self._is_orref_ref('minInternalStepSize')

    def is_set_min_internal_step_size(self):
        return 'minInternalStepSize' in self._values

    def unset_min_internal_step_size(self):
        self._values.pop('minInternalStepSize', None); self._orref_is_ref.pop('minInternalStepSize', None)

    def get_force_physical_correctness_value(self):
        return self._get_orref_value('forcePhysicalCorrectness')

    def get_force_physical_correctness_ref(self):
        return self._get_orref_ref('forcePhysicalCorrectness')

    def set_force_physical_correctness_value(self, value):
        self._set_orref_value('forcePhysicalCorrectness', value)

    def set_force_physical_correctness_ref(self, ref):
        self._set_orref_ref('forcePhysicalCorrectness', ref)

    def is_force_physical_correctness_ref(self):
        return self._is_orref_ref('forcePhysicalCorrectness')

    def is_set_force_physical_correctness(self):
        return 'forcePhysicalCorrectness' in self._values

    def unset_force_physical_correctness(self):
        self._values.pop('forcePhysicalCorrectness', None); self._orref_is_ref.pop('forcePhysicalCorrectness', None)

    def get_integrate_reduced_model_value(self):
        return self._get_orref_value('integrateReducedModel')

    def get_integrate_reduced_model_ref(self):
        return self._get_orref_ref('integrateReducedModel')

    def set_integrate_reduced_model_value(self, value):
        self._set_orref_value('integrateReducedModel', value)

    def set_integrate_reduced_model_ref(self, ref):
        self._set_orref_ref('integrateReducedModel', ref)

    def is_integrate_reduced_model_ref(self):
        return self._is_orref_ref('integrateReducedModel')

    def is_set_integrate_reduced_model(self):
        return 'integrateReducedModel' in self._values

    def unset_integrate_reduced_model(self):
        self._values.pop('integrateReducedModel', None); self._orref_is_ref.pop('integrateReducedModel', None)

    def get_use_reduced_model_value(self):
        return self._get_orref_value('useReducedModel')

    def get_use_reduced_model_ref(self):
        return self._get_orref_ref('useReducedModel')

    def set_use_reduced_model_value(self, value):
        self._set_orref_value('useReducedModel', value)

    def set_use_reduced_model_ref(self, ref):
        self._set_orref_ref('useReducedModel', ref)

    def is_use_reduced_model_ref(self):
        return self._is_orref_ref('useReducedModel')

    def is_set_use_reduced_model(self):
        return 'useReducedModel' in self._values

    def unset_use_reduced_model(self):
        self._values.pop('useReducedModel', None); self._orref_is_ref.pop('useReducedModel', None)

    def get_use_stiff_solver_value(self):
        return self._get_orref_value('useStiffSolver')

    def get_use_stiff_solver_ref(self):
        return self._get_orref_ref('useStiffSolver')

    def set_use_stiff_solver_value(self, value):
        self._set_orref_value('useStiffSolver', value)

    def set_use_stiff_solver_ref(self, ref):
        self._set_orref_ref('useStiffSolver', ref)

    def is_use_stiff_solver_ref(self):
        return self._is_orref_ref('useStiffSolver')

    def is_set_use_stiff_solver(self):
        return 'useStiffSolver' in self._values

    def unset_use_stiff_solver(self):
        self._values.pop('useStiffSolver', None); self._orref_is_ref.pop('useStiffSolver', None)

    def get_max_b_d_forder_value(self):
        return self._get_orref_value('maxBDForder')

    def get_max_b_d_forder_ref(self):
        return self._get_orref_ref('maxBDForder')

    def set_max_b_d_forder_value(self, value):
        self._set_orref_value('maxBDForder', value)

    def set_max_b_d_forder_ref(self, ref):
        self._set_orref_ref('maxBDForder', ref)

    def is_max_b_d_forder_ref(self):
        return self._is_orref_ref('maxBDForder')

    def is_set_max_b_d_forder(self):
        return 'maxBDForder' in self._values

    def unset_max_b_d_forder(self):
        self._values.pop('maxBDForder', None); self._orref_is_ref.pop('maxBDForder', None)

    def get_max_adams_order_value(self):
        return self._get_orref_value('maxAdamsOrder')

    def get_max_adams_order_ref(self):
        return self._get_orref_ref('maxAdamsOrder')

    def set_max_adams_order_value(self, value):
        self._set_orref_value('maxAdamsOrder', value)

    def set_max_adams_order_ref(self, ref):
        self._set_orref_ref('maxAdamsOrder', ref)

    def is_max_adams_order_ref(self):
        return self._is_orref_ref('maxAdamsOrder')

    def is_set_max_adams_order(self):
        return 'maxAdamsOrder' in self._values

    def unset_max_adams_order(self):
        self._values.pop('maxAdamsOrder', None); self._orref_is_ref.pop('maxAdamsOrder', None)

    def get_variable_step_size_value(self):
        return self._get_orref_value('variableStepSize')

    def get_variable_step_size_ref(self):
        return self._get_orref_ref('variableStepSize')

    def set_variable_step_size_value(self, value):
        self._set_orref_value('variableStepSize', value)

    def set_variable_step_size_ref(self, ref):
        self._set_orref_ref('variableStepSize', ref)

    def is_variable_step_size_ref(self):
        return self._is_orref_ref('variableStepSize')

    def is_set_variable_step_size(self):
        return 'variableStepSize' in self._values

    def unset_variable_step_size(self):
        self._values.pop('variableStepSize', None); self._orref_is_ref.pop('variableStepSize', None)

    def get_max_output_rows_value(self):
        return self._get_orref_value('maxOutputRows')

    def get_max_output_rows_ref(self):
        return self._get_orref_ref('maxOutputRows')

    def set_max_output_rows_value(self, value):
        self._set_orref_value('maxOutputRows', value)

    def set_max_output_rows_ref(self, ref):
        self._set_orref_ref('maxOutputRows', ref)

    def is_max_output_rows_ref(self):
        return self._is_orref_ref('maxOutputRows')

    def is_set_max_output_rows(self):
        return 'maxOutputRows' in self._values

    def unset_max_output_rows(self):
        self._values.pop('maxOutputRows', None); self._orref_is_ref.pop('maxOutputRows', None)

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_independent_variable_init_value(self):
        return self._get_orref_value('independentVariableInit')

    def get_independent_variable_init_ref(self):
        return self._get_orref_ref('independentVariableInit')

    def set_independent_variable_init_value(self, value):
        self._set_orref_value('independentVariableInit', value)

    def set_independent_variable_init_ref(self, ref):
        self._set_orref_ref('independentVariableInit', ref)

    def is_independent_variable_init_ref(self):
        return self._is_orref_ref('independentVariableInit')

    def is_set_independent_variable_init(self):
        return 'independentVariableInit' in self._values

    def unset_independent_variable_init(self):
        self._values.pop('independentVariableInit', None); self._orref_is_ref.pop('independentVariableInit', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'oneStepODESimulation')
        if 'independentStep' in self._values: d['independentStep'] = self._values['independentStep']
        if 'relativeTolerance' in self._values: d['relativeTolerance'] = self._values['relativeTolerance']
        if 'absoluteTolerance' in self._values: d['absoluteTolerance'] = self._values['absoluteTolerance']
        if 'absoluteToleranceVector' in self._values: d['absoluteToleranceVector'] = self._values['absoluteToleranceVector']
        if 'absoluteToleranceAdjustmentFactor' in self._values: d['absoluteToleranceAdjustmentFactor'] = self._values['absoluteToleranceAdjustmentFactor']
        if 'toleranceForRootFinder' in self._values: d['toleranceForRootFinder'] = self._values['toleranceForRootFinder']
        if 'initialStepSize' in self._values: d['initialStepSize'] = self._values['initialStepSize']
        if 'maxNumberOfSteps' in self._values: d['maxNumberOfSteps'] = self._values['maxNumberOfSteps']
        if 'maxInternalSteps' in self._values: d['maxInternalSteps'] = self._values['maxInternalSteps']
        if 'maxInternalStepSize' in self._values: d['maxInternalStepSize'] = self._values['maxInternalStepSize']
        if 'minInternalStepSize' in self._values: d['minInternalStepSize'] = self._values['minInternalStepSize']
        if 'forcePhysicalCorrectness' in self._values: d['forcePhysicalCorrectness'] = self._values['forcePhysicalCorrectness']
        if 'integrateReducedModel' in self._values: d['integrateReducedModel'] = self._values['integrateReducedModel']
        if 'useReducedModel' in self._values: d['useReducedModel'] = self._values['useReducedModel']
        if 'useStiffSolver' in self._values: d['useStiffSolver'] = self._values['useStiffSolver']
        if 'maxBDForder' in self._values: d['maxBDForder'] = self._values['maxBDForder']
        if 'maxAdamsOrder' in self._values: d['maxAdamsOrder'] = self._values['maxAdamsOrder']
        if 'variableStepSize' in self._values: d['variableStepSize'] = self._values['variableStepSize']
        if 'maxOutputRows' in self._values: d['maxOutputRows'] = self._values['maxOutputRows']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class OneStepStochasticSimulation(SedBase):
    """Generated from specsheets/tasks/OneStepStochasticSimulation/."""
    _FIELDS = [FieldSpec('independentStep', 'NumberOrRef', False, 'OneStepStochasticSimulation-0004', None, 'OneStepStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='OneStepStochasticSimulation-0005', item_kind=None, ref_target=None), FieldSpec('seed', 'NumberOrRef', False, 'AbstractStochasticSimulation-0001', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0002', item_kind=None, ref_target=None), FieldSpec('timeDependentRelativeTolerance', 'NumberOrRef', False, 'AbstractStochasticSimulation-0003', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0004', item_kind=None, ref_target=None), FieldSpec('variableStepSize', 'BooleanOrRef', False, 'AbstractStochasticSimulation-0005', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0006', item_kind=None, ref_target=None), FieldSpec('minimumTimeStep', 'NumberOrRef', False, 'AbstractStochasticSimulation-0007', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0008', item_kind=None, ref_target=None), FieldSpec('maximumTimeStep', 'NumberOrRef', False, 'AbstractStochasticSimulation-0009', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0010', item_kind=None, ref_target=None), FieldSpec('nonNegative', 'BooleanOrRef', False, 'AbstractStochasticSimulation-0011', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0012', item_kind=None, ref_target=None), FieldSpec('maxOutputRows', 'IntegerOrRef', False, 'AbstractStochasticSimulation-0013', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0014', item_kind=None, ref_target=None), FieldSpec('maxNumSteps', 'IntegerOrRef', False, 'AbstractStochasticSimulation-0015', None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractStochasticSimulation-0016', item_kind=None, ref_target=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'AbstractSimulation-0002', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0003', item_kind=None, ref_target=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, 'AbstractSimulation-0004', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0005', item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', False, 'AbstractSimulation-0006', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractSimulation-0007', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'oneStepStochasticSimulation'
    _TYPE_RULE_ID = 'OneStepStochasticSimulation-0006'
    _OWN_CATCHALL = 'OneStepStochasticSimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(outputVariables)'}, 'labels': {'source': 'static', 'expr': 'outputVariables'}, 'note': 'a single point, not a series'}]}, '[id].model': {'type': 'model'}, '[id].independentStep': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': '1'}, 'labels': None}], 'note': 'the actual elapsed step; if independentStep was given as input it equals that value, otherwise its value is generated by the simulation'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'oneStepStochasticSimulation'

    def get_independent_step_value(self):
        return self._get_orref_value('independentStep')

    def get_independent_step_ref(self):
        return self._get_orref_ref('independentStep')

    def set_independent_step_value(self, value):
        self._set_orref_value('independentStep', value)

    def set_independent_step_ref(self, ref):
        self._set_orref_ref('independentStep', ref)

    def is_independent_step_ref(self):
        return self._is_orref_ref('independentStep')

    def is_set_independent_step(self):
        return 'independentStep' in self._values

    def unset_independent_step(self):
        self._values.pop('independentStep', None); self._orref_is_ref.pop('independentStep', None)

    def get_seed_value(self):
        return self._get_orref_value('seed')

    def get_seed_ref(self):
        return self._get_orref_ref('seed')

    def set_seed_value(self, value):
        self._set_orref_value('seed', value)

    def set_seed_ref(self, ref):
        self._set_orref_ref('seed', ref)

    def is_seed_ref(self):
        return self._is_orref_ref('seed')

    def is_set_seed(self):
        return 'seed' in self._values

    def unset_seed(self):
        self._values.pop('seed', None); self._orref_is_ref.pop('seed', None)

    def get_time_dependent_relative_tolerance_value(self):
        return self._get_orref_value('timeDependentRelativeTolerance')

    def get_time_dependent_relative_tolerance_ref(self):
        return self._get_orref_ref('timeDependentRelativeTolerance')

    def set_time_dependent_relative_tolerance_value(self, value):
        self._set_orref_value('timeDependentRelativeTolerance', value)

    def set_time_dependent_relative_tolerance_ref(self, ref):
        self._set_orref_ref('timeDependentRelativeTolerance', ref)

    def is_time_dependent_relative_tolerance_ref(self):
        return self._is_orref_ref('timeDependentRelativeTolerance')

    def is_set_time_dependent_relative_tolerance(self):
        return 'timeDependentRelativeTolerance' in self._values

    def unset_time_dependent_relative_tolerance(self):
        self._values.pop('timeDependentRelativeTolerance', None); self._orref_is_ref.pop('timeDependentRelativeTolerance', None)

    def get_variable_step_size_value(self):
        return self._get_orref_value('variableStepSize')

    def get_variable_step_size_ref(self):
        return self._get_orref_ref('variableStepSize')

    def set_variable_step_size_value(self, value):
        self._set_orref_value('variableStepSize', value)

    def set_variable_step_size_ref(self, ref):
        self._set_orref_ref('variableStepSize', ref)

    def is_variable_step_size_ref(self):
        return self._is_orref_ref('variableStepSize')

    def is_set_variable_step_size(self):
        return 'variableStepSize' in self._values

    def unset_variable_step_size(self):
        self._values.pop('variableStepSize', None); self._orref_is_ref.pop('variableStepSize', None)

    def get_minimum_time_step_value(self):
        return self._get_orref_value('minimumTimeStep')

    def get_minimum_time_step_ref(self):
        return self._get_orref_ref('minimumTimeStep')

    def set_minimum_time_step_value(self, value):
        self._set_orref_value('minimumTimeStep', value)

    def set_minimum_time_step_ref(self, ref):
        self._set_orref_ref('minimumTimeStep', ref)

    def is_minimum_time_step_ref(self):
        return self._is_orref_ref('minimumTimeStep')

    def is_set_minimum_time_step(self):
        return 'minimumTimeStep' in self._values

    def unset_minimum_time_step(self):
        self._values.pop('minimumTimeStep', None); self._orref_is_ref.pop('minimumTimeStep', None)

    def get_maximum_time_step_value(self):
        return self._get_orref_value('maximumTimeStep')

    def get_maximum_time_step_ref(self):
        return self._get_orref_ref('maximumTimeStep')

    def set_maximum_time_step_value(self, value):
        self._set_orref_value('maximumTimeStep', value)

    def set_maximum_time_step_ref(self, ref):
        self._set_orref_ref('maximumTimeStep', ref)

    def is_maximum_time_step_ref(self):
        return self._is_orref_ref('maximumTimeStep')

    def is_set_maximum_time_step(self):
        return 'maximumTimeStep' in self._values

    def unset_maximum_time_step(self):
        self._values.pop('maximumTimeStep', None); self._orref_is_ref.pop('maximumTimeStep', None)

    def get_non_negative_value(self):
        return self._get_orref_value('nonNegative')

    def get_non_negative_ref(self):
        return self._get_orref_ref('nonNegative')

    def set_non_negative_value(self, value):
        self._set_orref_value('nonNegative', value)

    def set_non_negative_ref(self, ref):
        self._set_orref_ref('nonNegative', ref)

    def is_non_negative_ref(self):
        return self._is_orref_ref('nonNegative')

    def is_set_non_negative(self):
        return 'nonNegative' in self._values

    def unset_non_negative(self):
        self._values.pop('nonNegative', None); self._orref_is_ref.pop('nonNegative', None)

    def get_max_output_rows_value(self):
        return self._get_orref_value('maxOutputRows')

    def get_max_output_rows_ref(self):
        return self._get_orref_ref('maxOutputRows')

    def set_max_output_rows_value(self, value):
        self._set_orref_value('maxOutputRows', value)

    def set_max_output_rows_ref(self, ref):
        self._set_orref_ref('maxOutputRows', ref)

    def is_max_output_rows_ref(self):
        return self._is_orref_ref('maxOutputRows')

    def is_set_max_output_rows(self):
        return 'maxOutputRows' in self._values

    def unset_max_output_rows(self):
        self._values.pop('maxOutputRows', None); self._orref_is_ref.pop('maxOutputRows', None)

    def get_max_num_steps_value(self):
        return self._get_orref_value('maxNumSteps')

    def get_max_num_steps_ref(self):
        return self._get_orref_ref('maxNumSteps')

    def set_max_num_steps_value(self, value):
        self._set_orref_value('maxNumSteps', value)

    def set_max_num_steps_ref(self, ref):
        self._set_orref_ref('maxNumSteps', ref)

    def is_max_num_steps_ref(self):
        return self._is_orref_ref('maxNumSteps')

    def is_set_max_num_steps(self):
        return 'maxNumSteps' in self._values

    def unset_max_num_steps(self):
        self._values.pop('maxNumSteps', None); self._orref_is_ref.pop('maxNumSteps', None)

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_independent_variable_init_value(self):
        return self._get_orref_value('independentVariableInit')

    def get_independent_variable_init_ref(self):
        return self._get_orref_ref('independentVariableInit')

    def set_independent_variable_init_value(self, value):
        self._set_orref_value('independentVariableInit', value)

    def set_independent_variable_init_ref(self, ref):
        self._set_orref_ref('independentVariableInit', ref)

    def is_independent_variable_init_ref(self):
        return self._is_orref_ref('independentVariableInit')

    def is_set_independent_variable_init(self):
        return 'independentVariableInit' in self._values

    def unset_independent_variable_init(self):
        self._values.pop('independentVariableInit', None); self._orref_is_ref.pop('independentVariableInit', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'oneStepStochasticSimulation')
        if 'independentStep' in self._values: d['independentStep'] = self._values['independentStep']
        if 'seed' in self._values: d['seed'] = self._values['seed']
        if 'timeDependentRelativeTolerance' in self._values: d['timeDependentRelativeTolerance'] = self._values['timeDependentRelativeTolerance']
        if 'variableStepSize' in self._values: d['variableStepSize'] = self._values['variableStepSize']
        if 'minimumTimeStep' in self._values: d['minimumTimeStep'] = self._values['minimumTimeStep']
        if 'maximumTimeStep' in self._values: d['maximumTimeStep'] = self._values['maximumTimeStep']
        if 'nonNegative' in self._values: d['nonNegative'] = self._values['nonNegative']
        if 'maxOutputRows' in self._values: d['maxOutputRows'] = self._values['maxOutputRows']
        if 'maxNumSteps' in self._values: d['maxNumSteps'] = self._values['maxNumSteps']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ParameterRange(SedBase):
    """Generated from specsheets/tasks/ParameterRange/."""
    _FIELDS = [FieldSpec('modelElement', 'StringOrRef', True, 'ParameterRange-0002', 'ParameterRange-0001', 'ParameterRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='ParameterRange-0003', item_kind=None, ref_target=None), FieldSpec('start', 'NumberOrRef', False, 'NumericRange-0001', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0002', item_kind=None, ref_target=None), FieldSpec('end', 'NumberOrRef', False, 'NumericRange-0003', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0004', item_kind=None, ref_target=None), FieldSpec('interval', 'NumberOrRef', False, 'NumericRange-0005', None, 'NumericRange-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0006', item_kind=None, ref_target=None), FieldSpec('numberOfSteps', 'IntegerOrRef', False, 'NumericRange-0007', None, 'NumericRange-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0008', item_kind=None, ref_target=None), FieldSpec('scale', 'StringOrRef', False, 'NumericRange-0009', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('linear', 'log10'), ref_type_rule_id='NumericRange-0010', item_kind=None, ref_target=None), FieldSpec('values', 'ArrayOrRef', False, 'NumericRange-0011', None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='NumericRange-0012', item_kind='number', ref_target=None), FieldSpec('values', 'ArrayOrRef', False, 'Range-0001', None, 'Range-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Range-0002', item_kind='any', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'modelElement'}
    _TYPE_CONST = 'parameterRange'
    _TYPE_RULE_ID = 'ParameterRange-0016'
    _OWN_CATCHALL = 'ParameterRange-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(values) if provided(values) else numberOfSteps + 1', 'note': 'same derivation as NumericRange, inherited via NumericRangeCommon'}, 'labels': None}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'parameterRange'

    def get_model_element_value(self):
        return self._get_orref_value('modelElement')

    def get_model_element_ref(self):
        return self._get_orref_ref('modelElement')

    def set_model_element_value(self, value):
        self._set_orref_value('modelElement', value)

    def set_model_element_ref(self, ref):
        self._set_orref_ref('modelElement', ref)

    def is_model_element_ref(self):
        return self._is_orref_ref('modelElement')

    def is_set_model_element(self):
        return 'modelElement' in self._values

    def unset_model_element(self):
        self._values.pop('modelElement', None); self._orref_is_ref.pop('modelElement', None)

    def get_start_value(self):
        return self._get_orref_value('start')

    def get_start_ref(self):
        return self._get_orref_ref('start')

    def set_start_value(self, value):
        self._set_orref_value('start', value)

    def set_start_ref(self, ref):
        self._set_orref_ref('start', ref)

    def is_start_ref(self):
        return self._is_orref_ref('start')

    def is_set_start(self):
        return 'start' in self._values

    def unset_start(self):
        self._values.pop('start', None); self._orref_is_ref.pop('start', None)

    def get_end_value(self):
        return self._get_orref_value('end')

    def get_end_ref(self):
        return self._get_orref_ref('end')

    def set_end_value(self, value):
        self._set_orref_value('end', value)

    def set_end_ref(self, ref):
        self._set_orref_ref('end', ref)

    def is_end_ref(self):
        return self._is_orref_ref('end')

    def is_set_end(self):
        return 'end' in self._values

    def unset_end(self):
        self._values.pop('end', None); self._orref_is_ref.pop('end', None)

    def get_interval_value(self):
        return self._get_orref_value('interval')

    def get_interval_ref(self):
        return self._get_orref_ref('interval')

    def set_interval_value(self, value):
        self._set_orref_value('interval', value)

    def set_interval_ref(self, ref):
        self._set_orref_ref('interval', ref)

    def is_interval_ref(self):
        return self._is_orref_ref('interval')

    def is_set_interval(self):
        return 'interval' in self._values

    def unset_interval(self):
        self._values.pop('interval', None); self._orref_is_ref.pop('interval', None)

    def get_number_of_steps_value(self):
        return self._get_orref_value('numberOfSteps')

    def get_number_of_steps_ref(self):
        return self._get_orref_ref('numberOfSteps')

    def set_number_of_steps_value(self, value):
        self._set_orref_value('numberOfSteps', value)

    def set_number_of_steps_ref(self, ref):
        self._set_orref_ref('numberOfSteps', ref)

    def is_number_of_steps_ref(self):
        return self._is_orref_ref('numberOfSteps')

    def is_set_number_of_steps(self):
        return 'numberOfSteps' in self._values

    def unset_number_of_steps(self):
        self._values.pop('numberOfSteps', None); self._orref_is_ref.pop('numberOfSteps', None)

    def get_scale_value(self):
        return self._get_orref_value('scale')

    def get_scale_ref(self):
        return self._get_orref_ref('scale')

    def set_scale_value(self, value):
        self._set_orref_value('scale', value)

    def set_scale_ref(self, ref):
        self._set_orref_ref('scale', ref)

    def is_scale_ref(self):
        return self._is_orref_ref('scale')

    def is_set_scale(self):
        return 'scale' in self._values

    def unset_scale(self):
        self._values.pop('scale', None); self._orref_is_ref.pop('scale', None)

    def get_values_value(self):
        return self._get_orref_value('values')

    def get_values_ref(self):
        return self._get_orref_ref('values')

    def set_values_value(self, value):
        self._set_orref_value('values', value)

    def set_values_ref(self, ref):
        self._set_orref_ref('values', ref)

    def is_values_ref(self):
        return self._is_orref_ref('values')

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None); self._orref_is_ref.pop('values', None)

    def get_values_value(self):
        return self._get_orref_value('values')

    def get_values_ref(self):
        return self._get_orref_ref('values')

    def set_values_value(self, value):
        self._set_orref_value('values', value)

    def set_values_ref(self, ref):
        self._set_orref_ref('values', ref)

    def is_values_ref(self):
        return self._is_orref_ref('values')

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None); self._orref_is_ref.pop('values', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'parameterRange')
        if 'modelElement' in self._values: d['modelElement'] = self._values['modelElement']
        if 'start' in self._values: d['start'] = self._values['start']
        if 'end' in self._values: d['end'] = self._values['end']
        if 'interval' in self._values: d['interval'] = self._values['interval']
        if 'numberOfSteps' in self._values: d['numberOfSteps'] = self._values['numberOfSteps']
        if 'scale' in self._values: d['scale'] = self._values['scale']
        if 'values' in self._values: d['values'] = self._values['values']
        if 'values' in self._values: d['values'] = self._values['values']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ParameterScan(SedBase):
    """Generated from specsheets/tasks/ParameterScan/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'ParameterScan-0002', 'ParameterScan-0001', 'ParameterScan-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('outputVariableMap', 'DictOrRef', False, 'Repeat-0002', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Repeat-0003', item_kind='ref', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('parameterRanges', 'array', True, 'ParameterScan-0004', 'ParameterScan-0003', 'ParameterScan-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='ParameterRange', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('subTasks', 'dict', False, 'Repeat-0001', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('aggregateOutputVariables', 'dict', False, 'Repeat-0004', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='AggregationCalculation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'model', 'parameterRanges'}
    _TYPE_CONST = 'parameterScan'
    _TYPE_RULE_ID = 'ParameterScan-0006'
    _OWN_CATCHALL = 'ParameterScan-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'repeat': {'over': 'parameterRanges', 'size': {'source': 'static', 'expr': 'len(self)'}, 'labels': {'source': 'runtime', 'note': "that range's values, written as text the way numbers appear in formed strings (1, 2, 0.5, 0.25); known only once the range is expanded, so a label index here is not checked ahead of time"}, 'note': "one dimension per entry of parameterRanges, in parameterRanges order, each sized by that entry's own length; len(self) dispatches on the entry's actual Range/NumericRange/ParameterRange type - see core-spec.md Section 8; each dimension is named by (identified with) that entry's modelElement and labeled by that range's values"}}, {'size': {'source': 'static', 'expr': 'len(outputVariableMap)'}, 'labels': {'source': 'static', 'expr': 'keys(outputVariableMap)'}, 'note': 'the outputVariableMap entries, one per key, labeled by the keys; length 0 if outputVariableMap is empty'}, {'trailing': {'of': 'outputVariableMap', 'note': "the dimensions of the outputVariableMap entries' own values, if they have any, follow (all entries must have the same shape, since they are stacked into one array); how many there are is not known ahead of time"}}]}, '[id].aggregates': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(aggregateOutputVariables)'}, 'labels': None}, {'trailing': {'of': 'aggregateOutputVariables', 'note': 'if the underlying subTask output was itself multi-dimensional, that dimensionality carries through per entry; how many dimensions that is is not known ahead of time'}}]}, '[id].ranges': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(parameterRanges)'}, 'labels': {'source': 'static', 'expr': 'parameterRanges.modelElement'}, 'note': "one entry per ParameterRange child, in order, labeled with that child's modelElement (parameterRanges.modelElement is the modelElement of each entry, in order)"}], 'note': 'the current value of each entry of parameterRanges, within the loop only'}, '[id].indexes': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(parameterRanges)'}, 'labels': {'source': 'static', 'expr': 'parameterRanges.modelElement'}, 'note': "one entry per ParameterRange child, in order, labeled with that child's modelElement (parameterRanges.modelElement is the modelElement of each entry, in order)"}], 'note': 'the current index into each entry of parameterRanges, within the loop only'}, '[id].model': {'type': 'model', 'note': 'the model as modified for the current iteration, within the loop only'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._parameter_ranges = ListCollection()
        self._sub_tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._aggregate_output_variables = IdKeyedCollection(lambda tv, _cls=AggregationCalculation: (_cls, False))
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'parameterScan'

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_output_variable_map_value(self):
        return self._get_orref_value('outputVariableMap')

    def get_output_variable_map_ref(self):
        return self._get_orref_ref('outputVariableMap')

    def set_output_variable_map_value(self, value):
        self._set_orref_value('outputVariableMap', value)

    def set_output_variable_map_ref(self, ref):
        self._set_orref_ref('outputVariableMap', ref)

    def is_output_variable_map_ref(self):
        return self._is_orref_ref('outputVariableMap')

    def is_set_output_variable_map(self):
        return 'outputVariableMap' in self._values

    def unset_output_variable_map(self):
        self._values.pop('outputVariableMap', None); self._orref_is_ref.pop('outputVariableMap', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_parameter_ranges(self):
        return self._parameter_ranges.items()

    def add_parameter_ranges(self, obj):
        self._parameter_ranges.add(obj); obj._attach(self, self.get_document())

    def insert_parameter_ranges(self, index, obj):
        self._parameter_ranges.insert(index, obj); obj._attach(self, self.get_document())

    def remove_parameter_ranges(self, index):
        self._parameter_ranges.remove(index)

    def get_sub_tasks(self):
        return self._sub_tasks.ids()

    def get_sub_tasks_item(self, item_id):
        return self._sub_tasks.get(item_id)

    def add_sub_tasks(self, item_id, obj):
        self._sub_tasks.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_sub_tasks(self, index, item_id, obj):
        self._sub_tasks.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_sub_tasks(self, item_id):
        self._sub_tasks.remove(item_id)

    def set_id_on_sub_tasks(self, old_id, new_id):
        self._sub_tasks.set_id(old_id, new_id)

    def get_aggregate_output_variables(self):
        return self._aggregate_output_variables.ids()

    def get_aggregate_output_variables_item(self, item_id):
        return self._aggregate_output_variables.get(item_id)

    def add_aggregate_output_variables(self, item_id, obj):
        self._aggregate_output_variables.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_aggregate_output_variables(self, index, item_id, obj):
        self._aggregate_output_variables.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_aggregate_output_variables(self, item_id):
        self._aggregate_output_variables.remove(item_id)

    def set_id_on_aggregate_output_variables(self, old_id, new_id):
        self._aggregate_output_variables.set_id(old_id, new_id)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._parameter_ranges.items())
        kids.extend(self._sub_tasks.get(i) for i in self._sub_tasks.ids())
        kids.extend(self._aggregate_output_variables.get(i) for i in self._aggregate_output_variables.ids())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'subTasks': return self._sub_tasks
        if field_name == 'aggregateOutputVariables': return self._aggregate_output_variables
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._parameter_ranges.items()):
            out.append((item, '/parameterRanges/%d' % idx))
        for i in self._sub_tasks.ids():
            out.append((self._sub_tasks.get(i), '/subTasks/' + i))
        for i in self._aggregate_output_variables.ids():
            out.append((self._aggregate_output_variables.get(i), '/aggregateOutputVariables/' + i))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return ['subTasks', 'aggregateOutputVariables']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'parameterScan')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'outputVariableMap' in self._values: d['outputVariableMap'] = self._values['outputVariableMap']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._parameter_ranges): d['parameterRanges'] = [it.to_json_value() for it in self._parameter_ranges.items()]
        if len(self._sub_tasks): d['subTasks'] = {i: self._sub_tasks.get(i).to_json_value() for i in self._sub_tasks.ids()}
        if len(self._aggregate_output_variables): d['aggregateOutputVariables'] = {i: self._aggregate_output_variables.get(i).to_json_value() for i in self._aggregate_output_variables.ids()}
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Range(SedBase):
    """Generated from specsheets/tasks/Range/."""
    _FIELDS = [FieldSpec('values', 'ArrayOrRef', False, 'Range-0001', None, 'Range-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Range-0002', item_kind='any', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'range'
    _TYPE_RULE_ID = 'Range-0003'
    _OWN_CATCHALL = 'Range-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(values)'}, 'labels': None}]}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'range'

    def get_values_value(self):
        return self._get_orref_value('values')

    def get_values_ref(self):
        return self._get_orref_ref('values')

    def set_values_value(self, value):
        self._set_orref_value('values', value)

    def set_values_ref(self, ref):
        self._set_orref_ref('values', ref)

    def is_values_ref(self):
        return self._is_orref_ref('values')

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None); self._orref_is_ref.pop('values', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'range')
        if 'values' in self._values: d['values'] = self._values['values']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class RelabelData(SedBase):
    """Generated from specsheets/tasks/RelabelData/."""
    _FIELDS = [FieldSpec('input', 'SIdRef', True, 'RelabelData-0002', 'RelabelData-0001', 'RelabelData-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('labels', 'ArrayOrRef', True, 'RelabelData-0004', 'RelabelData-0003', 'RelabelData-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='RelabelData-0005', item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'input', 'labels'}
    _TYPE_CONST = 'relabelData'
    _TYPE_RULE_ID = 'RelabelData-0006'
    _OWN_CATCHALL = 'RelabelData-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': {'source': 'static', 'expr': 'shapeOf(input)', 'note': "same dimensions as the referenced input AnnotatedData - this task only replaces the topmost dimension's labels (from labels), not the shape"}}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'relabelData'

    def get_input(self):
        if 'input' not in self._values: raise ApiError('input is not set')
        return self._values['input']

    def set_input(self, value):
        self._values['input'] = value

    def is_set_input(self):
        return 'input' in self._values

    def unset_input(self):
        self._values.pop('input', None)

    def get_labels_value(self):
        return self._get_orref_value('labels')

    def get_labels_ref(self):
        return self._get_orref_ref('labels')

    def set_labels_value(self, value):
        self._set_orref_value('labels', value)

    def set_labels_ref(self, ref):
        self._set_orref_ref('labels', ref)

    def is_labels_ref(self):
        return self._is_orref_ref('labels')

    def is_set_labels(self):
        return 'labels' in self._values

    def unset_labels(self):
        self._values.pop('labels', None); self._orref_is_ref.pop('labels', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'relabelData')
        if 'input' in self._values: d['input'] = self._values['input']
        if 'labels' in self._values: d['labels'] = self._values['labels']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Scatter(SedBase):
    """Generated from specsheets/tasks/Scatter/."""
    _FIELDS = [FieldSpec('outputVariableMap', 'DictOrRef', False, 'Repeat-0002', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Repeat-0003', item_kind='ref', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('subTasks', 'dict', False, 'Repeat-0001', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('aggregateOutputVariables', 'dict', False, 'Repeat-0004', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='AggregationCalculation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('range', 'ref-discriminator', True, 'Scatter-0005', 'Scatter-0004', 'Scatter-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='RangeInline', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'range'}
    _TYPE_CONST = 'scatter'
    _TYPE_RULE_ID = 'Scatter-0003'
    _OWN_CATCHALL = 'Scatter-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(range)'}, 'labels': {'source': 'runtime', 'note': "the range's values, written as text the way numbers appear in formed strings (an integral value without a decimal point: 1, 2; otherwise 0.5, 0.25); known only once the range is expanded, so a label index here is not checked ahead of time"}, 'note': "dimension 0 is the iteration: one row per value in range, labeled by those values (there is no separate column holding the range values); len(range) dispatches on range's actual Range/NumericRange/ParameterRange type"}, {'size': {'source': 'static', 'expr': 'len(outputVariableMap)'}, 'labels': {'source': 'static', 'expr': 'keys(outputVariableMap)'}, 'note': 'dimension 1 holds the outputVariableMap entries, one per key, labeled by the keys; length 0 if outputVariableMap is empty'}, {'trailing': {'of': 'outputVariableMap', 'note': "the dimensions of the outputVariableMap entries' own values, if they have any, follow (all entries must have the same shape, since they are stacked into one array); how many there are is not known ahead of time"}}]}, '[id].aggregates': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(aggregateOutputVariables)'}, 'labels': None, 'note': "each entry collapses the range dimension of [id] to a single value (per Repeat, the applied dimension defaults to this Scatter's own range), unless the underlying subTask output was itself multi-dimensional, in which case that dimensionality carries through per entry"}, {'trailing': {'of': 'aggregateOutputVariables', 'note': 'if the underlying subTask output was itself multi-dimensional, that dimensionality carries through per entry; how many dimensions that is is not known ahead of time'}}]}, '[id].range': {'type': 'annotatedData', 'dimensions': [], 'note': 'the current value of range, within each iteration'}, '[id].index': {'type': 'annotatedData', 'dimensions': [], 'note': 'the current index into range, within each iteration'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._sub_tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._aggregate_output_variables = IdKeyedCollection(lambda tv, _cls=AggregationCalculation: (_cls, False))
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()
        self._range = None

    def get_type(self):
        return 'scatter'

    def get_output_variable_map_value(self):
        return self._get_orref_value('outputVariableMap')

    def get_output_variable_map_ref(self):
        return self._get_orref_ref('outputVariableMap')

    def set_output_variable_map_value(self, value):
        self._set_orref_value('outputVariableMap', value)

    def set_output_variable_map_ref(self, ref):
        self._set_orref_ref('outputVariableMap', ref)

    def is_output_variable_map_ref(self):
        return self._is_orref_ref('outputVariableMap')

    def is_set_output_variable_map(self):
        return 'outputVariableMap' in self._values

    def unset_output_variable_map(self):
        self._values.pop('outputVariableMap', None); self._orref_is_ref.pop('outputVariableMap', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_sub_tasks(self):
        return self._sub_tasks.ids()

    def get_sub_tasks_item(self, item_id):
        return self._sub_tasks.get(item_id)

    def add_sub_tasks(self, item_id, obj):
        self._sub_tasks.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_sub_tasks(self, index, item_id, obj):
        self._sub_tasks.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_sub_tasks(self, item_id):
        self._sub_tasks.remove(item_id)

    def set_id_on_sub_tasks(self, old_id, new_id):
        self._sub_tasks.set_id(old_id, new_id)

    def get_aggregate_output_variables(self):
        return self._aggregate_output_variables.ids()

    def get_aggregate_output_variables_item(self, item_id):
        return self._aggregate_output_variables.get(item_id)

    def add_aggregate_output_variables(self, item_id, obj):
        self._aggregate_output_variables.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_aggregate_output_variables(self, index, item_id, obj):
        self._aggregate_output_variables.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_aggregate_output_variables(self, item_id):
        self._aggregate_output_variables.remove(item_id)

    def set_id_on_aggregate_output_variables(self, old_id, new_id):
        self._aggregate_output_variables.set_id(old_id, new_id)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_range(self):
        if self._range is None: raise ApiError('range is not set')
        return self._range

    def set_range(self, obj):
        self._range = obj; obj._attach(self, self.get_document())

    def is_set_range(self):
        return self._range is not None

    def unset_range(self):
        self._range = None

    def _children(self):
        kids = []
        kids.extend(self._sub_tasks.get(i) for i in self._sub_tasks.ids())
        kids.extend(self._aggregate_output_variables.get(i) for i in self._aggregate_output_variables.ids())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        if self._range is not None: kids.append(self._range)
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'subTasks': return self._sub_tasks
        if field_name == 'aggregateOutputVariables': return self._aggregate_output_variables
        return None

    def _children_with_locations(self):
        out = []
        for i in self._sub_tasks.ids():
            out.append((self._sub_tasks.get(i), '/subTasks/' + i))
        for i in self._aggregate_output_variables.ids():
            out.append((self._aggregate_output_variables.get(i), '/aggregateOutputVariables/' + i))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._range is not None: out.append((self._range, '/range'))
        return out

    def _id_collection_names(self):
        return ['subTasks', 'aggregateOutputVariables']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'scatter')
        if 'outputVariableMap' in self._values: d['outputVariableMap'] = self._values['outputVariableMap']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._sub_tasks): d['subTasks'] = {i: self._sub_tasks.get(i).to_json_value() for i in self._sub_tasks.ids()}
        if len(self._aggregate_output_variables): d['aggregateOutputVariables'] = {i: self._aggregate_output_variables.get(i).to_json_value() for i in self._aggregate_output_variables.ids()}
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._range is not None: d['range'] = self._range.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class SteadyState(SedBase):
    """Generated from specsheets/tasks/SteadyState/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, None, 'SteadyState-0001', 'SteadyState-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='model'), FieldSpec('independentVariable', 'StringOrRef', False, 'SteadyState-0004', None, 'SteadyState-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('outputVariables', 'ArrayOrRef', True, None, 'SteadyState-0002', 'SteadyState-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind='string', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('workingAlgorithms', 'array', False, 'SteadyState-0007', None, 'SteadyState-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'model', 'outputVariables'}
    _TYPE_CONST = 'steadyState'
    _TYPE_RULE_ID = 'SteadyState-0003'
    _OWN_CATCHALL = 'SteadyState-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': [{'size': {'source': 'static', 'expr': 'len(outputVariables)'}, 'labels': {'source': 'static', 'expr': 'outputVariables'}}]}, '[id].model': {'type': 'model'}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'steadyState'

    def get_model(self):
        if 'model' not in self._values: raise ApiError('model is not set')
        return self._values['model']

    def set_model(self, value):
        self._values['model'] = value

    def is_set_model(self):
        return 'model' in self._values

    def unset_model(self):
        self._values.pop('model', None)

    def get_independent_variable_value(self):
        return self._get_orref_value('independentVariable')

    def get_independent_variable_ref(self):
        return self._get_orref_ref('independentVariable')

    def set_independent_variable_value(self, value):
        self._set_orref_value('independentVariable', value)

    def set_independent_variable_ref(self, ref):
        self._set_orref_ref('independentVariable', ref)

    def is_independent_variable_ref(self):
        return self._is_orref_ref('independentVariable')

    def is_set_independent_variable(self):
        return 'independentVariable' in self._values

    def unset_independent_variable(self):
        self._values.pop('independentVariable', None); self._orref_is_ref.pop('independentVariable', None)

    def get_output_variables_value(self):
        return self._get_orref_value('outputVariables')

    def get_output_variables_ref(self):
        return self._get_orref_ref('outputVariables')

    def set_output_variables_value(self, value):
        self._set_orref_value('outputVariables', value)

    def set_output_variables_ref(self, ref):
        self._set_orref_ref('outputVariables', ref)

    def is_output_variables_ref(self):
        return self._is_orref_ref('outputVariables')

    def is_set_output_variables(self):
        return 'outputVariables' in self._values

    def unset_output_variables(self):
        self._values.pop('outputVariables', None); self._orref_is_ref.pop('outputVariables', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_working_algorithms(self):
        return self._working_algorithms.items()

    def add_working_algorithms(self, obj):
        self._working_algorithms.add(obj); obj._attach(self, self.get_document())

    def insert_working_algorithms(self, index, obj):
        self._working_algorithms.insert(index, obj); obj._attach(self, self.get_document())

    def remove_working_algorithms(self, index):
        self._working_algorithms.remove(index)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'steadyState')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'outputVariables' in self._values: d['outputVariables'] = self._values['outputVariables']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class StringFormation(SedBase):
    """Generated from specsheets/tasks/StringFormation/."""
    _FIELDS = [FieldSpec('concatenate', 'ArrayOrRef', True, 'StringFormation-0002', 'StringFormation-0001', 'StringFormation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='StringFormation-0003', item_kind='any', ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'concatenate'}
    _TYPE_CONST = 'stringFormation'
    _TYPE_RULE_ID = 'StringFormation-0004'
    _OWN_CATCHALL = 'StringFormation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _OUTPUTS_JSON = {'outputs': {'[id]': {'type': 'annotatedData', 'dimensions': {'source': 'runtime', 'note': "scalar when no element of concatenate is itself a list; otherwise N-D matching the shape of the list element(s) within concatenate (1D for one list element, higher-D when several list elements are combined pairwise, all sharing the same length/shape per dimension) - not derivable without evaluating concatenate's actual element values"}}, '[id].strings': {'type': 'stringList', 'dimensions': {'source': 'runtime', 'note': "same as [id]'s dimensions above; not derivable without evaluating concatenate"}}}}
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'stringFormation'

    def get_concatenate_value(self):
        return self._get_orref_value('concatenate')

    def get_concatenate_ref(self):
        return self._get_orref_ref('concatenate')

    def set_concatenate_value(self, value):
        self._set_orref_value('concatenate', value)

    def set_concatenate_ref(self, ref):
        self._set_orref_ref('concatenate', ref)

    def is_concatenate_ref(self):
        return self._is_orref_ref('concatenate')

    def is_set_concatenate(self):
        return 'concatenate' in self._values

    def unset_concatenate(self):
        self._values.pop('concatenate', None); self._orref_is_ref.pop('concatenate', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'stringFormation')
        if 'concatenate' in self._values: d['concatenate'] = self._values['concatenate']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Plot2D(SedBase):
    """Generated from specsheets/outputs/Plot2D/."""
    _FIELDS = [FieldSpec('legend', 'BooleanOrRef', False, 'Plot-0001', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Plot-0002', item_kind=None, ref_target=None), FieldSpec('height', 'NumberOrRef', False, 'Plot-0003', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Plot-0004', item_kind=None, ref_target=None), FieldSpec('width', 'NumberOrRef', False, 'Plot-0005', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Plot-0006', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('curves', 'dict', True, 'Plot2D-0002', 'Plot2D-0001', 'Plot2D-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractCurve', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('outputParameters', 'array', False, 'AbstractOutput-0001', None, 'AbstractOutput-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='OutputParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('rightYAxis', 'ref-class', False, 'Plot2D-0003', None, 'Plot2D-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Axis', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('xAxis', 'ref-class', False, 'Plot-0007', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Axis', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('yAxis', 'ref-class', False, 'Plot-0008', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Axis', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'curves'}
    _TYPE_CONST = 'plot2D'
    _TYPE_RULE_ID = 'Plot2D-0004'
    _OWN_CATCHALL = 'Plot2D-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._curves = IdKeyedCollection(_dispatch_AbstractCurve)
        self._output_parameters = ListCollection()
        self._annotations = ListCollection()
        self._right_y_axis = None
        self._x_axis = None
        self._y_axis = None

    def get_type(self):
        return 'plot2D'

    def get_legend_value(self):
        return self._get_orref_value('legend')

    def get_legend_ref(self):
        return self._get_orref_ref('legend')

    def set_legend_value(self, value):
        self._set_orref_value('legend', value)

    def set_legend_ref(self, ref):
        self._set_orref_ref('legend', ref)

    def is_legend_ref(self):
        return self._is_orref_ref('legend')

    def is_set_legend(self):
        return 'legend' in self._values

    def unset_legend(self):
        self._values.pop('legend', None); self._orref_is_ref.pop('legend', None)

    def get_height_value(self):
        return self._get_orref_value('height')

    def get_height_ref(self):
        return self._get_orref_ref('height')

    def set_height_value(self, value):
        self._set_orref_value('height', value)

    def set_height_ref(self, ref):
        self._set_orref_ref('height', ref)

    def is_height_ref(self):
        return self._is_orref_ref('height')

    def is_set_height(self):
        return 'height' in self._values

    def unset_height(self):
        self._values.pop('height', None); self._orref_is_ref.pop('height', None)

    def get_width_value(self):
        return self._get_orref_value('width')

    def get_width_ref(self):
        return self._get_orref_ref('width')

    def set_width_value(self, value):
        self._set_orref_value('width', value)

    def set_width_ref(self, ref):
        self._set_orref_ref('width', ref)

    def is_width_ref(self):
        return self._is_orref_ref('width')

    def is_set_width(self):
        return 'width' in self._values

    def unset_width(self):
        self._values.pop('width', None); self._orref_is_ref.pop('width', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_curves(self):
        return self._curves.ids()

    def get_curves_item(self, item_id):
        return self._curves.get(item_id)

    def add_curves(self, item_id, obj):
        self._curves.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_curves(self, index, item_id, obj):
        self._curves.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_curves(self, item_id):
        self._curves.remove(item_id)

    def set_id_on_curves(self, old_id, new_id):
        self._curves.set_id(old_id, new_id)

    def get_output_parameters(self):
        return self._output_parameters.items()

    def add_output_parameters(self, obj):
        self._output_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_output_parameters(self, index, obj):
        self._output_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_output_parameters(self, index):
        self._output_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_right_y_axis(self):
        if self._right_y_axis is None: raise ApiError('right_y_axis is not set')
        return self._right_y_axis

    def set_right_y_axis(self, obj):
        self._right_y_axis = obj; obj._attach(self, self.get_document())

    def is_set_right_y_axis(self):
        return self._right_y_axis is not None

    def unset_right_y_axis(self):
        self._right_y_axis = None

    def get_x_axis(self):
        if self._x_axis is None: raise ApiError('x_axis is not set')
        return self._x_axis

    def set_x_axis(self, obj):
        self._x_axis = obj; obj._attach(self, self.get_document())

    def is_set_x_axis(self):
        return self._x_axis is not None

    def unset_x_axis(self):
        self._x_axis = None

    def get_y_axis(self):
        if self._y_axis is None: raise ApiError('y_axis is not set')
        return self._y_axis

    def set_y_axis(self, obj):
        self._y_axis = obj; obj._attach(self, self.get_document())

    def is_set_y_axis(self):
        return self._y_axis is not None

    def unset_y_axis(self):
        self._y_axis = None

    def _children(self):
        kids = []
        kids.extend(self._curves.get(i) for i in self._curves.ids())
        kids.extend(self._output_parameters.items())
        kids.extend(self._annotations.items())
        if self._right_y_axis is not None: kids.append(self._right_y_axis)
        if self._x_axis is not None: kids.append(self._x_axis)
        if self._y_axis is not None: kids.append(self._y_axis)
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'curves': return self._curves
        return None

    def _children_with_locations(self):
        out = []
        for i in self._curves.ids():
            out.append((self._curves.get(i), '/curves/' + i))
        for idx, item in enumerate(self._output_parameters.items()):
            out.append((item, '/outputParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._right_y_axis is not None: out.append((self._right_y_axis, '/rightYAxis'))
        if self._x_axis is not None: out.append((self._x_axis, '/xAxis'))
        if self._y_axis is not None: out.append((self._y_axis, '/yAxis'))
        return out

    def _id_collection_names(self):
        return ['curves']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'plot2D')
        if 'legend' in self._values: d['legend'] = self._values['legend']
        if 'height' in self._values: d['height'] = self._values['height']
        if 'width' in self._values: d['width'] = self._values['width']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._curves): d['curves'] = {i: self._curves.get(i).to_json_value() for i in self._curves.ids()}
        if len(self._output_parameters): d['outputParameters'] = [it.to_json_value() for it in self._output_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._right_y_axis is not None: d['rightYAxis'] = self._right_y_axis.to_json_value()
        if self._x_axis is not None: d['xAxis'] = self._x_axis.to_json_value()
        if self._y_axis is not None: d['yAxis'] = self._y_axis.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Plot3D(SedBase):
    """Generated from specsheets/outputs/Plot3D/."""
    _FIELDS = [FieldSpec('legend', 'BooleanOrRef', False, 'Plot-0001', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Plot-0002', item_kind=None, ref_target=None), FieldSpec('height', 'NumberOrRef', False, 'Plot-0003', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Plot-0004', item_kind=None, ref_target=None), FieldSpec('width', 'NumberOrRef', False, 'Plot-0005', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Plot-0006', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('surfaces', 'dict', True, 'Plot3D-0002', 'Plot3D-0001', 'Plot3D-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Surface', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('outputParameters', 'array', False, 'AbstractOutput-0001', None, 'AbstractOutput-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='OutputParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('zAxis', 'ref-class', False, 'Plot3D-0003', None, 'Plot3D-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Axis', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('xAxis', 'ref-class', False, 'Plot-0007', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Axis', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('yAxis', 'ref-class', False, 'Plot-0008', None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Axis', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'surfaces'}
    _TYPE_CONST = 'plot3D'
    _TYPE_RULE_ID = 'Plot3D-0004'
    _OWN_CATCHALL = 'Plot3D-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._surfaces = IdKeyedCollection(lambda tv, _cls=Surface: (_cls, False))
        self._output_parameters = ListCollection()
        self._annotations = ListCollection()
        self._z_axis = None
        self._x_axis = None
        self._y_axis = None

    def get_type(self):
        return 'plot3D'

    def get_legend_value(self):
        return self._get_orref_value('legend')

    def get_legend_ref(self):
        return self._get_orref_ref('legend')

    def set_legend_value(self, value):
        self._set_orref_value('legend', value)

    def set_legend_ref(self, ref):
        self._set_orref_ref('legend', ref)

    def is_legend_ref(self):
        return self._is_orref_ref('legend')

    def is_set_legend(self):
        return 'legend' in self._values

    def unset_legend(self):
        self._values.pop('legend', None); self._orref_is_ref.pop('legend', None)

    def get_height_value(self):
        return self._get_orref_value('height')

    def get_height_ref(self):
        return self._get_orref_ref('height')

    def set_height_value(self, value):
        self._set_orref_value('height', value)

    def set_height_ref(self, ref):
        self._set_orref_ref('height', ref)

    def is_height_ref(self):
        return self._is_orref_ref('height')

    def is_set_height(self):
        return 'height' in self._values

    def unset_height(self):
        self._values.pop('height', None); self._orref_is_ref.pop('height', None)

    def get_width_value(self):
        return self._get_orref_value('width')

    def get_width_ref(self):
        return self._get_orref_ref('width')

    def set_width_value(self, value):
        self._set_orref_value('width', value)

    def set_width_ref(self, ref):
        self._set_orref_ref('width', ref)

    def is_width_ref(self):
        return self._is_orref_ref('width')

    def is_set_width(self):
        return 'width' in self._values

    def unset_width(self):
        self._values.pop('width', None); self._orref_is_ref.pop('width', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_surfaces(self):
        return self._surfaces.ids()

    def get_surfaces_item(self, item_id):
        return self._surfaces.get(item_id)

    def add_surfaces(self, item_id, obj):
        self._surfaces.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_surfaces(self, index, item_id, obj):
        self._surfaces.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_surfaces(self, item_id):
        self._surfaces.remove(item_id)

    def set_id_on_surfaces(self, old_id, new_id):
        self._surfaces.set_id(old_id, new_id)

    def get_output_parameters(self):
        return self._output_parameters.items()

    def add_output_parameters(self, obj):
        self._output_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_output_parameters(self, index, obj):
        self._output_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_output_parameters(self, index):
        self._output_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def get_z_axis(self):
        if self._z_axis is None: raise ApiError('z_axis is not set')
        return self._z_axis

    def set_z_axis(self, obj):
        self._z_axis = obj; obj._attach(self, self.get_document())

    def is_set_z_axis(self):
        return self._z_axis is not None

    def unset_z_axis(self):
        self._z_axis = None

    def get_x_axis(self):
        if self._x_axis is None: raise ApiError('x_axis is not set')
        return self._x_axis

    def set_x_axis(self, obj):
        self._x_axis = obj; obj._attach(self, self.get_document())

    def is_set_x_axis(self):
        return self._x_axis is not None

    def unset_x_axis(self):
        self._x_axis = None

    def get_y_axis(self):
        if self._y_axis is None: raise ApiError('y_axis is not set')
        return self._y_axis

    def set_y_axis(self, obj):
        self._y_axis = obj; obj._attach(self, self.get_document())

    def is_set_y_axis(self):
        return self._y_axis is not None

    def unset_y_axis(self):
        self._y_axis = None

    def _children(self):
        kids = []
        kids.extend(self._surfaces.get(i) for i in self._surfaces.ids())
        kids.extend(self._output_parameters.items())
        kids.extend(self._annotations.items())
        if self._z_axis is not None: kids.append(self._z_axis)
        if self._x_axis is not None: kids.append(self._x_axis)
        if self._y_axis is not None: kids.append(self._y_axis)
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'surfaces': return self._surfaces
        return None

    def _children_with_locations(self):
        out = []
        for i in self._surfaces.ids():
            out.append((self._surfaces.get(i), '/surfaces/' + i))
        for idx, item in enumerate(self._output_parameters.items()):
            out.append((item, '/outputParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        if self._z_axis is not None: out.append((self._z_axis, '/zAxis'))
        if self._x_axis is not None: out.append((self._x_axis, '/xAxis'))
        if self._y_axis is not None: out.append((self._y_axis, '/yAxis'))
        return out

    def _id_collection_names(self):
        return ['surfaces']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'plot3D')
        if 'legend' in self._values: d['legend'] = self._values['legend']
        if 'height' in self._values: d['height'] = self._values['height']
        if 'width' in self._values: d['width'] = self._values['width']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._surfaces): d['surfaces'] = {i: self._surfaces.get(i).to_json_value() for i in self._surfaces.ids()}
        if len(self._output_parameters): d['outputParameters'] = [it.to_json_value() for it in self._output_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        if self._z_axis is not None: d['zAxis'] = self._z_axis.to_json_value()
        if self._x_axis is not None: d['xAxis'] = self._x_axis.to_json_value()
        if self._y_axis is not None: d['yAxis'] = self._y_axis.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Report(SedBase):
    """Generated from specsheets/outputs/Report/."""
    _FIELDS = [FieldSpec('data', 'SIdRef', True, 'Report-0002', 'Report-0001', 'Report-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('outputParameters', 'array', False, 'AbstractOutput-0001', None, 'AbstractOutput-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='OutputParameter', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'data'}
    _TYPE_CONST = 'report'
    _TYPE_RULE_ID = 'Report-0003'
    _OWN_CATCHALL = 'Report-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._output_parameters = ListCollection()
        self._annotations = ListCollection()

    def get_type(self):
        return 'report'

    def get_data(self):
        if 'data' not in self._values: raise ApiError('data is not set')
        return self._values['data']

    def set_data(self, value):
        self._values['data'] = value

    def is_set_data(self):
        return 'data' in self._values

    def unset_data(self):
        self._values.pop('data', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_output_parameters(self):
        return self._output_parameters.items()

    def add_output_parameters(self, obj):
        self._output_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_output_parameters(self, index, obj):
        self._output_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_output_parameters(self, index):
        self._output_parameters.remove(index)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._output_parameters.items())
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._output_parameters.items()):
            out.append((item, '/outputParameters/%d' % idx))
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'report')
        if 'data' in self._values: d['data'] = self._values['data']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._output_parameters): d['outputParameters'] = [it.to_json_value() for it in self._output_parameters.items()]
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Surface(SedBase):
    """Generated from specsheets/outputs/Surface/."""
    _FIELDS = [FieldSpec('surfaceType', 'StringOrRef', True, 'Surface-0002', 'Surface-0001', 'Surface-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('parametricCurve', 'surfaceMesh', 'surfaceContour', 'contour', 'heatMap', 'stackedCurves', 'bar'), ref_type_rule_id='Surface-0003', item_kind=None, ref_target=None), FieldSpec('x', 'SIdRef', True, 'Surface-0005', 'Surface-0004', 'Surface-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('y', 'SIdRef', True, 'Surface-0007', 'Surface-0006', 'Surface-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('z', 'SIdRef', True, 'Surface-0009', 'Surface-0008', 'Surface-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('style', 'SIdRef', False, 'Surface-0010', None, 'Surface-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('order', 'IntegerOrRef', False, 'Surface-0011', None, 'Surface-0000', minimum=0, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Surface-0012', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'surfaceType', 'x', 'y', 'z'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'Surface-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_surface_type_value(self):
        return self._get_orref_value('surfaceType')

    def get_surface_type_ref(self):
        return self._get_orref_ref('surfaceType')

    def set_surface_type_value(self, value):
        self._set_orref_value('surfaceType', value)

    def set_surface_type_ref(self, ref):
        self._set_orref_ref('surfaceType', ref)

    def is_surface_type_ref(self):
        return self._is_orref_ref('surfaceType')

    def is_set_surface_type(self):
        return 'surfaceType' in self._values

    def unset_surface_type(self):
        self._values.pop('surfaceType', None); self._orref_is_ref.pop('surfaceType', None)

    def get_x(self):
        if 'x' not in self._values: raise ApiError('x is not set')
        return self._values['x']

    def set_x(self, value):
        self._values['x'] = value

    def is_set_x(self):
        return 'x' in self._values

    def unset_x(self):
        self._values.pop('x', None)

    def get_y(self):
        if 'y' not in self._values: raise ApiError('y is not set')
        return self._values['y']

    def set_y(self, value):
        self._values['y'] = value

    def is_set_y(self):
        return 'y' in self._values

    def unset_y(self):
        self._values.pop('y', None)

    def get_z(self):
        if 'z' not in self._values: raise ApiError('z is not set')
        return self._values['z']

    def set_z(self, value):
        self._values['z'] = value

    def is_set_z(self):
        return 'z' in self._values

    def unset_z(self):
        self._values.pop('z', None)

    def get_style(self):
        if 'style' not in self._values: raise ApiError('style is not set')
        return self._values['style']

    def set_style(self, value):
        self._values['style'] = value

    def is_set_style(self):
        return 'style' in self._values

    def unset_style(self):
        self._values.pop('style', None)

    def get_order_value(self):
        return self._get_orref_value('order')

    def get_order_ref(self):
        return self._get_orref_ref('order')

    def set_order_value(self, value):
        self._set_orref_value('order', value)

    def set_order_ref(self, ref):
        self._set_orref_ref('order', ref)

    def is_order_ref(self):
        return self._is_orref_ref('order')

    def is_set_order(self):
        return 'order' in self._values

    def unset_order(self):
        self._values.pop('order', None); self._orref_is_ref.pop('order', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'surfaceType' in self._values: d['surfaceType'] = self._values['surfaceType']
        if 'x' in self._values: d['x'] = self._values['x']
        if 'y' in self._values: d['y'] = self._values['y']
        if 'z' in self._values: d['z'] = self._values['z']
        if 'style' in self._values: d['style'] = self._values['style']
        if 'order' in self._values: d['order'] = self._values['order']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Annotation(SedBase):
    """Generated from specsheets/auxiliary/Annotation/."""
    _FIELDS = [FieldSpec('qualifier', 'any', True, 'Annotation-0002', 'Annotation-0001', 'Annotation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('value', 'any', True, None, 'Annotation-0003', 'Annotation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'qualifier', 'value'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'Annotation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_qualifier(self):
        if 'qualifier' not in self._values: raise ApiError('qualifier is not set')
        return self._values['qualifier']

    def set_qualifier(self, value):
        self._values['qualifier'] = value

    def is_set_qualifier(self):
        return 'qualifier' in self._values

    def unset_qualifier(self):
        self._values.pop('qualifier', None)

    def get_value(self):
        if 'value' not in self._values: raise ApiError('value is not set')
        return self._values['value']

    def set_value(self, value):
        self._values['value'] = value

    def is_set_value(self):
        return 'value' in self._values

    def unset_value(self):
        self._values.pop('value', None)

    def _children(self):
        kids = []
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'qualifier' in self._values: d['qualifier'] = self._values['qualifier']
        if 'value' in self._values: d['value'] = self._values['value']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Axis(SedBase):
    """Generated from specsheets/auxiliary/Axis/."""
    _FIELDS = [FieldSpec('scale', 'StringOrRef', False, 'Axis-0001', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('linear', 'log10'), ref_type_rule_id='Axis-0002', item_kind=None, ref_target=None), FieldSpec('min', 'NumberOrRef', False, 'Axis-0003', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Axis-0004', item_kind=None, ref_target=None), FieldSpec('max', 'NumberOrRef', False, 'Axis-0005', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Axis-0006', item_kind=None, ref_target=None), FieldSpec('grid', 'BooleanOrRef', False, 'Axis-0007', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Axis-0008', item_kind=None, ref_target=None), FieldSpec('style', 'SIdRef', False, 'Axis-0009', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('reverse', 'BooleanOrRef', False, 'Axis-0010', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Axis-0011', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'Axis-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_scale_value(self):
        return self._get_orref_value('scale')

    def get_scale_ref(self):
        return self._get_orref_ref('scale')

    def set_scale_value(self, value):
        self._set_orref_value('scale', value)

    def set_scale_ref(self, ref):
        self._set_orref_ref('scale', ref)

    def is_scale_ref(self):
        return self._is_orref_ref('scale')

    def is_set_scale(self):
        return 'scale' in self._values

    def unset_scale(self):
        self._values.pop('scale', None); self._orref_is_ref.pop('scale', None)

    def get_min_value(self):
        return self._get_orref_value('min')

    def get_min_ref(self):
        return self._get_orref_ref('min')

    def set_min_value(self, value):
        self._set_orref_value('min', value)

    def set_min_ref(self, ref):
        self._set_orref_ref('min', ref)

    def is_min_ref(self):
        return self._is_orref_ref('min')

    def is_set_min(self):
        return 'min' in self._values

    def unset_min(self):
        self._values.pop('min', None); self._orref_is_ref.pop('min', None)

    def get_max_value(self):
        return self._get_orref_value('max')

    def get_max_ref(self):
        return self._get_orref_ref('max')

    def set_max_value(self, value):
        self._set_orref_value('max', value)

    def set_max_ref(self, ref):
        self._set_orref_ref('max', ref)

    def is_max_ref(self):
        return self._is_orref_ref('max')

    def is_set_max(self):
        return 'max' in self._values

    def unset_max(self):
        self._values.pop('max', None); self._orref_is_ref.pop('max', None)

    def get_grid_value(self):
        return self._get_orref_value('grid')

    def get_grid_ref(self):
        return self._get_orref_ref('grid')

    def set_grid_value(self, value):
        self._set_orref_value('grid', value)

    def set_grid_ref(self, ref):
        self._set_orref_ref('grid', ref)

    def is_grid_ref(self):
        return self._is_orref_ref('grid')

    def is_set_grid(self):
        return 'grid' in self._values

    def unset_grid(self):
        self._values.pop('grid', None); self._orref_is_ref.pop('grid', None)

    def get_style(self):
        if 'style' not in self._values: raise ApiError('style is not set')
        return self._values['style']

    def set_style(self, value):
        self._values['style'] = value

    def is_set_style(self):
        return 'style' in self._values

    def unset_style(self):
        self._values.pop('style', None)

    def get_reverse_value(self):
        return self._get_orref_value('reverse')

    def get_reverse_ref(self):
        return self._get_orref_ref('reverse')

    def set_reverse_value(self, value):
        self._set_orref_value('reverse', value)

    def set_reverse_ref(self, ref):
        self._set_orref_ref('reverse', ref)

    def is_reverse_ref(self):
        return self._is_orref_ref('reverse')

    def is_set_reverse(self):
        return 'reverse' in self._values

    def unset_reverse(self):
        self._values.pop('reverse', None); self._orref_is_ref.pop('reverse', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'scale' in self._values: d['scale'] = self._values['scale']
        if 'min' in self._values: d['min'] = self._values['min']
        if 'max' in self._values: d['max'] = self._values['max']
        if 'grid' in self._values: d['grid'] = self._values['grid']
        if 'style' in self._values: d['style'] = self._values['style']
        if 'reverse' in self._values: d['reverse'] = self._values['reverse']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Curve(SedBase):
    """Generated from specsheets/auxiliary/Curve/."""
    _FIELDS = [FieldSpec('curveType', 'StringOrRef', True, 'Curve-0002', 'Curve-0001', 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('points', 'bar', 'barStacked', 'horizontalBar', 'horizontalBarStacked', 'shadedArea'), ref_type_rule_id='Curve-0003', item_kind=None, ref_target=None), FieldSpec('y', 'SIdRef', True, 'Curve-0005', 'Curve-0004', 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('xErrorUpper', 'SIdRef', False, 'Curve-0006', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('xErrorLower', 'SIdRef', False, 'Curve-0007', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('yErrorUpper', 'SIdRef', False, 'Curve-0008', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('yErrorLower', 'SIdRef', False, 'Curve-0009', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('yFrom', 'SIdRef', False, 'Curve-0010', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('yTo', 'SIdRef', False, 'Curve-0011', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('x', 'SIdRef', True, 'AbstractCurve-0002', 'AbstractCurve-0001', 'AbstractCurve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target='annotatedData'), FieldSpec('order', 'IntegerOrRef', False, 'AbstractCurve-0003', None, 'AbstractCurve-0000', minimum=0, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='AbstractCurve-0004', item_kind=None, ref_target=None), FieldSpec('style', 'SIdRef', False, 'AbstractCurve-0005', None, 'AbstractCurve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('yAxis', 'StringOrRef', False, 'AbstractCurve-0006', None, 'AbstractCurve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=('right', 'left'), ref_type_rule_id='AbstractCurve-0007', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'curveType', 'y', 'x'}
    _TYPE_CONST = 'curve'
    _TYPE_RULE_ID = 'Curve-0012'
    _OWN_CATCHALL = 'Curve-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_type(self):
        return 'curve'

    def get_curve_type_value(self):
        return self._get_orref_value('curveType')

    def get_curve_type_ref(self):
        return self._get_orref_ref('curveType')

    def set_curve_type_value(self, value):
        self._set_orref_value('curveType', value)

    def set_curve_type_ref(self, ref):
        self._set_orref_ref('curveType', ref)

    def is_curve_type_ref(self):
        return self._is_orref_ref('curveType')

    def is_set_curve_type(self):
        return 'curveType' in self._values

    def unset_curve_type(self):
        self._values.pop('curveType', None); self._orref_is_ref.pop('curveType', None)

    def get_y(self):
        if 'y' not in self._values: raise ApiError('y is not set')
        return self._values['y']

    def set_y(self, value):
        self._values['y'] = value

    def is_set_y(self):
        return 'y' in self._values

    def unset_y(self):
        self._values.pop('y', None)

    def get_x_error_upper(self):
        if 'xErrorUpper' not in self._values: raise ApiError('x_error_upper is not set')
        return self._values['xErrorUpper']

    def set_x_error_upper(self, value):
        self._values['xErrorUpper'] = value

    def is_set_x_error_upper(self):
        return 'xErrorUpper' in self._values

    def unset_x_error_upper(self):
        self._values.pop('xErrorUpper', None)

    def get_x_error_lower(self):
        if 'xErrorLower' not in self._values: raise ApiError('x_error_lower is not set')
        return self._values['xErrorLower']

    def set_x_error_lower(self, value):
        self._values['xErrorLower'] = value

    def is_set_x_error_lower(self):
        return 'xErrorLower' in self._values

    def unset_x_error_lower(self):
        self._values.pop('xErrorLower', None)

    def get_y_error_upper(self):
        if 'yErrorUpper' not in self._values: raise ApiError('y_error_upper is not set')
        return self._values['yErrorUpper']

    def set_y_error_upper(self, value):
        self._values['yErrorUpper'] = value

    def is_set_y_error_upper(self):
        return 'yErrorUpper' in self._values

    def unset_y_error_upper(self):
        self._values.pop('yErrorUpper', None)

    def get_y_error_lower(self):
        if 'yErrorLower' not in self._values: raise ApiError('y_error_lower is not set')
        return self._values['yErrorLower']

    def set_y_error_lower(self, value):
        self._values['yErrorLower'] = value

    def is_set_y_error_lower(self):
        return 'yErrorLower' in self._values

    def unset_y_error_lower(self):
        self._values.pop('yErrorLower', None)

    def get_y_from(self):
        if 'yFrom' not in self._values: raise ApiError('y_from is not set')
        return self._values['yFrom']

    def set_y_from(self, value):
        self._values['yFrom'] = value

    def is_set_y_from(self):
        return 'yFrom' in self._values

    def unset_y_from(self):
        self._values.pop('yFrom', None)

    def get_y_to(self):
        if 'yTo' not in self._values: raise ApiError('y_to is not set')
        return self._values['yTo']

    def set_y_to(self, value):
        self._values['yTo'] = value

    def is_set_y_to(self):
        return 'yTo' in self._values

    def unset_y_to(self):
        self._values.pop('yTo', None)

    def get_x(self):
        if 'x' not in self._values: raise ApiError('x is not set')
        return self._values['x']

    def set_x(self, value):
        self._values['x'] = value

    def is_set_x(self):
        return 'x' in self._values

    def unset_x(self):
        self._values.pop('x', None)

    def get_order_value(self):
        return self._get_orref_value('order')

    def get_order_ref(self):
        return self._get_orref_ref('order')

    def set_order_value(self, value):
        self._set_orref_value('order', value)

    def set_order_ref(self, ref):
        self._set_orref_ref('order', ref)

    def is_order_ref(self):
        return self._is_orref_ref('order')

    def is_set_order(self):
        return 'order' in self._values

    def unset_order(self):
        self._values.pop('order', None); self._orref_is_ref.pop('order', None)

    def get_style(self):
        if 'style' not in self._values: raise ApiError('style is not set')
        return self._values['style']

    def set_style(self, value):
        self._values['style'] = value

    def is_set_style(self):
        return 'style' in self._values

    def unset_style(self):
        self._values.pop('style', None)

    def get_y_axis_value(self):
        return self._get_orref_value('yAxis')

    def get_y_axis_ref(self):
        return self._get_orref_ref('yAxis')

    def set_y_axis_value(self, value):
        self._set_orref_value('yAxis', value)

    def set_y_axis_ref(self, ref):
        self._set_orref_ref('yAxis', ref)

    def is_y_axis_ref(self):
        return self._is_orref_ref('yAxis')

    def is_set_y_axis(self):
        return 'yAxis' in self._values

    def unset_y_axis(self):
        self._values.pop('yAxis', None); self._orref_is_ref.pop('yAxis', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'curve')
        if 'curveType' in self._values: d['curveType'] = self._values['curveType']
        if 'y' in self._values: d['y'] = self._values['y']
        if 'xErrorUpper' in self._values: d['xErrorUpper'] = self._values['xErrorUpper']
        if 'xErrorLower' in self._values: d['xErrorLower'] = self._values['xErrorLower']
        if 'yErrorUpper' in self._values: d['yErrorUpper'] = self._values['yErrorUpper']
        if 'yErrorLower' in self._values: d['yErrorLower'] = self._values['yErrorLower']
        if 'yFrom' in self._values: d['yFrom'] = self._values['yFrom']
        if 'yTo' in self._values: d['yTo'] = self._values['yTo']
        if 'x' in self._values: d['x'] = self._values['x']
        if 'order' in self._values: d['order'] = self._values['order']
        if 'style' in self._values: d['style'] = self._values['style']
        if 'yAxis' in self._values: d['yAxis'] = self._values['yAxis']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class LoopVariable(SedBase):
    """Generated from specsheets/auxiliary/LoopVariable/."""
    _FIELDS = [FieldSpec('initialValue', 'any', True, None, 'LoopVariable-0001', 'LoopVariable-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('subsequentValues', 'SIdRef', True, 'LoopVariable-0003', 'LoopVariable-0002', 'LoopVariable-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'initialValue', 'subsequentValues'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'LoopVariable-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_initial_value(self):
        if 'initialValue' not in self._values: raise ApiError('initial_value is not set')
        return self._values['initialValue']

    def set_initial_value(self, value):
        self._values['initialValue'] = value

    def is_set_initial_value(self):
        return 'initialValue' in self._values

    def unset_initial_value(self):
        self._values.pop('initialValue', None)

    def get_subsequent_values(self):
        if 'subsequentValues' not in self._values: raise ApiError('subsequent_values is not set')
        return self._values['subsequentValues']

    def set_subsequent_values(self, value):
        self._values['subsequentValues'] = value

    def is_set_subsequent_values(self):
        return 'subsequentValues' in self._values

    def unset_subsequent_values(self):
        self._values.pop('subsequentValues', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'initialValue' in self._values: d['initialValue'] = self._values['initialValue']
        if 'subsequentValues' in self._values: d['subsequentValues'] = self._values['subsequentValues']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class OutputParameter(SedBase):
    """Generated from specsheets/auxiliary/OutputParameter/."""
    _FIELDS = [FieldSpec('value', 'any', True, None, 'OutputParameter-0001', 'OutputParameter-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'value'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'OutputParameter-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_value(self):
        if 'value' not in self._values: raise ApiError('value is not set')
        return self._values['value']

    def set_value(self, value):
        self._values['value'] = value

    def is_set_value(self):
        return 'value' in self._values

    def unset_value(self):
        self._values.pop('value', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'value' in self._values: d['value'] = self._values['value']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Span(SedBase):
    """Generated from specsheets/auxiliary/Span/."""
    _FIELDS = [FieldSpec('start', 'NumberOrRef', True, 'Span-0002', 'Span-0001', 'Span-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Span-0003', item_kind=None, ref_target=None), FieldSpec('end', 'NumberOrRef', True, 'Span-0005', 'Span-0004', 'Span-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id='Span-0006', item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'start', 'end'}
    _TYPE_CONST = 'span'
    _TYPE_RULE_ID = 'Span-0007'
    _OWN_CATCHALL = 'Span-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_type(self):
        return 'span'

    def get_start_value(self):
        return self._get_orref_value('start')

    def get_start_ref(self):
        return self._get_orref_ref('start')

    def set_start_value(self, value):
        self._set_orref_value('start', value)

    def set_start_ref(self, ref):
        self._set_orref_ref('start', ref)

    def is_start_ref(self):
        return self._is_orref_ref('start')

    def is_set_start(self):
        return 'start' in self._values

    def unset_start(self):
        self._values.pop('start', None); self._orref_is_ref.pop('start', None)

    def get_end_value(self):
        return self._get_orref_value('end')

    def get_end_ref(self):
        return self._get_orref_ref('end')

    def set_end_value(self, value):
        self._set_orref_value('end', value)

    def set_end_ref(self, ref):
        self._set_orref_ref('end', ref)

    def is_end_ref(self):
        return self._is_orref_ref('end')

    def is_set_end(self):
        return 'end' in self._values

    def unset_end(self):
        self._values.pop('end', None); self._orref_is_ref.pop('end', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'span')
        if 'start' in self._values: d['start'] = self._values['start']
        if 'end' in self._values: d['end'] = self._values['end']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class TaskParameter(SedBase):
    """Generated from specsheets/auxiliary/TaskParameter/."""
    _FIELDS = [FieldSpec('value', 'any', True, None, 'TaskParameter-0001', 'TaskParameter-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'value'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'TaskParameter-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_value(self):
        if 'value' not in self._values: raise ApiError('value is not set')
        return self._values['value']

    def set_value(self, value):
        self._values['value'] = value

    def is_set_value(self):
        return 'value' in self._values

    def unset_value(self):
        self._values.pop('value', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'value' in self._values: d['value'] = self._values['value']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class WorkingAlgorithm(SedBase):
    """Generated from specsheets/auxiliary/WorkingAlgorithm/."""
    _FIELDS = [FieldSpec('algorithm', 'StringOrRef', True, None, 'WorkingAlgorithm-0001', 'WorkingAlgorithm-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('notes', 'any', False, 'SEDBase-0003', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('annotations', 'array', False, 'SEDBase-0004', None, 'SEDBase-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Annotation', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'algorithm'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'WorkingAlgorithm-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._annotations = ListCollection()

    def get_algorithm_value(self):
        return self._get_orref_value('algorithm')

    def get_algorithm_ref(self):
        return self._get_orref_ref('algorithm')

    def set_algorithm_value(self, value):
        self._set_orref_value('algorithm', value)

    def set_algorithm_ref(self, ref):
        self._set_orref_ref('algorithm', ref)

    def is_algorithm_ref(self):
        return self._is_orref_ref('algorithm')

    def is_set_algorithm(self):
        return 'algorithm' in self._values

    def unset_algorithm(self):
        self._values.pop('algorithm', None); self._orref_is_ref.pop('algorithm', None)

    def get_notes(self):
        if 'notes' not in self._values: raise ApiError('notes is not set')
        return self._values['notes']

    def set_notes(self, value):
        self._values['notes'] = value

    def is_set_notes(self):
        return 'notes' in self._values

    def unset_notes(self):
        self._values.pop('notes', None)

    def get_annotations(self):
        return self._annotations.items()

    def add_annotations(self, obj):
        self._annotations.add(obj); obj._attach(self, self.get_document())

    def insert_annotations(self, index, obj):
        self._annotations.insert(index, obj); obj._attach(self, self.get_document())

    def remove_annotations(self, index):
        self._annotations.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._annotations.items())
        return kids

    def _get_id_collection(self, field_name):
        return None

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._annotations.items()):
            out.append((item, '/annotations/%d' % idx))
        return out

    def _id_collection_names(self):
        return []

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'algorithm' in self._values: d['algorithm'] = self._values['algorithm']
        if 'notes' in self._values: d['notes'] = self._values['notes']
        if len(self._annotations): d['annotations'] = [it.to_json_value() for it in self._annotations.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


def _dispatch_AbstractTask(type_value):
    branches = {
        'aggregationCalculation': AggregationCalculation,
        'boundedODESimulation': BoundedODESimulation,
        'boundedStochasticSimulation': BoundedStochasticSimulation,
        'calculation': Calculation,
        'createDataBlock': CreateDataBlock,
        'csvImport': CsvImport,
        'dataImport': DataImport,
        'drawFromDistribution': DrawFromDistribution,
        'explicitODESimulation': ExplicitODESimulation,
        'explicitStochasticSimulation': ExplicitStochasticSimulation,
        'fluxBalanceAnalysis': FluxBalanceAnalysis,
        'jacobianFull': JacobianFull,
        'jacobianReduced': JacobianReduced,
        'loop': Loop,
        'modelChange': ModelChange,
        'modelElementList': ModelElementList,
        'modelImport': ModelImport,
        'numericRange': NumericRange,
        'oneStepODESimulation': OneStepODESimulation,
        'oneStepStochasticSimulation': OneStepStochasticSimulation,
        'parameterRange': ParameterRange,
        'parameterScan': ParameterScan,
        'range': Range,
        'relabelData': RelabelData,
        'scatter': Scatter,
        'steadyState': SteadyState,
        'stringFormation': StringFormation,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_AbstractTask(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractTask holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('AbstractTask-0002', '')
    tv = raw['_type']
    cls = _dispatch_AbstractTask(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {} 
    if m and m.group(1) not in known:
        return UnknownAbstractTask(tv, raw), None
    return UnknownAbstractTask(tv, raw), make_problem('AbstractTask-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


def _dispatch_RangeInline(type_value):
    branches = {
        'numericRange': NumericRange,
        'parameterRange': ParameterRange,
        'range': Range,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_RangeInline(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownRangeInline holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('Range-0004', '')
    tv = raw['_type']
    cls = _dispatch_RangeInline(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {} 
    if m and m.group(1) not in known:
        return UnknownRangeInline(tv, raw), None
    return UnknownRangeInline(tv, raw), make_problem('RangeInline-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


def _dispatch_AbstractOutput(type_value):
    branches = {
        'plot2D': Plot2D,
        'plot3D': Plot3D,
        'report': Report,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_AbstractOutput(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractOutput holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('AbstractOutput-0002', '')
    tv = raw['_type']
    cls = _dispatch_AbstractOutput(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {} 
    if m and m.group(1) not in known:
        return UnknownAbstractOutput(tv, raw), None
    return UnknownAbstractOutput(tv, raw), make_problem('AbstractOutput-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


def _dispatch_AbstractCurve(type_value):
    branches = {
        'curve': Curve,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_AbstractCurve(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractCurve holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('AbstractCurve-0008', '')
    tv = raw['_type']
    cls = _dispatch_AbstractCurve(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {} 
    if m and m.group(1) not in known:
        return UnknownAbstractCurve(tv, raw), None
    return UnknownAbstractCurve(tv, raw), make_problem('AbstractCurve-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


def _load_fields(obj, raw: dict):
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if 'name' in raw: obj.set_name(raw['name'])
    if 'description' in raw: obj.set_description(raw['description'])
    if '_type' in raw: obj._values['_type'] = raw['_type']
    for spec in obj._FIELDS:
        if spec.name not in raw or spec.kind in ('dict', 'array', 'any-dict', 'ref-class', 'ref-discriminator'):
            continue
        v = raw[spec.name]
        if spec.kind in ('StringOrRef', 'NumberOrRef', 'IntegerOrRef', 'BooleanOrRef', 'ArrayOrRef', 'DictOrRef'):
            if is_reference(v):
                obj._set_orref_ref(spec.name, v)
            else:
                obj._set_orref_value(spec.name, v)
        else:
            obj._values[spec.name] = v
    for prefix, specs in obj._NAMESPACE_FIELDS.items():
        for spec in specs:
            if spec.name in raw:
                obj._values[spec.name] = raw[spec.name]
    allowed = obj._allowed_keys()
    for key, value in raw.items():
        if key in ('_type', 'name', 'description'):
            continue
        if key in allowed:
            continue
        m = NAMESPACE_KEY_PATTERN.match(key)
        if m:
            prefix, ns_key = m.group(1), m.group(2)
            obj.set_namespace_attribute(prefix, ns_key, value)
            if prefix in obj._KNOWN_NAMESPACE_PREFIXES:
                catchall = obj._NAMESPACE_CATCHALL.get(prefix, obj._OWN_CATCHALL)
                obj._load_problems.append(make_problem(catchall, '', **{
                    'schema-message': f"Additional property '{key}' is not allowed."}))
            continue
        obj._load_problems.append(make_problem(obj._OWN_CATCHALL, '', **{
            'schema-message': f"Additional property '{key}' is not allowed."}))
    for spec in obj._FIELDS:
        if spec.kind == 'dict' and spec.name in raw:
            raw_value = raw[spec.name]
            if not isinstance(raw_value, dict):
                rid = spec.rule_id or spec.origin_catchall
                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                    'attr': spec.name, 'class': obj.__class__.__name__,
                    'id': obj._own_id_for_message(), 'value': raw_value}))
                continue
            coll = getattr(obj, '_' + _pyname(spec.name))
            dispatch = globals()['parse_' + spec.item_discriminator] if spec.item_discriminator else None
            for item_id, item_raw in raw_value.items():
                if not SID_PATTERN.match(item_id):
                    rid = spec.rule_id or spec.origin_catchall
                    obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                        'attr': spec.name, 'class': obj.__class__.__name__,
                        'id': obj._own_id_for_message(), 'value': item_id}))
                if dispatch is not None:
                    child, problem = dispatch(item_raw)
                    if problem is not None:
                        obj._load_problems.append(problem)
                else:
                    # Plain (non-discriminated) item class: no _type dispatch.
                    child = globals()[spec.item_class]()
                    _load_fields(child, item_raw)
                if child is not None:
                    coll.add(item_id, child)
        elif spec.kind == 'array' and spec.name in raw:
            raw_value = raw[spec.name]
            if not isinstance(raw_value, list):
                rid = spec.rule_id or spec.origin_catchall
                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                    'attr': spec.name, 'class': obj.__class__.__name__,
                    'id': obj._own_id_for_message(), 'value': raw_value}))
                continue
            coll = getattr(obj, '_' + _pyname(spec.name))
            item_cls = globals()[spec.item_class]
            for item_raw in raw_value:
                child = item_cls()
                _load_fields(child, item_raw)
                coll.add(child)
        elif spec.kind == 'any-dict' and spec.name in raw:
            # Every value is stored as-is - a plain JSON value, never
            # constructed as a class instance (see spec.py's _classify_type
            # additionalProperties branch and _collection_accessors' any-dict
            # branch above).
            raw_value = raw[spec.name]
            if not isinstance(raw_value, dict):
                rid = spec.rule_id or spec.origin_catchall
                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                    'attr': spec.name, 'class': obj.__class__.__name__,
                    'id': obj._own_id_for_message(), 'value': raw_value}))
                continue
            coll = getattr(obj, '_' + _pyname(spec.name))
            for item_id, item_value in raw_value.items():
                if not SID_PATTERN.match(item_id):
                    rid = spec.rule_id or spec.origin_catchall
                    obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                        'attr': spec.name, 'class': obj.__class__.__name__,
                        'id': obj._own_id_for_message(), 'value': item_id}))
                coll.add(item_id, item_value)
        elif spec.kind in ('ref-class', 'ref-discriminator') and spec.name in raw:
            # A single nested SedBase-derived child (see emit_model_py's own
            # child_fields/_child_accessors docstring) - 'ref-class' constructs
            # a fixed target class directly; 'ref-discriminator' dispatches on
            # the raw JSON's own _type via the matching parse_* function, same
            # as a dict-kind field's own discriminated items above.
            raw_value = raw[spec.name]
            if not isinstance(raw_value, dict):
                rid = spec.rule_id or spec.origin_catchall
                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                    'attr': spec.name, 'class': obj.__class__.__name__,
                    'id': obj._own_id_for_message(), 'value': raw_value}))
                continue
            if spec.kind == 'ref-discriminator':
                dispatch = globals()['parse_' + spec.item_discriminator]
                child, problem = dispatch(raw_value)
                if problem is not None:
                    obj._load_problems.append(problem)
            else:
                child = globals()[spec.item_class]()
                _load_fields(child, raw_value)
            if child is not None:
                setattr(obj, '_' + _pyname(spec.name), child)


def _pyname(name):
    import re as _re2
    if '@' in name:
        p, k = name.split('@', 1)
        return p + '_' + _pyname(k)
    return _re2.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
