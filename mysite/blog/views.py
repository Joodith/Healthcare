from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from django.utils import timezone
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse

# Class based views for Post
def index(request):
    return render(request,"blog/index.html")
class AboutView(TemplateView):
    template_name="about.html"
class PostListView(ListView):
    model=Post
    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    template_name="post_list.html"
class PostDetailView(DetailView):
    model=Post
    template_name="post_detail.html"
class PostCreateView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm
    model=Post
    template_name="post_form.html"
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name='blog/post_form.html'
    form_class=PostForm
    model=Post
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy("blog:post_list")
    template_name="post_confirm_delete.html"
class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name="blog/post_list.html"
    model=Post
    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('create_date')
    template_name="post_draft_list.html"


#Function based views for comment
@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect("blog:post_detail",pk=post.pk)
    else:
        form=CommentForm()
    return render(request,"blog/comment_form.html",{'form':form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect("blog:post_detail",pk=comment.post.pk)

@login_required
def comment_delete(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect("blog:post_detail",pk=post_pk)

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect("blog:post_detail",pk=pk)

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Username:{} and password:{} failed while login".format(username,password))
            return HttpResponse("Invalid login")
    else:
        return render(request,'registration/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))








