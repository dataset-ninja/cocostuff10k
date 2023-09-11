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

    class_to_supercategory = {
        "banner": "textile",
        "blanket": "textile",
        "branch": "plant",
        "bridge": "building",
        "building-other": "building",
        "bush": "plant",
        "cabinet": "furniture-stuff",
        "cage": "structural",
        "cardboard": "raw-material",
        "carpet": "floor",
        "ceiling-other": "ceiling",
        "ceiling-tile": "ceiling",
        "cloth": "textile",
        "clothes": "textile",
        "clouds": "sky",
        "counter": "furniture-stuff",
        "cupboard": "furniture-stuff",
        "curtain": "textile",
        "desk-stuff": "furniture-stuff",
        "dirt": "ground",
        "door-stuff": "furniture-stuff",
        "fence": "structural",
        "floor-marble": "floor",
        "floor-other": "floor",
        "floor-stone": "floor",
        "floor-tile": "floor",
        "floor-wood": "floor",
        "flower": "plant",
        "fog": "water",
        "food-other": "food-stuff",
        "fruit": "food-stuff",
        "furniture-other": "furniture-stuff",
        "grass": "plant",
        "gravel": "ground",
        "ground-other": "ground",
        "hill": "solid",
        "house": "building",
        "leaves": "plant",
        "light": "furniture-stuff",
        "mat": "textile",
        "metal": "raw-material",
        "mirror-stuff": "furniture-stuff",
        "moss": "plant",
        "mountain": "solid",
        "mud": "ground",
        "napkin": "textile",
        "net": "structural",
        "paper": "raw-material",
        "pavement": "ground",
        "pillow": "textile",
        "plant-other": "plant",
        "plastic": "raw-material",
        "platform": "ground",
        "playingfield": "ground",
        "railing": "structural",
        "railroad": "ground",
        "river": "water",
        "road": "ground",
        "rock": "solid",
        "roof": "building",
        "rug": "textile",
        "salad": "food-stuff",
        "sand": "ground",
        "sea": "water",
        "shelf": "furniture-stuff",
        "sky-other": "sky",
        "skyscraper": "building",
        "snow": "ground",
        "solid-other": "solid",
        "stairs": "furniture-stuff",
        "stone": "solid",
        "straw": "plant",
        "structural-other": "structural",
        "table": "furniture-stuff",
        "tent": "building",
        "textile-other": "textile",
        "towel": "textile",
        "tree": "plant",
        "vegetable": "food-stuff",
        "wall-brick": "wall",
        "wall-concrete": "wall",
        "wall-other": "wall",
        "wall-panel": "wall",
        "wall-stone": "wall",
        "wall-tile": "wall",
        "wall-wood": "wall",
        "water-other": "water",
        "waterdrops": "water",
        "window-blind": "window",
        "window-other": "window",
        "wood": "solid",
        "skateboard": "sports",
        "tennis racket": "sports",
        "surfboard": "sports",
        "baseball bat": "sports",
        "baseball glove": "sports",
        "kite": "sports",
        "sports ball": "sports",
        "snowboard": "sports",
        "skis": "sports",
        "frisbee": "sports",
        "cup": "kitchen",
        "tv": "electronic",
        "knife": "kitchen",
        "bottle": "kitchen",
        "bird": "animal",
        "dining table": "furniture",
        "zebra": "animal",
        "couch": "furniture",
        "stop sign": "outdoor",
        "bicycle": "vehicle",
        "suitcase": "accessory",
        "teddy bear": "indoor",
        "bus": "vehicle",
        "pizza": "food",
        "boat": "vehicle",
        "scissors": "indoor",
        "toaster": "appliance",
        "cake": "food",
        "carrot": "food",
        "motorcycle": "vehicle",
        "cat": "animal",
        "sheep": "animal",
        "sandwich": "food",
        "fire hydrant": "outdoor",
        "traffic light": "outdoor",
        "potted plant": "furniture",
        "handbag": "accessory",
        "tie": "accessory",
        "toilet": "furniture",
        "car": "vehicle",
        "microwave": "appliance",
        "hot dog": "food",
        "hair drier": "indoor",
        "train": "vehicle",
        "sink": "appliance",
        "cow": "animal",
        "keyboard": "electronic",
        "airplane": "vehicle",
        "bench": "outdoor",
        "backpack": "accessory",
        "wine glass": "kitchen",
        "vase": "indoor",
        "chair": "furniture",
        "spoon": "kitchen",
        "remote": "electronic",
        "donut": "food",
        "bed": "furniture",
        "banana": "food",
        "cell phone": "electronic",
        "truck": "vehicle",
        "broccoli": "food",
        "giraffe": "animal",
        "bowl": "kitchen",
        "bear": "animal",
        "clock": "indoor",
        "fork": "kitchen",
        "horse": "animal",
        "laptop": "electronic",
        "book": "indoor",
        "apple": "food",
        "elephant": "animal",
        "refrigerator": "appliance",
        "toothbrush": "indoor",
        "orange": "food",
        "mouse": "animal",
        "umbrella": "accessory",
        "dog": "animal",
        "parking meter": "outdoor",
        "oven": "appliance",
    }

    supercategory_to_outdoor_things = {
        "sports": ("outdoor", "things"),
        "accessory": ("outdoor", "things"),
        "animal": ("outdoor", "things"),
        "outdoor": ("outdoor", "things"),
        "vehicle": ("outdoor", "things"),
        "person": ("outdoor", "things"),
    }

    supercategory_to_indoor_things = {
        "indoor": ("indoor", "things"),
        "appliance": ("indoor", "things"),
        "electronic": ("indoor", "things"),
        "furniture": ("indoor", "things"),
        "food": ("indoor", "things"),
        "kitchen": ("indoor", "things"),
    }

    supercategory_to_outdoor_stuff = {
        "water": ("outdoor", "stuff"),
        "ground": ("outdoor", "stuff"),
        "solid": ("outdoor", "stuff"),
        "sky": ("outdoor", "stuff"),
        "plant": ("outdoor", "stuff"),
        "structural": ("outdoor", "stuff"),
        "building": ("outdoor", "stuff"),
    }

    supercategory_to_indoor_stuff = {
        "food": ("indoor", "stuff"),
        "textile": ("indoor", "stuff"),
        "furniture": ("indoor", "stuff"),
        "window": ("indoor", "stuff"),
        "floor": ("indoor", "stuff"),
        "ceiling": ("indoor", "stuff"),
        "wall": ("indoor", "stuff"),
        "rawmaterial": ("indoor", "stuff"),
    }

    supercategores = [
        supercategory_to_outdoor_things,
        supercategory_to_indoor_things,
        supercategory_to_outdoor_stuff,
        supercategory_to_indoor_stuff,
    ]

    def get_subcategories_values(curr_class_name):
        subcategories_values = []
        if curr_class_name == "person":
            subcategories_values = ("outdoor", "things")
        elif curr_class_name == "other":
            subcategories_values = "other"

        else:
            subcategory = class_to_supercategory.get(curr_class_name)
            subcategories_values.append(subcategory)
            if subcategory in ["food", "furniture"]:
                if curr_class_name in [
                    "food-other",  # door and desk are the same in both parent subcategories, but they are not in this dataset :)
                    "vegetable",
                    "salad",
                    "fruit",
                    "furniture-other",
                    "stairs",
                    "light",
                    "counter",
                    "mirror",
                    "cupboard",
                    "cabinet",
                    "shelf",
                    "table",
                ]:
                    parent_subcategory = ("indoor", "stuff")
            else:
                for supercategores_data in supercategores:
                    parent_subcategory = supercategores_data.get(subcategory)
                    if parent_subcategory is not None:
                        subcategories_values.extend(parent_subcategory)

        if type(subcategories_values) is not str:
            subcategories_values = ", ".join(subcategories_values)

        return subcategories_values

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
                label_tags = []
                obj_class = pixel_to_class[curr_pixel]
                curr_class_name = obj_class.name
                if curr_class_name != "unlabeled":
                    subcategories_values = get_subcategories_values(curr_class_name)
                    tag_category = sly.Tag(tag_category_meta, value=subcategories_values)
                    label_tags.append(tag_category)
                obj_mask = mask == curr_pixel
                ret, curr_mask = connectedComponents(obj_mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if curr_bitmap.area > 50:
                        curr_label = sly.Label(curr_bitmap, obj_class, tags=label_tags)
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

    tag_meta = sly.TagMeta("caption", sly.TagValueType.ANY_STRING)
    tag_category_meta = sly.TagMeta("category", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=list(pixel_to_class.values()), tag_metas=[tag_meta, tag_category_meta]
    )
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
