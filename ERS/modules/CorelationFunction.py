from cmath import log,exp

#Corelation Function : After fuld props and HX props are established    
def dongjunqi (Re_cs, F_p=4, F_h=9.7, L_d=145, L=20, A2=2.4):# : Nu,f)    
    c1 = F_p/F_h  
    c2 = A2/L  
    c3 = L_d/L  
    c4 = A2/F_p  
    Nu= 0.0864*pow(Re_cs,0.914)*pow(c1,(-0.301))*pow(c2,(0.7875))*pow(c3,(-0.254))*pow(c4,(-0.226))  
    f = 15.46*pow(Re_cs,(-0.416))*pow(c1,(-0.138))*pow(c2,(1.098))*pow(c3,(-0.45))*pow(c4,(-0.506))
    return (Nu,f,"N")

def bergles (W_hs, Hi_hs, t_hs, OL_hs, Re_hs): # : j_hs,f_hs)    
    alpha_ratio = W_hs/Hi_hs  
    delta_ratio = t_hs/OL_hs  
    lambda_ratio = t_hs/W_hs    
    j_hs = 0.6522*pow(Re_hs,(-0.5403))*pow(alpha_ratio,(0.1541))*pow(delta_ratio,(0.1499))*pow(lambda_ratio,(0.0678)) * pow((1 + 5.269*pow(10,(-5)) *pow(Re_hs,(1.340))*pow(alpha_ratio,(0.504))*pow(delta_ratio,(0.1499))*pow(lambda_ratio,(1.055))),(0.1))   
    f_hs = 9.6243*pow(Re_hs,(-0.7422))*pow(alpha_ratio,(-0.1856))*pow(delta_ratio,(0.3053))*pow(lambda_ratio,(0.2659)) * pow((1 + 7.669*pow(10,(-8)) *pow(Re_hs,(4.429))*pow(alpha_ratio,(0.920))*pow(delta_ratio,(3.767))*pow(lambda_ratio,(0.236))),(0.1))
    return (j_hs,f_hs,"j")
    #f factor Raj M. Manglik & Arthur E. Bergles

def Corelation_eqn(Fin_name,Re):
    if Fin_name=='Hongsheng_offset_3':
        j_hs_OC = (0.012113)+(0.11172)*(exp((-0.10265)*pow(Re,(0.606828))).real) #// Wuxi Relation  'Hongsheng_offset_3'
        f_hs_OC =(-0.22934)+(0.264449)*exp((6.54507)*pow(Re,(-0.51143)))  #// Wuxi Relation 'Hongsheng_offset_3'

'''def PlainTube(Relrough,D_in,L_tube,Re,Pr_a):
    f_H=(pow((-2*log10(2*Relrough/7.54-5.02*log10(2*Relrough/7.54+13/Re)/Re)),(-2))).real 
    f_H_avg = f_H*pow(1+(D_in/L_tube),0.7)  
    Nussult_H = ((f_H_avg/8)*(Re-1000)*Pr_a[237])/(1+12.7*(pow(Pr_a[237],(2/3))-1)*pow((f_H_avg/8),(1/2)))'''

def choose_Corelation(Corelation_name,Fin_name,W, Hi, t, OL,Re):
    if Corelation_name==None:
        return Corelation_eqn(Fin_name,Re)
    elif  Corelation_name=='bergles':
        return bergles(W, Hi, t, OL,Re)
    elif Corelation_name=='dongjunqi':
        return dongjunqi(Re)


    

