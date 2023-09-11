from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "COCO-Stuff 10k"
PROJECT_NAME_FULL: str = "COCO-Stuff 10K Dataset: Common Objects in Context Stuff 10k v1.1"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(url="https://github.com/nightrome/cocostuff10k#licensing")
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Domain.General(is_used=False)]
CATEGORY: Category = Category.General(benchmark=True)

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.SemanticSegmentation(),
    CVTask.ObjectDetection(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = "2017-04-06"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://github.com/nightrome/cocostuff10k"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 3550978
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/cocostuff10k"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "Images and annotations (.mat format) [2.0 GB]": "http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/cocostuff-10k-v1.1.zip",
    "Annotations in .json format [62.3 GB]": "http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/cocostuff-10k-v1.1.json",
    "Labels [2.3 KB]": "https://raw.githubusercontent.com/nightrome/cocostuff10k/master/dataset/cocostuff-labels.txt",
    "Readme [6.5 KB]": "https://raw.githubusercontent.com/nightrome/cocostuff10k/master/README.md",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = ["https://arxiv.org/abs/1612.03716", "https://arxiv.org/abs/1405.0312"]
CITATION_URL: Optional[str] = "https://arxiv.org/abs/1612.03716"
AUTHORS: Optional[List[str]] = ["Holger Caesar", "Jasper Uijlings", "Vittorio Ferrari"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "University of Edinburgh, United Kingdom",
    "Google AI Perception",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://www.ed.ac.uk/",
    "https://research.google/teams/perception/",
]

SLYTAGSPLIT: Optional[Dict[str, List[str]]] = {
    "__PRETEXT__": "Additionally, images have ***caption*** tags, while objects contain ***category*** tags with information about labels hierarchy. Explore them in supervisely"
}
TAGS: List[str] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "license": LICENSE,
        "hide_dataset": HIDE_DATASET,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["project_name_full"] = PROJECT_NAME_FULL or PROJECT_NAME
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    return settings
