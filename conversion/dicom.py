import os
import nibabel as nib
from nibabel.nifti1 import Nifti1Image
import numpy as np
import pandas as pd
from tqdm import tqdm

from ..logging import info
from ..nifti import recreate_nifti
from ..types import Regions
from .signals import create_flag

def convert_to_nifti(
    dataset: 'Dataset',
    regions: Regions = 'all',
    anonymise: bool = False) -> None:
    # Create NIFTI dataset.
    nifti_ds = recreate_nifti(dataset.name)
    info(f"Converting '{dataset}' to '{nifti_ds}'...")

    # Load all patients.
    pats = dataset.list_patients(regions=regions)

    if anonymise:
        # Create map between patient ID and anonymous ID.
        map_df = pd.DataFrame(pats, columns=['patient-id'])

        # Save map.
        filepath = os.path.join(nifti_ds.path, f'id-map.csv')
        map_df.to_csv(filepath)

    for pat in tqdm(pats):
        # Get anonymous ID.
        if anonymise:
            anon_id = map_df[map_df['patient-id'] == pat].index.values[0]
            filename = f'{anon_id}.nii.gz'
        else:
            filename = f'{pat}.nii.gz'

        # Create image NIFTI.
        patient = dataset.patient(pat)
        data = patient.ct_data()
        spacing = patient.ct_spacing()
        offset = patient.ct_offset()
        affine = np.array([
            [spacing[0], 0, 0, offset[0]],
            [0, spacing[1], 0, offset[1]],
            [0, 0, spacing[2], offset[2]],
            [0, 0, 0, 1]])
        img = Nifti1Image(data, affine)
        filepath = os.path.join(nifti_ds.path, 'data', 'ct', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        nib.save(img, filepath)

        # Create region NIFTIs.
        pat_regions = patient.list_regions(whitelist=regions)
        region_data = patient.region_data(regions=pat_regions)
        for region, data in region_data.items():
            img = Nifti1Image(data.astype(np.int32), affine)
            filepath = os.path.join(nifti_ds.path, 'data', region, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            nib.save(img, filepath)

    # Indicate success.
    create_flag(nifti_ds, '__CONVERT_TO_NIFTI_SUCCESS__')
