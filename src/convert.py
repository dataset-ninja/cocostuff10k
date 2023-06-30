import os

import numpy as np
import supervisely as sly
from scipy.io import loadmat
from supervisely.io.fs import get_file_name
from tqdm import tqdm

BATCH_SIZE = 500


def create_meta(path_to_labels):
    labels_map = {}
    with open(path_to_labels, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(": ")
                labels_map[int(key)] = value

    obj_classes = []
    for label_name in labels_map.values():
        obj_classes.append(sly.ObjClass(label_name, sly.Bitmap))

    train_tag_meta = sly.TagMeta("train", sly.TagValueType.NONE)
    test_tag_meta = sly.TagMeta("test", sly.TagValueType.NONE)
    meta = sly.ProjectMeta(obj_classes=obj_classes, tag_metas=[train_tag_meta, test_tag_meta])
    return meta, labels_map


def create_label(meta, labels_map, image_data):
    labels = []
    unique_labels = np.unique(image_data)
    for label_id in unique_labels:
        lbl_mask = image_data == label_id
        label = sly.Label(sly.Bitmap(lbl_mask), obj_class=meta.get_obj_class(labels_map[label_id]))
        labels.append(label)
    return labels


def create_traintest_sets(train_path, test_path):
    traintest_map = {}

    with open(train_path, "r") as file:
        train_names = [line.strip() for line in file.readlines()]
        traintest_map["train"] = train_names
    with open(test_path, "r") as file:
        test_names = [line.strip() for line in file.readlines()]
        traintest_map["test"] = test_names
    return traintest_map


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "../datasets-bot/datasets/cocostuff10k"
    labels_file_path = os.path.join(dataset_path, "cocostuff-labels.txt")
    train_file_path = os.path.join(dataset_path, "imageLists", "train.txt")
    test_file_path = os.path.join(dataset_path, "imageLists", "test.txt")

    meta, labels_map = create_meta(labels_file_path)
    traintest_map = create_traintest_sets(train_file_path, test_file_path)

    img_dir = os.path.join(dataset_path, "images")
    ann_dir = os.path.join(dataset_path, "annotations")

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    api.project.update_meta(project.id, meta.to_json())
    for ds_name in traintest_map:
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
        names = traintest_map[ds_name]
        ann_paths = [os.path.join(ann_dir, f"{name}.mat") for name in names]
        img_paths = [os.path.join(img_dir, f"{name}.jpg") for name in names]

        tag = sly.Tag(meta.get_tag_meta(f"{ds_name}"))
        with tqdm(total=len(img_paths), desc=f"Processing images in {dataset.name}") as pbar:
            for img_paths_batch, ann_paths_batch in zip(
                sly.batched(img_paths, batch_size=BATCH_SIZE),
                sly.batched(ann_paths, batch_size=BATCH_SIZE),
            ):
                images_names = [get_file_name(img_path) for img_path in img_paths_batch]
                anns = []
                for ann_path in ann_paths_batch:
                    data = loadmat(ann_path)

                    image_size = data["S"].shape
                    data_captions = data["captions"]
                    captions = ""
                    for caption in data_captions:
                        captions += caption[0][0] + "\n"

                    image_datas = [
                        data["S"],
                        # data["regionLabelsStuff"],
                        # data["regionMapStuff"]
                    ]
                    labels = []
                    for image_data in image_datas:
                        data_labels = create_label(meta, labels_map, image_data)
                        labels.extend(data_labels)

                    ann = sly.Annotation(
                        img_size=image_size,
                        labels=labels,
                        img_tags=[tag],
                        # img_description=captions,
                    )
                    anns.append(ann)

                img_infos = api.image.upload_paths(dataset.id, images_names, img_paths_batch)
                img_ids = [im_info.id for im_info in img_infos]
                api.annotation.upload_anns(img_ids, anns)
                pbar.update(len(img_paths_batch))

    return project
