from django.shortcuts import HttpResponse
import json
from datetime import datetime
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User_Details,Lead_List
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict
from .models import Followed_History
from .forms import Lead_List_form



@csrf_exempt
@api_view(['POST'])
def signupApiView (request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    if userC.is_superuser:
        v = request.data                                                                                  
        form = SignUpForm(v)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            userD = User_Details(username=user.username,designation=v.get('designation'))
            userD.save()
            login(request,user)
            data = {'username':user.username,'email':user.email,'session_Id':request.session.session_key}
            return JsonResponse({
                'body':data,
                'status' : "success",
                'code'   : '200',
                })
        else:
            error = str(form.errors.as_data())
            code = "400"
            status = "error"
            message = str(form.errors.as_data())
            if "required" in error:
                message = "Fill all the feilds"
            elif "username already exists" in error:
                message = "Username already exists"
            elif "match" in error:
                message = "Passwords do not match"
            return JsonResponse(dict({
                'status' : status,
                'code' : code,
                'message' : message,
            }))
    else: 
        return Response(data={
            'code':'400',
            'message':'Not a super user'
        })

          
from django.core import serializers

@csrf_exempt
@api_view(['GET', 'POST', ])
def loginREST(request):

    user = User.objects.all()
    return Response(data={
        'forr':serializers.serialize('json',user)
    })

    # if request.method == 'POST':
    #     message = ""
    #     v = dict(request.data)
    #     if  v.get('password')== "" or v.get('username') == "":
    #             message = "All feilds are required"
    #             return Response({
    #             'code': '400',
    #             'message' : message,
    #             'status' : 'error',
    #             })
    #     else:        
    #         bh = User.objects.filter(username=v.get('username')).count()
    #         if(bh == 1):
    #             username = v.get('username')
    #             password =  v.get('password')
    #             user = authenticate(username=username, password=password)
    #             if user is not None:
    #                 login(request,user)
    #                 data = {
    #                     'username':user.username,
    #                     'session_Id':request.session.session_key,
    #                     }
    #                 return Response({
    #                     'body' : data,
    #                     'status' : "success",
    #                     'code' : '200',
    #                 })
    #             else:
    #                     message = "Wrong password"        
    #         else:
    #             message = "User does not exist.\n Please signup"        

    #         return Response({
    #             'code': '400',
    #             'message' : message,
    #             'status' : "error",
    #             })
    # else:
    #     return Response({
    #         'message':'Only POST is accepted',
    #         'code' : '405',
    #         'status' : "error",
    #         })



@api_view(['GET','POST'])
def lead_view(request):
    if(request.method == 'POST'):
        # Dealing with session ID
        data = request.data
        # if the lead phone nuber is already present return error
        c = Lead_List.objects.filter(phone_number = data.get('phone_number')).count()
        if(c == 1):
            return Response({
                'status' : 'error',
                'message' : "Lead already registered with this phone number",
                'code' :'400'
            })
        else:
            session = data.get('user_fllwng')
            session = Session.objects.get(session_key=session)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
            # #creating a lead model object
            data["user_fllwng"] = user
            user = User_Details.objects.get(username=user.username)
            form = Lead_List_form(data)
            if form.is_valid() and form.validate():
                lead = form.save(commit=False)
                lead.user_fllwng = user
                lead.save()
                return Response({
                    'lead_name':lead.name,
                    'status' : 'success',
                    'code' : '200',
                    })
            else:
                return Response(data=dict({
                    'message': str(form.errors.as_data()),
                    'code' :'400',
                    'status' : 'error'
                }))



@csrf_exempt
@api_view(['POST'])
def dash_view(request):
    if(request.method == 'POST'):
        data = request.data
        message=""
        body = ""
        if(data.get('user_session_Id')== None):
           message = "Not logged in"
           body = ""
           code = "400"
        else:
            session = data.get('user_session_Id')
            session = Session.objects.get(session_key=session)
            uid = session.get_decoded().get('_auth_user_id')
            userC = User.objects.get(pk=uid)
            user_details = User_Details.objects.get(username = userC.username)
            user = dict({
                'username':userC.username,
                'designation':user_details.designation
            })
            # getting the leads of the user
            leads = user_details.lead_list_data.all()
            lead_list = []
            for i in leads:
                lead = model_to_dict(i)
                lead = dict({
                    'lead_name' : lead.get('name'),
                    'phone_number' : lead.get('phone_number'),
                    'follow_up_date' : lead.get('nxt_flw_dt'),
                    'status' : lead.get('status')
                })
                lead_list.append(lead)
            user['leads'] = lead_list
            # getting the reporters of the user
            reporters = user_details.report_list.all()
            reporter_list = []
            for j in reporters:
                tmp_usr = User_Details.objects.get(id=j.report_from_id)
                reporter = dict({
                    'name' : tmp_usr.username,
                    'designation' : tmp_usr.designation
                })
                reporter_list.append(reporter)
            user['reporters'] = reporter_list
            body = user
            message = "success"
            code = "200"

        return Response(data = dict({
            'code' : code,
            'body' : body,
            'message': message
        }))

# @csrf_exempt
# @api_view(['GET','POST'])
# def lead_view(request):


    
@csrf_exempt
@api_view(['GET','POST'])
def add_follow_up_view(request):
    if(request.method == 'POST'):
        data = request.data
        session = data.get('user_session_Id')
        session = Session.objects.get(session_key=session)
        uid = session.get_decoded().get('_auth_user_id')
        userC = User.objects.get(pk=uid)
        user_details = User_Details.objects.get(username = userC.username)
        lead = Lead_List.objects.filter(phone_number=data.get('phone_number')).count()
        if(lead  == 0):
             return Response(data=dict({
            'code' : '400',
            'message' : "lead is not present"}))
        lead = Lead_List.objects.get(phone_number=data.get('phone_number'))
        status = lead.status
        reason = data.get('reason')
        date = data.get('date')
        follwd = Followed_History(date=date,status=status,reason=reason,lead_id=lead,user=user_details)
        follwd.save()
        return Response(data=dict({
            'code' : '200',
            'message' : 'sucessfull',
            'body' : 'Saved in to records'
        }))
    else:
        return Response(data=dict({
            'code' : '405',
            'message' : "GEt not allowed"
        }))


# dictionary of status 
status_dict = dict({
    'open' : 1,
    'follow_up' : 2,
    'walked_in' : 3,
    'converted' : 4,
    'closed' : 5
})

@csrf_exempt
@api_view(['POST'])
def change_status(request):
    if(request.method == 'POST'):
        data = request.data
        session = data.get('user_session_Id')
        session = Session.objects.get(session_key=session)
        uid = session.get_decoded().get('_auth_user_id')
        userC = User.objects.get(pk=uid)
        user_details = User_Details.objects.get(username = userC.username)
        lead = Lead_List.objects.filter(phone_number=data.get('phone_number')).count()
        if(lead  == 0):
             return Response(data=dict({
            'code' : '400',
            'message' : "lead is not present"
            }))
        lead = Lead_List.objects.get(phone_number=data.get('phone_number'))
        body = ""
        message = ""
        to_status = status_dict.get(data.get('status'))
        from_status = status_dict.get(lead.status)
        if to_status > from_status:
            if lead.user_fllwng.id is user_details.id:
                lead.status = data.get('status')
                lead.nxt_flw_dt = data.get('nxt_flw_dt')
                lead.save()
                code = '200'
                body = 'Changed status of lead'
            else:
                code = '400'
                message = 'The lead is not assigned to this user'
        else:
            code = '400'
            if(to_status == from_status):
                message = "This is already current status"
            else:
                message = 'Cannot go backwards of status'
        return Response(data=dict({
            'code' : code,
            'body' : body,
            'message' : message
        }))

    else:
        return Response(data=dict({
            'code' : '405',
            'message' : 'GET not allowed'
        }))

@csrf_exempt
@api_view(['POST'])
def lead_details(request):
    data = request.data
    session = data.get('user_session_Id')
    if session is "":
        return Response(data = dict({
            'code':'400',
            'message':'Please sign in'
        }))
    session = Session.objects.get(session_key=session)
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    user_details = User_Details.objects.get(username = userC.username)
    leadm = Lead_List.objects.get(phone_number = data.get('phone_number'))

    lead = dict({
        'name': leadm.name,
        'phone_number' : leadm.phone_number,
        'address' : leadm.address,
        'yop' : leadm.yop,
        'degree' : leadm.degree,
        'marks' : leadm.marks,
        'status':leadm.status
    })

    fllwd_histry = leadm.lead_history.values('date','status','reason')
    fllw_list =[]
    for i in fllwd_histry:
        flw = dict(i)
        fllw_list.append(flw)


    lead['fllwng_hstry'] = fllw_list

    in_li = leadm.lead_invoice_list.values('invc_date','invc_id')
    inv_list = []
    for j in in_li:
        inc = dict(j)
        inv_list.append(inc)
        
    lead['invc_list'] = inv_list

    data = dict({
        'code':'200',
        'body' : lead,
    })
    return Response(data=data)


@csrf_exempt
@api_view(['POST'])
def users_data(request):

    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    if userC.is_superuser:
        usr_lst = User_Details.objects.all()
        usr_lst_data = []
        for m in usr_lst:
            usr_lst_data.append(model_to_dict(m))
        return Response(data={
            'body':usr_lst_data,
            'code':'200'
            })
    else:
        return Response(data={
            'code':'400',
            'message':'not a super user'
        })


@csrf_exempt
@api_view(['POST'])
def updt_usr(request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    if userC.is_superuser:
        usrd = User_Details.objects.get(id=data.get('id'))
        #updating the User_Details table
        usr = User.objects.get(username = usrd.username)
        if data.get('username') is not "":
            usrd.username = data.get('username')
        if data.get('designation') is  not "":
           usrd.designation = data.get('designation')
        usrd.save()
        #updating the inbuilt user account
        if data.get('username') is  not "":
            usr.username = data.get('username')

        if data.get('username') is  not "":
            usr.username = data.get('username')

        if data.get('first_name') is  not "":
            usr.first_name = data.get('first_name')

        if data.get('last_name') is  not "":
            usr.last_name = data.get('last_name')

        if data.get('email') is  not "":
            usr.email = data.get('email')

        if data.get('password') is  not "":
            usr.set_password(data.get('password'))
        usr.save()
        
        return Response(data={
            'code':'200',
            'body' : 'Successfully updated'
        })

    else:
        return Response(data={
            'code':'400',
            'message':'Sorry, not a super user'
        })



@csrf_exempt
@api_view(['POST'])
def user_data(request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    if userC.is_superuser:
        usr = User_Details.objects.get(id=data.get('id'))
        usr_dtl = model_to_dict(usr)
        usr = User.objects.get(username=usr.username)
        usr = model_to_dict(usr)
        usr_dtl.update(usr)
        usr_dtl['id'] = data.get('id')
        return Response(data={
            'code':'200',
            'body' : usr_dtl
        })
    else:
        return Response(data={
            'code':'400',
            'message':'Sorry, Not a super user'
        })




















# @csrf_exempt
# @api_view(['POST'])
# def invoice_view(request):
#     if(request.method == 'POST'):
#         data = request.data
#         session = data.get('user_session_Id')
#         session = Session.objects.get(session_key=session)
#         uid = session.get_decoded().get('_auth_user_id')
#         userC = User.objects.get(pk=uid)
#         user_details = User_Details.objects.get(username = userC.username)
#         lead = Lead_List.objects.filter(phone_number=data.get('phone_number')).count()
#         if(lead  == 0):
#              return Response(data=dict({
#             'code' : '400',
#             'message' : "lead is not present"
#             }))
#         lead = Lead_List.objects.get(phone_number=data.get('phone_number'))


















    #      name:"Ravi",
    #    phone_number:"9898455",
    #    email:"asasjhg@hgf.com",
    #    address:"asdadsdadas",
    #    nxt_flw_dt:"",
    #    dob:"",
    #    user_fllwng:"",
    #    status:"",

        
