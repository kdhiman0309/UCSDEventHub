from django.shortcuts import render
from .models import Event
from .apis import add_event_to_db,event_details
from .apis import search_events
from .apis import upcoming_events
from django.http import HttpResponse
from django.utils import dateparse
from datetime import datetime
import re

import json
from django.http import HttpResponse
# Create your views here.

class Utils():

	@staticmethod
	def format_day(date):
		return date.strftime("%a, %b %d")
	
	@staticmethod
	def format_time(date):
		return date.strftime("%I:%M %p")
	
	@staticmethod
	def format_date(date):
		return Utils.format_day(date)+" "+Utils.format_time(date)
	
	@staticmethod
	def get_image_url(image):
		return Constants.media_path+image
	
		
class Constants():
	app_name="hub"
	media_path="/media/"


def event_list(request):
    events=upcoming_events()#.sort(key=lambda e: e.date)[:3]
    for event in events:
        event["image_url"] = "/media/" + event["image"]
        event["start_date"] = event["start_date"].strftime("%a, %b %d, %I:%M %p")
    return render(request, 'hub/Homepage.html', {'events':events})


def event_upload(request):
    return render(request, 'hub/event_upload.html', {})

def event_detail(request):
    eventId = request.GET.get("id")
    evntId = int(eventId)
    events = event_details(evntId)
    event = events[0]
    event["googleDate"] = event["start_date"].strftime("%Y%m%dT%H%M%S")+"/"+event["end_date"].strftime("%Y%m%dT%H%M%S")
    event["start_day"] = event["start_date"].strftime("%a, %b %d")
    event["start_time"] = event["start_date"].strftime("%I:%M %p")
    event["image_url"] = "/media/"+event["image"]
	
    return render(request, 'hub/event_details.html', {'events':event})


	
class SearchListing():
	name = "search_page"
	base_url = "event_search/"
	template = Constants.app_name+"/search_page.html"
		
	class Response():
		
		def __init__(self):
			self.events = []
			self.empty_search = True
		
	def __init__(self):
		self.response = SearchListing.Response()
		
	def _get_keywords(self,request):
		return request.GET.get("q")
	
	def _clean_search_keywords(self, key):
		key = re.sub(' ', '-', key)
		key = re.sub('[^A-Za-z0-9-]', '', key)
		key = re.sub('-+',' ', key)
		return key
	
	def _generate_repsonse(self, events):
		
		for event in events:
			event["start_day"] = Utils.format_day(event["start_date"])
			event["start_time"] = Utils.format_time(event["start_date"])
			event["image_url"] = Utils.get_image_url(event["image"])
		
		self.response.empty_search = False
		self.response.events = events
	
	def _render_me(self, request):
		return render(request, self.template, 
								{"events":self.response.events, 
								"empty_search":self.response.empty_search}
								)
								
	
	def render(self, request):
		search_keywords = self._get_keywords(request)
		
		if not search_keywords:
			return self._render_me(request)
		
		search_keywords = self._clean_search_keywords(search_keywords)
		
		events = search_events(search_keywords)
		
		self._generate_repsonse(events)
		
		return self._render_me(request)
	
	@staticmethod
	def render_page(request):
		module = SearchListing()
		return module.render(request)
	
	def build_url(self, keywords):
		return base_url+"?"+keywords
	
	
	
# Event Upload related views
def get_alert(text,alerttype):
	div=""
	if alerttype == 'fail':
		div = '<div id="valErr" class="row viewerror clearfix">\n'
		div = div + '   <div class="alert alert-danger">'+text+'</div>\n'
		div = div+'</div>'
	else:
		div = '<div id="valErr" class="row viewerror clearfix">\n'
		div = div + '   <div class="alert alert-success">'+text+'</div>\n'
		div = div+'</div>'
	return div

def event_upload(request):
    return render(request, 'hub/event_upload.html', {'div_elem': " "})

def submit_event(request):
	data = request.POST.items()
	for key, value in data:
		print("%s %s" % (key, value))

	# Build the events
	new_event = Event()
	new_event.title = request.POST.get('n_title',"")
	new_event.contact_email = request.POST.get('n_email',"")
	new_event.organizer = request.POST.get('n_org',"")
	new_event.location = request.POST.get('n_loc',"")
	new_event.description = request.POST.get('n_title',"n_desc")
	startdate_object = datetime.strptime(request.POST.get('n_startdate'),'%m/%d/%Y %I:%M %p')
	enddate_object = datetime.strptime(request.POST.get('n_enddate'),'%m/%d/%Y %I:%M %p')
	new_event.start_date = startdate_object
	new_event.end_date = enddate_object

	uploaded_poster = request.FILES['n_uploadedposter']
	new_event.image = uploaded_poster
	new_event.hashtags = request.POST.get('n_tags')
	add_event_to_db(new_event)
	return render(request, 'hub/event_upload.html', {'div_elem':get_alert('Event Upload is Successful','sucess')})


