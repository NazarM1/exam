from django.apps import apps
import pkgutil
import inspect
from importlib import import_module
from django.db import models as dj_models
# from .Hall import Hall
# from .OutExamVenue import OutExamVenue
# from .ExamVenue import ExamVenue
# from .Period4Exam import Period4Exam
# from .ExamSchedule import ExamSchedule
# from .ExamVenueAssignment import ExamVenueAssignment
# from .ExamRegistration import ExamRegistration
# from .Invigilator import Invigilator
# from .UnavailableDate import UnavailableDate
# from .InvigilationDuty import InvigilationDuty
# from .ExamConflict import ExamConflict
# from .external import Building, Organization, SemesterSubject, GradeDistribution, StudentSubject, GradesRecord, TestForm

def _discover_models():
    models_map = {}
    package = __name__  # e.g., 'control.models'
    for _finder, module_name, ispkg in pkgutil.iter_modules(__path__):
        if ispkg:
            continue
        if module_name.startswith('_') or module_name == '__init__':
            continue
        try:
            module = import_module(f"{package}.{module_name}")
        except Exception:
            # Skip modules that fail to import to avoid breaking discovery
            continue
        for attr_name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, dj_models.Model) and obj.__module__ == module.__name__:
                models_map[attr_name] = obj
    return models_map

# Cache discovered models at import time
_MODELS_CACHE = None

def _get_models_cache():
    global _MODELS_CACHE
    if _MODELS_CACHE is None:
        _MODELS_CACHE = _discover_models()
    return _MODELS_CACHE

def refresh_models_cache():
    global _MODELS_CACHE
    _MODELS_CACHE = _discover_models()
    return _MODELS_CACHE

def get_model_by_name(name):
    models_map = _get_models_cache()
    # Try exact, then case-insensitive
    if name in models_map:
        return models_map[name]
    for k, v in models_map.items():
        if k.lower() == str(name).lower():
            return v
    try:
        return apps.get_model('control', name)
    except LookupError:
        for m in apps.get_app_config('control').get_models():
            if m.__name__.lower() == str(name).lower():
                return m
    return None

def get_model_by_table(table_name):
    # Check discovered first
    for m in _get_models_cache().values():
        if getattr(m._meta, 'db_table', None) == table_name:
            return m
    # Fallback to app registry
    for m in apps.get_app_config('control').get_models():
        if m._meta.db_table == table_name:
            return m
    return None

def list_models():
    # Merge discovered with registry (discovered wins on name conflicts)
    discovered = _get_models_cache()
    registry_map = {m.__name__: m for m in apps.get_app_config('control').get_models()}
    merged = {**registry_map, **discovered}
    return merged
