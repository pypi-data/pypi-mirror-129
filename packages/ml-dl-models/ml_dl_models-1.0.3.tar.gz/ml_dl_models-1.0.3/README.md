# ML-DL-Models
---
ML-DL-Models is library to integrate various pre-trained Machine Learning and Deep Learning to your project through ml-dl-models api [link](https://ml-dl-models.herokuapp.com/).


## Usage
---
In the following paragraphs, I am going to describe how you can get and use ml-dl-models for your projects.


### Getting it
To download ml-dl-models, either fork this github repo or simply use Pypi via pip.

```sh
$ python -m pip install --upgrade pip
$ pip install ml-dl-models
```

### Using it
ML-DL-Models was programmed with ease-of-use in mind. First, import models from it.

```python
from ml_dl_models import MelodyGenerator
```

Now you are ready to create an Melody from a MelodyGenerator model.

```python
data = {'keys':'c d e', 'default':True}
path = '/home/LaxmanMaharjan/melody.mp3' # default value is 'melody.mp3' in same directory.
mg = MelodyGenerator(data = data, path = path)
mg.generate_melody()
```
You can also get the cached notes(notes that are already fetched to model) from Melody Generator.

```python
mg = MelodyGenerator()
print(mg.get_cached_notes)
```
You can instantiate MelodyGenerator class with default value of data and path.
```python
mg = MelodyGenerator()
mg.generate_melody()
```
__Note:__
If you use default value of data and path to instantiate MelodyGenerator class than data is chosen from one of the values from cached data.

__Learn more about Data Representation [link](https://ml-dl-models.herokuapp.com/documentation)__
