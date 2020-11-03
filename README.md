# HMM for Protein Prediction

## General

This project was designed to participate in [CAFA4](https://www.biofunctionprediction.org/cafa/4/)

The goal of this program is to take in a protein amino acid sequence and construct a model that would predict the most likely functions of the protein.

Results are still being processed and when results arrive, this repository will be updated to reflect results

## Requirements ([Anaconda](https://www.anaconda.com/products/individual))
1) conda create --n HMMeta python=3.7
1) conda activate HMMeta
1) pip install -r requirements.txt

## How-To

The only thing a user should have to interact with would be `HMMeta.py`.

Hidden Markov Models are notoriously computate-intensive and this program is not designed to be run straight through, it would take months. It is designed to be run in chunks, making the data, training the models, and the making predictions

This program is also not designed to be run without large amounts of resources. To get results on any significant scale, it would need to be run on a machine with at least 32 cores.

### Making files

Due to the uneven relationship between GO functions and the number of sequences that correspond to them, we used data augmentation to generate additional data for the functions that had a low number of references.

We are working on a solution for hosting the training data and the augmented files, the link will appear below here if we find a solution.

To run this part of the program run
```bash
python3 HMMeta.py --make /path/to/input/data/ /path/to/unformatted/training/data/ /path/to/testing/data
```

### Training Models
Training models is the most computationally complex portion of this process.

Once again, we are working on getting a solution for our already made models and the link will appear below if we can get a solution prepared.

We will be adding options to further customize training parameters, but for now they will be a 5 state Hidden Markov Model.

```bash
python3 HMMeta.py --train /path/to/training/folder/ /path/for/models/to/be/saved
```

### Making Predictions
Predictions will take files in FASTA format and make GO function predictions.

```bash
python3 HMMeta.py --predict /path/to/test/sequences/ /path/to/models/ /path/to/save/output/files/
```

### Optimizations
Before: 125.68732424900008
4 Jobs process queue: 94.48131372599892 (32% faster?)
