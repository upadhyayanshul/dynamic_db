from django.shortcuts import render, redirect
from .forms import UserForm,UserProfileForm,LoginForm,UserProductForm,DataBaseProductForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .models import Profile,User,Product
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder
from .serializers import ProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,QueryDict,HttpResponse
from .token import account_activation_token
from django.conf import settings
from django.db import connection,connections
from django.apps import apps
from .helper import to_utf8

## HOME PAGE VIEW [CONTAINS SITE TASK INFO] ##
def home_view(request):
    #RENDER HOME PAGE FROM TEMPLATE
    return render(request, 'polls/home.html')

## SIGNUP USER BY THE ADMIN FOR THE DATBASE ACCESS ##
def signup_view(request):
    
    # GET SIGNUP FORM WITH VALIDATION 
    u_form,p_form= UserForm(request.POST), UserProfileForm(request.POST)
    
    # IF METHOD IS POST PROCEED NEXT
    if request.method  == 'POST':

        # CHECK FORM VALIDATIONS FROM COMBINATION
        if u_form.is_valid() and p_form.is_valid():
            
            # SAVE BOTH FORMS AND ADD REQUIRED ATTRIBUTES
            user,profile = u_form.save(),p_form.save(commit=False)
            
            # SET AS NORMAL USER NOT ADMIN USER  
            user.is_staff=True
           
            # ADD ATTRIBUTES TO PROFILE MODEL
            profile.user = user
            profile.email = u_form.cleaned_data.get('email')
            profile.signup_confirmation = False
           
            # SET ACTIVATION FIELD IN DJANGO AUTHENTICATION
            user.is_active = False
            
            #SAVE UPDATED TO FORM ABOVE
            user.save()
            profile.save()
            
            # RETURN  SUCCESS SIGNUP 
            messages.success(request,'User Signup Successfully,Please Verify Using Email')
            
            # SEND VERIFICATION MAIL TO NEW USER
            emailSender(request_body=user.email,message='Account Activation',template_path='polls/activation_request.html',mail_obj={
            'user': user,
            "password":u_form.cleaned_data.get('password1'),
            'domain': get_current_site(request),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'database_access':p_form.cleaned_data.get('database_access')
            },subject='Please Activate Your Account & login')
            
            # REDIRECT RESPONSE TO DASHBOARD ONCE SUCCESS
            return HttpResponseRedirect('dashboard')
        else:
            # RETURN THE FORM ERROR FOR TEST
            print("u_form.errors : ",u_form.errors,"p_form.errors",p_form.errors)

    # RENDER SIGNUP FORM WITH VALIDATIONS
    return render(request, 'polls/signup.html', context={'u_form': u_form, 'p_form': p_form,'f_validate':True})

## ACTIVATE USER ACCOUNT  ##
def activate(request, uidb64, token):
    
    # PUT TRY CATCH BLOCK FOR USER DECODE
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
   

    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        
        # if valid set active true SAVE USER DDETAILS
        user.is_active = True
        user.save()
        
        # SHOW SUCCESS MESSAGE
        messages.success(request,'Activation success,Ready To use Account')
        
        # LOGIN THROIUGH DJANGO USER
        login(request, user)

        #REDIRECT TO DASHBOARD ONCE VERIFIED
        return HttpResponseRedirect('/polls/dashboard/')
    else:
        # RENDER MESSAGE TO ADMIN CONTACT
        messages.error(request,'Activation Failed,Please contact to admin for Account Activation')

        #CALL LOGFORM
        log_form = LoginForm(request.POST)

        #REDIRECT TO LOGIN PAGE
        return render(request, 'polls/login.html', context={'log_form': log_form})

## LOGIN PAGE VIEW [ALLOW THE USERS TO LOGIN INTO PAGE] ##
def login_view(request):
    #IMPORT LOGIN FORM FROM THE DJANGO MODEL FORMS
    log_form = LoginForm(request.POST)

    #DEFINE THE USER TYPE FROM QUERY PARAMS
    login_type=request.GET.get('from',None)

    # FOR POST REQUEST WITH LOGIN 
    if request.method == 'POST':

        # EXTRACT LOGIN BODY DETAILS    
        username,password = request.POST['username'],request.POST['password']

        # MAKE USER AUTHENTICATION
        user = authenticate(username=to_utf8(username), password=to_utf8(password))
        
        # IF USER FOUND PROCEED TO LOGIN
        if user is not None:
            if user.is_active:
                # ALLOW USER TO LOGIN
                login(request, user)

                #SHOW SUCCESS MESSAGE
                messages.success(request,'Login Successfully')
                # REDIRECT TO USER DASHBOARD
                return HttpResponseRedirect("/polls/dashboard")
            else:
                 # RETUERN THE INACTIVE INFO TO USER
                 messages.info(request,'Account is inactive ,Please activate using email sent to you')
        else:
            # RETURN INVALID CREDENTIAL TO USER
            print ("invalid login details " + username + " " + password)

            # RETUERN INVALID WARNING MESSAGE TO USER
            messages.error(request,'Invalide username Or password')
    
    # THE LOGIN IS A  GET REQUEST, RENDER LOGIN FORM FOR THE USER [HANDLE ALL ABOVE CASES]
    return render(request, 'polls/login.html', context={'log_form': log_form,'login_type':login_type})

## LOGOUT PAGE VIEW [CLEAR ALL THE USER SESSION FROM BY LOGOUT] ##
def logout_user(request):
    
    # import the login form
    log_form = LoginForm(request.POST)
    
    # PUT LOGOUT REQUEST 
    logout(request)
    
    # RENDER SUCCESS MESSAGE
    messages.success(request,'logout Successfully')
   
    # Redirect back to LOGIN page.
    return render(request, 'polls/login.html', context={'log_form': log_form})

## REQUEST FOR FORGET PASSWORD ##
def forget_password_view(request):

    #IMPORT FORM LOGIN
    log_form = LoginForm(request.POST)

    # FILTER USERS ON MAIL 
    user= list(User.objects.filter(email=to_utf8(request.POST.get('email'))))

    # CHECK THE USER EXISTANCE
    if len(user) > 0:
        
        # SEND MAIL FOR ACVTIVE USER
        if user[0].is_active:

            # send mail to the user
            emailSender(request_body=to_utf8(request.POST.get('email')),message='Forget Password',template_path='polls/forget_pass_request.html',mail_obj={
            'user': user[0],
            'domain': get_current_site(request),
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': account_activation_token.make_token(user[0]),
            },subject="Forget Password Request")

            # SHOW RESET LINK MESSAGE TO USER
            messages.success(request,'An email reset link is sent to your mail account')
    else:
        # HANDLE ERROR MESSAGING
        messages.info(request,'User With Email Does Not Exists,Please try with different Email')

    # RETURN THE TEMPLATE FOR FORGET PASSWORD
    return render(request, 'polls/login.html', context={'log_form': log_form})

## reset_password_view FOR FORGET PASSWORD ##
def reset_password_view(request, uidb64, token):
    # RESET PASSWORD LOGIN FORM
    log_form = LoginForm(request.POST)

    # VERIFY USER TOKEN FROM THE MAIL
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        
        messages.success(request,'Password Changed Successfully')

        # RENDER THE RESPONSE FOR RESSET PASSWORD
        return render(request, 'polls/reset_password.html',{'username':user.username})
    else:
        #SHOW ERROR MESSAGE
        messages.error(request,'Invalid Reset Password Request')
    
    # LOGIN USER TEMPLATE IN EITHER CASE 
    return render(request, 'polls/login.html', context={'log_form': log_form})

## PROCESS ON SUBMIT PASSWORD REQUEST ##
def reset_password_confirm(request):
    # IMPORT LOGIN FORM 
    log_form = LoginForm(request.POST)

    #EXTRACT LOGIN DETAILS OF USER
    username,password = request.POST.get('username'),request.POST.get('password')

    # EXTRACT UNIQUE USER
    try:
        user = User.objects.get(username=to_utf8(username))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # PROCESS FOR NOT NONE USER
    if user is not None :
        # SET PASSWORD IN MODEL
        user.set_password(to_utf8(password))
        user.save()
        #SHOW NOTIFICATION
        messages.success(request,'Password Reset Successfully')
    else:
        messages.error(request,'Some error in password reset,please make new request')

    # RENDER TEMPLATE
    return render(request, 'polls/login.html', context={'log_form': log_form})

# OPEN DASHBOARD FOR USER WITH THE DATABASE DETAILS 
def dashboard_view(request):

    # EXTRACT ALL THE DATABASE FROM SPECIFIC USER
    databases = Profile.objects.get(user_id=request.user.id)
   
    # CLEAR ARRAY STRING OF DB
    clean_database = eval(databases.database_access.encode("utf8"))

    # LIST ALL THE DB'S WITH DECODE
    db_list = [db_name.encode("utf8") for db_name in clean_database]
    
    # CHECK CORRESPONDING DATABASE TYPE
    database_access = [ {db:settings.DATABASES[db]['ENGINE'].split(".")[-1]} for db in settings.DATABASES.keys() if db in db_list ]

    # ALLOW SUPERADMIN TO HAVE ACCESS IN DEFAULT SYSTEM
    if(request.user.is_superuser):
        database_access.append({"default":"postgresql_psycopg2"})

    # RENDER RESPONSE TO DASHBOARD WITH DB DETAILS [LOGIN REQUIRED]
    return render(request, 'polls/dashboard.html',context={"database_access":database_access})

# LIST ALL THE TABLES FROM SPECIFIC DATABASE IN DASHBOARD DB PANEL 
def show_db_view(request,db_name,db_table=None):
    
    # FETCH ALL THE TABLES
    tables =[ (table).encode("utf8") for table in connections[to_utf8(db_name)].introspection.table_names()]

    # GET THE REUESTED TABLE FROM LIST
    req_table =  db_table if db_table else connections[to_utf8(db_name)].introspection.table_names()[0]
    
    # CREATE REUESTED TABLE MODEL INSTANCE
    model = next((model_instance for model_instance in apps.get_models() if model_instance._meta.db_table== req_table.encode('utf8')), None)

    #DEFIEN TABLE TO RENDER
    table_to_render=None
    
    #CONDITIONS ON MODEL
    if(model is not None):
       
        blog = model.objects.using(to_utf8(db_name)).all().values()
        
        #CLEAN THE TABLE DATA ON QUERY
        table_data = json.dumps(list(blog), cls=DjangoJSONEncoder)
        
        # TABLE TO RENDER IN DASHBOARD
        table_to_render = [ to_utf8(x) for x in json.loads(table_data)]

    # RENDER DATABASE TABLE ACCORDING TO DB 
    return render(request, 'polls/dashboard.html',context={"tables":tables,"database":db_name,"table_data":table_to_render,"table_name":db_table})

# PERMISSION PANEL FOR THE ADMIN TO MANAGE USER 
def permission_view(request):
    # CHECK ADMIN REQUEST
    if request.method == 'GET':

        # RETRIVE ALL THE PROFILES
        profile =Profile.objects.all()

        # GET CLEAN PROFILE DATA
        serializer = ProfileSerializer(profile, many=True)
        
        # DECODE PROFILE PERMISSION SET FOR EACH PROFILE
        permission_table_data =[ to_utf8(table)  for table in to_dict(serializer.data)]
        
        # RENDER PERMISSION TABLE TO HANDLE USER PERMISSION
        return render(request, 'polls/permission_table.html', context={'permission_table': permission_table_data})

# EDIT MULTIPLE PROFILE OF THE USER BASED ON PROFILE PK
def edit_permission(request,profile_id):
    #PARSE THE REQUEST DATA
    request_data = QueryDict(request.body)

    # CLEAN DATA TO REMOVE UNICODES
    clean_request_data = { to_utf8(key):to_utf8(val) for key, val in request_data.lists()}

    #UPDATE SPECIFIC PROFILE
    updated_profile = Profile.objects.filter(id=profile_id).update(database_access=clean_request_data['database_access[]'])
    
    # SHOW MESSAGE ON SUCCESS OR FAILIURE
    if(updated_profile):
        messages.success(request,'Permission Updated Successfully')
    else:
        messages.error(request,"Can't Update Permission Due To Incorrect Request")

    # RETURN JSON RESPONSE TO HANDLE BY JQUERY
    return HttpResponse(
            json.dumps({'status': 'success',}),
            content_type="application/json"
        )

# ADD AND SHOW PRODUCTS IN PRODUCT VIEW
def product_view(request,db_name=None):
   
    # RENDER PRODUCT FORM WITH RELATED FIELD
    product_form ,database_list = UserProductForm(request.POST),DataBaseProductForm(request.POST)
    
    # CONTROLL METHOD ACCESS
    if request.method  == 'POST':

        if not (db_name.encode("utf8") in settings.DATABASES):
            messages.info(request,'Selected DB not exists in application,please try from options')
        else:
        # VALIDATE PRODUCT FORM IN DATABASE
            if product_form.is_valid() and database_list.is_valid() :

                #PRODUCT ATTRIBIUTES REQUIRED
                product =product_form.save(commit=False)
                product.product_database = database_list.cleaned_data.get('database_access')
                product.user_id = request.user.id
                
                # UPDATE PROFILE AND SAVE       
                product.save()

                # RETURN RESPONSE TO PRODUCT TABLE
                return HttpResponseRedirect('/polls/show_table/'+db_name+'/polls_product')
            else:
                print("u_form.errors : ",product_form.errors)

    # RENDER PRODUCT FORM 
    return render(request, 'polls/product.html', context={'product_form': product_form,'database_list':database_list})



class emailSender:

    from_email = settings.DEFAULT_FROM_EMAIL

    def __init__(self,request_body,message,template_path,mail_obj,subject):
        print("request_bodyrequest_body",request_body)

        self.subject = subject
        self.subject=self.subject
        self.from_email = self.from_email
        self.to_list = [request_body]
        self.template_path = template_path
        self.mail_obj = mail_obj
        self.message =message
        return self.load_template()

    def load_template(self):
        print("==========================self.mail_obj",self.mail_obj)
        self.html_message = render_to_string(self.template_path, self.mail_obj)
        return self.send_email()

    def send_email(self):
        mail.send_mail(self.subject, self.message, self.from_email, self.to_list,
                       fail_silently=False, html_message=self.html_message)


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))