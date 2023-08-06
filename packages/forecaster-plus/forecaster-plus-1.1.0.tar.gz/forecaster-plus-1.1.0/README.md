# forecaster-plus (forecaster 1.1ish)
-----

An internally overhauled but fundamentally similar version of Forecaster by Jingjing Chen and David Kipping, originally presented in arXiv:1603.08614 and hosted at https://github.com/chenjj2/forecaster.

The model itself has not changed- no new data was included and the hyperparameter file was not regenerated. All functions were rewritten to take advantage of Numpy vectorization and some additional user features were added.

## Install
-----
To install this package with [`pip`](https://pip.pypa.io/en/stable/), run

```bash
pip install forecaster-plus
```

## Changes
-----
Changes include but are not limited to:
* Rewriting all functions to take advantage of Numpy vectorization
* Including the ability to input asymmetric uncertainties in mass or radius
* Enabling pip installation


## Citation
-----
If used, please cite [the original Forecaster paper](https://ui.adsabs.harvard.edu/abs/2017ApJ...834...17C/abstract) and the bibcode for this implementation eventually hosted on the Astrophysics Source Code Library (ASCL).

