Dataset **COCO-Stuff 10k** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://www.dropbox.com/scl/fi/z9r0dcxhd5nz2q4pll11a/coco-stuff-10k-DatasetNinja.tar?rlkey=xluc51ldpxah15l8jfdynpgwr&dl=1)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='COCO-Stuff 10k', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [Images and annotations (.mat format) [2.0 GB]](http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/cocostuff-10k-v1.1.zip)
- [Annotations in .json format [62.3 GB]](http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/cocostuff-10k-v1.1.json)
- [Labels [2.3 KB]](https://raw.githubusercontent.com/nightrome/cocostuff10k/master/dataset/cocostuff-labels.txt)
- [Readme [6.5 KB]](https://raw.githubusercontent.com/nightrome/cocostuff10k/master/README.md)
