# IB Color Naming Model

Python package for accessing the color naming model from:

Noga Zaslavsky, Charles Kemp, Terry Regier, and Naftali Tishby (2018).
Efficient compression in color naming and its evolution. *PNAS*, 115(31):7937– 7942.
https://doi.org/10.1073/pnas.1800521115 

[![Efficient compression in color naming and its evolution](https://www.nogsky.com/publication/2018a-pnas/featured.png)](https://www.youtube.com/watch?v=4nJ35y9iYiM&feature=emb_logo)

## Usage

Run `python main.py` to see a simple demo.
This demo shows how to load the model, plot the theoretical bound,
evaluate new naming data (with respect to the WCS color naming grid),
and plot mode maps.

## Model

The model is composed of the following components:

- `pM`	— capacity-achieving prior over color chips
- `pU_M` — speaker's mental representations, m(u)
- `betas` —	the values of &beta; used for the reverse deterministic annealing schedule
- `IB_curve` —	the IB theoretical bound defined by I<sub>&beta;</sub>(M;W) and I<sub>&beta;</sub>(W;U)
- `qW_M`	—	the optimal IB encoders (color naming systems) for each value of &beta;

See the paper for more details on each component.

The class `IBNamingModel` allows easy access to the model,
and implements useful functions for evaluating data. 

## Integrating in another project

If you'd like to use this model in your project, you can define this packge as a submodule by running the following command:

```shell
git submodule add https://github.com/nogazs/ib-color-naming.git ib_color_naming
```

In your python scrip, you can then import the model's module like this: 

```python
from ib_color_naming.src import ib_naming_model
```
If you do so, please don't forget to acknowledge this work (see citation details below).

## Requirements

- A standard scientific installation of python (see `requirements.txt`).  
- The package `zipfile` is used only when downloading the model for the first time. This can also be done manually by
downloading the model's file from  [here](https://www.dropbox.com/s/70w953orv27kz1o/IB_color_naming_model.zip?dl=1)
and unzipping it under a `./models` directory.

## Citation

If you find this useful, please consider acknowledging this repo and citing the following paper: 
```bibtex
@article{Zaslavsky2018efficient,
    author = {Zaslavsky, Noga and Kemp, Charles and Regier, Terry and Tishby, Naftali},
    title = {Efficient compression in color naming and its evolution},
    journal = {Proceedings of the National Academy of Sciences}
    volume = {115},
    number = {31},
    pages = {7937--7942},
    year = {2018},
    doi = {10.1073/pnas.1800521115},
    publisher = {National Academy of Sciences},
    issn = {0027-8424}
}
```
Link to repo: https://github.com/nogazs/ib-color-naming
