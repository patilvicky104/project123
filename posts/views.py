from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse, reverse_lazy
from django.http import request , Http404, HttpResponse, request,HttpResponsePermanentRedirect
from django.views import generic
from django.views.generic import CreateView
# from noconflict import classmaker


from braces.views import SelectRelatedMixin

from posts import forms
from posts import models

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from posts.forms import PostForm ,DocumentForm
from posts.models import Post,UploadFile
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group',)
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
    
    
def upload_list(request):
    pdf = UploadFile.objects.all()
    return render(request,'posts/pdf_list.html',{'pdf':pdf})

def upload_pdf(request):
    if request.method == 'POST':
        upload_form = DocumentForm(request.POST,request.FILES)
        if upload_form.is_valid():
            upload_form.save()
            html = "<html><body><p>successfully uploaded.</p></body></html>"
            success_url = reverse_lazy('upload_list')
            return redirect('posts:upload_list')

        else:
            upload_form = DocumentForm()
    else:
        upload_form = DocumentForm()
        return render(request,"posts/upload_book.html",{'upload_form': upload_form})