**COCO-Stuff 10K Dataset: Common Objects in Context Stuff 10k v1.1** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is applicable or relevant across various domains. 

The dataset consists of 10000 images with 228313 labeled objects belonging to 183 different classes including *unlabeled*, *person*, *tree*, and other: *wall-other*, *sky-other*, *grass*, *building-other*, *clouds*, *road*, *pavement*, *chair*, *car*, *structural-other*, *dining table*, *fence*, *window-other*, *ground-other*, *cup*, *plant-other*, *bottle*, *bush*, *ceiling-other*, *furniture-other*, *light*, *bowl*, *table*, *dirt*, *door-stuff*, and 155 more.

Images in the COCO-Stuff 10k dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are 2 splits in the dataset: *train* (9000 images) and *test* (1000 images). Additionally, images have ***caption*** tags, while objects contain ***category*** tags with information about labels hierarchy. Explore them in supervisely. The dataset was released in 2017 by the University of Edinburgh, United Kingdom and Google AI Perception.

Here is a visualized example for randomly selected sample classes:

[Dataset classes](https://github.com/dataset-ninja/cocostuff10k/raw/main/visualizations/classes_preview.webm)
