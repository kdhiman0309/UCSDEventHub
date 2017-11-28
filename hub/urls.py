from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from .views import SearchListing, EventUpload, OrganizationPage, EventDetails

urlpatterns = [
    url(r'^$', views.event_list, name='event_list'),
    url(r'^'+EventUpload.base_url, EventUpload.render_page, name=EventUpload.name),
    url(r'^'+EventDetails.base_url, EventDetails.render_page, name=EventDetails.name),
    url(r'^'+SearchListing.base_url, SearchListing.render_page, name=SearchListing.name),
    url(r'^'+EventUpload.submit_url, EventUpload.event_upload_handler, name=EventUpload.submit_view_name),
    url(r'^login/', views.login,name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^myevents/', views.myevents, name='My Events Page'),
	url(r'^'+OrganizationPage.base_url, OrganizationPage.render_page, name=OrganizationPage.name),
	url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
	url(r'^ajax/saveRSVP/$', views.save_RSVP, name='saveRSVP'),
	url(r'^ajax/removeRSVP/$', views.remove_RSVP, name='removeRSVP')
]
