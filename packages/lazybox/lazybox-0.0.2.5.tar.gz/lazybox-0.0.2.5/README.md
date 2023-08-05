# LazyBox
> A user friendly API to jump-start your Deep Learning project based on Fastai. 


The library is still in early development, but a lot of new features will be added in future

    [ ] Support for non-image Datasets
    [ ] Import NN architecture from the timm library
    [ ] Make it better

## Install

`pip install lazybox`

## How to use

Let's go through a typical workflow for a DeepLearning task. Let's download this Dataset on Kaggle: https://www.kaggle.com/tongpython/cat-and-dog which are images of cat and dogs.

```
# we lazy folks only use wild imports
from lazybox.all import *

path = Path('test_dataset')

path.find('archive')
```




    'test_dataset/archive.zip'



Let's decompress this archive
