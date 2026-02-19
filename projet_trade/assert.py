from build import builder_uni
import numpy as np
import yfinance as yf

class validation(builder_uni):
    def __init__(self,name:str):
        ticker = yf.Ticker(name) #Objet : entreprise,action,etf...
        self.historique = ticker.history(start="2020-01-01",end="2020-01-30",interval="1d").reset_index() #historique sur laquel on travaillera 
        self.historique_anterieur = ticker.history(start="2019-12-01",end="2020-01-30",interval="1d").reset_index() #historique antérieur , utile pour calculer la première valeur de certains index surtout pour les indexs récurssifs
        self.index_correspondance =super().correspondance()
        self.rendement_4 = super().rendement(4)
        self.sma_20 = super().SMA(20)
        self.vol_20 = super().Volume_norm(20)
        self.atr_14 = super().ATR(14)
    

if __name__ == "__main__":
    aapl = validation("AAPL")
    assert aapl.index_correspondance == 25
    assert np.allclose(aapl.rendement_4.values,[0.00945606,0.03130024,0.01244072,-0.02407041],atol=1e-06)
    assert np.allclose(aapl.sma_20.values,[68.912947,70.886452,72.596126,74.121637])
    assert np.allclose(aapl.vol_20.values,[122264740.0,129972960.0,131106480.0,131038080.0])
    #Pour les fonctions récursives calcul trop long 
    print("Le code fonctionne conformément à ce qui est attendu")



