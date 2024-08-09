
from rest_framework import routers
from .viewsets import UserViewSets, ScriptViewSets, FolderViewSets

router = routers.DefaultRouter()

router.register(
    "users",
    UserViewSets,
    basename='users_viewsets'
)
router.register(
    "folder",
    FolderViewSets,
    basename='folder_viewsets'
)
router.register(
    "script",
    ScriptViewSets,
    basename='script_viewsets'
)
