import pickle
from tools import *


def load_model(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


class IBNamingModel(object):

    def __init__(self, pM, pU_M, betas, IB_curve, qW_M):
        self.pM = pM if len(pM.shape) == 2 else pM[:, None]
        self.pU_M = pU_M
        self.I_MU = MI(pU_M * self.pM)
        self.betas = betas
        self.IB_curve = IB_curve
        self.qW_M = qW_M
        self.qW_M_orig = None
        self.F = IB_curve[0] - betas * IB_curve[1]

    def complexity(self, pW_M):
        return MI(pW_M * self.pM)

    def accuracy(self, pW_M):
        pMW = pW_M * self.pM
        pWU = pMW.T @ self.pU_M
        return MI(pWU)

    def d_IB(self, pW_M):
        return self.I_MU - self.accuracy(pW_M)

    def fit(self, pW_M):
        Fl = self.complexity(pW_M) - self.betas * self.accuracy(pW_M)
        dFl = Fl - self.F
        bl_ind = dFl.argmin()
        bl = self.betas[bl_ind]
        epsilon = dFl.min() / bl
        qW_M_fit = self.qW_M[bl_ind]
        gnid = gNID(pW_M, qW_M_fit, self.pM)
        return epsilon, gnid, bl, qW_M_fit

