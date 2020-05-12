import numpy as np
import matplotlib.pyplot as plt
import ib_naming_model
from tools import *
from figrues import mode_map

LOGGER = get_logger('main')


def main():
    # load model
    model = ib_naming_model.load_model()
    curve = model.IB_curve

    # theoretical bound
    plt.figure()
    plt.plot(curve[0], curve[1])
    plt.xlabel('complexity, $I(M;W)$')
    plt.ylabel('accuracy, $I(W;U)$')
    plt.xlim([0, H(model.pM)])
    plt.ylim([0, model.I_MU + 0.1])

    # generate fake data and fit an optimal IB system
    pW_M_fake = np.random.rand(330, 10)
    pW_M_fake /= pW_M_fake.sum(axis=1)[:, None]
    print(model.complexity(pW_M_fake), model.accuracy(pW_M_fake))
    epsilon, gnid, bl, qW_M_fit = model.fit(pW_M_fake)

    # let's plot a mode map!
    plt.figure(figsize=(6.4, 2.5))
    qW_M = model.qW_M[500]
    mode_map(qW_M, model)
    plt.tight_layout()


if __name__ == '__main__':
    main()
