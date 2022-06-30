from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from ERS.demo1 import *
from ERS.ERS_Trial1 import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import csv,json
#from django.core.mail import send_mail
#from django.conf import settings
#from CoolerProps.settings import EMAIL_HOST_USER



#First function which will render the login page once the application opened.
def home(request):
    logout(request)
    return render(request,"login.html")

#Loging out from the application and redirecting to the login page.
def logout_out(request):
    print("logged out..")
    logout(request)
    return redirect("/")

#Login function by verifing the user-id and password.
def login_in(request):
    logout(request)
    if request.method=="POST":
        username=request.POST['username']
        psw=request.POST['psw']
        user=authenticate(username=username,password=psw)
        print(user)
        if user is not None: 
            check=Registration_Approval.objects.filter(UserID = username,Aprove=0)
            if len(check)!=0: #Checking whether the user is approved or not.
                login(request,user)
                return redirect(Main_home)
            else:
                return render(request,"login.html",{'error':"Wait for Admin approval."})
        else:
            return render(request,"login.html",{'error':"Incorrect userId or password"})

        '''user=users.objects.filter(userID=username,password=psw)
        print(len(user))
        if len(user)!=0:
            check=Registration_Approval.objects.filter(UserID = username,Aprove=0)
            if len(check)!=0:
                return Main_home(request)
            else:
                return render(request,"login.html",{'error':"Wait for Admin approval."})
        else:
            return render(request,"login.html",{'error':"Incorrect userId or password"})'''
    else:
        return redirect("/")

#rendering the main home page.
def Main_home(request):  
    return render(request,"Home.html")

#Registration function.
def register(request):   
    if request.method == 'POST':
        username = request.POST['userid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        #phone = request.POST['phone']
        #dob = request.POST['dob']
        psw1 = request.POST['psw1']
        psw2 = request.POST['psw2']

        '''user1=users.objects.filter(userID=username)
        user2=users.objects.filter(Email=email)
        print(user1.count())
        print(user2.count())'''
        if User.objects.filter(username=username).exists(): #UserID verification for uniqueness.
            return render(request,"register.html",{"error":"Username is already taken","fname":fname,"lname":lname,"email":email,"userid":username})
        elif User.objects.filter(email=email).exists(): #Email-ID verification for uniqueness.
            return render(request,"register.html",{"error":"Mail-id is already taken","fname":fname,"lname":lname,"email":email,"userid":username})
        elif psw1!=psw2: #Password matching or not verfication.
            return render(request,"register.html",{"error":"Password mismatch","fname":fname,"lname":lname,"email":email,"userid":username})
        else:
            print("Account registered successfully..")
            #Account creating and saving in the database.
            user= User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=psw1)
            user.save()
            #Updating for admin approval.
            Reg_App=Registration_Approval(UserID=username,Email=email,Aprove=1)
            Reg_App.save()
            '''######################### mail system ####################################
            sub='welcome to SNS'
            message= f"Your registration is successful.."
            email_from= settings.EMAIL_HOST_USER
            to= [email]
            send_mail( sub,message,email_from,to)'''
            return redirect("/",{"error":"Wait for admin approval.."})
    else:
        return render(request,"register.html")

#Plate and Bar Processing Function.
def demo1(request):
    if request.method=="POST":
        Fluid=request.POST['Fluid']
        T_amb=request.POST['T_amb']
        RH_amb=request.POST['RH_amb']
        Altitude=request.POST['Altitude']
        FAD=request.POST['FAD']
        T_H_In=request.POST['T_H_In']
        P=request.POST['P']
        Q=request.POST['Q']
        Delta_preheat=request.POST['Delta_preheat']
        M_dot_C=request.POST['M_dot_C']
        L_core=request.POST['L_core']
        T_core=request.POST['T_core']
        N_pass_cs=request.POST['N_pass_cs']
        N_pass_hs=request.POST['N_pass_hs']
        n_coldrows=request.POST['n_coldrows']
        Fin_Name_Cold=request.POST['Fin_Name_Cold']
        Fin_Name_Hot=request.POST['Fin_Name_Hot']
        print(T_amb,RH_amb,Altitude,FAD,T_H_In,P,Q,Delta_preheat,M_dot_C,L_core,T_core,N_pass_cs,N_pass_hs,n_coldrows,Fin_Name_Cold,Fin_Name_Hot)
        #calling the Standalonr plate and bar module.
        (Q,Weight,T_H,T_C,D_C,D_H)=demo123(Fluid,T_amb,RH_amb,Altitude,FAD,T_H_In,P,Q,Delta_preheat,M_dot_C,L_core,T_core,N_pass_cs,N_pass_hs,n_coldrows,Fin_Name_Cold,Fin_Name_Hot)
        #returning output the webpage
        return HttpResponse(json.dumps({"Q":Q,"Weight":Weight,"T_H":T_H,"T_C":T_C,"D_H":D_H,"D_C":D_C}),content_type ="application/json")
    else:
        fin_details=Fin_parameters.objects.all()
        return render(request,"demo2.html",{"fin_details":fin_details})
        
#Admin main page showing all the tables in the database.
def admin_main(request):
    Reg_app=Registration_Approval.objects.filter(Aprove=1)
    Ret_app=Reset_password_Approval.objects.filter(Aprove=1)
    user_d=User.objects.all()
    HCA_d=HCA_details.objects.all()
    CD26_a_d=CD26_airend_data.objects.all()
    CD26_a_d_r=CD26_airend_data_rated.objects.all()
    #return render(request,"admin_main.html",{'Reg_app':Reg_app,'Ret_app':Ret_app})
    return render(request,"Admin_All.html",{'Reg_app':Reg_app,'Ret_app':Ret_app,'user_d':user_d,'HCA_d':HCA_d,'CD26_a_d':CD26_a_d,'CD26_a_d_r':CD26_a_d_r})

#To approve or reject the new user registration request from admin page.
def Register_request(request):
    if request.POST['approve']=="Approve":  # Approving function.
        userid=request.POST['userid']
        print(userid)
        X=Registration_Approval.objects.filter(UserID = userid).update(Aprove=0)
        print("Approved")
    elif request.POST['approve']=="Reject": # Rejecting function.
        X=Registration_Approval.objects.filter(UserID = userid).update(Aprove=-1)
        print("Rejected")
    return redirect(admin_main)

#To approve or reject the reset password request from admin page.
def Reset_pwd_request(request):
    if request.POST['approve']=="Approve":  # Approving function.
        userid=request.POST['userid']
        print(userid)
        X=Reset_password_Approval.objects.filter(UserID = userid).update(Aprove=0)
        Y=Reset_password_Approval.objects.filter(UserID = userid)
        for i in Y:
            psw=i.Password
        Z=User.objects.get(username = userid)    
        Z.set_password(psw)                          #to hash the raw password
        Z.save()                                     #to update in the database
        print("Approved")
    elif request.POST['approve']=="Reject":          # Rejecting function.
        X=Reset_password_Approval.objects.filter(UserID = userid).update(Aprove=-1)
        print("Rejected")
    return redirect(admin_main)

#Upload data to the database to CD26_airend_data_rated table
def upload_data(request):  
    path="C:\\Users\\pxc2007.ext\\Desktop\\CD26 Airend Data Rated pressure.CSV"
    list=[]
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row)
    for i in range(len(list)):
        add= CD26_airend_data_rated(Model_id=list[i][0],rated_P=float(list[i][1]))
        ''',p_S1=float(list[i][2]),p_S2=float(list[i][3]),FAD=float(list[i][4]),
            Q_sh=float(list[i][5]),Pr_ratio_stg1=float(list[i][6]),Pr_ratio_stg2=float(list[i][7]),n_stg1=float(list[i][8]),n_stg2=float(list[i][9]))'''
        add.save()
        print(i)
    list=Reset_password_Approval.objects.filter(Aprove=1)
    for i in list:
        print(i.UserID)   
        print(i.Email )
        print(i.Aprove)
    return render(request,"admin_main.html",{'data':list})

#Same as below send_data function.
'''def calculate(request):
    if(request.method=="POST"):
        T_amb=request.POST['T_amb']
        RH_amb=request.POST['RH_amb']
        Altitude=request.POST['Altitude']
        model_id=request.POST['Model_id']
        P=request.POST['P']
        Pr_type=request.POST['Pressure']
        TW_in=request.POST['T_in']
        TW_out=request.POST['T_out']
        CTD_ac=request.POST['CTD_ac']
        CTD_ic=request.POST['CTD_ic']
        input_=[T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic]
        RP=CD26_airend_data_rated.objects.filter(Model_id=model_id)
        for i in RP:
            data=i
        Rated_P=data.rated_P
        MD=CD26_airend_data.objects.filter(Model_id=model_id,P=Rated_P)
        for i in MD:
            data=i
        M_data=data
        print("-------------------------------",M_data.P)
        (WF,ReH,DT)=ERS_TRIAL(float(T_amb),float(RH_amb),float(Altitude),model_id,float(P),Pr_type,float(TW_in),float(TW_out),float(CTD_ac),float(CTD_ic),M_data)
        print(T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic)
        
        list=CD26_airend_data_rated.objects.all()
        return render(request,"Home.html",{"model_id":list,"WF":WF,"ReH":ReH,"DT":DT})
    else:
        WF,ReH,DT=10,15,20
        list=CD26_airend_data_rated.objects.all()
        return render(request,"Home.html",{"model_id":list,"WF":WF,"ReH":ReH,"DT":DT})'''

#This function is used to send the output from the ERS_TRIAL module to the main page.
def send_data(request):
    if request.method=="POST":
        TYPE=request.POST['TYPE']
        T_amb=request.POST['T_amb']
        T_amb_unit=request.POST['T_amb_unit']
        RH_amb=request.POST['RH_amb']
        Altitude=request.POST['Altitude']
        Altitude_unit=request.POST['Altitude_unit']
        model_id=request.POST['Model_id']
        P=request.POST['P']
        Pr_type=request.POST['Pr_type']
        TW_in=request.POST['T_in']
        TW_in_unit=request.POST['T_in_unit']
        TW_out=request.POST['T_out']
        TW_out_unit=request.POST['T_out_unit']
        CTD_ac=request.POST['CTD_ac']
        CTD_ic=request.POST['CTD_ic']
        print(T_amb,T_amb_unit,RH_amb,Altitude,Altitude_unit,model_id,P,Pr_type,TW_in,TW_in_unit,TW_out,TW_out_unit,CTD_ac,CTD_ic)
        #unit conversion
        if(T_amb_unit=="K"):
            T_amb=float(T_amb)-273.15;
        elif(T_amb_unit=="F"):
            T_amb=(float(T_amb) - 32)*(5/9);

        if Altitude_unit=="Feet":
            Altitude=(float(Altitude) /3.281)

        if(TW_in_unit=="K"):
            TW_in=float(TW_in)-273.15;
        elif(TW_in_unit=="F"):
            TW_in=(float(TW_in) - 32)*(5/9);

        if(TW_out_unit=="K"):
            TW_out=float(TW_out)-273.15;
        elif(TW_out_unit=="F"):
            TW_out=(float(TW_out) - 32)*(5/9);

        #collecting Airend data from database.
        if Pr_type=="Rated_Pressure":
            RP=CD26_airend_data_rated.objects.filter(Model_id=model_id)
            for i in RP:
                data=i
            Rated_P=data.rated_P
            MD=CD26_airend_data.objects.filter(Model_id=model_id,P=Rated_P)
            for i in MD:
                data=i
            M_data=data
        else:
            M_data=CD26_airend_data.objects.filter(Model_id=model_id)
        #calling the ERS_TRIAL function 
        (Q_dot_1,Q_dot_2,Q_oil)=ERS_TRIAL(TYPE,float(T_amb),float(RH_amb),float(Altitude),model_id,float(P),Pr_type,float(TW_in),float(TW_out),float(CTD_ac),float(CTD_ic),M_data)
        print(TYPE,T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic)
        print(model_id,"-------------------------------------------------------------------")
        return HttpResponse(json.dumps({ "Q_dot_1":Q_dot_1, "Q_dot_2":Q_dot_2, "Q_oil":Q_oil}),content_type ="application/json")

#To open the parallel configuration of ERS-tool
def home_parallel(request):
    list=CD26_airend_data_rated.objects.all()
    data={}
    data1={}
    for i in list:
        data[i.Model_id]=i.Max
        data1[i.Model_id]=i.T_W_out
    #print(data)
    max_v=json.dumps(data)
    max_T=json.dumps(data1)
    return render(request,"Home_parallel.html",{"model_id":list,"max_v":max_v,"max_T":max_T})

#To open the series configuration of ERS-tool
def home_series(request):
    list=CD26_airend_data_rated.objects.all()
    data={}
    data1={}
    for i in list:
        data[i.Model_id]=i.Max
        data1[i.Model_id]=i.T_W_out
    #print(data)
    max_v=json.dumps(data)
    max_T=json.dumps(data1)
    return render(request,"Home_series.html",{"model_id":list,"max_v":max_v,"max_T":max_T})

#Trial ERS-tool parallel configutaton for editing and testing.
def HTP(request):
    list=CD26_airend_data_rated.objects.all()
    data={}
    data1={}
    for i in list:
        data[i.Model_id]=i.Max
        data1[i.Model_id]=i.T_W_out
    #print(data)
    max_v=json.dumps(data)
    max_T=json.dumps(data1)
    return render(request,"HPT.html",{"model_id":list,"max_v":max_v,"max_T":max_T})

#To Reset password the user or admin password
def reset_password(request):
    if request.method=="POST":
        username=request.POST['userid']
        email=request.POST['email']
        user=User.objects.filter(username=username,email=email)
        print(len(user))
        if len(user)==0: #checking for user existness
            return render(request,"reset_password.html",{"error":"User not exist..","uid":username,"eid":email})
        psw1=request.POST['psw1']
        psw2=request.POST['psw2']
        if psw1==psw2: #verifying the password match
            ReP_App=Reset_password_Approval(UserID=username,Email=email,Password=psw1,Aprove=1) 
            ReP_App.save()        #Updating for admin approval to reset password.
            return render(request,"Login.html",{"error":"Wait for admin approval.."})
        else:
            return render(request,"reset_password.html",{"error":"Password not matching..","uid":username,"eid":email})
    else:
        return render(request,"reset_password.html")

#To open and validate the admin login.
def admin_login(request):
    logout(request)
    if request.method=="POST":
        username=request.POST['username']
        psw=request.POST['psw']
        a_user=authenticate(username=username,password=psw)
        print(a_user)
        if a_user is not None:          #checking for user existness   
            if  a_user.is_authenticated:
                print("Authenticated")
            check=User.objects.filter(username=username,is_superuser = True)
            print(len(check))
            for i in check:  
                print(i)
            if len(check)!=0:    #checking for admin existness
                login(request,a_user)
                return redirect(admin_main)
            else:
                return render(request,"Admin_login.html",{'error':"You don't have access to admin"})
        else:
            return render(request,"Admin_login.html",{'error':"Incorrect adminId or password"})
    else:
        return render(request,"Admin_login.html")

