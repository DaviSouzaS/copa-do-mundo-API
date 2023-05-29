from django.urls import path
from .views import TeamView, TeamViewId

urlpatterns = [
    path('teams/', TeamView.as_view()),
    path('teams/<int:team_id>/', TeamViewId.as_view())
]
