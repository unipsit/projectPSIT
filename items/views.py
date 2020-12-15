from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Item
from django.db import models
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
    context = {
        'item' : Item.objects.all()
    }
    return render(request, 'home.html', context)

class ItemListView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
      return Item.objects.filter(need_at__gt = timezone.now()).order_by('-status')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'item_new_form.html'
    fields = ['item_name', 'where', 'need_at', 'pic_item']

    def form_valid(self, form):
        form.instance.post_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'item_update.html'
    fields = ['item_name', 'where', 'need_at', 'pic_item']
    
    def form_valid(self, form):
        form.instance.post_by = self.request.user
        return super().form_valid(form)

class ItemAcceptView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'item_accept.html'
    success_url = '/'
    fields = ['return_at']

    def form_valid(self, form):
        form.instance.accept_by = self.request.user
        form.instance.status = 'Accepted'
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user != post.post_by:
            return True
        return False

class ItemRecieveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'item_recieve.html'
    success_url = '/'
    fields = []

    def form_valid(self, form):
        form.instance.status = 'Recieved'
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_by:
            return True
        return False

class ItemCancelView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'item_cancel.html'
    success_url = '/'
    fields = []

    def form_valid(self, form):
        post = self.get_object()
        all_status = {
            'Yet': 1,
            'Accepted': 2,
            'Recieved': 3
        }
        num = all_status[post.status] - 1
        if num == 1:
            form.instance.accept_by = None
            form.instance.status = 'Yet'
        elif num == 2:
            form.instance.status = 'Accepted'
        return super().form_valid(form)


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_by or self.request.user == post.accept_by:
            return True
        return False
