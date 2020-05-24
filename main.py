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

    # let's plot a mode map!
    indx = 500
    qW_M = model.qW_M[indx]
    plt.figure(figsize=(6.4, 2.5))
    model.mode_map(qW_M)
    plt.title('Optimal IB system for $\\beta = %.3f$' % model.betas[indx])
    plt.tight_layout()
    print(model.complexity(qW_M), model.accuracy(qW_M))


if __name__ == '__main__':
    main()
