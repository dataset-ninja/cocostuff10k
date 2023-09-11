The authors of the **COCO-Stuff 10k v1.1** dataset addressed the distinction between semantic classes, categorizing them as either ***thing*** (an object with well-defined shapes such as cars and people) or ***stuff*** (amorphous background regions like grass and sky). They noted that while a significant amount of research has focused on "thing" classes, relatively less attention has been devoted to "stuff" classes. They emphasized the importance of "stuff" classes in image understanding, as they play a crucial role in defining scene types, contextual reasoning, and describing physical attributes and geometric properties of scenes.

To promote the understanding of "stuff" and "things" within context, the authors introduced COCO-Stuff, an extension of the COCO 2015 dataset. COCO-Stuff augmented 10K images from COCO 2014. To be compatible with COCO, version 1.1 of COCO-Stuff has 91 thing classes (1-91), 91 stuff classes (92-182) and 1 class "unlabeled" (0). Note that 11 of the thing classes from COCO 2015 do not have any segmentation annotations. The *classes desk*, *door* and *mirror* could be either stuff or things and therefore occur in both COCO and COCO-Stuff. To avoid confusion we add the suffix "-stuff" to those classes in COCO-Stuff.

Furthermore, the authors used COCO-Stuff to analyze various aspects, including the importance of "stuff" and "thing" classes in terms of surface coverage and frequency in image captions, the spatial relationships between "stuff" and "things," and the performance of modern semantic segmentation methods on these classes.

They underscored the significance of "stuff" classes, emphasizing that they constitute the majority of visual surroundings and provide critical context for recognizing and understanding "things." "Stuff" classes influence the type of scene and constrain the possible locations of "things." Additionally, they help determine depth ordering and relative positions of "things" and support the interpretation of relationships between them. The context provided by "stuff" is instrumental in recognizing smaller or less common "things" in images.

The hierarchy of labels:

<img src="https://github.com/supervisely/supervisely/assets/78355358/d3c78712-cd5b-496b-91ff-7fb0beafceb7" alt="image" width="600">

COCO-Stuff was introduced as a valuable addition to COCO, enabling the exploration of rich relationships between "stuff" and "things" in complex scenes. It was noted that COCO-Stuff offered a significant contribution to complete scene understanding.
