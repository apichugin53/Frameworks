from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login, RedirectURLMixin
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.shortcuts import resolve_url, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from dogs.forms import DogForm, CommentForm, ApproveCommentForm
from dogs.models import Dog, Breed, Comment
from users.models import Role


class DogsListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs_list.html'
    extra_context = {
        'title': _('Dogs'),
    }
    ordering = 'name'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        if request.GET and not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search', '').strip()
        breed = self.request.GET.get('breed', '').strip()
        if search:
            if breed:
                qs = qs.filter(Q(name__icontains=search) & Q(breed__name__icontains=breed))
            else:
                qs = qs.filter(Q(name__icontains=search) | Q(breed__name__icontains=search))
        elif breed:
            qs = qs.filter(Q(breed__name__icontains=breed))
        return qs


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    extra_context = {
        'title': _('Add dog'),
        'action_url': reverse_lazy('dogs:dog_add'),
    }

    def get(self, request, *args, **kwargs):
        self.object = Dog(owner=self.request.user)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        actor = self.request.user
        if actor.role == Role.USER:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    extra_context = {
        'title': _('Edit dog'),
    }

    def get_success_url(self):
        return reverse('dogs:dog_details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = {
            'action_url': reverse('dogs:dog_update', kwargs={'pk': self.object.id}),
            **kwargs,
        }
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        dog = super().get_object(queryset)
        actor = self.request.user
        if dog.owner == actor or not dog.owner and actor.is_moderator:
            return dog
        raise PermissionDenied

    def form_valid(self, form):
        actor = self.request.user
        if actor.role == Role.USER:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class DogDetailsView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dogs/dog_details.html'
    extra_context = {
        'title': _('Dog'),
    }

    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        self.object.update_views(self.request.user)
        return result

    def get_context_data(self, **kwargs):
        dog = self.object
        actor = self.request.user
        context = {
            'can_edit': actor.is_authenticated and (dog.owner_id == actor.id or actor.is_moderator),
            'comments': dog.comment_set.all(),
            **kwargs,
        }
        return super().get_context_data(**context)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    http_method_names = ['delete', 'options', 'post']
    success_url = reverse_lazy('dogs:dogs_list')

    def get_object(self, queryset=None):
        dog = super().get_object(queryset)
        actor = self.request.user
        if dog.owner == actor or actor.is_moderator:
            return dog
        raise PermissionDenied


class BreedsListView(LoginRequiredMixin, ListView):
    model = Breed
    template_name = 'dogs/breeds_list.html'
    extra_context = {
        'title': _('Breeds'),
    }
    ordering = 'name'
    paginate_by = 6


class BreedDetailsView(LoginRequiredMixin, DetailView):
    model = Breed
    template_name = 'dogs/breed_details.html'
    extra_context = {
        'title': _('Breed'),
    }


class DogPedigreeView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dogs/dog_pedigree.html'
    extra_context = {
        'title': _('Dog'),
    }

    def get_context_data(self, **kwargs):
        dog = self.object
        actor = self.request.user
        context = {
            'can_edit': actor.can_edit_user(dog.owner_id),
            'dogs': Dog.objects.filter(id__in=dog.ancestors.all().values('ancestor')),
            **kwargs,
        }
        return super().get_context_data(**context)


class CommentRedirectMixin(RedirectURLMixin):
    def get_initial(self):
        initial = super().get_initial()
        initial.update({'next': self.request.META.get('HTTP_REFERER')})
        return initial

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        return reverse('dogs:dog_comments', kwargs={'pk': self.object.dog_id})


class DogCommentListView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dogs/dog_comments.html'
    extra_context = {
        'title': _('Dog'),
    }

    def get_context_data(self, **kwargs):
        dog = self.object
        actor = self.request.user
        comments = dog.comment_set
        if not actor.is_moderator:
            comments = comments.filter(
                Q(is_active=True) | Q(user=self.request.user)
            )
        context = {
            'can_edit': actor.can_edit_user(dog.owner_id),
            'comments': comments.select_related('user'),
            **kwargs,
        }
        if actor.is_moderator:
            context.update({'next_page': self.request.path})
        return super().get_context_data(**context)


class DogCommentAddView(LoginRequiredMixin, CommentRedirectMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'dogs/comment_form.html'
    extra_context = {
        'title': _('Add comment'),
    }

    def get_context_data(self, **kwargs):
        context = {
            'dog': get_object_or_404(Dog, pk=self.kwargs['pk']),
            **kwargs,
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        actor = self.request.user
        form.instance.user = actor
        form.instance.dog = get_object_or_404(Dog, pk=self.kwargs['pk'])
        if actor.is_moderator:
            form.instance.is_active = True
        return super().form_valid(form)


class DogCommentUpdateView(LoginRequiredMixin, CommentRedirectMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'dogs/comment_form.html'
    extra_context = {
        'title': _('Edit comment'),
    }

    def get_queryset(self):
        return super().get_queryset().select_related('dog')

    def get_context_data(self, **kwargs):
        context = {
            'dog': self.object.dog,
            **kwargs,
        }
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        actor = self.request.user
        if comment.user_id == actor.id:
            return comment
        raise PermissionDenied


class DogCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    http_method_names = ['delete', 'options', 'post']

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        actor = self.request.user
        if comment.user_id == actor.id or actor.is_moderator:
            return comment
        raise PermissionDenied


class ModeratorAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_moderator


class CommentListView(LoginRequiredMixin, ModeratorAccessMixin, ListView):
    model = Comment
    paginate_by = 5
    template_name = 'dogs/comments_list.html'
    extra_context = {
        'title': _('Comments'),
    }

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False).select_related('user', 'dog', 'dog__breed')

class ApproveCommentView(LoginRequiredMixin, ModeratorAccessMixin, CommentRedirectMixin, UpdateView):
    model = Comment
    form_class = ApproveCommentForm
    http_method_names = ["post", "options"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_moderator:
            raise PermissionDenied
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        return reverse('dogs:comments_list')
