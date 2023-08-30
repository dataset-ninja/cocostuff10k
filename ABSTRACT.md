* 10,000 complex images from COCO [2]
* Dense pixel-level annotations
* 91 thing and 91 stuff classes
* Instance-level annotations for things from COCO [2]
* Complex spatial context between stuff and things
* 5 captions per image from COCO [2]

To be compatible with COCO, version 1.1 of COCO-Stuff has 91 thing classes (1-91), 91 stuff classes (92-182) and 1 class "unlabeled" (0). Note that 11 of the thing classes from COCO 2015 do not have any segmentation annotations. The classes desk, door and mirror could be either stuff or things and therefore occur in both COCO and COCO-Stuff. To avoid confusion we add the suffix "-stuff" to those classes in COCO-Stuff.

The Common Objects in COntext (COCO) [35] dataset
is a large-scale dataset of images of high complexity.
COCO has been designed to enable the study of thing-thing
interactions, and features images of complex scenes with
many small objects, annotated with very detailed outlines.
However, COCO is missing stuff annotations. In this paper
we augment COCO by adding dense pixel-wise stuff annotations. Since COCO is about complex, yet natural scenes
containing substantial areas of stuff, COCO-Stuff enables
the exploration of rich relations between things and stuff.
Therefore COCO-Stuff offers a valuable stepping stone towards complete scene understanding.
