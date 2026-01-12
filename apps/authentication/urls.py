from django.urls import path

from apps.authentication.views import InitSessionView, CurrentUserView, LoginView

apps_name = 'authentication'
urlpatterns = [
    path('session/',InitSessionView.as_view(),name='session'),
    path('token/', LoginView.as_view(), name='login_view'),
    # path('token/', JWTObtainPairView.as_view(), name='token_obtain_pair'),
    path('current-user/', CurrentUserView.as_view(), name='current_user_view'),
]