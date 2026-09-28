"""Generated concrete SED2 classes for libsed2test. GENERATED - do not
hand-edit; regenerate from test-specsheets/ via generator/generate.py."""
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
    """Generated from test-specsheets/core/SEDDocument/."""
    _FIELDS = [FieldSpec('version', 'string', True, ['SEDDocument-0002', 'SEDDocument-0003'], 'SEDDocument-0001', 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern='^v\\d+\\.\\d+\\.\\d+$', item_class=None, item_discriminator=None), FieldSpec('constants', 'dict', False, 'SEDDocument-0005', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AnyValueOrRef'), FieldSpec('tasks', 'dict', False, 'SEDDocument-0006', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask'), FieldSpec('outputs', 'dict', False, 'SEDDocument-0007', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractOutput'), FieldSpec('styles', 'dict', False, 'SEDDocument-0008', None, 'SEDDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='Style')]
    _REQUIRED_NAMES = {'version'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'SEDDocument-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._constants = IdKeyedCollection(_dispatch_AnyValueOrRef)
        self._tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._outputs = IdKeyedCollection(_dispatch_AbstractOutput)
        self._styles = IdKeyedCollection(_dispatch_Style)

    def get_version(self):
        if 'version' not in self._values: raise ApiError('version is not set')
        return self._values['version']

    def set_version(self, value):
        self._values['version'] = value

    def is_set_version(self):
        return 'version' in self._values

    def unset_version(self):
        self._values.pop('version', None)

    def get_constants(self):
        return self._constants.ids()

    def get_constants_item(self, item_id):
        return self._constants.get(item_id)

    def add_constants(self, item_id, obj):
        self._constants.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_constants(self, index, item_id, obj):
        self._constants.insert(index, item_id, obj); obj._attach(self, self.get_document())

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

    def _children(self):
        kids = []
        kids.extend(self._constants.get(i) for i in self._constants.ids())
        kids.extend(self._tasks.get(i) for i in self._tasks.ids())
        kids.extend(self._outputs.get(i) for i in self._outputs.ids())
        kids.extend(self._styles.get(i) for i in self._styles.ids())
        return kids

    def _children_with_locations(self):
        out = []
        for i in self._constants.ids():
            out.append((self._constants.get(i), '/constants/' + i))
        for i in self._tasks.ids():
            out.append((self._tasks.get(i), '/tasks/' + i))
        for i in self._outputs.ids():
            out.append((self._outputs.get(i), '/outputs/' + i))
        for i in self._styles.ids():
            out.append((self._styles.get(i), '/styles/' + i))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'version' in self._values: d['version'] = self._values['version']
        if len(self._constants): d['constants'] = {i: self._constants.get(i).to_json_value() for i in self._constants.ids()}
        if len(self._tasks): d['tasks'] = {i: self._tasks.get(i).to_json_value() for i in self._tasks.ids()}
        if len(self._outputs): d['outputs'] = {i: self._outputs.get(i).to_json_value() for i in self._outputs.ids()}
        if len(self._styles): d['styles'] = {i: self._styles.get(i).to_json_value() for i in self._styles.ids()}
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class AggregationCalculation(SedBase):
    """Generated from test-specsheets/tasks/AggregationCalculation/."""
    _FIELDS = [FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'input'}
    _TYPE_CONST = 'aggregationCalculation'
    _TYPE_RULE_ID = 'AggregationCalculation-0004'
    _OWN_CATCHALL = 'AggregationCalculation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'aggregationCalculation'

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'aggregationCalculation')
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class BoundedODESimulation(SedBase):
    """Generated from test-specsheets/tasks/BoundedODESimulation/."""
    _FIELDS = [FieldSpec('relativeTolerance', 'NumberOrRef', False, ['AbstractODESimulation-0001', 'AbstractODESimulation-0002'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('absoluteTolerance', 'NumberOrRef', False, ['AbstractODESimulation-0003', 'AbstractODESimulation-0004'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('absoluteToleranceAdjustmentFactor', 'NumberOrRef', False, ['AbstractODESimulation-0007', 'AbstractODESimulation-0008'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('toleranceForRootFinder', 'NumberOrRef', False, ['AbstractODESimulation-0009', 'AbstractODESimulation-0010'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('initialStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0011', 'AbstractODESimulation-0012'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maxNumberOfSteps', 'NumberOrRef', False, ['AbstractODESimulation-0013', 'AbstractODESimulation-0014'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maxInternalStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0017', 'AbstractODESimulation-0018'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('minInternalStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0019', 'AbstractODESimulation-0020'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, ['AbstractSimulation-0002', 'AbstractSimulation-0003'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, ['AbstractSimulation-0004', 'AbstractSimulation-0005'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'independentVariableSpan'}
    _TYPE_CONST = 'boundedODESimulation'
    _TYPE_RULE_ID = 'BoundedODESimulation-0006'
    _OWN_CATCHALL = 'BoundedODESimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()

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

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'boundedODESimulation')
        if 'relativeTolerance' in self._values: d['relativeTolerance'] = self._values['relativeTolerance']
        if 'absoluteTolerance' in self._values: d['absoluteTolerance'] = self._values['absoluteTolerance']
        if 'absoluteToleranceAdjustmentFactor' in self._values: d['absoluteToleranceAdjustmentFactor'] = self._values['absoluteToleranceAdjustmentFactor']
        if 'toleranceForRootFinder' in self._values: d['toleranceForRootFinder'] = self._values['toleranceForRootFinder']
        if 'initialStepSize' in self._values: d['initialStepSize'] = self._values['initialStepSize']
        if 'maxNumberOfSteps' in self._values: d['maxNumberOfSteps'] = self._values['maxNumberOfSteps']
        if 'maxInternalStepSize' in self._values: d['maxInternalStepSize'] = self._values['maxInternalStepSize']
        if 'minInternalStepSize' in self._values: d['minInternalStepSize'] = self._values['minInternalStepSize']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class BoundedStochasticSimulation(SedBase):
    """Generated from test-specsheets/tasks/BoundedStochasticSimulation/."""
    _FIELDS = [FieldSpec('seed', 'NumberOrRef', False, ['AbstractStochasticSimulation-0001', 'AbstractStochasticSimulation-0002'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('timeDependentRelativeTolerance', 'NumberOrRef', False, ['AbstractStochasticSimulation-0003', 'AbstractStochasticSimulation-0004'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('minimumTimeStep', 'NumberOrRef', False, ['AbstractStochasticSimulation-0007', 'AbstractStochasticSimulation-0008'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maximumTimeStep', 'NumberOrRef', False, ['AbstractStochasticSimulation-0009', 'AbstractStochasticSimulation-0010'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, ['AbstractSimulation-0002', 'AbstractSimulation-0003'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, ['AbstractSimulation-0004', 'AbstractSimulation-0005'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'independentVariableSpan'}
    _TYPE_CONST = 'boundedStochasticSimulation'
    _TYPE_RULE_ID = 'BoundedStochasticSimulation-0006'
    _OWN_CATCHALL = 'BoundedStochasticSimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()

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

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'boundedStochasticSimulation')
        if 'seed' in self._values: d['seed'] = self._values['seed']
        if 'timeDependentRelativeTolerance' in self._values: d['timeDependentRelativeTolerance'] = self._values['timeDependentRelativeTolerance']
        if 'minimumTimeStep' in self._values: d['minimumTimeStep'] = self._values['minimumTimeStep']
        if 'maximumTimeStep' in self._values: d['maximumTimeStep'] = self._values['maximumTimeStep']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Calculation(SedBase):
    """Generated from test-specsheets/tasks/Calculation/."""
    _FIELDS = [FieldSpec('math', 'StringOrRef', True, ['Calculation-0002', 'Calculation-0003'], 'Calculation-0001', 'Calculation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'math'}
    _TYPE_CONST = 'calculation'
    _TYPE_RULE_ID = 'Calculation-0004'
    _OWN_CATCHALL = 'Calculation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'calculation')
        if 'math' in self._values: d['math'] = self._values['math']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class CreateDataBlock(SedBase):
    """Generated from test-specsheets/tasks/CreateDataBlock/."""
    _FIELDS = [FieldSpec('data', 'string', True, ['CreateDataBlock-0002', 'CreateDataBlock-0003'], 'CreateDataBlock-0001', 'CreateDataBlock-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'data'}
    _TYPE_CONST = 'createDataBlock'
    _TYPE_RULE_ID = 'CreateDataBlock-0004'
    _OWN_CATCHALL = 'CreateDataBlock-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'createDataBlock'

    def get_data(self):
        if 'data' not in self._values: raise ApiError('data is not set')
        return self._values['data']

    def set_data(self, value):
        self._values['data'] = value

    def is_set_data(self):
        return 'data' in self._values

    def unset_data(self):
        self._values.pop('data', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'createDataBlock')
        if 'data' in self._values: d['data'] = self._values['data']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class CsvImport(SedBase):
    """Generated from test-specsheets/tasks/CsvImport/."""
    _FIELDS = [FieldSpec('organization', 'StringOrRef', False, ['CsvImport-0004', 'CsvImport-0005'], None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('separator', 'StringOrRef', False, ['CsvImport-0006', 'CsvImport-0007'], None, 'CsvImport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'location'}
    _TYPE_CONST = 'csvImport'
    _TYPE_RULE_ID = 'CsvImport-0018'
    _OWN_CATCHALL = 'CsvImport-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'csvImport'

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'csvImport')
        if 'organization' in self._values: d['organization'] = self._values['organization']
        if 'separator' in self._values: d['separator'] = self._values['separator']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class DataImport(SedBase):
    """Generated from test-specsheets/tasks/DataImport/."""
    _FIELDS = [FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'location', 'format'}
    _TYPE_CONST = 'dataImport'
    _TYPE_RULE_ID = 'DataImport-0007'
    _OWN_CATCHALL = 'DataImport-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'dataImport'

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'dataImport')
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class DrawFromDistribution(SedBase):
    """Generated from test-specsheets/tasks/DrawFromDistribution/."""
    _FIELDS = [FieldSpec('distribution', 'string', True, ['DrawFromDistribution-0008', 'DrawFromDistribution-0009'], 'DrawFromDistribution-0007', 'DrawFromDistribution-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'distribution', 'arguments'}
    _TYPE_CONST = 'drawFromDistribution'
    _TYPE_RULE_ID = 'DrawFromDistribution-0006'
    _OWN_CATCHALL = 'DrawFromDistribution-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'drawFromDistribution'

    def get_distribution(self):
        if 'distribution' not in self._values: raise ApiError('distribution is not set')
        return self._values['distribution']

    def set_distribution(self, value):
        self._values['distribution'] = value

    def is_set_distribution(self):
        return 'distribution' in self._values

    def unset_distribution(self):
        self._values.pop('distribution', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'drawFromDistribution')
        if 'distribution' in self._values: d['distribution'] = self._values['distribution']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ExplicitODESimulation(SedBase):
    """Generated from test-specsheets/tasks/ExplicitODESimulation/."""
    _FIELDS = [FieldSpec('relativeTolerance', 'NumberOrRef', False, ['AbstractODESimulation-0001', 'AbstractODESimulation-0002'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('absoluteTolerance', 'NumberOrRef', False, ['AbstractODESimulation-0003', 'AbstractODESimulation-0004'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('absoluteToleranceAdjustmentFactor', 'NumberOrRef', False, ['AbstractODESimulation-0007', 'AbstractODESimulation-0008'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('toleranceForRootFinder', 'NumberOrRef', False, ['AbstractODESimulation-0009', 'AbstractODESimulation-0010'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('initialStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0011', 'AbstractODESimulation-0012'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maxNumberOfSteps', 'NumberOrRef', False, ['AbstractODESimulation-0013', 'AbstractODESimulation-0014'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maxInternalStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0017', 'AbstractODESimulation-0018'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('minInternalStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0019', 'AbstractODESimulation-0020'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, ['AbstractSimulation-0002', 'AbstractSimulation-0003'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, ['AbstractSimulation-0004', 'AbstractSimulation-0005'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'independentVariableRange'}
    _TYPE_CONST = 'explicitODESimulation'
    _TYPE_RULE_ID = 'ExplicitODESimulation-0006'
    _OWN_CATCHALL = 'ExplicitODESimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()

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

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'explicitODESimulation')
        if 'relativeTolerance' in self._values: d['relativeTolerance'] = self._values['relativeTolerance']
        if 'absoluteTolerance' in self._values: d['absoluteTolerance'] = self._values['absoluteTolerance']
        if 'absoluteToleranceAdjustmentFactor' in self._values: d['absoluteToleranceAdjustmentFactor'] = self._values['absoluteToleranceAdjustmentFactor']
        if 'toleranceForRootFinder' in self._values: d['toleranceForRootFinder'] = self._values['toleranceForRootFinder']
        if 'initialStepSize' in self._values: d['initialStepSize'] = self._values['initialStepSize']
        if 'maxNumberOfSteps' in self._values: d['maxNumberOfSteps'] = self._values['maxNumberOfSteps']
        if 'maxInternalStepSize' in self._values: d['maxInternalStepSize'] = self._values['maxInternalStepSize']
        if 'minInternalStepSize' in self._values: d['minInternalStepSize'] = self._values['minInternalStepSize']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ExplicitStochasticSimulation(SedBase):
    """Generated from test-specsheets/tasks/ExplicitStochasticSimulation/."""
    _FIELDS = [FieldSpec('seed', 'NumberOrRef', False, ['AbstractStochasticSimulation-0001', 'AbstractStochasticSimulation-0002'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('timeDependentRelativeTolerance', 'NumberOrRef', False, ['AbstractStochasticSimulation-0003', 'AbstractStochasticSimulation-0004'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('minimumTimeStep', 'NumberOrRef', False, ['AbstractStochasticSimulation-0007', 'AbstractStochasticSimulation-0008'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maximumTimeStep', 'NumberOrRef', False, ['AbstractStochasticSimulation-0009', 'AbstractStochasticSimulation-0010'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, ['AbstractSimulation-0002', 'AbstractSimulation-0003'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, ['AbstractSimulation-0004', 'AbstractSimulation-0005'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'independentVariableRange'}
    _TYPE_CONST = 'explicitStochasticSimulation'
    _TYPE_RULE_ID = 'ExplicitStochasticSimulation-0006'
    _OWN_CATCHALL = 'ExplicitStochasticSimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()

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

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'explicitStochasticSimulation')
        if 'seed' in self._values: d['seed'] = self._values['seed']
        if 'timeDependentRelativeTolerance' in self._values: d['timeDependentRelativeTolerance'] = self._values['timeDependentRelativeTolerance']
        if 'minimumTimeStep' in self._values: d['minimumTimeStep'] = self._values['minimumTimeStep']
        if 'maximumTimeStep' in self._values: d['maximumTimeStep'] = self._values['maximumTimeStep']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class FluxBalanceAnalysis(SedBase):
    """Generated from test-specsheets/tasks/FluxBalanceAnalysis/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'FluxBalanceAnalysis-0002', 'FluxBalanceAnalysis-0001', 'FluxBalanceAnalysis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'model', 'outputVariables'}
    _TYPE_CONST = 'fluxBalanceAnalysis'
    _TYPE_RULE_ID = 'FluxBalanceAnalysis-0008'
    _OWN_CATCHALL = 'FluxBalanceAnalysis-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'fluxBalanceAnalysis')
        if 'model' in self._values: d['model'] = self._values['model']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class JacobianFull(SedBase):
    """Generated from test-specsheets/tasks/JacobianFull/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'JacobianFull-0002', 'JacobianFull-0001', 'JacobianFull-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'model'}
    _TYPE_CONST = 'jacobianFull'
    _TYPE_RULE_ID = 'JacobianFull-0003'
    _OWN_CATCHALL = 'JacobianFull-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'jacobianFull')
        if 'model' in self._values: d['model'] = self._values['model']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class JacobianReduced(SedBase):
    """Generated from test-specsheets/tasks/JacobianReduced/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'JacobianReduced-0002', 'JacobianReduced-0001', 'JacobianReduced-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'model'}
    _TYPE_CONST = 'jacobianReduced'
    _TYPE_RULE_ID = 'JacobianReduced-0003'
    _OWN_CATCHALL = 'JacobianReduced-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'jacobianReduced')
        if 'model' in self._values: d['model'] = self._values['model']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Loop(SedBase):
    """Generated from test-specsheets/tasks/Loop/."""
    _FIELDS = [FieldSpec('outputVariableMap', 'string', False, ['Repeat-0002', 'Repeat-0003'], None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('loopVariables', 'dict', True, 'Loop-0003', 'Loop-0002', 'Loop-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='LoopVariable'), FieldSpec('subTasks', 'dict', False, 'Repeat-0001', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask'), FieldSpec('aggregateOutputVariables', 'dict', False, 'Repeat-0004', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AggregationCalculation'), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'loopVariables'}
    _TYPE_CONST = 'loop'
    _TYPE_RULE_ID = 'Loop-0005'
    _OWN_CATCHALL = 'Loop-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._loop_variables = IdKeyedCollection(_dispatch_LoopVariable)
        self._sub_tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._aggregate_output_variables = IdKeyedCollection(_dispatch_AggregationCalculation)
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'loop'

    def get_output_variable_map(self):
        if 'outputVariableMap' not in self._values: raise ApiError('output_variable_map is not set')
        return self._values['outputVariableMap']

    def set_output_variable_map(self, value):
        self._values['outputVariableMap'] = value

    def is_set_output_variable_map(self):
        return 'outputVariableMap' in self._values

    def unset_output_variable_map(self):
        self._values.pop('outputVariableMap', None)

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

    def _children(self):
        kids = []
        kids.extend(self._loop_variables.get(i) for i in self._loop_variables.ids())
        kids.extend(self._sub_tasks.get(i) for i in self._sub_tasks.ids())
        kids.extend(self._aggregate_output_variables.get(i) for i in self._aggregate_output_variables.ids())
        kids.extend(self._task_parameters.items())
        return kids

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
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'loop')
        if 'outputVariableMap' in self._values: d['outputVariableMap'] = self._values['outputVariableMap']
        if len(self._loop_variables): d['loopVariables'] = {i: self._loop_variables.get(i).to_json_value() for i in self._loop_variables.ids()}
        if len(self._sub_tasks): d['subTasks'] = {i: self._sub_tasks.get(i).to_json_value() for i in self._sub_tasks.ids()}
        if len(self._aggregate_output_variables): d['aggregateOutputVariables'] = {i: self._aggregate_output_variables.get(i).to_json_value() for i in self._aggregate_output_variables.ids()}
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ModelChange(SedBase):
    """Generated from test-specsheets/tasks/ModelChange/."""
    _FIELDS = [FieldSpec('inputModel', 'SIdRef', True, 'ModelChange-0002', 'ModelChange-0001', 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('setValues', 'string', False, ['ModelChange-0003', 'ModelChange-0004'], None, 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('replaceElements', 'string', False, ['ModelChange-0009', 'ModelChange-0010'], None, 'ModelChange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'inputModel'}
    _TYPE_CONST = 'modelChange'
    _TYPE_RULE_ID = 'ModelChange-0011'
    _OWN_CATCHALL = 'ModelChange-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_set_values(self):
        if 'setValues' not in self._values: raise ApiError('set_values is not set')
        return self._values['setValues']

    def set_set_values(self, value):
        self._values['setValues'] = value

    def is_set_set_values(self):
        return 'setValues' in self._values

    def unset_set_values(self):
        self._values.pop('setValues', None)

    def get_replace_elements(self):
        if 'replaceElements' not in self._values: raise ApiError('replace_elements is not set')
        return self._values['replaceElements']

    def set_replace_elements(self, value):
        self._values['replaceElements'] = value

    def is_set_replace_elements(self):
        return 'replaceElements' in self._values

    def unset_replace_elements(self):
        self._values.pop('replaceElements', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'modelChange')
        if 'inputModel' in self._values: d['inputModel'] = self._values['inputModel']
        if 'setValues' in self._values: d['setValues'] = self._values['setValues']
        if 'replaceElements' in self._values: d['replaceElements'] = self._values['replaceElements']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ModelElementList(SedBase):
    """Generated from test-specsheets/tasks/ModelElementList/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'ModelElementList-0002', 'ModelElementList-0001', 'ModelElementList-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'model'}
    _TYPE_CONST = 'modelElementList'
    _TYPE_RULE_ID = 'ModelElementList-0011'
    _OWN_CATCHALL = 'ModelElementList-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'modelElementList')
        if 'model' in self._values: d['model'] = self._values['model']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ModelImport(SedBase):
    """Generated from test-specsheets/tasks/ModelImport/."""
    _FIELDS = [FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'location', 'language'}
    _TYPE_CONST = 'modelImport'
    _TYPE_RULE_ID = 'ModelImport-0007'
    _OWN_CATCHALL = 'ModelImport-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'modelImport'

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'modelImport')
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class NumericRange(SedBase):
    """Generated from test-specsheets/tasks/NumericRange/."""
    _FIELDS = [FieldSpec('start', 'NumberOrRef', False, ['NumericRange-0001', 'NumericRange-0002'], None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('end', 'NumberOrRef', False, ['NumericRange-0003', 'NumericRange-0004'], None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('values', 'string', False, ['NumericRange-0011', 'NumericRange-0012'], None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('values', 'string', False, ['Range-0001', 'Range-0002'], None, 'Range-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'numericRange'
    _TYPE_RULE_ID = 'NumericRange-0013'
    _OWN_CATCHALL = 'NumericRange-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_values(self):
        if 'values' not in self._values: raise ApiError('values is not set')
        return self._values['values']

    def set_values(self, value):
        self._values['values'] = value

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None)

    def get_values(self):
        if 'values' not in self._values: raise ApiError('values is not set')
        return self._values['values']

    def set_values(self, value):
        self._values['values'] = value

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'numericRange')
        if 'start' in self._values: d['start'] = self._values['start']
        if 'end' in self._values: d['end'] = self._values['end']
        if 'values' in self._values: d['values'] = self._values['values']
        if 'values' in self._values: d['values'] = self._values['values']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class OneStepODESimulation(SedBase):
    """Generated from test-specsheets/tasks/OneStepODESimulation/."""
    _FIELDS = [FieldSpec('independentStep', 'NumberOrRef', True, ['OneStepODESimulation-0005', 'OneStepODESimulation-0006'], 'OneStepODESimulation-0004', 'OneStepODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('relativeTolerance', 'NumberOrRef', False, ['AbstractODESimulation-0001', 'AbstractODESimulation-0002'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('absoluteTolerance', 'NumberOrRef', False, ['AbstractODESimulation-0003', 'AbstractODESimulation-0004'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('absoluteToleranceAdjustmentFactor', 'NumberOrRef', False, ['AbstractODESimulation-0007', 'AbstractODESimulation-0008'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('toleranceForRootFinder', 'NumberOrRef', False, ['AbstractODESimulation-0009', 'AbstractODESimulation-0010'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('initialStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0011', 'AbstractODESimulation-0012'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maxNumberOfSteps', 'NumberOrRef', False, ['AbstractODESimulation-0013', 'AbstractODESimulation-0014'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maxInternalStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0017', 'AbstractODESimulation-0018'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('minInternalStepSize', 'NumberOrRef', False, ['AbstractODESimulation-0019', 'AbstractODESimulation-0020'], None, 'AbstractODESimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, ['AbstractSimulation-0002', 'AbstractSimulation-0003'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, ['AbstractSimulation-0004', 'AbstractSimulation-0005'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'independentStep'}
    _TYPE_CONST = 'oneStepODE'
    _TYPE_RULE_ID = 'OneStepODESimulation-0007'
    _OWN_CATCHALL = 'OneStepODESimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'oneStepODE'

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

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'oneStepODE')
        if 'independentStep' in self._values: d['independentStep'] = self._values['independentStep']
        if 'relativeTolerance' in self._values: d['relativeTolerance'] = self._values['relativeTolerance']
        if 'absoluteTolerance' in self._values: d['absoluteTolerance'] = self._values['absoluteTolerance']
        if 'absoluteToleranceAdjustmentFactor' in self._values: d['absoluteToleranceAdjustmentFactor'] = self._values['absoluteToleranceAdjustmentFactor']
        if 'toleranceForRootFinder' in self._values: d['toleranceForRootFinder'] = self._values['toleranceForRootFinder']
        if 'initialStepSize' in self._values: d['initialStepSize'] = self._values['initialStepSize']
        if 'maxNumberOfSteps' in self._values: d['maxNumberOfSteps'] = self._values['maxNumberOfSteps']
        if 'maxInternalStepSize' in self._values: d['maxInternalStepSize'] = self._values['maxInternalStepSize']
        if 'minInternalStepSize' in self._values: d['minInternalStepSize'] = self._values['minInternalStepSize']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class OneStepStochasticSimulation(SedBase):
    """Generated from test-specsheets/tasks/OneStepStochasticSimulation/."""
    _FIELDS = [FieldSpec('independentStep', 'NumberOrRef', False, ['OneStepStochasticSimulation-0004', 'OneStepStochasticSimulation-0005'], None, 'OneStepStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('seed', 'NumberOrRef', False, ['AbstractStochasticSimulation-0001', 'AbstractStochasticSimulation-0002'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('timeDependentRelativeTolerance', 'NumberOrRef', False, ['AbstractStochasticSimulation-0003', 'AbstractStochasticSimulation-0004'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('minimumTimeStep', 'NumberOrRef', False, ['AbstractStochasticSimulation-0007', 'AbstractStochasticSimulation-0008'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('maximumTimeStep', 'NumberOrRef', False, ['AbstractStochasticSimulation-0009', 'AbstractStochasticSimulation-0010'], None, 'AbstractStochasticSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('model', 'SIdRef', False, 'AbstractSimulation-0001', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, ['AbstractSimulation-0002', 'AbstractSimulation-0003'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariableInit', 'NumberOrRef', False, ['AbstractSimulation-0004', 'AbstractSimulation-0005'], None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('workingAlgorithms', 'array', False, 'AbstractSimulation-0008', None, 'AbstractSimulation-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='WorkingAlgorithm', item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'oneStepStochastic'
    _TYPE_RULE_ID = 'OneStepStochasticSimulation-0006'
    _OWN_CATCHALL = 'OneStepStochasticSimulation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._working_algorithms = ListCollection()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'oneStepStochastic'

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

    def _children(self):
        kids = []
        kids.extend(self._working_algorithms.items())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._working_algorithms.items()):
            out.append((item, '/workingAlgorithms/%d' % idx))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'oneStepStochastic')
        if 'independentStep' in self._values: d['independentStep'] = self._values['independentStep']
        if 'seed' in self._values: d['seed'] = self._values['seed']
        if 'timeDependentRelativeTolerance' in self._values: d['timeDependentRelativeTolerance'] = self._values['timeDependentRelativeTolerance']
        if 'minimumTimeStep' in self._values: d['minimumTimeStep'] = self._values['minimumTimeStep']
        if 'maximumTimeStep' in self._values: d['maximumTimeStep'] = self._values['maximumTimeStep']
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if 'independentVariableInit' in self._values: d['independentVariableInit'] = self._values['independentVariableInit']
        if len(self._working_algorithms): d['workingAlgorithms'] = [it.to_json_value() for it in self._working_algorithms.items()]
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ParameterRange(SedBase):
    """Generated from test-specsheets/tasks/ParameterRange/."""
    _FIELDS = [FieldSpec('modelElement', 'StringOrRef', True, ['ParameterRange-0002', 'ParameterRange-0003'], 'ParameterRange-0001', 'ParameterRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('start', 'NumberOrRef', False, ['NumericRange-0001', 'NumericRange-0002'], None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('end', 'NumberOrRef', False, ['NumericRange-0003', 'NumericRange-0004'], None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('values', 'string', False, ['NumericRange-0011', 'NumericRange-0012'], None, 'NumericRange-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('values', 'string', False, ['Range-0001', 'Range-0002'], None, 'Range-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'modelElement'}
    _TYPE_CONST = 'parameterRange'
    _TYPE_RULE_ID = 'ParameterRange-0016'
    _OWN_CATCHALL = 'ParameterRange-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_values(self):
        if 'values' not in self._values: raise ApiError('values is not set')
        return self._values['values']

    def set_values(self, value):
        self._values['values'] = value

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None)

    def get_values(self):
        if 'values' not in self._values: raise ApiError('values is not set')
        return self._values['values']

    def set_values(self, value):
        self._values['values'] = value

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'parameterRange')
        if 'modelElement' in self._values: d['modelElement'] = self._values['modelElement']
        if 'start' in self._values: d['start'] = self._values['start']
        if 'end' in self._values: d['end'] = self._values['end']
        if 'values' in self._values: d['values'] = self._values['values']
        if 'values' in self._values: d['values'] = self._values['values']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class ParameterScan(SedBase):
    """Generated from test-specsheets/tasks/ParameterScan/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, 'ParameterScan-0002', 'ParameterScan-0001', 'ParameterScan-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('outputVariableMap', 'string', False, ['Repeat-0002', 'Repeat-0003'], None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('parameterRanges', 'array', True, 'ParameterScan-0004', 'ParameterScan-0003', 'ParameterScan-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='ParameterRangeInline', item_discriminator=None), FieldSpec('subTasks', 'dict', False, 'Repeat-0001', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask'), FieldSpec('aggregateOutputVariables', 'dict', False, 'Repeat-0004', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AggregationCalculation'), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'model', 'parameterRanges'}
    _TYPE_CONST = 'parameterScan'
    _TYPE_RULE_ID = 'ParameterScan-0006'
    _OWN_CATCHALL = 'ParameterScan-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._parameter_ranges = ListCollection()
        self._sub_tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._aggregate_output_variables = IdKeyedCollection(_dispatch_AggregationCalculation)
        self._task_parameters = ListCollection()

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

    def get_output_variable_map(self):
        if 'outputVariableMap' not in self._values: raise ApiError('output_variable_map is not set')
        return self._values['outputVariableMap']

    def set_output_variable_map(self, value):
        self._values['outputVariableMap'] = value

    def is_set_output_variable_map(self):
        return 'outputVariableMap' in self._values

    def unset_output_variable_map(self):
        self._values.pop('outputVariableMap', None)

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

    def _children(self):
        kids = []
        kids.extend(self._parameter_ranges.items())
        kids.extend(self._sub_tasks.get(i) for i in self._sub_tasks.ids())
        kids.extend(self._aggregate_output_variables.get(i) for i in self._aggregate_output_variables.ids())
        kids.extend(self._task_parameters.items())
        return kids

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
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'parameterScan')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'outputVariableMap' in self._values: d['outputVariableMap'] = self._values['outputVariableMap']
        if len(self._parameter_ranges): d['parameterRanges'] = [it.to_json_value() for it in self._parameter_ranges.items()]
        if len(self._sub_tasks): d['subTasks'] = {i: self._sub_tasks.get(i).to_json_value() for i in self._sub_tasks.ids()}
        if len(self._aggregate_output_variables): d['aggregateOutputVariables'] = {i: self._aggregate_output_variables.get(i).to_json_value() for i in self._aggregate_output_variables.ids()}
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Range(SedBase):
    """Generated from test-specsheets/tasks/Range/."""
    _FIELDS = [FieldSpec('values', 'string', False, ['Range-0001', 'Range-0002'], None, 'Range-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'range'
    _TYPE_RULE_ID = 'Range-0003'
    _OWN_CATCHALL = 'Range-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'range'

    def get_values(self):
        if 'values' not in self._values: raise ApiError('values is not set')
        return self._values['values']

    def set_values(self, value):
        self._values['values'] = value

    def is_set_values(self):
        return 'values' in self._values

    def unset_values(self):
        self._values.pop('values', None)

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'range')
        if 'values' in self._values: d['values'] = self._values['values']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class RelabelData(SedBase):
    """Generated from test-specsheets/tasks/RelabelData/."""
    _FIELDS = [FieldSpec('input', 'SIdRef', True, 'RelabelData-0002', 'RelabelData-0001', 'RelabelData-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'input', 'labels'}
    _TYPE_CONST = 'relabelData'
    _TYPE_RULE_ID = 'RelabelData-0006'
    _OWN_CATCHALL = 'RelabelData-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'relabelData')
        if 'input' in self._values: d['input'] = self._values['input']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Scatter(SedBase):
    """Generated from test-specsheets/tasks/Scatter/."""
    _FIELDS = [FieldSpec('outputVariableMap', 'string', False, ['Repeat-0002', 'Repeat-0003'], None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('subTasks', 'dict', False, 'Repeat-0001', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractTask'), FieldSpec('aggregateOutputVariables', 'dict', False, 'Repeat-0004', None, 'Repeat-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AggregationCalculation'), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'scatter'
    _TYPE_RULE_ID = 'Scatter-0003'
    _OWN_CATCHALL = 'Scatter-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._sub_tasks = IdKeyedCollection(_dispatch_AbstractTask)
        self._aggregate_output_variables = IdKeyedCollection(_dispatch_AggregationCalculation)
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'scatter'

    def get_output_variable_map(self):
        if 'outputVariableMap' not in self._values: raise ApiError('output_variable_map is not set')
        return self._values['outputVariableMap']

    def set_output_variable_map(self, value):
        self._values['outputVariableMap'] = value

    def is_set_output_variable_map(self):
        return 'outputVariableMap' in self._values

    def unset_output_variable_map(self):
        self._values.pop('outputVariableMap', None)

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

    def _children(self):
        kids = []
        kids.extend(self._sub_tasks.get(i) for i in self._sub_tasks.ids())
        kids.extend(self._aggregate_output_variables.get(i) for i in self._aggregate_output_variables.ids())
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for i in self._sub_tasks.ids():
            out.append((self._sub_tasks.get(i), '/subTasks/' + i))
        for i in self._aggregate_output_variables.ids():
            out.append((self._aggregate_output_variables.get(i), '/aggregateOutputVariables/' + i))
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'scatter')
        if 'outputVariableMap' in self._values: d['outputVariableMap'] = self._values['outputVariableMap']
        if len(self._sub_tasks): d['subTasks'] = {i: self._sub_tasks.get(i).to_json_value() for i in self._sub_tasks.ids()}
        if len(self._aggregate_output_variables): d['aggregateOutputVariables'] = {i: self._aggregate_output_variables.get(i).to_json_value() for i in self._aggregate_output_variables.ids()}
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Span(SedBase):
    """Generated from test-specsheets/tasks/Span/."""
    _FIELDS = [FieldSpec('start', 'NumberOrRef', True, ['Span-0002', 'Span-0003'], 'Span-0001', 'Span-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('end', 'NumberOrRef', True, ['Span-0005', 'Span-0006'], 'Span-0004', 'Span-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None)]
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

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'span')
        if 'start' in self._values: d['start'] = self._values['start']
        if 'end' in self._values: d['end'] = self._values['end']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class SteadyState(SedBase):
    """Generated from test-specsheets/tasks/SteadyState/."""
    _FIELDS = [FieldSpec('model', 'SIdRef', True, None, 'SteadyState-0001', 'SteadyState-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('independentVariable', 'StringOrRef', False, 'SteadyState-0004', None, 'SteadyState-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'model', 'outputVariables'}
    _TYPE_CONST = 'steadyState'
    _TYPE_RULE_ID = 'SteadyState-0003'
    _OWN_CATCHALL = 'SteadyState-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

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

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'steadyState')
        if 'model' in self._values: d['model'] = self._values['model']
        if 'independentVariable' in self._values: d['independentVariable'] = self._values['independentVariable']
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class StringFormation(SedBase):
    """Generated from test-specsheets/tasks/StringFormation/."""
    _FIELDS = [FieldSpec('taskParameters', 'array', False, 'AbstractTask-0001', None, 'AbstractTask-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='TaskParameter', item_discriminator=None)]
    _REQUIRED_NAMES = {'concatenate'}
    _TYPE_CONST = 'stringFormation'
    _TYPE_RULE_ID = 'StringFormation-0004'
    _OWN_CATCHALL = 'StringFormation-0000'
    _NAME_RULE_ID = 'SEDBase-0001'
    _DESC_RULE_ID = 'SEDBase-0002'
    _BASE_CATCHALL = 'SEDBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._task_parameters = ListCollection()

    def get_type(self):
        return 'stringFormation'

    def get_task_parameters(self):
        return self._task_parameters.items()

    def add_task_parameters(self, obj):
        self._task_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_task_parameters(self, index, obj):
        self._task_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_task_parameters(self, index):
        self._task_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._task_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._task_parameters.items()):
            out.append((item, '/taskParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'stringFormation')
        if len(self._task_parameters): d['taskParameters'] = [it.to_json_value() for it in self._task_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Plot2D(SedBase):
    """Generated from test-specsheets/outputs/Plot2D/."""
    _FIELDS = [FieldSpec('height', 'NumberOrRef', False, ['Plot-0003', 'Plot-0004'], None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('width', 'NumberOrRef', False, ['Plot-0005', 'Plot-0006'], None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('curves', 'dict', True, 'Plot2D-0002', 'Plot2D-0001', 'Plot2D-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractCurve'), FieldSpec('outputParameters', 'array', False, 'AbstractOutput-0001', None, 'AbstractOutput-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='OutputParameter', item_discriminator=None)]
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

    def get_type(self):
        return 'plot2D'

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

    def _children(self):
        kids = []
        kids.extend(self._curves.get(i) for i in self._curves.ids())
        kids.extend(self._output_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for i in self._curves.ids():
            out.append((self._curves.get(i), '/curves/' + i))
        for idx, item in enumerate(self._output_parameters.items()):
            out.append((item, '/outputParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'plot2D')
        if 'height' in self._values: d['height'] = self._values['height']
        if 'width' in self._values: d['width'] = self._values['width']
        if len(self._curves): d['curves'] = {i: self._curves.get(i).to_json_value() for i in self._curves.ids()}
        if len(self._output_parameters): d['outputParameters'] = [it.to_json_value() for it in self._output_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Plot3D(SedBase):
    """Generated from test-specsheets/outputs/Plot3D/."""
    _FIELDS = [FieldSpec('height', 'NumberOrRef', False, ['Plot-0003', 'Plot-0004'], None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('width', 'NumberOrRef', False, ['Plot-0005', 'Plot-0006'], None, 'Plot-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('surfaces', 'dict', True, 'Plot3D-0002', 'Plot3D-0001', 'Plot3D-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='Surface'), FieldSpec('outputParameters', 'array', False, 'AbstractOutput-0001', None, 'AbstractOutput-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='OutputParameter', item_discriminator=None)]
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
        self._surfaces = IdKeyedCollection(_dispatch_Surface)
        self._output_parameters = ListCollection()

    def get_type(self):
        return 'plot3D'

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

    def _children(self):
        kids = []
        kids.extend(self._surfaces.get(i) for i in self._surfaces.ids())
        kids.extend(self._output_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for i in self._surfaces.ids():
            out.append((self._surfaces.get(i), '/surfaces/' + i))
        for idx, item in enumerate(self._output_parameters.items()):
            out.append((item, '/outputParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'plot3D')
        if 'height' in self._values: d['height'] = self._values['height']
        if 'width' in self._values: d['width'] = self._values['width']
        if len(self._surfaces): d['surfaces'] = {i: self._surfaces.get(i).to_json_value() for i in self._surfaces.ids()}
        if len(self._output_parameters): d['outputParameters'] = [it.to_json_value() for it in self._output_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Report(SedBase):
    """Generated from test-specsheets/outputs/Report/."""
    _FIELDS = [FieldSpec('data', 'SIdRef', True, 'Report-0002', 'Report-0001', 'Report-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('outputParameters', 'array', False, 'AbstractOutput-0001', None, 'AbstractOutput-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='OutputParameter', item_discriminator=None)]
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

    def get_output_parameters(self):
        return self._output_parameters.items()

    def add_output_parameters(self, obj):
        self._output_parameters.add(obj); obj._attach(self, self.get_document())

    def insert_output_parameters(self, index, obj):
        self._output_parameters.insert(index, obj); obj._attach(self, self.get_document())

    def remove_output_parameters(self, index):
        self._output_parameters.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._output_parameters.items())
        return kids

    def _children_with_locations(self):
        out = []
        for idx, item in enumerate(self._output_parameters.items()):
            out.append((item, '/outputParameters/%d' % idx))
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'report')
        if 'data' in self._values: d['data'] = self._values['data']
        if len(self._output_parameters): d['outputParameters'] = [it.to_json_value() for it in self._output_parameters.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Annotation(SedBase):
    """Generated from test-specsheets/auxiliary/Annotation/."""
    _FIELDS = []
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

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Axis(SedBase):
    """Generated from test-specsheets/auxiliary/Axis/."""
    _FIELDS = [FieldSpec('min', 'NumberOrRef', False, ['Axis-0003', 'Axis-0004'], None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('max', 'NumberOrRef', False, ['Axis-0005', 'Axis-0006'], None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('style', 'SIdRef', False, 'Axis-0009', None, 'Axis-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None)]
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

    def get_style(self):
        if 'style' not in self._values: raise ApiError('style is not set')
        return self._values['style']

    def set_style(self, value):
        self._values['style'] = value

    def is_set_style(self):
        return 'style' in self._values

    def unset_style(self):
        self._values.pop('style', None)

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'min' in self._values: d['min'] = self._values['min']
        if 'max' in self._values: d['max'] = self._values['max']
        if 'style' in self._values: d['style'] = self._values['style']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Curve(SedBase):
    """Generated from test-specsheets/auxiliary/Curve/."""
    _FIELDS = [FieldSpec('curveType', 'string', True, ['Curve-0002', 'Curve-0003'], 'Curve-0001', 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('y', 'SIdRef', True, 'Curve-0005', 'Curve-0004', 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('xErrorUpper', 'SIdRef', False, 'Curve-0006', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('xErrorLower', 'SIdRef', False, 'Curve-0007', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('yErrorUpper', 'SIdRef', False, 'Curve-0008', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('yErrorLower', 'SIdRef', False, 'Curve-0009', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('yFrom', 'SIdRef', False, 'Curve-0010', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('yTo', 'SIdRef', False, 'Curve-0011', None, 'Curve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('x', 'SIdRef', True, 'AbstractCurve-0002', 'AbstractCurve-0001', 'AbstractCurve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('style', 'SIdRef', False, 'AbstractCurve-0005', None, 'AbstractCurve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None), FieldSpec('yAxis', 'string', False, ['AbstractCurve-0006', 'AbstractCurve-0007'], None, 'AbstractCurve-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None)]
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

    def get_type(self):
        return 'curve'

    def get_curve_type(self):
        if 'curveType' not in self._values: raise ApiError('curve_type is not set')
        return self._values['curveType']

    def set_curve_type(self, value):
        self._values['curveType'] = value

    def is_set_curve_type(self):
        return 'curveType' in self._values

    def unset_curve_type(self):
        self._values.pop('curveType', None)

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

    def get_style(self):
        if 'style' not in self._values: raise ApiError('style is not set')
        return self._values['style']

    def set_style(self, value):
        self._values['style'] = value

    def is_set_style(self):
        return 'style' in self._values

    def unset_style(self):
        self._values.pop('style', None)

    def get_y_axis(self):
        if 'yAxis' not in self._values: raise ApiError('y_axis is not set')
        return self._values['yAxis']

    def set_y_axis(self, value):
        self._values['yAxis'] = value

    def is_set_y_axis(self):
        return 'yAxis' in self._values

    def unset_y_axis(self):
        self._values.pop('yAxis', None)

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

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
        if 'style' in self._values: d['style'] = self._values['style']
        if 'yAxis' in self._values: d['yAxis'] = self._values['yAxis']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class OutputParameter(SedBase):
    """Generated from test-specsheets/auxiliary/OutputParameter/."""
    _FIELDS = []
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

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class TaskParameter(SedBase):
    """Generated from test-specsheets/auxiliary/TaskParameter/."""
    _FIELDS = []
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

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class WorkingAlgorithm(SedBase):
    """Generated from test-specsheets/auxiliary/WorkingAlgorithm/."""
    _FIELDS = [FieldSpec('algorithm', 'StringOrRef', True, None, 'WorkingAlgorithm-0001', 'WorkingAlgorithm-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None)]
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

    def _children(self):
        kids = []
        return kids

    def _children_with_locations(self):
        out = []
        return out

    def _own_id_for_message(self):
        p = self.get_parent()
        return '?'

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'algorithm' in self._values: d['algorithm'] = self._values['algorithm']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


def _dispatch_AbstractTask(type_value):
    branches = {
        'aggregationCalculation': AggregationCalculation,
        'calculation': Calculation,
        'createDataBlock': CreateDataBlock,
        'csvImport': CsvImport,
        'dataImport': DataImport,
        'drawFromDistribution': DrawFromDistribution,
        'fluxBalanceAnalysis': FluxBalanceAnalysis,
        'jacobianFull': JacobianFull,
        'jacobianReduced': JacobianReduced,
        'modelChange': ModelChange,
        'modelElementList': ModelElementList,
        'modelImport': ModelImport,
        'relabelData': RelabelData,
        'steadyState': SteadyState,
        'stringFormation': StringFormation,
    }
    return branches.get(type_value)


def parse_AbstractTask(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractTask holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
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
        'range': Range,
    }
    return branches.get(type_value)


def parse_RangeInline(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownRangeInline holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
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
        'report': Report,
    }
    return branches.get(type_value)


def parse_AbstractOutput(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractOutput holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
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
    return branches.get(type_value)


def parse_AbstractCurve(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractCurve holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
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
    if 'name' in raw: obj.set_name(raw['name'])
    if 'description' in raw: obj.set_description(raw['description'])
    if '_type' in raw: obj._values['_type'] = raw['_type']
    for spec in obj._FIELDS:
        if spec.name not in raw or spec.kind in ('dict', 'array'):
            continue
        v = raw[spec.name]
        if spec.kind in ('StringOrRef', 'NumberOrRef'):
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
            dispatch = globals()['parse_' + spec.item_discriminator]
            for item_id, item_raw in raw_value.items():
                if not SID_PATTERN.match(item_id):
                    rid = spec.rule_id or spec.origin_catchall
                    obj._load_problems.append(make_problem(rid, '/' + spec.name, **{
                        'attr': spec.name, 'class': obj.__class__.__name__,
                        'id': obj._own_id_for_message(), 'value': item_id}))
                child, problem = dispatch(item_raw)
                if problem is not None:
                    obj._load_problems.append(problem)
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


def _pyname(name):
    import re as _re2
    if '@' in name:
        p, k = name.split('@', 1)
        return p + '_' + _pyname(k)
    return _re2.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
