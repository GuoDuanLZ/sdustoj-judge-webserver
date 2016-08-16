from rest_framework_nested import routers

from .function_views import LoginViewSet, Logout
from .user_views import UserViewSet


router = routers.SimpleRouter()

router.register(r'login', LoginViewSet, base_name='login')
router.register(r'logout', Logout, base_name='logout')

router.register(r'users', UserViewSet, base_name='users')

urlpatterns = []
urlpatterns += router.urls
