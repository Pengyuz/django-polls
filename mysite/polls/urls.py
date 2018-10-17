from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # the following is just from tutorial
    path('',views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/results',views.ResultsView.as_view(),name='results'),
    path('<int:question_id>/vote',views.vote,name='vote'),
    # the following are used
    path('login',views.login,name='login'),
    # the following are not used just for test
    path('homepage',views.homepage,name='homepage'),
    path('show_questions',views.show_questions,name = 'show_questions'),
    path('show_choices',views.show_choices,name = 'show_choices'),
    # path('reset_data',views.reset_data,name = 'reset_data'),
]