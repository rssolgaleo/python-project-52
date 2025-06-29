from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError
from django.contrib.auth import get_user_model
from django.views.generic import (
  CreateView,
  UpdateView,
  DeleteView,
  ListView
)
from django.contrib.auth.mixins import (
  LoginRequiredMixin,
  UserPassesTestMixin,
)
from task_manager.users.forms import (
  CustomUserCreationForm,
  CustomUserUpdateForm,
)
from django.contrib.auth.views import (
  LoginView,
  LogoutView,
)

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("User created successfully"))
        return super().form_valid(form)


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You don't have permission to update this user.")
        )
        return redirect("user_list")

    def form_valid(self, form):
        messages.success(self.request, _("User updated successfully"))
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(
                request,
                _("You don't have permission to delete this user.")
            )
            return redirect("user_list")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, _("Account successfully deleted"))
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                _(
                    "Cannot delete the account because they are assigned "
                    "to at least one task."
                )
            )
            return redirect("user_list")
