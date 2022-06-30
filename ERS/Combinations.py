def Combinations(T_H_In,T_C_In,T_H_out,T_C_out,M_dot_H,M_dot_C,Q):
    if T_H_In==None and T_C_In==None:
        print("ERROR: T_H_In and T_C_In is Mandatory")
        return False   
    elif M_dot_H == None and M_dot_C == None and Q==None:
        print("ERROR: You have to give any one of this(m_dot_H,m_dot_C,Q).")
        return False
    elif Q!=None:
        if M_dot_H !=None:
            #print("Q & M_dot_H Given")
            if (M_dot_C==None and T_H_out==None and T_C_out!=None ):
                return True
            elif (M_dot_C==None and T_H_out==None and T_C_out==None ):
                return True
            elif (M_dot_C!=None and T_H_out==None and T_C_out==None ):
                return True
            else:
                print("ERROR: Too many Inputs among (M_dot_C,T_H_out,T_C_out) ")
                if M_dot_C!=None:
                    print("ERROR: T_H_out & T_C_out has be None ")
                else:
                    print("ERROR: T_H_out & T_C_out has be None or T_H_out only to be none")            
                return False
        elif M_dot_C !=None:
            #print("Q & M_dot_C Given")
            if (M_dot_H==None and T_H_out==None and T_C_out==None ):
                return True
            elif (M_dot_H==None and T_H_out!=None and T_C_out==None ):
                return True
            else:
                print("ERROR : Too many Inputs among ( M_dot_H,T_H_out,T_C_out)")
                if T_H_out!=None:
                    print("ERROR: M_dot_H & T_C_out has be None ")
                else:
                    print("ERROR: M_dot_H & T_C_out has be None ")
                return False
        elif M_dot_H ==None and  M_dot_C ==None:
            return True
            #print("Only Q Given")
        else:
            print("ERROR : No Proper Inputs are given ")
            return False
    elif Q==None:
        if M_dot_H!=None:
            #print("Only M_dot_H Given")
            if (M_dot_C==None and T_H_out==None and T_C_out!=None ):
                return True
            elif (M_dot_C==None and T_H_out!=None and T_C_out!=None ):
                return True
            elif (M_dot_C==None and T_H_out!=None and T_C_out==None ):
                return True
            elif (M_dot_C!=None and T_H_out==None and T_C_out==None ):
                return True
            elif (M_dot_C!=None and T_H_out!=None and T_C_out==None ):
                return True
            elif (M_dot_C!=None and T_H_out==None and T_C_out!=None ):
                return True
            else:
                print("ERROR : Too many Inputs among (Q,M_dot_H,T_H_out,T_C_out)")
                if M_dot_C==None:
                    print("ERROR: Either T_H_out or T_C_out or both has be Given ")
                else:
                    print("ERROR: Either T_H_out or T_C_out or both has be None ")
                return False
    else:
        print("ERROR : No Proper Inputs are given")
        return False