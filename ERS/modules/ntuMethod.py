from convertion import convert
from cmath import exp

def ntusensiblemethod (m_dot_c, C_p_c_avg, m_dot_h, C_p_h_avg,UA,HX): #: epsilon,C_dot_min,C_dot_H,C_dot_C)    
    C_dot_H = m_dot_h*C_p_h_avg  
    C_dot_C = m_dot_c*C_p_c_avg
    # print("m_dot_h",m_dot_h,C_p_h_avg,"m_dot_c",m_dot_c,C_p_c_avg) 
    C_dot_min=min(C_dot_H,C_dot_C)   
    #//Minimum capacitance rate  
    C_dot_max=max(C_dot_H,C_dot_C) 
    #//Maximum capacitance rate 
    CR=C_dot_min/C_dot_max 
    # print("C_dot_H",C_dot_H,"C_dot_C",C_dot_C,"CR",CR)
    NTU =(UA)/C_dot_min   
    if HX=="PlateBar" or HX==None:
        epsilon=(1-exp((pow(NTU,0.22)/CR)*(exp(-(CR*pow(NTU,0.78)))-1))).real 
    elif(HX=="TubefinC"):
        epsilon=(1-(exp(-(1-exp(-CR*NTU))/CR))).real
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
    NTU_lat=(UA)/C_dot_min_lat  
    epsilon_lat=(1-exp((pow(NTU_lat,0.22)/CR)*(exp(-(CR*pow(NTU_lat,0.78)))-1))).real                
    #epsilon_lat=HX('crossflow_both_unmixed', NTU_lat, C_dot_H_lat, C_dot_C_lat, 'epsilon')   ###############################
    return (epsilon_lat,C_dot_min_lat,C_dot_H_lat,C_dot_C_lat)
    #// Sensible Effectiveness-NTU_AC solution 

def ntumethod (Q,Q_Sen,T_HIN,T_HOUT,m_dot_c, C_p_c_avg,m_dot_h, C_p_h_avg,UA,HX): #: epsilon_lat,C_dot_min_lat,C_dot_H_lat,C_dot_C_lat)  
    if Q/Q_Sen > 0.1 :  
        C_dot_H = Q/(T_HIN-T_HOUT)  
    else:
        C_dot_H = m_dot_h*C_p_h_avg
    C_dot_C = m_dot_c*C_p_c_avg
    # print("m_dot_h",m_dot_h,C_p_h_avg,"m_dot_c",m_dot_c,C_p_c_avg) 
    C_dot_min=min(C_dot_H,C_dot_C)      #//Minimum capacitance rate  
    C_dot_max=max(C_dot_H,C_dot_C)     #//Maximum capacitance rate 
    CR=C_dot_min/C_dot_max 
    # print("C_dot_H",C_dot_H,"C_dot_C",C_dot_C,"CR",CR)
    NTU =(UA)/C_dot_min   
    if HX=="PlateBar" or HX==None:
        epsilon=(1-exp((pow(NTU,0.22)/CR)*(exp(-(CR*pow(NTU,0.78)))-1))).real 
    elif(HX=="TubefinC"):
        epsilon=(1-(exp(-(1-exp(-CR*NTU))/CR))).real
    #epsilon=HX('crossflow_both_unmixed', NTU, C_dot_C, C_dot_H, 'epsilon')   ##################################
    return (epsilon,C_dot_min,C_dot_H,C_dot_C)
    #//Access effectiveness-NTU_OC solution   
