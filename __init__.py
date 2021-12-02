from typing import Optional

from .dataset import Dataset, DatasetType, to_type
from .dicom import DICOMDataset
from .dicom import list as list_dicom
from .nifti import NIFTIDataset
from .nifti import list as list_nifti

def get(
    modality: str = 'CT', 
    name: Optional[str] = None,
    path: Optional[str] = None,
    type: str = 'DICOM') -> Dataset:
    """
    returns: the dataset.
    args:
        name: the dataset name.
        path: the dataset path.
        type: the dataset type string. Case is lowered before comparison with types.
    raises:
        ValueError: if neither or both of 'name' and 'path' are given.
        ValueError: if 'type' is not valid.
    """
    # Validate arguments.
    if bool(name) == bool(path):
        raise ValueError(f"One (only) of 'name' or 'path' must be given.")

    # Create dataset.
    type = to_type(type)
    if type == DatasetType.DICOM:
        return DICOMDataset(name)
    elif type == DatasetType.NIFTI:
        return NIFTIDataset(name)
    else:
        types = [t.name for t in DatasetType]
        raise ValueError(f"Dataset type '{type}' not found, expected one of '{types}.")

def default() -> Optional[Dataset]:
    """
    returns: the default active dataset.
    """
    # Preferences from high to low.
    nifti_ds = list_nifti()
    if len(nifti_ds) != 0:
        return get(nifti_ds[0])

    dicom_ds = list_dicom()
    if len(dicom_ds) != 0:
        return get(dicom_ds[0])

    return None

ds = default()

def select(
    name: str,
    type: Optional[str] = None) -> None:
    global ds
    ds = get(name, type)

def active() -> Optional[str]:
    return str(ds) if ds else None

# DICOMDataset API.

def list_patients(*args, **kwargs):
    return ds.list_patients(*args, **kwargs)

def list_regions(*args, **kwargs):
    return ds.list_regions(*args, **kwargs)

def info(*args, **kwargs):
    return ds.info(*args, **kwargs)

def ct_distribution(*args, **kwargs):
    return ds.ct_distribution(*args, **kwargs)

def ct_summary(*args, **kwargs):
    return ds.ct_summary(*args, **kwargs)

def patient(*args, **kwargs):
    return ds.patient(*args, **kwargs)

def region_summary(*args, **kwargs):
    return ds.region_summary(*args, **kwargs)

def trimmed_errors(*args, **kwargs):
    return ds.trimmed_errors(*args, **kwargs)

# NIFTIDataset API.

def list_patients(*args, **kwargs):
    return ds.list_patients(*args, **kwargs)

def list_regions(*args, **kwargs):
    return ds.list_regions(*args, **kwargs)

def object(*args, **kwargs):
    return ds.object(*args, **kwargs)

# TrainingDataset API.

def manifest(*args, **kwargs):
    return ds.manifest(*args, **kwargs)

def params(*args, **kwargs):
    return ds.params(*args, **kwargs)

def class_frequencies(*args, **kwargs):
    return ds.class_frequencies(*args, **kwargs)

def partition(*args, **kwargs):
    return ds.partition(*args, **kwargs)
