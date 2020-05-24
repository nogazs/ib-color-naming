import pickle
from zipfile import ZipFile
from tools import *
import figrues as figs

LOGGER = get_logger('ib_naming_model')
DEFAULT_MODEL_URL = 'https://www.dropbox.com/s/70w953orv27kz1o/IB_color_naming_model.zip?dl=1'


def load_model(filename=None):
    ensure_dir('./models')
    if filename is None:
        filename = './models/IB_color_naming_model/model.pkl'
        if not os.path.isfile(filename):
            LOGGER.info('downloading default model from %s  ...' % DEFAULT_MODEL_URL)
            urlretrieve(DEFAULT_MODEL_URL, './models/temp.zip')
            LOGGER.info('extracting model files ...')
            with ZipFile('./models/temp.zip', 'r') as zf:
                zf.extractall('./models')
                os.remove('./models/temp.zip')
                os.rename('./models/IB_color_naming_model/IB_color_naming.pkl', filename)
    with open(filename, 'rb') as f:
        LOGGER.info('loading model from file: %s' % filename)
        model_data = pickle.load(f)
        return IBNamingModel(**model_data)


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

    def m_hat(self, qW_M):
        """
        :param qW_M: encoder (naming system)
        :return: optimal decoder (Bayesian listener) that corresponds to the encoder
        """
        pMW = qW_M * self.pM
        pM_W = pMW.T / pMW.sum(axis=0)[:, None]
        return pM_W.dot(self.pU_M)

    def complexity(self, pW_M):
        """
        :param pW_M: encoder (naming system)
        :return: I(M;W)
        """
        return MI(pW_M * self.pM)

    def accuracy(self, pW_M):
        """
        :param pW_M: encoder (naming system)
        :return: I(W;U)
        """
        pMW = pW_M * self.pM
        pWU = pMW.T @ self.pU_M
        return MI(pWU)

    def d_IB(self, pW_M):
        """
        :param pW_M: encoder (naming system)
        :return: E[D[m||m_hat]] = I(M;U) - I(W;U)
        """
        return self.I_MU - self.accuracy(pW_M)

    def fit(self, pW_M):
        """
        fits the naming system by
        :param pW_M: encoder (naming system)
        :return:
            epsilon - deviation from optimality of pW_M
            gnid - gNID between qW_M and qW_M_fit
            bl - beta_l, the value of beta that was fitted to pW_M
            qW_M_fit - the optimal IB system at bl
        """
        Fl = self.complexity(pW_M) - self.betas * self.accuracy(pW_M)
        dFl = Fl - self.F
        bl_ind = dFl.argmin()
        bl = self.betas[bl_ind]
        epsilon = dFl.min() / bl
        qW_M_fit = self.qW_M[bl_ind]
        gnid = gNID(pW_M, qW_M_fit, self.pM)
        return epsilon, gnid, bl, qW_M_fit

    def mode_map(self, pW_M):
        """
        :param pW_M: encoder (naming system)
        """
        figs.mode_map(pW_M, self.pM)
