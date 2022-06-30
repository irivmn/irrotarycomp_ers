from ERS.fin_geometry import *
from ERS.CorelationFunction import *
from ERS.overallUA import *
from ERS.ntuMethod import *

Fluid_N={"Oil"   : [514,705,700,502]
        ,"Inter" : [512,137,137,512]
        ,"After" : [513,237,237,513]}

def Platebar_NTU_standalone(T_H_IN,T_H_OUT,T_C_IN,T_C_OUT,m_dot_H,m_dot_C,Rho_a,C_p_a,Mu_a,k_avg,Pr_avg,Fin_Name_Cold,Fin_Name_Hot,Fluid,Q,Q_Sen,N_pass_cs,N_pass_hs,L_core,T_core,n_coldrows,H_cs, lambda_2_cs, t_cs, H_hs, lambda_2_hs, t_hs,OL_hs,OL_cs):

    #//Fin geometry calculations   
    (W_core_cs,L_core_cs,W_cs,Hi_cs,n_cs,Dh_cs,Af_cs,At_cs,Ap_cs,As_cs,FA_cs,Beta_HX_cs,Alpha_HX_cs,A_facecs,H_cs,lambda_2_cs,t_cs,OL_cs,weight_cs) = geometry (L_core, T_core, H_cs, lambda_2_cs, t_cs, n_coldrows,OL_cs, Fin_Name_Cold, "cold", "wavy") 
    (W_core_hs,L_core_hs,W_hs,Hi_hs,n_hs,Dh_hs,Af_hs,At_hs,Ap_hs,As_hs,FA_hs,Beta_HX_hs,Alpha_HX_hs,A_facehs,H_hs,lambda_2_hs,t_hs,OL_hs,weight_hs) = geometry (L_core, T_core, H_hs, lambda_2_hs, t_hs, n_coldrows,OL_hs, Fin_Name_Hot, "hot", "offset") 
    W_core_IC=corewidth (H_cs, n_cs,H_hs, n_hs)
    weight_core=Platebar_Weight(weight_hs,weight_cs,H_cs,n_cs,H_hs,n_hs,L_core,T_core)

    #//Cold Side Heat Transfer Calculation  
    g_cs = (m_dot_C*N_pass_cs)/(n_cs*Af_cs*W_core_cs) #//Mass Velocity Cold side of IC 
    Re_cs = (g_cs*Dh_cs)/Mu_a[Fluid_N[Fluid][0]]  #//Renolds Number Cold Side IC  
    
    Corelation_name="dongjunqi"
    (Nu_j,f_cs,Factor)=choose_Corelation(Corelation_name,Fin_Name_Cold,W_cs, Hi_cs, t_cs, OL_cs,Re_cs)
    if(Factor=="N"):
        alpha_cs = (Nu_j*k_avg)/Dh_cs  #//Cold side Nussult Coefficient of heat transfer
    else:
        St_hs = Nu_j/pow(Pr_avg,(2/3))  #//Hot Side Stanton Number 
        alpha_cs = St_hs*g_cs*C_p_a[Fluid_N[Fluid][1]]*10**3 #//Hot side Coefficient of heat transfer 

    #//Hot SIde Heat Transfer Calculation  
    g_hs = (m_dot_H*N_pass_hs)/(n_hs*Af_hs*W_core_hs) #//Mass Velocity Hot side of IC 
    Re_hs = (g_hs*Dh_hs)/Mu_a[Fluid_N[Fluid][1]]  #//Renolds Number Hot IC  

    Corelation_name="bergles"
    print(Corelation_name,Fin_Name_Hot,W_hs, Hi_hs, t_hs, OL_hs,Re_hs,"------------------------")
    (Nu_j,f_hs,Factor)=choose_Corelation(Corelation_name,Fin_Name_Hot,W_hs, Hi_hs, t_hs, OL_hs,Re_hs)
    if(Factor=="N"):
        alpha_hs = (Nu_j*k_avg)/Dh_cs  #//Cold side Nussult Coefficient of heat transfer
    else:
        St_hs = Nu_j/pow(Pr_avg,(2/3))  #//Hot Side Stanton Number 
        alpha_hs = St_hs*g_hs*C_p_a[Fluid_N[Fluid][1]] #//Hot side Coefficient of heat transfer 
    
    #//Overall HTC  
    (UA_hs,UA_cs,UA)=overallucoeff (alpha_cs, t_cs,H_cs, As_cs,At_cs,alpha_hs,t_hs,H_hs,As_hs,At_hs,FA_cs,FA_hs)  #//Pressure Drop  
    DELTAP_hs_Core = (4*f_hs*g_hs**2*N_pass_hs*L_core_hs)/(2*Dh_hs*Rho_a[Fluid_N[Fluid][2]]) #// Hot Core Pressure Drop 
    DELTAP_hs = 1.3*DELTAP_hs_Core   #// Hot Inter Cooler Pressure Drop 
    DELTAP_cs = (4*f_cs*g_cs**2*N_pass_cs*L_core_cs)/(2*Dh_cs*Rho_a[Fluid_N[Fluid][3]]) #// Cold Core Pressure Drop 

    #//NTU Effectiveness Method Calcualtion 
    (epsilon,C_dot_min,C_dot_H,C_dot_C)=ntumethod (Q,Q_Sen,T_H_IN,T_H_OUT,m_dot_C, C_p_a[Fluid_N[Fluid][0]], m_dot_H, C_p_a[Fluid_N[Fluid][1]],UA,"PlateBar")
    Q_dot_NTU=C_dot_min*(T_H_IN-T_C_IN)*epsilon   #//Actual heat transfer rate 
    T_150_NTU=round(T_H_IN-Q_dot_NTU/C_dot_H,0)   #//Hot-side fluid exit temperature 
    T_525_NTU=round(T_C_IN+Q_dot_NTU/C_dot_C,0)   #//Cold-side fluid exit temperature 
    Margin_NTU = ((Q_dot_NTU/Q)-1)*100 #// Margin NTU 

    DELTAT_cs = T_C_OUT - T_C_IN
    #print(weight_core,"-------------------------------------------------------------------------------")
    return (T_150_NTU,T_525_NTU,Margin_NTU,DELTAT_cs,UA,Q_dot_NTU,C_dot_H,DELTAP_hs,weight_core,DELTAP_cs)