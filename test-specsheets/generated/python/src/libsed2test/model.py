"""Generated concrete SED2 classes for libsed2test. GENERATED - do not
hand-edit; regenerate from test-specsheets/ via generator/generate.py."""
from __future__ import annotations

from ._runtime import (SedBase, FieldSpec, ApiError, IdKeyedCollection,
                       ListCollection, make_problem, ValidationProblem,
                       is_reference, SID_PATTERN, NAMESPACE_KEY_PATTERN)

class UnknownAbstractWidget(SedBase):
    """Opaque holder for a AbstractWidget instance whose _type names an
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


class UnknownAbstractReport(SedBase):
    """Opaque holder for a AbstractReport instance whose _type names an
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


class UnknownChoiceInline(SedBase):
    """Opaque holder for a ChoiceInline instance whose _type names an
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


class TestDocument(SedBase):
    """Generated from test-specsheets/core/TestDocument/."""
    _FIELDS = [FieldSpec('version', 'string', True, None, 'TestDocument-0001', 'TestDocument-0000', minimum=None, exclusive_minimum=None, pattern='^v\\d+\\.\\d+\\.\\d+$', item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('widgets', 'dict', False, 'TestDocument-0002', None, 'TestDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractWidget', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('reports', 'dict', False, 'TestDocument-0003', None, 'TestDocument-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractReport', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'version'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'TestDocument-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _IS_DOCUMENT_CLASS = True
    _MAX_KNOWN_DOCUMENT_VERSION = 'v1.0.0'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._widgets = IdKeyedCollection(_dispatch_AbstractWidget)
        self._reports = IdKeyedCollection(_dispatch_AbstractReport)
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

    def get_widgets(self):
        return self._widgets.ids()

    def get_widgets_item(self, item_id):
        return self._widgets.get(item_id)

    def add_widgets(self, item_id, obj):
        self._widgets.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_widgets(self, index, item_id, obj):
        self._widgets.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_widgets(self, item_id):
        self._widgets.remove(item_id)

    def set_id_on_widgets(self, old_id, new_id):
        self._widgets.set_id(old_id, new_id)

    def get_reports(self):
        return self._reports.ids()

    def get_reports_item(self, item_id):
        return self._reports.get(item_id)

    def add_reports(self, item_id, obj):
        self._reports.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_reports(self, index, item_id, obj):
        self._reports.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_reports(self, item_id):
        self._reports.remove(item_id)

    def set_id_on_reports(self, old_id, new_id):
        self._reports.set_id(old_id, new_id)

    def _children(self):
        kids = []
        kids.extend(self._widgets.get(i) for i in self._widgets.ids())
        kids.extend(self._reports.get(i) for i in self._reports.ids())
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'widgets': return self._widgets
        if field_name == 'reports': return self._reports
        return None

    def _children_with_locations(self):
        out = []
        for i in self._widgets.ids():
            out.append((self._widgets.get(i), '/widgets/' + i))
        for i in self._reports.ids():
            out.append((self._reports.get(i), '/reports/' + i))
        return out

    def _id_collection_names(self):
        return ['widgets', 'reports']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        if 'version' in self._values: d['version'] = self._values['version']
        if len(self._widgets): d['widgets'] = {i: self._widgets.get(i).to_json_value() for i in self._widgets.ids()}
        if len(self._reports): d['reports'] = {i: self._reports.get(i).to_json_value() for i in self._reports.ids()}
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class FancyWidget(SedBase):
    """Generated from test-specsheets/tasks/FancyWidget/."""
    _FIELDS = [FieldSpec('value', 'StringOrRef', True, None, 'FancyWidget-0001', 'FancyWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('label', 'StringOrRef', False, 'AbstractWidget-0001', None, 'AbstractWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('retries', 'integer', False, 'WidgetOptions-0001', None, 'WidgetOptions-0000', minimum=0, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('timeoutSeconds', 'number', False, 'WidgetOptions-0002', None, 'WidgetOptions-0000', minimum=None, exclusive_minimum=0, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('choices', 'dict', False, None, None, 'FancyWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='ChoiceInline', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('notes', 'array', False, None, None, 'WidgetOptions-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Note', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'value'}
    _TYPE_CONST = 'fancyWidget'
    _TYPE_RULE_ID = 'FancyWidget-0002'
    _OWN_CATCHALL = 'FancyWidget-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._choices = IdKeyedCollection(_dispatch_ChoiceInline)
        self._notes = ListCollection()

    def get_type(self):
        return 'fancyWidget'

    def get_value_value(self):
        return self._get_orref_value('value')

    def get_value_ref(self):
        return self._get_orref_ref('value')

    def set_value_value(self, value):
        self._set_orref_value('value', value)

    def set_value_ref(self, ref):
        self._set_orref_ref('value', ref)

    def is_value_ref(self):
        return self._is_orref_ref('value')

    def is_set_value(self):
        return 'value' in self._values

    def unset_value(self):
        self._values.pop('value', None); self._orref_is_ref.pop('value', None)

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

    def get_retries(self):
        if 'retries' not in self._values: raise ApiError('retries is not set')
        return self._values['retries']

    def set_retries(self, value):
        self._values['retries'] = value

    def is_set_retries(self):
        return 'retries' in self._values

    def unset_retries(self):
        self._values.pop('retries', None)

    def get_timeout_seconds(self):
        if 'timeoutSeconds' not in self._values: raise ApiError('timeout_seconds is not set')
        return self._values['timeoutSeconds']

    def set_timeout_seconds(self, value):
        self._values['timeoutSeconds'] = value

    def is_set_timeout_seconds(self):
        return 'timeoutSeconds' in self._values

    def unset_timeout_seconds(self):
        self._values.pop('timeoutSeconds', None)

    def get_choices(self):
        return self._choices.ids()

    def get_choices_item(self, item_id):
        return self._choices.get(item_id)

    def add_choices(self, item_id, obj):
        self._choices.add(item_id, obj); obj._attach(self, self.get_document())

    def insert_choices(self, index, item_id, obj):
        self._choices.insert(index, item_id, obj); obj._attach(self, self.get_document())

    def remove_choices(self, item_id):
        self._choices.remove(item_id)

    def set_id_on_choices(self, old_id, new_id):
        self._choices.set_id(old_id, new_id)

    def get_notes(self):
        return self._notes.items()

    def add_notes(self, obj):
        self._notes.add(obj); obj._attach(self, self.get_document())

    def insert_notes(self, index, obj):
        self._notes.insert(index, obj); obj._attach(self, self.get_document())

    def remove_notes(self, index):
        self._notes.remove(index)

    def _children(self):
        kids = []
        kids.extend(self._choices.get(i) for i in self._choices.ids())
        kids.extend(self._notes.items())
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'choices': return self._choices
        return None

    def _children_with_locations(self):
        out = []
        for i in self._choices.ids():
            out.append((self._choices.get(i), '/choices/' + i))
        for idx, item in enumerate(self._notes.items()):
            out.append((item, '/notes/%d' % idx))
        return out

    def _id_collection_names(self):
        return ['choices']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'fancyWidget')
        if 'value' in self._values: d['value'] = self._values['value']
        if 'label' in self._values: d['label'] = self._values['label']
        if 'retries' in self._values: d['retries'] = self._values['retries']
        if 'timeoutSeconds' in self._values: d['timeoutSeconds'] = self._values['timeoutSeconds']
        if len(self._choices): d['choices'] = {i: self._choices.get(i).to_json_value() for i in self._choices.ids()}
        if len(self._notes): d['notes'] = [it.to_json_value() for it in self._notes.items()]
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class MathWidget(SedBase):
    """Generated from test-specsheets/tasks/MathWidget/."""
    _FIELDS = [FieldSpec('math', 'StringOrRef', True, 'MathWidget-0002', 'MathWidget-0001', 'MathWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=True, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('label', 'StringOrRef', False, 'AbstractWidget-0001', None, 'AbstractWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'math'}
    _TYPE_CONST = 'mathWidget'
    _TYPE_RULE_ID = 'MathWidget-0003'
    _OWN_CATCHALL = 'MathWidget-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_type(self):
        return 'mathWidget'

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

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

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
        d['_type'] = self._values.get('_type', 'mathWidget')
        if 'math' in self._values: d['math'] = self._values['math']
        if 'label' in self._values: d['label'] = self._values['label']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class SimpleWidget(SedBase):
    """Generated from test-specsheets/tasks/SimpleWidget/."""
    _FIELDS = [FieldSpec('value', 'StringOrRef', True, None, 'SimpleWidget-0001', 'SimpleWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('label', 'StringOrRef', False, 'AbstractWidget-0001', None, 'AbstractWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'value'}
    _TYPE_CONST = 'simpleWidget'
    _TYPE_RULE_ID = 'SimpleWidget-0002'
    _OWN_CATCHALL = 'SimpleWidget-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {'acme': [FieldSpec('acme@priority', 'NumberOrRef', False, 'SimpleWidget-acme-0001', None, 'SimpleWidget-acme-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]}
    _NAMESPACE_CATCHALL = {'acme': 'SimpleWidget-acme-0000'}
    _KNOWN_NAMESPACE_PREFIXES = {'acme'}

    def __init__(self):
        super().__init__()

    def get_type(self):
        return 'simpleWidget'

    def get_value_value(self):
        return self._get_orref_value('value')

    def get_value_ref(self):
        return self._get_orref_ref('value')

    def set_value_value(self, value):
        self._set_orref_value('value', value)

    def set_value_ref(self, ref):
        self._set_orref_ref('value', ref)

    def is_value_ref(self):
        return self._is_orref_ref('value')

    def is_set_value(self):
        return 'value' in self._values

    def unset_value(self):
        self._values.pop('value', None); self._orref_is_ref.pop('value', None)

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

    def get_acme_priority_value(self):
        return self._get_orref_value('acme@priority')
    def get_acme_priority_ref(self):
        return self._get_orref_ref('acme@priority')
    def set_acme_priority_value(self, value):
        self._set_orref_value('acme@priority', value)
    def set_acme_priority_ref(self, ref):
        self._set_orref_ref('acme@priority', ref)
    def is_acme_priority_ref(self):
        return self._is_orref_ref('acme@priority')
    def is_set_acme_priority(self):
        return 'acme@priority' in self._values
    def unset_acme_priority(self):
        self._values.pop('acme@priority', None)

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
        d['_type'] = self._values.get('_type', 'simpleWidget')
        if 'value' in self._values: d['value'] = self._values['value']
        if 'label' in self._values: d['label'] = self._values['label']
        if 'acme@priority' in self._values: d['acme@priority'] = self._values['acme@priority']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class TypesWidget(SedBase):
    """Generated from test-specsheets/tasks/TypesWidget/."""
    _FIELDS = [FieldSpec('anyValue', 'any', False, None, None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('enabled', 'BooleanOrRef', False, 'TypesWidget-0001', None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('count', 'IntegerOrRef', False, 'TypesWidget-0003', None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('items', 'ArrayOrRef', False, 'TypesWidget-0004', None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind='any', ref_target=None), FieldSpec('settings', 'DictOrRef', False, 'TypesWidget-0005', None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind='any', ref_target=None), FieldSpec('label', 'StringOrRef', False, 'AbstractWidget-0001', None, 'AbstractWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('extras', 'any-dict', False, 'TypesWidget-0007', None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('primaryNote', 'ref-class', False, 'TypesWidget-0006', None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class='Note', item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('report', 'ref-discriminator', False, None, None, 'TypesWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator='AbstractReport', is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'typesWidget'
    _TYPE_RULE_ID = 'TypesWidget-0002'
    _OWN_CATCHALL = 'TypesWidget-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()
        self._extras = IdKeyedCollection(None)
        self._primary_note = None
        self._report = None

    def get_type(self):
        return 'typesWidget'

    def get_any_value(self):
        if 'anyValue' not in self._values: raise ApiError('any_value is not set')
        return self._values['anyValue']

    def set_any_value(self, value):
        self._values['anyValue'] = value

    def is_set_any_value(self):
        return 'anyValue' in self._values

    def unset_any_value(self):
        self._values.pop('anyValue', None)

    def get_enabled_value(self):
        return self._get_orref_value('enabled')

    def get_enabled_ref(self):
        return self._get_orref_ref('enabled')

    def set_enabled_value(self, value):
        self._set_orref_value('enabled', value)

    def set_enabled_ref(self, ref):
        self._set_orref_ref('enabled', ref)

    def is_enabled_ref(self):
        return self._is_orref_ref('enabled')

    def is_set_enabled(self):
        return 'enabled' in self._values

    def unset_enabled(self):
        self._values.pop('enabled', None); self._orref_is_ref.pop('enabled', None)

    def get_count_value(self):
        return self._get_orref_value('count')

    def get_count_ref(self):
        return self._get_orref_ref('count')

    def set_count_value(self, value):
        self._set_orref_value('count', value)

    def set_count_ref(self, ref):
        self._set_orref_ref('count', ref)

    def is_count_ref(self):
        return self._is_orref_ref('count')

    def is_set_count(self):
        return 'count' in self._values

    def unset_count(self):
        self._values.pop('count', None); self._orref_is_ref.pop('count', None)

    def get_items_value(self):
        return self._get_orref_value('items')

    def get_items_ref(self):
        return self._get_orref_ref('items')

    def set_items_value(self, value):
        self._set_orref_value('items', value)

    def set_items_ref(self, ref):
        self._set_orref_ref('items', ref)

    def is_items_ref(self):
        return self._is_orref_ref('items')

    def is_set_items(self):
        return 'items' in self._values

    def unset_items(self):
        self._values.pop('items', None); self._orref_is_ref.pop('items', None)

    def get_settings_value(self):
        return self._get_orref_value('settings')

    def get_settings_ref(self):
        return self._get_orref_ref('settings')

    def set_settings_value(self, value):
        self._set_orref_value('settings', value)

    def set_settings_ref(self, ref):
        self._set_orref_ref('settings', ref)

    def is_settings_ref(self):
        return self._is_orref_ref('settings')

    def is_set_settings(self):
        return 'settings' in self._values

    def unset_settings(self):
        self._values.pop('settings', None); self._orref_is_ref.pop('settings', None)

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

    def get_extras(self):
        return self._extras.ids()

    def get_extras_item(self, item_id):
        return self._extras.get(item_id)

    def add_extras(self, item_id, value):
        self._extras.add(item_id, value)

    def insert_extras(self, index, item_id, value):
        self._extras.insert(index, item_id, value)

    def remove_extras(self, item_id):
        self._extras.remove(item_id)

    def set_id_on_extras(self, old_id, new_id):
        self._extras.set_id(old_id, new_id)

    def get_primary_note(self):
        if self._primary_note is None: raise ApiError('primary_note is not set')
        return self._primary_note

    def set_primary_note(self, obj):
        self._primary_note = obj; obj._attach(self, self.get_document())

    def is_set_primary_note(self):
        return self._primary_note is not None

    def unset_primary_note(self):
        self._primary_note = None

    def get_report(self):
        if self._report is None: raise ApiError('report is not set')
        return self._report

    def set_report(self, obj):
        self._report = obj; obj._attach(self, self.get_document())

    def is_set_report(self):
        return self._report is not None

    def unset_report(self):
        self._report = None

    def _children(self):
        kids = []
        if self._primary_note is not None: kids.append(self._primary_note)
        if self._report is not None: kids.append(self._report)
        return kids

    def _get_id_collection(self, field_name):
        if field_name == 'extras': return self._extras
        return None

    def _children_with_locations(self):
        out = []
        if self._primary_note is not None: out.append((self._primary_note, '/primaryNote'))
        if self._report is not None: out.append((self._report, '/report'))
        return out

    def _id_collection_names(self):
        return ['extras']

    def _own_json_value(self):
        d = {}
        if self._name is not None: d['name'] = self._name
        if self._description is not None: d['description'] = self._description
        d['_type'] = self._values.get('_type', 'typesWidget')
        if 'anyValue' in self._values: d['anyValue'] = self._values['anyValue']
        if 'enabled' in self._values: d['enabled'] = self._values['enabled']
        if 'count' in self._values: d['count'] = self._values['count']
        if 'items' in self._values: d['items'] = self._values['items']
        if 'settings' in self._values: d['settings'] = self._values['settings']
        if 'label' in self._values: d['label'] = self._values['label']
        if len(self._extras): d['extras'] = {i: self._extras.get(i) for i in self._extras.ids()}
        if self._primary_note is not None: d['primaryNote'] = self._primary_note.to_json_value()
        if self._report is not None: d['report'] = self._report.to_json_value()
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class SimpleReport(SedBase):
    """Generated from test-specsheets/outputs/SimpleReport/."""
    _FIELDS = [FieldSpec('source', 'SIdRef', True, None, 'SimpleReport-0001', 'SimpleReport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('format', 'StringOrRef', False, 'AbstractReport-0001', None, 'AbstractReport-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'source'}
    _TYPE_CONST = 'simpleReport'
    _TYPE_RULE_ID = 'SimpleReport-0002'
    _OWN_CATCHALL = 'SimpleReport-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_type(self):
        return 'simpleReport'

    def get_source(self):
        if 'source' not in self._values: raise ApiError('source is not set')
        return self._values['source']

    def set_source(self, value):
        self._values['source'] = value

    def is_set_source(self):
        return 'source' in self._values

    def unset_source(self):
        self._values.pop('source', None)

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
        d['_type'] = self._values.get('_type', 'simpleReport')
        if 'source' in self._values: d['source'] = self._values['source']
        if 'format' in self._values: d['format'] = self._values['format']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Choice(SedBase):
    """Generated from test-specsheets/auxiliary/Choice/."""
    _FIELDS = [FieldSpec('label', 'StringOrRef', False, 'Choice-0003', None, 'Choice-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {}
    _TYPE_CONST = 'choice'
    _TYPE_RULE_ID = 'Choice-0002'
    _OWN_CATCHALL = 'Choice-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_type(self):
        return 'choice'

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

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
        d['_type'] = self._values.get('_type', 'choice')
        if 'label' in self._values: d['label'] = self._values['label']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class Note(SedBase):
    """Generated from test-specsheets/auxiliary/Note/."""
    _FIELDS = [FieldSpec('text', 'StringOrRef', True, None, 'Note-0001', 'Note-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'text'}
    _TYPE_CONST = None
    _TYPE_RULE_ID = None
    _OWN_CATCHALL = 'Note-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_text_value(self):
        return self._get_orref_value('text')

    def get_text_ref(self):
        return self._get_orref_ref('text')

    def set_text_value(self, value):
        self._set_orref_value('text', value)

    def set_text_ref(self, ref):
        self._set_orref_ref('text', ref)

    def is_text_ref(self):
        return self._is_orref_ref('text')

    def is_set_text(self):
        return 'text' in self._values

    def unset_text(self):
        self._values.pop('text', None); self._orref_is_ref.pop('text', None)

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
        if 'text' in self._values: d['text'] = self._values['text']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class WeightedChoice(SedBase):
    """Generated from test-specsheets/auxiliary/WeightedChoice/."""
    _FIELDS = [FieldSpec('weight', 'NumberOrRef', True, None, 'WeightedChoice-0001', 'WeightedChoice-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('label', 'StringOrRef', False, 'Choice-0003', None, 'Choice-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'weight'}
    _TYPE_CONST = 'weightedChoice'
    _TYPE_RULE_ID = 'WeightedChoice-0002'
    _OWN_CATCHALL = 'WeightedChoice-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_type(self):
        return 'weightedChoice'

    def get_weight_value(self):
        return self._get_orref_value('weight')

    def get_weight_ref(self):
        return self._get_orref_ref('weight')

    def set_weight_value(self, value):
        self._set_orref_value('weight', value)

    def set_weight_ref(self, ref):
        self._set_orref_ref('weight', ref)

    def is_weight_ref(self):
        return self._is_orref_ref('weight')

    def is_set_weight(self):
        return 'weight' in self._values

    def unset_weight(self):
        self._values.pop('weight', None); self._orref_is_ref.pop('weight', None)

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

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
        d['_type'] = self._values.get('_type', 'weightedChoice')
        if 'weight' in self._values: d['weight'] = self._values['weight']
        if 'label' in self._values: d['label'] = self._values['label']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


class AcmeWidget(SedBase):
    """Generated from test-specsheets/tasks/AcmeWidget/."""
    _FIELDS = [FieldSpec('acme@acmeLevel', 'NumberOrRef', True, None, 'acme-AcmeWidget-0001', 'AcmeWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None), FieldSpec('label', 'StringOrRef', False, 'AbstractWidget-0001', None, 'AbstractWidget-0000', minimum=None, exclusive_minimum=None, pattern=None, item_class=None, item_discriminator=None, is_math=False, min_length=None, enum=None, ref_type_rule_id=None, item_kind=None, ref_target=None)]
    _REQUIRED_NAMES = {'acme@acmeLevel'}
    _TYPE_CONST = 'acme@acmeWidget'
    _TYPE_RULE_ID = 'acme-AcmeWidget-0002'
    _OWN_CATCHALL = 'acme-AcmeWidget-0000'
    _NAME_RULE_ID = 'TestBase-0001'
    _DESC_RULE_ID = None
    _BASE_CATCHALL = 'TestBase-0000'
    _NAMESPACE_FIELDS = {}
    _NAMESPACE_CATCHALL = {}

    def __init__(self):
        super().__init__()

    def get_type(self):
        return 'acme@acmeWidget'

    def get_acme_acme_level_value(self):
        return self._get_orref_value('acme@acmeLevel')

    def get_acme_acme_level_ref(self):
        return self._get_orref_ref('acme@acmeLevel')

    def set_acme_acme_level_value(self, value):
        self._set_orref_value('acme@acmeLevel', value)

    def set_acme_acme_level_ref(self, ref):
        self._set_orref_ref('acme@acmeLevel', ref)

    def is_acme_acme_level_ref(self):
        return self._is_orref_ref('acme@acmeLevel')

    def is_set_acme_acme_level(self):
        return 'acme@acmeLevel' in self._values

    def unset_acme_acme_level(self):
        self._values.pop('acme@acmeLevel', None); self._orref_is_ref.pop('acme@acmeLevel', None)

    def get_label_value(self):
        return self._get_orref_value('label')

    def get_label_ref(self):
        return self._get_orref_ref('label')

    def set_label_value(self, value):
        self._set_orref_value('label', value)

    def set_label_ref(self, ref):
        self._set_orref_ref('label', ref)

    def is_label_ref(self):
        return self._is_orref_ref('label')

    def is_set_label(self):
        return 'label' in self._values

    def unset_label(self):
        self._values.pop('label', None); self._orref_is_ref.pop('label', None)

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
        d['_type'] = self._values.get('_type', 'acme@acmeWidget')
        if 'acme@acmeLevel' in self._values: d['acme@acmeLevel'] = self._values['acme@acmeLevel']
        if 'label' in self._values: d['label'] = self._values['label']
        for (pfx, key), value in self._ns_attrs.items():
            d[f'{pfx}@{key}'] = value
        return d

    def to_json_value(self):
        return self._own_json_value()


def _dispatch_AbstractWidget(type_value):
    branches = {
        'fancyWidget': FancyWidget,
        'mathWidget': MathWidget,
        'simpleWidget': SimpleWidget,
        'typesWidget': TypesWidget,
        'acme@acmeWidget': AcmeWidget,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_AbstractWidget(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractWidget holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('AbstractWidget-0002', '')
    tv = raw['_type']
    cls = _dispatch_AbstractWidget(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {'acme'} 
    if m and m.group(1) not in known:
        return UnknownAbstractWidget(tv, raw), None
    return UnknownAbstractWidget(tv, raw), make_problem('AbstractWidget-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


def _dispatch_AbstractReport(type_value):
    branches = {
        'simpleReport': SimpleReport,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_AbstractReport(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownAbstractReport holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('AbstractReport-0002', '')
    tv = raw['_type']
    cls = _dispatch_AbstractReport(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {} 
    if m and m.group(1) not in known:
        return UnknownAbstractReport(tv, raw), None
    return UnknownAbstractReport(tv, raw), make_problem('AbstractReport-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


def _dispatch_ChoiceInline(type_value):
    branches = {
        'choice': Choice,
        'weightedChoice': WeightedChoice,
    }
    if not isinstance(type_value, str):
        return None
    return branches.get(type_value)


def parse_ChoiceInline(raw: dict):
    """Returns (obj, problem_or_None). obj is None only when _type is
    entirely absent; an unrecognized-but-registered or bare-unrecognized
    _type still returns an UnknownChoiceInline holder plus a violation - an
    unregistered-namespace _type returns one with no violation at all.
    See Design.md's Namespaces / Schema-Pass Errors sections."""
    if not isinstance(raw, dict):
        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)
    if '_type' not in raw:
        return None, make_problem('ChoiceInline-0000', '', **{'schema-message': 'missing _type'})
    tv = raw['_type']
    cls = _dispatch_ChoiceInline(tv)
    if cls is not None:
        obj = cls()
        _load_fields(obj, raw)
        return obj, None
    from ._runtime import NAMESPACE_KEY_PATTERN
    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None
    known = {} 
    if m and m.group(1) not in known:
        return UnknownChoiceInline(tv, raw), None
    return UnknownChoiceInline(tv, raw), make_problem('ChoiceInline-0000', '', **{'schema-message': f'unrecognized _type {tv!r}'})


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
