from django.urls import path
from .test import *
from .dash import dashboard 
from .views import * 
 
urlpatterns = [
   path('signup/',signupview,name='signup'),
   path('api/signup/',signupApiView,name='Test'),
   path('api/login/',loginREST,name='LoginRest'),
   path('login/',loginView,name='Login'),
   path('reporterList/',reportersList,name='reporterList'),
   path('reporterLoad/',reportLoad),
   path('api/dashboard/',dashboard,name='DashBoard'),
   path('api/lead/add/',lead_view,name='LeadView'),
   path('api/load_dash/',dash_view,name='Load_Dsah'),
   path('api/add_folow_up/',add_follow_up_view,name='AddFollwUp'),
   path('api/change_status/',change_status,name='ChangeStatus'),
   path('api/lead/details/',lead_details,name='Lead_Details'),
   path('api/users/load/',users_data),
   path('api/user/update/',updt_usr),
   path('api/user/data/',user_data),
   path('api/user/delete/',delete_user),
   path('api/user/report/',report_to_usr),
   path('api/roles/',roles),
   path('api/courses/',courses),
   path('api/invoice/',invoice),
   path('api/branch/',branches),
   path('api/bill/',bills),
   path('api/invoice/view/',inv_view),
   path('api/bill/pdf/',bill_view),
   # path('api/bill/view/',bill_view)

]




