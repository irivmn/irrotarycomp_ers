from CoolProp.HumidAirProp import HAPropsSI
from ERS.convertion import convert
from ERS.AmbientAirProps import *
from ERS.compressed_air_Prop import *
from ERS.PlateBar_NTU_standalone import *
from ERS.Combinations import *
from ERS.M_Dot_Calculation import *

def demo123(T_amb_demo,RH_amb_demo,Altitude_demo,HCA):
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
    Fin_Name_Cold=None
    Fin_Name_Hot=None
    H_cs,lambda_2_cs,t_cs,OL_cs=None,None,None,None
    H_hs,lambda_2_hs,t_hs,OL_hs=None,None,None,None
    T_150_NTU=None

    Fluid_N={"Oil"   : [502,527,514,705,700,502,700,710]
            ,"Inter" : [500,525,512,137,137,512,125,125]
            ,"After" : [501,526,513,237,237,513,225,225]}
            
    #------------------------------------------Start of INPUTS ----------------------------------"  
    # Inputs From Airend Data Sheet

    T_amb = float(T_amb_demo)+273.15 #[C]  Ambient                   
    RH_amb = float(RH_amb_demo) #RH   
    Altitude = float(Altitude_demo) #[m]  //Altitide of Package    
    P_amb=ambientpressure(Altitude); # print("P_amb : ", P_amb) #(Altitude : P_amb)  #//Ambient Pressure calculation
    omega_amb = HAPropsSI('W','T',T_amb,'P',P_amb,'R',RH_amb); # print("omega_amb : ",omega_amb) #SPECFIC HUMIDITY OF AMBIENT AIR
    h_amb = HAPropsSI('H','T',T_amb,'P',P_amb,'W',omega_amb); # print("h_amb : ",h_amb)      #AMBIENT ENTHALPHY 
    P_w_amb = HAPropsSI('P_w','T',T_amb,'P',P_amb,'W',omega_amb); # print("P_w_amb : ",P_w_amb)
    v_amb = HAPropsSI('Vha','T',T_amb,'P',P_amb,'W',omega_amb); # print("v_amb : ",v_amb)


    # //Inputs of Heat exchanger  
    L_core = 1485 *convert('mm','m') # [mm]*convert(mm,m) #//Length of core 
    T_core = 140 *convert('mm','m') # [mm]*convert(mm,m) #//Thickness of core
    #HX = "platebar"
    Fin_Name_Cold = "Hongsheng_wavy_9.5"
    N_pass_cs = 1  #//Number of Cold Passes 
    n_coldrows = 17  #//Number of cold rows
    N_pass_hs = 1  #//Number of Hot Passes    
    Fin_Name_Hot='Hongsheng_offset_6.5'
    N_pass_hs = 1  #//Number of Hot Passes

    FAD = HCA.FAD #[m^3/hr]  FAD   
    P_[125]= HCA.P_input*pow(10,5) #[bar] Cooler Inlet Pressure 
    DELTAP_150 =  0  #Cooler Pressure drop
    CTD_150 = None
    Delta_preheat = 4 #[C]  #Pre Heat temperature 

    T_H_In=HCA.T_H_In +273.15                       # to assign Input values of temperatures
    T_C_In=315                               # to assign Input values of temperatures
    T_H_out=None                               # to assign Input values of temperatures
    T_C_out= None                              # to assign Input values of temperatures
    m_dot_H= None                              # to assign input hot mass flow
    m_dot_C=2.6                          # to assign input cold mass flow
    Q=HCA.Q_input
    Fluid_Type="compressed_air"
    if (Delta_preheat != None and T_C_In!= None ):
        print ("Both Delta_preheat and T_C_In are given remove one")
    elif (Delta_preheat != None):
        T_C_In = T_amb + Delta_preheat
    else:
        T_C_In = T_C_In

    if (CTD_150 != None and T_H_out!= None ):
        print ("Both CTD_150 or approach and T_H_out are given remove one")
    elif (CTD_150 != None):
        T_H_out = T_amb + CTD_150
    else:
        T_H_out = T_H_out

    if (FAD != None and m_dot_H !=None ):
        print ("Both FAD and M_dot_h are given remove one")
    elif(FAD != None):
        m_dot_H = (FAD/3600) / v_amb
    else:
        m_dot_H = m_dot_H

    #print("Assigned values,T_H_In :",T_H_In,"T_C_In :",T_C_In,"T_H_out :",T_H_out,"T_C_out :",T_C_out,"m_dot_H :",m_dot_H,"m_dot_C :",m_dot_C,"Q",Q)
    # to check valid inputs are provided
    if Combinations(T_H_In,T_C_In,T_H_out,T_C_out,m_dot_H,m_dot_C,Q):
        pass
    else:
        exit()

    # Start of cooler program
    P_[500] = P_amb  #Cooling air side Pressure  
    omega_[500] = omega_amb  # Cooling air side Humidity 

    #Package Inlet  
    T_[100] = T_amb  # Compressed air Inlet
    P_[100] = P_amb
    omega_[100] = omega_amb
    h_a[100] = HAPropsSI('H','T',T_[100],'P',P_[100],'W',omega_[100])

    # the random values of temperature is assigned to compute iteration
    T_[125],T_[500] = T_H_In,T_C_In
    T_[150],T_[525] = T_H_out,T_C_out
    m_dot_a[100],m_dot_a[500]=m_dot_H,m_dot_C
    T_H_max=T_[125]                             
    T_H_min=T_C_In+2
    T_C_max=T_[125]-2
    T_C_min=T_C_In

    M_H_const,M_C_const=None,None       # to have M_dot constant as feed by user

    if(m_dot_H!=None):
        M_H_const=m_dot_H
    if(m_dot_C!=None):
        M_C_const=m_dot_C

    if (Q == None and m_dot_C != None) :
        # Runs for first iteration to find Q, before Q from NTU is looped
        if(T_[525]!=None):
            (T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a,Q)=M_DOT_C(T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a)

        else:
            T_[525]=(T_[125]+T_[500])/2
            (T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a,Q)=M_DOT_C(T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a)

        #print ("Q_first_Itr_from_M_C :",Q)
    count = 0

    Q_H = Q_C = Q

    while True:
        count +=1
        P_[150] = P_[125] - DELTAP_150  # Cooler OUT Cooler Pressure
        if(m_dot_H == None and Q_H!=None):
            # Runs to find m_dot_H for given Q with or with out T_H_out
            if(T_[150]==None):
                T_[150]=(T_[125]+T_[500])/2     
            (T_,P_,omega_,Q_dot,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a)=M_DOT_H_None(T_,P_,omega_,Q_H,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a,P_w_amb,Fluid_Type)
            m_dot_H=m_dot_a[100]
            #print("m_dot_H first itr" ,m_dot_a[100])

        elif((m_dot_H!=None and Q_H!=None) or (m_dot_H!=None and Q_H==None)):        
            if T_[150]==None:
                T_[150]=(T_[125]+T_[500])/2
            # iteration based on T_H_out_NTU
            if M_H_const==None:             # User has not provided M_dot_H its computed via other inputs or Runs based on T_H_NTU
                (T_,P_,omega_,Q_dot,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a)=M_DOT_H_None(T_,P_,omega_,Q_H,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a,P_w_amb,Fluid_Type)
                #print("m_dot_H second or nth itr :",m_dot_a[100],"Q_dot",Q_dot,"Count",count)   
            else:
                (T_,P_,omega_,Q_dot,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a)=M_DOT_H(T_,P_,omega_,Q_H,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a,P_w_amb,Fluid_Type)
                #print("Q second or nth itr :",Q_dot,"Count",count)
            Q_H=Q_dot

        Q_Sen_H = m_dot_a[125] * C_p_a[137] * (T_[125] - T_[150]) 

        #//Cold Side Property                                                   // Iterative loop to consider the average properties
        
        if m_dot_C==None and Q_C!=None:
            if T_[525]==None:
                T_[525]=(T_[125]+T_[500])/2
            (T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a,Q_C)=M_DOT_C(T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a)
            m_dot_a[500]=Q_C/((T_[525]-T_[500])*C_p_a[512])
            m_dot_C=m_dot_a[500]
        elif m_dot_C!=None and Q_C!=None:
            if T_[525] == None:
                T_[525]=(T_[125]+T_[500])/2
            (T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a,Q_C)=M_DOT_C(T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a)
            if M_C_const==None:
                m_dot_a[500]=Q_C/((T_[525]-T_[500])*C_p_a[512])
        #print("T_C_OUT Cold Side Prop",T_[525])

            
        #" ------------------------------------START OF INLINE INTERCOOLER CALCULATION---------------------------------------------------"  

        (T_150_NTU,T_525_NTU,Margin_NTU_IC,DELTAT_cs_IC,UA_IC,Q_dot_NTU,C_dot_H,DELTAP_150,weight_core,DELTAP_cs) = Platebar_NTU_standalone(T_[125],T_[150],T_[500],T_[525],m_dot_a[100],m_dot_a[500],Rho_a,C_p_a,Mu_a,k_a[512],Pr_a[137],Fin_Name_Cold,Fin_Name_Hot,"Inter",Q_H,Q_Sen_H,N_pass_cs,N_pass_hs,L_core,T_core,n_coldrows,H_cs, lambda_2_cs, t_cs, H_hs, lambda_2_hs, t_hs,OL_hs,OL_cs)
        
        if(abs(Q_H-Q_dot_NTU)>1 or abs(Q_C-Q_dot_NTU)>1 or abs(Q_C-Q_H)>1):
        
            if(Q_H<Q_dot_NTU):
                T_H_max=T_[150]
            else:
                T_H_min=T_[150]
                
            if(Q_C<Q_dot_NTU):
                T_C_min=T_[525]
            else:
                T_C_max=T_[525]
            T_[150]=(T_H_min+T_H_max)/2
            T_[525]=(T_C_min+T_C_max)/2
        else:break
        if(abs(T_[150]-T_C_In)<=2 or abs(T_C_min-T_C_max)<0.1 or abs(T_H_min-T_H_max)<0.1):
            break     #ERRROR : convolution issue
        #print(T_C_min,T_C_max,"TTTTTTTTTTTTTTTTTTTTTT")
        #print('T_[125]',T_[125],"T_[150]",T_[150],'T_150_NTU',T_150_NTU,"Q",Q_dot,'Q_dot_NTU',Q_dot_NTU,'T_C_IN',T_[500],"T_C_OUT",T_[525],'T_525_NTU',T_525_NTU,"P_[150]",P_[150],"Count",count,Q_C,Q_H)
    #end main while loop

    #print('T_[125]',T_[125],"T_[150]",T_[150],'T_150_NTU',T_150_NTU,"Q",Q_dot,'Q_dot_NTU',Q_dot_NTU,'T_C_IN',T_[500],"T_C_OUT",T_[525],'T_525_NTU',T_525_NTU,"P_[150]",P_[150],"Count",count)

    #print(DELTAP_cs)

    return (round(Q_dot,2),round(weight_core,2))
