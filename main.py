import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ib_naming_model


def main():
    model = ib_naming_model.load_model('ib_color_naming.pkl')
    curve = model.IB_curve
    plt.plot(curve[0], curve[1])


if __name__ == '__main__':
    main()
