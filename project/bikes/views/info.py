from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Bike, Component, ComponentStatistic
from .forms import ComponentForm, ComponentStatisticForm

from .helpers.view_stats_helper import Filter
