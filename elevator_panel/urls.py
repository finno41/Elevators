from django.urls import path
from elevator_panel.apis import request_elevator, edit_settings, elevator_statuses

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("request_elevator", request_elevator, name="request_elevator"),
    path("elevator_statuses", elevator_statuses, name="elevator_statuses"),
    path("edit_settings", edit_settings, name="edit_settings")
]
