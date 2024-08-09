from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from first_api.views_new.RunScriptView import RunScriptView
from first_api.views_new.ContentCodeView import ContentCodeView
from .routers import router
from first_api.views_new.RunBGPScriptView import RunBgpScriptView
from .views_new.AuthUserView import AuthUserView
from .views_new.HelloWorldView import HelloWorldView

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/script-run/<int:pk>', RunScriptView.as_view(),
         name='script-run'),
    path('api/v1/script-visualize', ContentCodeView.as_view(),
         name='script-visualize'),
    path('hello-world/', HelloWorldView.as_view(), name='hello-world'),
    path('auth/token', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/user', AuthUserView.as_view(),
         name='auth-usr'),
]
