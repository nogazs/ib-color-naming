# IB Color Naming Model

Python wrapper for the color naming model proposed in the paper:

Noga Zaslavsky, Charles Kemp, Terry Regier, and Naftali Tishby (2018).
Efficient compression in color naming and its evolution. *PNAS*, 115(31):7937– 7942.
https://doi.org/10.1073/pnas.1800521115 


### Usage

Run `python main.py` to see a simple demo.
This demo shows how to load the model, plot the theoretical bound,
evaluate new naming data (with respect to the WCS color naming grid),
and plot mode maps.

### Model

The model is composed of the following components:

- `pM`	— capacity-achieving prior over color chips
- `pU_M` — speaker's mental representations, m(u)
- `betas` —	the values of beta used for the reverse deterministic annealing schedule
- `IB_curve` —	the IB curve defined by (I_beta(M;W), I_beta(W;U))
- `qW_M`	—	the optimal IB encoders (color naming systems) for each value of beta

See the paper for more details on each component.

The class `IBNamingModel` allows easy access to the model,
and implements useful functions for evaluating data. 
