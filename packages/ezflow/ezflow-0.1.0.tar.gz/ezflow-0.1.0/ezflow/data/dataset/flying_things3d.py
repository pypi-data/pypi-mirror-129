import os.path as osp
from glob import glob

import numpy as np

from .base_dataset import BaseDataset


class FlyingThings3D(BaseDataset):
    """
    Dataset Class for preparing the Flying Things 3D Synthetic dataset for training and validation.

    Parameters
    ----------
    root_dir : str
        path of the root directory for the flying things 3D dataset
    split : str, default : "training"
        specify the training or validation split
    dstype : str, default : "frames_cleanpass"
        specify dataset type
    is_prediction : bool, default : False
        If True, only image data are loaded for prediction otherwise both images and flow data are loaded
    init_seed : bool, default : False
        If True, sets random seed to worker
    augment : bool, default : True
        If True, applies data augmentation
    aug_param : :obj:`dict`, optional
        The parameters for data augmentation
    """

    def __init__(
        self,
        root_dir,
        split="training",
        dstype="frames_cleanpass",
        is_prediction=False,
        init_seed=False,
        augment=True,
        aug_params={
            "crop_size": (224, 224),
            "color_aug_params": {"aug_prob": 0.2},
            "eraser_aug_params": {"aug_prob": 0.5},
            "spatial_aug_params": {"aug_prob": 0.8},
        },
    ):
        super(FlyingThings3D, self).__init__(
            augment,
            aug_params,
            is_prediction,
            init_seed,
        )
        assert (
            split.lower() == "training" or split.lower() == "validation"
        ), "Incorrect split values. Accepted split values: training, validation"

        self.is_prediction = is_prediction

        if split.lower() == "training":
            split = "TRAIN"

        if split.lower() == "validation":
            split = "TEST"

        for cam in ["left"]:
            for direction in ["into_future", "into_past"]:
                image_dirs = sorted(glob(osp.join(root_dir, dstype, split + "/*/*")))
                image_dirs = sorted([osp.join(f, cam) for f in image_dirs])

                flow_dirs = sorted(
                    glob(osp.join(root_dir, "optical_flow/", split + "/*/*"))
                )
                flow_dirs = sorted([osp.join(f, direction, cam) for f in flow_dirs])

                for idir, fdir in zip(image_dirs, flow_dirs):
                    images = sorted(glob(osp.join(idir, "*.png")))
                    flows = sorted(glob(osp.join(fdir, "*.pfm")))
                    for i in range(len(flows) - 1):
                        if direction == "into_future":
                            self.image_list += [[images[i], images[i + 1]]]
                            self.flow_list += [flows[i]]
                        elif direction == "into_past":
                            self.image_list += [[images[i + 1], images[i]]]
                            self.flow_list += [flows[i + 1]]
