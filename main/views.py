from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import request, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from cart.forms import CartAddProductForm
from .forms import CommentForm
from .models import Category, Drug, Comment


class CatalogView(ListView):
    model = Category
    template_name = 'main/index.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(parent=None)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['children'] = Category.objects.filter(parent__isnull=False)
        context['drugs'] = Drug.objects.order_by('-added_at')[:5]
        return context


class DrugsListView(ListView):
    model = Drug
    template_name = 'main/drugs_list2.html'
    context_object_name = 'drugs'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('q')
        sort = self.request.GET.get('sort')
        if sort:
            queryset = queryset.filter(category_id=category).order_by(sort)
        if search:
            queryset = queryset.filter(Q(title__icontains=search))
        else:
            if category == 'pills':
                queryset = queryset.filter(category__parent='pills')
            else:
                queryset = queryset.filter(category_id=category)
        return queryset


def drug_detail(request, pk):
    drug = Drug.objects.get(id=pk)
    cart_drug_form = CartAddProductForm()
    form = CommentForm()
    comments = Comment.objects.filter(drug_id=pk)
    context = {'drug': drug,
               'comments': comments,
               'cart_drug_form': cart_drug_form,
               'form': form}
    return render(request, 'main/drug_detail.html', context)


def addcomment(request, pk):
    drug = Drug.objects.get(id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(drug_id=pk,
                                             user_id=request.user.id,
                                             subject=form.cleaned_data['subject'],
                                             comment=form.cleaned_data['comment'],
                                             rate=form.cleaned_data['rate'])
            return redirect(drug.get_absolute_url())
        else:
            messages.warning(request, 'Please, fill the blanks')
            form = CommentForm()
            return redirect(drug.get_absolute_url())











