

from expensemanager import views
from django.urls import path



urlpatterns = [
    path('', views.home, name="home"),
    #path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user, name="logout"),
    path('register/',views.signup, name="register"),
    path('homemain/',views.homemain, name="homemain"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('addexp/',views.addexp, name="addexp"),
    path('reportgen/',views.reportgen, name="reportgen"),
    path('totaldata/',views.totaldata, name="totaldata"),
    path('daterange/',views.daterange, name="daterange"),
    path('categorydata/',views.categorydata, name="categorydata"),
    
    
    
]