from django.urls import path
from .views import (
    sluzba_post_detail_view,
    sluzba_post_list_view,
    sluzba_post_update_view,
    sluzba_post_delete_view,
    pojanja_list_view,
    folder_list,
    )


urlpatterns = [
    path('', sluzba_post_list_view),
    path('<str:slug>/', sluzba_post_detail_view),
    path('<str:slug>/edit/', sluzba_post_update_view),
    path('<str:slug>/delete/', sluzba_post_delete_view),
]
