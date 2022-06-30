import time
start = time.time()
from cmath import log,tanh,exp,pi,log10
from CoolProp.HumidAirProp import HAPropsSI
from CoolProp.CoolProp import PropsSI
from ERS.convertion import convert
from ERS.ultracoolantProp_direct import *
from ERS.interpolation import *

def ERS_TRIAL(T_amb_IN,RH_amb_IN,Altitude_ID,Model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic,M_data):
    Model_data={}
    m_dot_a={}
    m_dot_w={}
    omega_={}
    T_sat={}
    T_sat_w={}
    T_={}
    P_={}
    h_a={}
    h_w={}
    Rho_a={}
    C_p_a={}
    Mu_a={}
    k_a={}
    Pr_a={}
    v_a={}
    P_amb=0
    P_w_amb=0

    if Pr_type=="Rated_Pressure":
        Model_data["P"]=M_data.P
        Model_data["p_S1"]=M_data.p_S1
        Model_data["p_S2"]=M_data.p_S2
        Model_data["FAD"]=M_data.FAD
        Model_data["Q_sh"]=M_data.Q_sh
        Model_data["Pr_ratio_stg1"]=M_data.Pr_ratio_stg1
        Model_data["Pr_ratio_stg2"]=M_data.Pr_ratio_stg2
        Model_data["n_stg1"]=M_data.n_stg1
        Model_data["n_stg2"]=M_data.n_stg2
    else:
        (Model_data["p_S1"],Model_data["p_S2"],Model_data["FAD"],Model_data["Q_sh"],Model_data["Pr_ratio_stg1"],
            Model_data["Pr_ratio_stg2"],Model_data["n_stg1"],Model_data["n_stg2"])=P_Interpolation(M_data,P)


    def condensate(m_dot_dry_air, m_dot_pa, m_dot_pw, omega_p, P_c, T_c, cond,P_w_amb,P_100): #: m_dot_ca, m_dot_cw, omega_c,T_c_sat):
        T_c_sat= HAPropsSI('D','P_w',P_w_amb*(P_c/P_100),'P',P_c,'R',1)                        
        if T_c < T_c_sat :
            omega_c = HAPropsSI('W','T',T_c,'P',P_c,'R',1.00); #humrat(AirH2O,T=T_c,R=1.00,P=P_c)   
            m_dot_cw = (m_dot_dry_air * (omega_p - omega_c)) + m_dot_pw   
            m_dot_ca = m_dot_pa - (m_dot_dry_air * (omega_p - omega_c))  
        else:  
            if (cond!=205 and cond!=215 and cond!=225) : 
                omega_c = omega_p 
                #print("omega_125 : ",omega)   
                m_dot_ca = m_dot_pa  
                #print(m_dot_a[cond])  
                m_dot_cw = 0  + m_dot_pw 
                #print(m_dot_w[cond])
            else:
                if T_c == T_c_sat :   
                    omega_c = omega_p    
                    m_dot_ca = m_dot_pa    
                    m_dot_cw = 0  + m_dot_pw   
                else  :  
                    omega_pw = omega_p + (m_dot_pw / m_dot_dry_air)                                                          #"Omega_w ' wet ' assumes all water carryover is vaporized"    
                    T_c_sat = HAPropsSI('D','P_w',P_w_amb*(P_c/P_100),'P',P_c,'R',1);#print("T_c_sat_w : ",T_sat[cond])
                    if T_c < T_c_sat :    
                        omega_c = HAPropsSI('W','T',T_c,'P',P_c,'R',1.00);                                               #humrat(AirH2O,T=T_c,R=1.00,P=P_c)     
                        m_dot_cw = ((m_dot_dry_air * omega_p) + m_dot_pw)  - (m_dot_dry_air * omega_c)              #"Conservation of mass"      
                        m_dot_ca = (m_dot_pa + m_dot_pw) - m_dot_cw    
                    else :    
                        omega_c = omega_pw     
                        m_dot_ca = (m_dot_pa + m_dot_pw)     
                        m_dot_cw= 0 #[kg/s]
        '''print("m_dot_a_dict : ",m_dot_a)
        print("m_dot_w_dict : ",m_dot_w)
        print("omega_dict : ",omega_)
        print("T_sat_dict",T_sat)'''
        return (m_dot_ca, m_dot_cw, omega_c,T_c_sat)

    def compressedairprop (T, omega, P) : #: h_a,h_w,Rho_a,C_p_a,Mu_a,k_a,Pr_a) 
        h_a = HAPropsSI('H','T',T,'P',P,'W',omega) #enthalpy(AirH2O,T=T,w=omega,P=P)   
        h_w = PropsSI('H','T',T,'P',P,'IF97::Water'); #print(h_125) #enthalpy(Water,T=T,P=P)                      
        Rho_a = 1/HAPropsSI('Vha','T',T,'P',P,'W',omega)  #density(AirH2O,T=T,w=omega,P=P)             
        C_p_a = HAPropsSI('Cha','T',T,'P',P,'W',omega); #print(C_p_a)  #cp(AirH2O,T=T,w=omega,P=P)                 
        Mu_a = HAPropsSI('mu','T',T,'P',P,'W',omega); #print(Mu_a)   #viscosity(AirH2O,T=T,w=omega,P=P)            
        k_a = HAPropsSI('K','T',T,'P',P,'W',omega)    #conductivity(AirH2O,T=T,w=omega,P=P)          
        Pr_a = (Mu_a*C_p_a)/k_a; #print(Pr_a)   #prandtl(AirH2O,T=T,w=omega,P=P)   
        return (h_a,h_w,Rho_a,C_p_a,Mu_a,k_a,Pr_a)



    def ambientpressure(Altitude) : #(Altitude : P_amb):   #" *** Pressure at altitude calculations *** "  
        g_o = 9.80665 #[m/s^2] #"Universal constants"  
        M = 28.9644 #[kg/kmol] #"Universal constants"  
        R = 8314.32 #[N-m/kmol-K] #"Universal constants"  
        #"Atmospheric layer constants for less than 11,000 meters. Reference: https://en.wikipedia.org/wiki/Barometric_formula"  
        P_b = 101325 #[Pa]  #"Static pressure"  
        T_b = 288.15 #[K]  #"Standard temperature"  
        h_b = 0 #[m]  #"Height at bottom of layer b (e.g.: h_1 = 11,000 m)"  
        L_b = -0.0065 #[K/m]  #"Standard temperature lapse rate in ISA"  
        H = Altitude  ##############################
        P_amb = (P_b * pow((T_b / (T_b + L_b * (H - h_b))),((g_o * M)/(R*L_b))))
        return P_amb #############################

    def geometry(L_core, T_core,H, lambda_, t, n_coldrows, side, type):
        if side=="cold":                        # for coldside
            th_Lbar = 11.5*convert('mm','m')
            W_core = L_core - 2 * th_Lbar
            if type=="wavy":  # for coldwavyfin
                L_core = T_core*1.083
            else:             # for coldoffsetfin
                L_core = T_core
        elif side=="hot":                        # for Hotside
            th_Wbar = 6*convert('mm','m')
            W_core = T_core - 2 * th_Wbar
            n_coldrows-=1
            if type=="wavy":    # for hotwavyfin
                L_core*=1.083
        else :
            print("ERROR")
        
        W = lambda_ - t
        Hi = H - t 
        Dh = (2*W*Hi)/(W+Hi)  
        Af = (W*Hi)/lambda_  
        At = (2*(W+Hi))/lambda_  
        Ap = (2*W)/lambda_  
        As = (2*Hi)/lambda_  
        FA = At*L_core*W_core*n_coldrows  
        Beta = FA/(H*W_core*L_core*n_coldrows)  
        Alpha = (Af*W_core*n_coldrows)/(H*W_core*n_coldrows)  
        A_face = (H*W_core*n_coldrows)
        return (W_core,L_core,W,Hi,n_coldrows,Dh,Af,At,Ap,As,FA,Beta,Alpha,A_face)
            

    def corewidth (H_cs, n_cs,H_hs, n_hs): #: W_core)   
        th_middleplate = 0.5*convert('mm','m') # #[mm]*convert(mm,m) 
        th_cover = 3*convert('mm','m') # #[mm]*convert(mm,m) 
        W_core = (H_cs*n_cs)+(H_hs*n_hs)+(th_middleplate*(n_cs+n_hs+1))+(th_cover*4) 
        return W_core

    def ntusensiblemethod (m_dot_c, C_p_c_avg, m_dot_h, C_p_h_avg,UA): #: epsilon,C_dot_min,C_dot_H,C_dot_C)    
        C_dot_H = m_dot_h*C_p_h_avg  
        C_dot_C = m_dot_c*C_p_c_avg  
        C_dot_min=min(C_dot_H,C_dot_C)   
        #//Minimum capacitance rate  
        C_dot_max=max(C_dot_H,C_dot_C) 
        #//Maximum capacitance rate 
        CR=C_dot_min/C_dot_max 
        NTU =(UA*convert('W/C','kW/C'))/C_dot_min   
        epsilon=(1-exp((pow(NTU,0.22)/CR)*(exp(-(CR*pow(NTU,0.78)))-1))).real                    
        #epsilon=HX('crossflow_both_unmixed', NTU, C_dot_C, C_dot_H, 'epsilon')   ##################################
        return (epsilon,C_dot_min,C_dot_H,C_dot_C)
        #//Access effectiveness-NTU_OC solution   

    def ntulatentmethod (Q_dot, T_HIN, T_HOUT,m_dot_c, C_p_c_avg,UA): #: epsilon_lat,C_dot_min_lat,C_dot_H_lat,C_dot_C_lat)    
        C_dot_H_lat = Q_dot/(T_HIN-T_HOUT)  
        C_dot_C_lat = m_dot_c*C_p_c_avg 
        #//Cold Sensible capacitance rate  
        C_dot_min_lat=min(C_dot_H_lat,C_dot_C_lat)  
        #//Sensible Minimum capacitance rate  
        C_dot_max_lat=max(C_dot_H_lat,C_dot_C_lat)  
        #// Sensible Maximum capacitance rate 
        CR=C_dot_min_lat/C_dot_max_lat 
        NTU_lat=(UA*convert('W/C','kW/C'))/C_dot_min_lat  
        epsilon_lat=(1-exp((pow(NTU_lat,0.22)/CR)*(exp(-(CR*pow(NTU_lat,0.78)))-1))).real                
        #epsilon_lat=HX('crossflow_both_unmixed', NTU_lat, C_dot_H_lat, C_dot_C_lat, 'epsilon')   ###############################
        return (epsilon_lat,C_dot_min_lat,C_dot_H_lat,C_dot_C_lat)
        #// Sensible Effectiveness-NTU_AC solution 

    def overallucoeff (alpha_cs, t_cs,H_cs, As_cs,At_cs,alpha_hs,t_hs,H_hs,As_hs,At_hs,FA_cs,FA_hs): #: UA_hs,UA_cs,UA)   
        k_cs = 192 #[W/m C]  
        m_cs = pow(((2*alpha_cs)/(k_cs*t_cs)),(1/2))
        eta_f_cs = (tanh(m_cs*H_cs*0.5)/(m_cs*H_cs*0.5)).real                 
        eta_O_cs = 1- ((1-eta_f_cs)*(As_cs/At_cs))   
        k_hs = 192 #[W/m C]   
        m_hs = pow(((2*alpha_hs)/(k_hs*t_hs)),(1/2)) 
        eta_f_hs = (tanh(m_hs*H_hs*0.5)/(m_hs*H_hs*0.5)).real                 
        eta_O_hs = 1- ((1-eta_f_hs)*(As_hs/At_hs))  
        #//Overall Heat Transfer Calcualtion   
        alpha_0_cs = 1/((1/(alpha_cs*eta_O_cs))+(FA_cs/(FA_hs*alpha_hs*eta_O_hs)))  
        alpha_0_hs = 1/((1/(alpha_hs*eta_O_hs))+(FA_hs/(FA_cs*alpha_cs*eta_O_cs)))    
        UA_hs = alpha_0_hs*FA_hs  
        UA_cs = alpha_0_cs*FA_cs
        print(alpha_hs,alpha_cs)
        print(m_cs,eta_f_cs,eta_O_cs)
        print(m_hs,eta_f_hs,eta_O_hs)
        print(alpha_0_cs,alpha_0_hs)
        print(FA_cs,FA_hs) 
        print(UA_hs,UA_cs)
        UA = max(UA_hs,UA_cs)
        return (UA_hs,UA_cs,UA)

    def avgprop (Rho_IN, C_p_IN, Mu_IN,k_IN,Pr_IN,Rho_OUT, C_p_OUT, Mu_OUT,k_OUT,Pr_OUT,avg ) : # Rho_avg,C_p_avg,Mu_avg,k_avg,Pr_avg)    
        Rho_a[avg]  =  (Rho_IN+Rho_OUT)/2  
        C_p_a[avg] =  (C_p_IN+C_p_OUT)/2  
        Mu_a[avg]  =  (Mu_IN+Mu_OUT)/2   
        k_a[avg]  =  (k_IN+k_OUT)/2   
        Pr_a[avg]  =  (Pr_IN+Pr_OUT)/2  

    def coolingairprop (T, omega, P,n) : #h_ca,v_ca,Rho_ca,C_p_ca,Mu_ca,k_ca,Pr_ca)   
        h_a[n] = HAPropsSI('H','T',T,'P',P,'W',omega)    #enthalpy(AirH2O,T=T,w=omega,P=P)  
        v_a[n] = HAPropsSI('Vha','T',T,'P',P,'W',omega)     #volume(AirH2O,T=T,w=omega,P=P)  
        Rho_a[n] = 1/HAPropsSI('Vha','T',T,'P',P,'W',omega) #density(AirH2O,T=T,w=omega,P=P)            
        C_p_a[n] = HAPropsSI('Cha','T',T,'P',P,'W',omega)   #cp(AirH2O,T=T,w=omega,P=P)                 
        Mu_a[n] = HAPropsSI('M','T',T,'P',P,'W',omega)   #viscosity(AirH2O,T=T,w=omega,P=P)  
        k_a[n]= HAPropsSI('K','T',T,'P',P,'W',omega)    #conductivity(AirH2O,T=T,w=omega,P=P)   
        Pr_a[n] = (Mu_a[n]*C_p_a[n])/k_a[n]         #prandtl(AirH2O,T=T,w=omega,P=P)             

    def qlattent (Q_dot_Total, Q_dot_Sensible ): #Q_dot_Lattnet)    
        Q_dot_Lattnet = Q_dot_Total - Q_dot_Sensible  
        if Q_dot_Lattnet < 0 :  
            Q_dot_Lattnet = 0 
        return Q_dot_Lattnet

    #------------------------------------------Start of INPUTS ----------------------------------"  
    # //Inputs From Airend Data Sheet ( To be Commented when parametric table is used ) 


    T_amb = T_amb_IN+273.15 #[C]  Ambient
    RH_amb = RH_amb_IN  #RH   
    FAD = Model_data["FAD"] #[m^3/hr]  FAD   
    p_S1= Model_data["p_S1"]*pow(10,5) #[bar]  Stage 1 Pressure  
    T_[125] = ((Model_data["Pr_ratio_stg1"]**((Model_data["n_stg1"]-1)/Model_data["n_stg1"]))*(T_amb)) #[C]  Stage 1 Temperature  
    p_S2= Model_data["p_S2"]*pow(10,5) #[bar]   Stage 2  
    T_[225] = ((Model_data["Pr_ratio_stg2"]**((Model_data["n_stg2"]-1)/Model_data["n_stg2"]))*(TW_in+11+273.15)) #C]  Stage 2 Temperature  
    Q_sh = Model_data["Q_sh"]*pow(10,3)

    #Secondary Inputs To cooler  
    Altitude = Altitude_ID #[m]  //Altitide of Package  
    DELTAT_pkg_rise = 4 #[C]  #Inside Package temperature rise   
    DELTAP_100 = 0  #Filter Pressure drop  
    DELTAP_150 =  0  #Interstage Pressure drop  
    CTD_150 = CTD_ic #[C]  //CTD for Intercooler  
    DELTAP_250 = 0  #Second Stage Pressure drop  
    CTD_250 = CTD_ac #[C]  //CTD for After Cooler 


    P_amb=ambientpressure(Altitude); print("P_amb : ", P_amb) #(Altitude : P_amb)  #//Ambient Pressure calculatio

    #----------------------------------START OF AMBEINT AIR PROPERTY CALCULATION ----------------------------

    omega_amb = HAPropsSI('W','T',T_amb,'P',P_amb,'R',RH_amb); print("omega_amb : ",omega_amb) #SPECFIC HUMIDITY OF AMBIENT AI
    h_amb = HAPropsSI('H','T',T_amb,'P',P_amb,'W',omega_amb); print("h_amb : ",h_amb)      #AMBIENT ENTHALPHY 
    P_w_amb = HAPropsSI('P_w','T',T_amb,'P',P_amb,'W',omega_amb); print("P_w_amb : ",P_w_amb)
    #Package Inlet  
    T_[100] = T_amb
    P_[100] = P_amb - DELTAP_100 
    omega_[100] = omega_amb
    v_100a = HAPropsSI('Vha','T',T_amb,'P',P_amb,'W',omega_[100]); print("v_100a : ",v_100a)
    m_dot_a[100] = (FAD/3600) / v_100a           
    m_dot_w[100] = 0 #[kg/s]
    m_dot_dry_air = m_dot_a[100] / (1+omega_[100]) 
    m_dot_wv = m_dot_a[100] - m_dot_dry_air 
    h_a[100] = HAPropsSI('H','T',T_[100],'P',P_[100],'W',omega_[100]); print("h_100a : ",h_a[100])


    #------------------------------------ START OF STAGE 1 PROPERTY CALC  ------------------------------------

    P_[125] = p_S1                             
    (m_dot_a[125], m_dot_w[125], omega_[125],T_sat[125])=condensate (m_dot_dry_air, m_dot_a[100], m_dot_w[100], omega_[100], P_[125], T_[125],125,P_w_amb,P_[100])  # : m_dot_125a, m_dot_125w, omega_125)      # Inline IC IN Properties 
    print("OOOOOOO    ", omega_[125])
    print("ma    " ,m_dot_a[125])
    print("mw    " ,m_dot_w[125])
    n=125
    (h_a[125],h_w[125],Rho_a[125],C_p_a[125],Mu_a[125],k_a[125],Pr_a[125])=compressedairprop (T_[125], omega_[125], P_[125]) #: h_125a,h_125w,Rho_125a,C_p_125a,Mu_125a,k_125a,Pr_125a)                    # Inline IC IN Properties 
    P_[150] = P_[125] - DELTAP_150             # Inline IC OUT Cooler Pressure  
    T_[150] = TW_in+273.15 + CTD_150                #  Inline IC OUT Cooler NTU Temperature  
    (m_dot_a[150], m_dot_w[150], omega_[150],T_sat[150])=condensate (m_dot_dry_air, m_dot_a[125], m_dot_w[125], omega_[125], P_[150], T_[150],150,P_w_amb,P_[100]) #: m_dot_150a, m_dot_150w, omega_150)      # Inline IC Out Properties  
    (h_a[150],h_w[150],Rho_a[150],C_p_a[150],Mu_a[150],k_a[150],Pr_a[150])=compressedairprop (T_[150], omega_[150], P_[150]) #: h_150a,h_150w,Rho_150a,C_p_150a,Mu_150a,k_150a,Pr_150a)                    # Inline IC Out Properties 
    avgprop (Rho_a[125], C_p_a[125], Mu_a[125],k_a[125],Pr_a[125],Rho_a[150], C_p_a[150], Mu_a[150],k_a[150],Pr_a[150], 137) #: Rho_137a,C_p_137a,Mu_137a,k_137a,Pr_137a)           # Inline IC AVG Props   "

    # *** Moisture seperator at interstage (Proximity 200) *** " 
    DELTAP_200 = 0                       # Mos Delta Pressure 
    P_[200] = P_[150] - DELTAP_200           # MOS Out Pressure
    T_[200] = T_[150]                        #"Assume isothermal" 
    omega_[200] = omega_[150]                #"Assume isothermal and negligible pressure drop" 
    m_dot_a[200] = m_dot_a[150]   
    EPSILON_ms1 = 0.5                    # Eff of MOS 
    m_dot_w[200] = (1 - EPSILON_ms1) * m_dot_w[150]            # Flow of Stage 1 condensate 
    #LPH_ms1 = EPSILON_ms1 * (m_dot_w[150] * volume(Water,T=T_[150],P=P_[150])) * convert(m^3/s, L/hr)         ##################### Flow of Stage 1 Condensate

    # ------------------------------------------ INLINE START OF STAGE 2  PROPERTY CALC  -----------------------------"

    P_[225] = p_S2      
    (m_dot_a[225], m_dot_w[225], omega_[225],T_sat[225])=condensate (m_dot_dry_air, m_dot_a[200], m_dot_w[200], omega_[200], P_[225], T_[225],225,P_w_amb,P_[100]) #: m_dot_225a, m_dot_225w, omega_225,T_225_sat) #// Inline AC IN Properties 
    (h_a[225],h_w[225],Rho_a[225],C_p_a[225],Mu_a[225],k_a[225],Pr_a[225])=compressedairprop (T_[225], omega_[225], P_[225]) #: h_225a,h_225w,Rho_225a,C_p_225a,Mu_225a,k_225a,Pr_225a)  #// Inline AC Properties 

    P_[250] = P_[225] - DELTAP_250   #//Inline AC OUT Cooler Pressure  
    T_[250] = TW_in+273.15 + CTD_250  #//Inline AC OUT Cooler NTU Temperature  
    (m_dot_a[250], m_dot_w[250], omega_[250],T_sat[250])=condensate (m_dot_dry_air, m_dot_a[225], m_dot_w[225], omega_[225], P_[250], T_[250],250,P_w_amb,P_[100]) #: m_dot_250a, m_dot_250w, omega_250) #// Inline AC Out Properties 
    (h_a[250],h_w[250],Rho_a[250],C_p_a[250],Mu_a[250],k_a[250],Pr_a[250])=compressedairprop (T_[250], omega_[250], P_[250]) #: h_250a,h_250w,Rho_250a,C_p_250a,Mu_250a,k_250a,Pr_250a)  #// Inline AC Out Properties 
    avgprop (Rho_a[225], C_p_a[225], Mu_a[225],k_a[225],Pr_a[225],Rho_a[250], C_p_a[250], Mu_a[250],k_a[250],Pr_a[250], 237) #: Rho_237a,C_p_237a,Mu_237a,k_237a,Pr_237a) #// Inline AC AVG Props   

    DELTAP_300 = 0  #//Mos Delta Pressure 
    P_[300] = P_[250] - DELTAP_200  #//MOS Out Pressure 
    T_[300] = T_[250]   #"Assume isothermal" 
    omega_[300] = omega_[250]   #"Assume isothermal and negligible pressure drop" 
    m_dot_a[300] = m_dot_a[250]   
    EPSILON_ms2 = 0.5  #// Eff of MOS 
    m_dot_300w = (1 - EPSILON_ms2) * m_dot_w[250] #// Flow of Stage 1 condensate 
    #LPH_ms2 = EPSILON_ms2 * (m_dot_w[250] * volume(Water,T=T_[250],P=P_[250])) * convert(m^3/s, L/hr) #// Flow of Stage 1 Condensate

    #"--------------------------------START OF STAGE 1 & STAGE 2 HEAT LOADS CALC---------------------------------------"    

    Q_dot_1 = ((m_dot_a[125] * h_a[125]) - (m_dot_a[150] * h_a[150])) + ((m_dot_w[150] * h_w[150]) - (m_dot_w[125] * h_w[125])) #//Inline IC Total Heat Load 
    Q_dot_1Sen = m_dot_a[125] * C_p_a[137] * (T_[125] - T_[150])  #//Inline IC Sensible Heat Load 
    Q_dot_1_InAir = m_dot_a[125] * C_p_a[137] * (T_[150] - T_[100])   
    Q_dot_2 = ((m_dot_a[225] * h_a[225]) + (m_dot_w[225] * h_w[225])) - ((m_dot_a[250] * h_a[250]) + (m_dot_w[250] * h_w[250])) #//Inline AC Total Heat Load 
    Q_dot_2Sen = m_dot_a[225] * C_p_a[237] * (T_[225] - T_[250])  #//Inline AC Sensible Heat Load 
    qlattent (Q_dot_2, Q_dot_2Sen) #: Q_dot_2lat)  #//Inline AC Lattent Heat Load   
    Q_AIR = Q_dot_1Sen+Q_dot_2Sen 
    Q_oil = Q_sh - Q_AIR - (Q_sh*0.03) - Q_dot_1_InAir 

    print("Q_dot_1 :", Q_dot_1)
    print("Q_dot_2 :", Q_dot_2)
    print("Q_oil :", Q_oil)  

    print(T_amb_IN,RH_amb_IN,Altitude_ID,Model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic)
    #print(M_data.P,M_data.p_S1,M_data.p_S2,M_data.FAD,M_data.Q_sh,M_data.Pr_ratio_stg1,M_data.Pr_ratio_stg2,M_data.n_stg1,M_data.n_stg1)
    print(T_[125],T_[225],T_[150],T_[250])
    return (int(Q_dot_1/1000),int(Q_dot_2/1000),int(Q_oil/1000))