from django.shortcuts import render, redirect, get_object_or_404
from .models import List, TreatBrands, Comment, Reply
from .forms import ListForm
from django.contrib import messages
from .forms import SearchForm, ReviewForm, CommentForm, ReplyForm
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import Http404



# Create your views here.
class IndexView(ListView):
    model = List
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = List
    template_name = 'post_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj 

def home(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        """if form.is_valid():
            form.save()
            all_items = List.objects.all
            return render(request, 'home.html', {'all_items': all_items}) """
    else:  
        all_items = List.objects.all
        return render(request, 'home.html',{'all_items': all_items})

def detail(request, pk):
    all_items = List.objects.get(pk=pk)
    review_form = ReviewForm()
    #post1 = get_object_or_404(List,pk=pk)
    #reviews = post1.review.all()
    reviews = all_items.review.all()
    if request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.post = all_items
            f.author = request.user
            f.save() 
            return redirect("detail", pk=pk)
    else:
        return render(request, 'detail.html',{'all_items': all_items,'review_form': review_form,'reviews': reviews})
        

def addtoform(request):
    model = List.objects.values()
    form = ListForm(request.POST )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, 'addtoform.html', {'form': form})
    else:
        form = ListForm()
        return render(request, 'addtoform.html', {'form': form})


logger = logging.getLogger('development')
class SearchView(generic.ListView):
    paginate_by = 5
    template_name = 'search.html'
    model = List
    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('shopname', None),
            self.request.POST.get('treatbrand', None),
            self.request.POST.get('treatused', None),
            self.request.POST.get('genre', None),
            self.request.POST.get('address', None),
        ]
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        shopname = ''
        treatbrand = ''
        treatused = ''
        genre = ''
        address = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            shopname = form_value[0]
            treatbrand = form_value[1]
            treatused = form_value[2]
            genre = form_value[3]
            address = form_value[4]
        default_data = {'shopname': shopname,  # タイトル
                        'treatbrand': treatbrand,  
                        'treatused': treatused,
                        'genre' : genre,
                        'address': address, # 内容
                        }
        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form
        return context
    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            shopname = form_value[0]
            treatbrand = form_value[1]
            treatused = form_value[2]
            genre = form_value[3]
            address = form_value[4]
            # 検索条件
            condition_shopname = Q()
            condition_treatbrand = Q()
            condition_treatused = Q()
            condition_genre = Q()
            condition_address = Q()
            if len(shopname) != 0 and shopname[0]:
                condition_shopname = Q(shopname__icontains=shopname)
            if len(treatbrand) != 0 and treatbrand[0]:
                condition_treatbrand = Q(treatbrand__contains=treatbrand)
            if len(treatused) != 0 and treatused[0]:
                condition_treatused = Q(treatused__contains=treatused)
            if len(genre) != 0 and genre[0]:
                condition_genre = Q(genre__contains=genre)
            if len(address) != 0 and address[0]:
                condition_address = Q(address__contains=address)
            return List.objects.select_related().filter(condition_shopname & condition_treatbrand & condition_treatused & condition_genre & condition_address)
        else:
            # 何も返さない
            return List.objects.none()


class TreatBrandsListView(ListView):
    queryset = TreatBrands.objects.annotate(num_posts=Count('brandname'))

class TreatBrandsPostView(ListView):
    model = List
    template_name = 'treatbrands_post.html'

    def get_queryset(self):
        treatbrands_slug = self.kwargs['treatbrands_slug']
        self.treatbrands = get_object_or_404(TreatBrands, slug=treatbrands_slug)
        qs = super().get_queryset().filter(treat_brand=self.treatbrands)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['treatbrands'] = self.treatbrands
        return context 
    
class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(List, pk=post_pk)
        comment.save()
        return redirect('shop_list:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(List, pk=post_pk)
        return context


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('shop_list:post_detail', pk=comment.post.pk)
 
 
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('shop_list:post_detail', pk=comment.post.pk)


class ReplyFormView(CreateView):
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('shop_list:post_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    return redirect('shop_list:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('shop_list:post_detail', pk=reply.comment.post.pk)