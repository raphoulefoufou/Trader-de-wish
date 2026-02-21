
import yfinance as yf #librairie nous permettant  d'avoir l'historique boursier des entreprises
import pandas as pd #Pour construire le dataset plus facilement 
from datetime import datetime 

class builder_uni(): #Classe qu'on appellera pour construire notre dataset
    def __init__(self,name):
        ticker = yf.Ticker(name) #Objet : entreprise,action,etf...
        self.historique = ticker.history(period="8y").reset_index() #historique sur laquel on travaillera 
        self.historique_anterieur = ticker.history(period="9y").reset_index() #historique antérieur , utile pour calculer la première valeur de certains index surtout pour les indexs récurssifs
        self.index_correspondance = self.correspondance()
    def correspondance(self)->int:
        date_start = str(self.historique.loc[4,"Date"])
        date_start_search = date_start[:10]
        index = 0
        for i in range(len(self.historique_anterieur)):
            date_start_2 = str(self.historique_anterieur.loc[i,"Date"])
            date_start_search_2 = date_start_2[:10]
            if (date_start_search == date_start_search_2): index += i
        return int(index)    

    def RSI_norm(self, period):
        nom = f"RSI({period})"
        closes = self.historique["Close"]
        dates = self.historique["Date"]
    
        deltas = closes.diff()
        gains = deltas.clip(lower=0)
        pertes = -deltas.clip(upper=0)
    
    # Moyenne initiale de Wilder (SMA sur la première fenêtre)
        avg_gain = gains.iloc[1:period+1].mean()
        avg_perte = pertes.iloc[1:period+1].mean()
    
        rsi_vals = []
        rsi_dates = []
    
        for i in range(period + 1, len(closes)):
            avg_gain = (avg_gain * (period - 1) + gains.iloc[i]) / period
            avg_perte = (avg_perte * (period - 1) + pertes.iloc[i]) / period
        
            if avg_gain == 0 and avg_perte == 0:
                rsi_val = 0.5
            elif avg_perte == 0:
                rsi_val = 1.0
            elif avg_gain == 0:
                rsi_val = 0.0
            else:
                rs = avg_gain / avg_perte
                rsi_val = (100 - 100 / (1 + rs)) / 100
        
            if i % 4 == 0:  # on ne garde qu'une valeur sur 4
                rsi_vals.append(rsi_val)
                rsi_dates.append(dates.iloc[i])
        return pd.Series(rsi_vals, index=rsi_dates, name=nom)   
    def rendement(self,period): #Indice donnant le rendement sur 4 j
        nom = "Rendement("+str(period)+")" 
        index = self.index_correspondance -4
        tab = []
        dates = []    
        for j in range(4,len(self.historique)):
            c4 = self.historique_anterieur.loc[index+j,"Close"]
            c0 = self.historique_anterieur.loc[index+j-period,"Close"]
            tab.append((c4 - c0)/c0)
            dates.append(self.historique.loc[j,"Date"])
        Rend = pd.Series(tab,index=dates,name=nom) 
        mask = [i % 4 == 0 for i in range(4, len(self.historique))]
        Rend = Rend[mask]
        return Rend    
    def launch(self): #Fonction appeller depuis un autre fichier qui assemble les différents index
        rsi4_series = self.RSI_norm(4)
        rsi14_series = self.RSI_norm(14)
        rend4_series = self.rendement(4)
        rend14_series = self.rendement(14)
        macd_series = self.MACD()
        atr4_series = self.ATR(4)
        atr14_series = self.ATR(14)
        sma20_series = self.SMA(20)
        sma50_series = self.SMA(50)
        sma_ratio = sma20_series/sma50_series
        vnorm_series = self.Volume_norm(20)
        

        histo_filtered = self.historique[self.historique["Date"].isin(rsi4_series.index)].copy()
        histo_filtered = histo_filtered.set_index("Date")

        histo_filtered["RSI(4)"] = rsi4_series
        histo_filtered["RSI(14)"] = rsi14_series
        histo_filtered["rendement(4)"] = rend4_series
        histo_filtered["rendement(14)"] = rend14_series
        histo_filtered["MACD"] = macd_series
        histo_filtered["ATR(14)"] = atr14_series
        histo_filtered["ATR(4)"] = atr4_series
        histo_filtered["SMA(20)"] = sma20_series
        histo_filtered["SMA(50)"] = sma50_series
        histo_filtered["Ratio[SMA(20)/SMA(50)]"] = sma_ratio
        histo_filtered["Volume_norm(20)"] = vnorm_series

        close = histo_filtered["Close"]
        atr = histo_filtered["ATR(14)"]

        # On s'assure que les deux séries sont alignées sur le même index
        histo_filtered["decision"] = ((close.shift(-1) - close) / atr)

        histo_filtered = histo_filtered.iloc[:-1]
        return histo_filtered
    def MACD(self): #ouai ouai
        index = self.index_correspondance
        sum_12 = 0.0
        sum_26 = 0.0    
        for i in range(12):
            sum_12 += float(self.historique_anterieur.loc[index-i,"Close"])
        sma_12 = sum_12/12    
        for i in range(26):
            sum_26 += float(self.historique_anterieur.loc[index-i,"Close"])
        sma_26 = sum_26/26
        #Multiplicateur = 2 / (Période + 1)
        m_26 = 2/27
        m_12 = 2/13
        #EMA_aujourd'hui = (Prix_aujourd'hui × Multiplicateur) + (EMA_hier × (1 - Multiplicateur))
        ema_12_tab = []
        dates = []
        for i in range(4,len(self.historique)):
            prix_ajd = float(self.historique.loc[i,"Close"])
            if i == 4:
                ema_start = (prix_ajd*m_12)+(sma_12*(1-m_12))
                ema_12_tab.append(ema_start)
                dates.append(self.historique.loc[i,"Date"])
            else:
                ema_hier = ema_12_tab[-1]
                ema = (prix_ajd*m_12)+(ema_hier*(1-m_12))
                ema_12_tab.append(ema)
                dates.append(self.historique.loc[i,"Date"])
        ema_26_tab = []
        for i in range(4,len(self.historique)):
            prix_ajd = float(self.historique.loc[i,"Close"])
            if i == 4:
                ema_start = (prix_ajd*m_26)+(sma_26*(1-m_26))
                ema_26_tab.append(ema_start)
            else:
                ema_hier = ema_26_tab[-1]
                ema = (prix_ajd*m_26)+(ema_hier*(1-m_26))
                ema_26_tab.append(ema)    
        macd_tab = []        
        for i in range(len(ema_12_tab)):
            macd = ema_12_tab[i] - ema_26_tab[i]
            macd_tab.append(macd)
        Macd =  pd.Series(macd_tab,index=dates,name="MACD")   
        mask = [i % 4 == 0 for i in range(4, len(self.historique))]
        Macd = Macd[mask]
        return Macd   
    def ATR(self,period): #indice permettant d'avoir des infos sur la volatilitée de l'action 
        index = self.index_correspondance
        nom = "ATR("+str(period)+")"
        dates = []
        #Faire la moyenne TR des 14 premiers jours pour l'initialisation
        tr_tab = []
        for i in range(index-period,index):
            high = float(self.historique_anterieur.loc[i,"High"])
            low = float(self.historique_anterieur.loc[i,"Low"])
            close_hier = float(self.historique_anterieur.loc[i-1,"Close"])
            high_low = abs(high - low)
            high_close = abs(high - close_hier)
            low_close = abs(low - close_hier)
            tr = max(high_low,high_close,low_close)
            tr_tab.append(tr)
        somme = 0
        for i in tr_tab:
            somme +=i    
        moyenne = somme/period
        atr = []
        #ATR(aujourd'hui) = [(ATR(précédent) × 13) + TR(aujourd'hui)] / 14
        for i in range(index,len(self.historique_anterieur)):
            high = float(self.historique_anterieur.loc[i,"High"])
            low = float(self.historique_anterieur.loc[i,"Low"])
            close_hier = float(self.historique_anterieur.loc[i-1,"Close"])
            high_low = abs(high - low)
            high_close = abs(high - close_hier)
            low_close = abs(low - close_hier)
            tr = max(high_low,high_close,low_close)
            if i == index:
                atr_values = ((moyenne*(period-1))+tr)/period
                atr.append(atr_values)
                dates.append(self.historique_anterieur.loc[i,"Date"])
            else:
                last = float(atr[-1])
                atr_values = ((last*(period-1))+tr)/period
                atr.append(atr_values)
                dates.append(self.historique_anterieur.loc[i,"Date"])
        Atr =  pd.Series(atr,index=dates,name=nom)   
        mask = [i % 4 == 0 for i in range(4, len(self.historique))]
        Atr = Atr[mask]
        return Atr        
    def SMA(self,period:int):
        nom = "SMA("+str(period)+")" 
        index = self.index_correspondance -4
        tab = []
        dates = []    
        for j in range(4,len(self.historique)):
            somme = 0
            moyenne = 0
            for x in range(1+index+j-period, index+j+1):
                somme += float(self.historique_anterieur.loc[x,"Close"])
            moyenne = somme/period
            tab.append(moyenne) 
            dates.append(self.historique.loc[j,"Date"]) 
        Sma =  pd.Series(tab,index=dates,name=nom)   
        mask = [i % 4 == 0 for i in range(4, len(self.historique))]
        Sma = Sma[mask]
        return Sma  
    def Volume_norm(self,period):
        nom = "Vol_norm("+str(period)+")" 
        index = self.index_correspondance - 4
        tab = []
        dates = []
        for j in range(4,len(self.historique)):
            somme = 0
            moyenne = 0
            for x in range(1+index+j-period, index+j+1):
                somme += float(self.historique_anterieur.loc[x,"Volume"])
            moyenne = somme/period 
            tab.append(moyenne) 
            dates.append(self.historique.loc[j,"Date"]) 
        Vnorm =  pd.Series(tab,index=dates,name=nom)   
        mask = [i % 4 == 0 for i in range(4, len(self.historique))]
        Vnorm = Vnorm[mask]
        return Vnorm      

