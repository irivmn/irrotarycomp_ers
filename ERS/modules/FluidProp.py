from CoolProp.HumidAirProp import HAPropsSI
from CoolProp.CoolProp import PropsSI
from AmbientAirProps import ambientpressure
from compressed_air_Prop import *


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
P_amb=0
P_w_amb=0


def avgprop (Rho_IN, C_p_IN, Mu_IN,k_IN,Pr_IN,Rho_OUT, C_p_OUT, Mu_OUT,k_OUT,Pr_OUT,avg ) : # Rho_avg,C_p_avg,Mu_avg,k_avg,Pr_avg)    
    Rho_a[avg]  =  (Rho_IN+Rho_OUT)/2  
    C_p_a[avg] =  (C_p_IN+C_p_OUT)/2  
    Mu_a[avg]  =  (Mu_IN+Mu_OUT)/2   
    k_a[avg]  =  (k_IN+k_OUT)/2   
    Pr_a[avg]  =  (Pr_IN+Pr_OUT)/2  

'''def ultracoolantprop (T) : #Rho_O,C_p_O,Mu_O,k_O,Pr_O)                       #################################
    Rho_O = interpolate(Ultracoolant, 'T','Density',T=T)  
    C_p_O = interpolate(Ultracoolant, 'T','C_p',T=T)  
    Mu_O = interpolate(Ultracoolant, 'T','Viscosity_Dynamic',T=T)  
    k_O = interpolate(Ultracoolant, 'T','Conductivity',T=T)  
    Pr_O = (Mu_O*C_p_O)/k_O   

def coolingairprop (T, omega, P) : #h_ca,v_ca,Rho_ca,C_p_ca,Mu_ca,k_ca,Pr_ca)   
    h_ca = HAPropsSI('H','T',T,'P',P,'W',omega)    #enthalpy(AirH2O,T=T,w=omega,P=P)  
    v_ca = HAPropsSI('Vha','T',T,'P',P,'W',omega)     #volume(AirH2O,T=T,w=omega,P=P)  
    Rho_ca = density(AirH2O,T=T,w=omega,P=P)            ##########################
    C_p_ca = cp(AirH2O,T=T,w=omega,P=P)                 ##########################
    Mu_ca = HAPropsSI('M','T',T,'P',P,'W',omega)   #viscosity(AirH2O,T=T,w=omega,P=P)  
    k_ca = HAPropsSI('K','T',T,'P',P,'W',omega)    #conductivity(AirH2O,T=T,w=omega,P=P)   
    Pr_ca = prandtl(AirH2O,T=T,w=omega,P=P)             ##########################'''

def qlattent (Q_dot_Total, Q_dot_Sensible ): #Q_dot_Lattnet)    
    Q_dot_Lattnet = Q_dot_Total - Q_dot_Sensible  
    if Q_dot_Lattnet < 0 :  
        Q_dot_Lattnet = 0 

#------------------------------------------Start of INPUTS ----------------------------------"  
# //Inputs From Airend Data Sheet ( To be Commented when parametric table is used ) 

T_amb = 38+273.15 #[C]  Ambient
RH_amb = 0.4  #RH   
FAD = 1486 #[m^3/hr]  FAD   
p_S1= 3.59*pow(10,5) #[bar]  Stage 1 Pressure  
T_[125] = 198.4+273.15 #[C]  Stage 1 Temperature  
p_S2= 11.9*pow(10,5) #[bar]   Stage 2  
T_[205] = 214.2+273.15 #[C]  Stage 2 Temperature  
T_[225] = 214.2+273.15 #C]  Stage 2 Temperature  
Q_sh = 176*pow(10,3)

#Secondary Inputs To cooler  
Altitude = 0 #[m]  //Altitide of Package  
DELTAT_pkg_rise = 4 #[C]  #Inside Package temperature rise   
DELTAP_100 = 0  #Filter Pressure drop  
DELTAP_150 =  0  #Interstage Pressure drop  
DELTAP_215 = 0  
CTD_150 = 11 #[C]  //CTD for Intercooler  
DELTAP_250 = 0  #Second Stage Pressure drop  
CTD_250 = 11 #[C]  //CTD for After Cooler 
FAD_cfm = FAD* 0.588577779   
T_215_NTU= 180+273.15 

'''m_dot_C_velocity = 7.5 #[kg/m^2-s]  
m_dot_a[500] = m_dot_C_velocity*A_facecs_IC #// Cold Side mass flowrate  
m_dot_a[501] = m_dot_C_velocity*A_facecs_AC #//Cold Side mass flowrate    
m_dot_C1_velocity = 6.8 #[kg/m^2-s]  
m_dot_a[502] = m_dot_C1_velocity*A_facecs_OC   
m_dot_a[505] = m_dot_a[502]  #{ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
m_dot_C3_velocity = 5.3 #[kg/m^2-s]  
m_dot_a[505] = m_dot_C3_velocity*A_face_c_PC #}   '''

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
T_[150] = T_amb + CTD_150                #  Inline IC OUT Cooler NTU Temperature  
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

P_[205] = p_S2 
(m_dot_a[205], m_dot_w[205], omega_[205],T_sat[205])=condensate (m_dot_dry_air, m_dot_a[200], m_dot_w[200], omega_[200], P_[205], T_[205],205,P_w_amb,P_[100]) # : m_dot_205a, m_dot_205w, omega_205,T_205_sat) #// PC IN Properties 
(h_a[205],h_w[205],Rho_a[205],C_p_a[205],Mu_a[205],k_a[205],Pr_a[205])=compressedairprop (T_[205], omega_[205], P_[205]) #: h_205a,h_205w,Rho_205a,C_p_205a,Mu_205a,k_205a,Pr_205a)  #// PC Properties 

P_[215] = P_[205] - DELTAP_215   #//PC OUT Cooler Pressure  
T_[215] = T_215_NTU    #//PC OUT Cooler NTU Temperature    
(m_dot_a[215], m_dot_w[215], omega_[215],T_sat[215])=condensate (m_dot_dry_air, m_dot_a[205], m_dot_w[205], omega_[205], P_[215], T_[215],215,P_w_amb,P_[100]) #: m_dot_215a, m_dot_215w, omega_215,T_215_sat) #// PC IN Properties 
(h_a[215],h_w[215],Rho_a[215],C_p_a[215],Mu_a[215],k_a[215],Pr_a[215])=compressedairprop (T_[215], omega_[215], P_[215]) #: h_215a,h_215w,Rho_215a,C_p_215a,Mu_215a,k_215a,Pr_215a)  #// PC Properties 
avgprop (Rho_a[205],C_p_a[205],Mu_a[205],k_a[205],Pr_a[205],Rho_a[215],C_p_a[215],Mu_a[215],k_a[215],Pr_a[215], 210) #: Rho_210a,C_p_210a,Mu_210a,k_210a,Pr_210a) #// PC AVG Props

T_[225] =  T_[215] 
P_[225] = p_S2      
(m_dot_a[225], m_dot_w[225], omega_[225],T_sat[225])=condensate (m_dot_dry_air, m_dot_a[200], m_dot_w[200], omega_[200], P_[225], T_[225],225,P_w_amb,P_[100]) #: m_dot_225a, m_dot_225w, omega_225,T_225_sat) #// Inline AC IN Properties 
(h_a[225],h_w[225],Rho_a[225],C_p_a[225],Mu_a[225],k_a[225],Pr_a[225])=compressedairprop (T_[225], omega_[225], P_[225]) #: h_225a,h_225w,Rho_225a,C_p_225a,Mu_225a,k_225a,Pr_225a)  #// Inline AC Properties 

P_[250] = P_[225] - DELTAP_250   #//Inline AC OUT Cooler Pressure  
T_[250] = T_amb + CTD_250  #//Inline AC OUT Cooler NTU Temperature  
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
Q_dot_10 = ((m_dot_a[205] * h_a[205]) + (m_dot_w[205] * h_w[205])) - ((m_dot_a[215] * h_a[215]) + (m_dot_w[215] * h_w[215])) #//Normal PC Total Heat Load 
Q_dot_10Sen = m_dot_a[205] * C_p_a[210] * (T_[205] - T_[215])  #//Normal PC Sensible Heat Load     
Q_dot_2 = ((m_dot_a[225] * h_a[225]) + (m_dot_w[225] * h_w[225])) - ((m_dot_a[250] * h_a[250]) + (m_dot_w[250] * h_w[250])) #//Inline AC Total Heat Load 
Q_dot_2Sen = m_dot_a[225] * C_p_a[237] * (T_[225] - T_[250])  #//Inline AC Sensible Heat Load 
qlattent (Q_dot_2, Q_dot_2Sen) #: Q_dot_2lat)  #//Inline AC Lattent Heat Load   
Q_AIR = Q_dot_1Sen+Q_dot_2Sen+Q_dot_10 
Q_oil = Q_sh - Q_AIR - (Q_sh*0.03) - Q_dot_1_InAir 

print("Q_dot_1 :", Q_dot_1)
print("Q_dot_2 :", Q_dot_2)
print("Q_oil :", Q_oil)