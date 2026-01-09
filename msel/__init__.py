'''
| 
| Authors:      Ahmad Khoureich Ka
| Date:         01/2026
|
'''

from charm.toolbox.pairinggroup import ZR, extract_key 
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.toolbox.securerandom import OpenSSLRand

from ipfe_ddh import IPFEDDH

class MSEL():
    def __init__(self, group_obj, l):
        self.name = 'msel-ddh'
        self.group = group_obj
        self.ipfe = IPFEDDH(group_obj, l)
        self.l = l
        self.BLOCK_SIZE = 16
    
    def H(self, e):
        return extract_key(e)

    def setup(self):
        (msk, mpk) = self.ipfe.setup()
        return msk, mpk
        
    def keyder(self, msk, x):
        sk = self.ipfe.keygen(msk, x)
        return sk
        
    def encrypt(self, mpk, pi, M):  
        S = []      
        r =  OpenSSLRand().getRandomBytes(self.BLOCK_SIZE)
        C = [r]

        for i, m_i in enumerate(M):
            while True:
                s_i = self.group.random(ZR)
                if s_i not in S:
                    S.append(s_i)
                    break
            
            sym = SymmetricCryptoAbstraction(self.H(mpk['g1']**s_i))
            SE = sym._initCipher(r)
            u_i = SE.encrypt(sym._padding.encode(m_i))
            s_ie_pi = [0] * self.l
            s_ie_pi[pi[i]] = s_i
            v_i = self.ipfe.encrypt(mpk, s_ie_pi)
            C.append((u_i, v_i))
        
        return C
    
    def decrypt(self, SKx, C):
        M = []
        t = len(C) - 1

        for i in range(t):
            (u_i, v_i) = C[i + 1]
            rho_i = self.ipfe.decrypt(SKx, v_i)
            if rho_i != self.group.init(ZR, 1):
                sym = SymmetricCryptoAbstraction(self.H(rho_i))
                SE = sym._initCipher(C[0])
                m_i = SE.decrypt(u_i)
                M.append(sym._padding.decode(m_i))
        return M