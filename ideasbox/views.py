from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, UpdateView, CreateView,
                                  DeleteView)

user_model = get_user_model()


def index(request):
    return render(request, 'index.html', {})


class UserList(ListView):
    model = user_model
    template_name = 'ideasbox/user_list.html'
    context_object_name = 'user_list'


class UserDetail(DetailView):
    model = user_model
    template_name = 'ideasbox/user_detail.html'
    context_object_name = 'obj'


class UserFormMixin(object):
    exclude = ['password', 'last_login']

    def get_form_class(self):
        return modelform_factory(self.model, exclude=self.exclude)


class UserUpdate(UserFormMixin, UpdateView):
    model = user_model
    template_name = 'ideasbox/user_form.html'
    context_object_name = 'obj'


class UserCreate(UserFormMixin, CreateView):
    model = user_model
    template_name = 'ideasbox/user_form.html'
    context_object_name = 'obj'


class UserDelete(DeleteView):
    model = user_model
    template_name = 'ideasbox/user_confirm_delete.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('user_list')
