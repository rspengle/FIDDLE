# FIDDLE

An integrative deep learning framework for functional genomic data inference.

Based on: [http://biorxiv.org/content/early/2016/10/17/081380.full.pdf]

Thanks to [Dylan Marshall](https://github.com/DylanM-Marshall) for documentation & organization.

<img src="https://preview.ibb.co/iDo3v5/FIDDLE_001.jpg" title="Architecture" />
<img src="https://preview.ibb.co/eSebF5/FIDDLE_002.jpg" title="case study" />

![alt text](https://cloud.githubusercontent.com/assets/1741502/24565878/28229be6-1625-11e7-88e5-555508e3e25c.gif)

<img src="https://preview.ibb.co/mwc2oQ/FIDDLE_003.jpg" title="interpretation" />

## Installation and Quick Start

Docker image to be made eventually, for now:

### 1) Set up FIDDLE environment

_NOTE: Requires python 2.7 and pip. Anaconda can be a nuisance, make sure to comment it out in your ~/.bash_profile:_

```markdown 
sudo easy_install pip 
sudo pip install virtualenv
```

```markdown 
git clone https://github.com/ueser/FIDDLE.git 
sudo virtualenv venvFIDDLE
source venvFIDDLE/bin/activate
pip install -r requirements.txt
cd FIDDLE/
mkdir -p data/hdf5datasets/
```

_NOTE: Keras comes with default Theano backend. Change keras backend configuration to Tensorflow:_  

```markdown
vim ~/.keras/keras.json
```

Then change "backend":"theano" --> "backend":"tensorflow"

### 2) Download training/validation/test datasets:

Place the following datasets in /FIDDLE/data/hdf5datasets/

_WARNING: several gb of data_

[training.h5](https://drive.google.com/file/d/0B9aDFb1Ds4IzWWZ5aWhtTkVUWE0/view?usp=sharing)

[validation.h5](https://drive.google.com/file/d/0B9aDFb1Ds4IzZ3JrLXp3SEY5aGs/view?usp=sharing)

[test.h5](https://drive.google.com/file/d/0B9aDFb1Ds4IzT05wTTZVQmFvcG8/view?usp=sharing)

### 3) Run it:

Change directories to /FIDDLE/fiddle/

```markdown
python main.py
```

_note: solution to matplotlib RuntimeError: http://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python_

### 4) Create visualization of training:

```markdown
python visualization.py --vizType tssseq
```

### 5) Check out training trajectory:

Change directories to FIDDLE/results/experiment/, open up the gif in a browser.

### Documentation...

On its way
