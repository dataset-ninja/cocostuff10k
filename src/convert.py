# https://github.com/nightrome/cocostuff10k#dataset

import os

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "APP_DATA/dataset"
    batch_size = 10
    images_ext = ".jpg"
    masks_ext = ".mat"
    images_folder_name = "images"
    anns_folder_name = "annotations"
    split_train_file = "imageLists/train.txt"
    split_test_file = "imageLists/test.txt"
    classes_file_path = "APP_DATA/cocostuff-labels.txt"

    ds_name_to_split = {"train": split_train_file, "test": split_test_file}

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        mask_name = get_file_name(image_path) + masks_ext
        mask_path = os.path.join(masks_path, mask_name)

        if file_exists(mask_path):
            import scipy.io

            mat = scipy.io.loadmat(mask_path)
            mask = mat["S"]
            tags_data = mat["captions"]
            for data in tags_data:
                tag_value = data[0][0]
                tag = sly.Tag(tag_meta, value=tag_value)
                tags.append(tag)

            unique_pixels = np.unique(mask)
            for curr_pixel in unique_pixels:
                obj_class = pixel_to_class[curr_pixel]
                obj_mask = mask == curr_pixel
                ret, curr_mask = connectedComponents(obj_mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if curr_bitmap.area > 50:
                        curr_label = sly.Label(curr_bitmap, obj_class)
                        labels.append(curr_label)

            return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    pixel_to_class = {}
    with open(classes_file_path) as f:
        content = f.read().split("\n")
        for curr_data in content:
            if len(curr_data) > 0:
                curr_data = curr_data.split(": ")
                obj_class = sly.ObjClass(curr_data[1], sly.Bitmap)
                pixel_to_class[int(curr_data[0])] = obj_class

    tag_meta = sly.TagMeta("info", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(pixel_to_class.values()), tag_metas=[tag_meta])
    api.project.update_meta(project.id, meta.to_json())

    images_path = os.path.join(dataset_path, images_folder_name)
    masks_path = os.path.join(dataset_path, anns_folder_name)

    for ds_name, split_file in ds_name_to_split.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
        split_path = os.path.join(dataset_path, split_file)
        with open(split_path) as f:
            contant = f.read().split("\n")

        images_names = [im_name + images_ext for im_name in contant if len(im_name) > 0]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [os.path.join(images_path, im_name) for im_name in img_names_batch]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))
    return project
