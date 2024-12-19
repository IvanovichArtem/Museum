from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from catalog.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from user.models import User, EmailVerification
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def basket_view(request):
    baskets = Basket.objects.filter(user=request.user)

    if request.method == "POST":
        for basket in baskets:
            quantity = request.POST.get(f"basketID_{basket.id}")
            if quantity is not None:
                basket.quantity = int(quantity)
                basket.save()

        messages.success(request, "Корзина обновлена!")
        return HttpResponseRedirect(reverse("user:basket"))

    total_quantity = sum(basket.quantity for basket in baskets)
    total_sum = sum(basket.sum() for basket in baskets)

    context = {
        "baskets": baskets,
        "total_quantity": total_quantity,
        "total_sum": total_sum,
    }

    return render(request, "user/basket.html", context)


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("catalog:home"))
        else:
            print("form is not valid")
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "user/login.html", context)


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "user/registration.html"
    success_url = reverse_lazy("user:login")
    success_message = "Вы успешно зарегестрированы"


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("catalog:home"))


class UserProfileView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "user/profile.html"
    success_message = "Информация изменена!"
    title = "Личный кабинет"

    def get_success_url(self) -> str:
        return reverse_lazy("user:profile", args=(self.object.id,))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user)
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Подтверждение электронной почты"
    template_name = "user/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if (
            email_verifications.exists()
            and not email_verifications.first().is_expired()
        ):
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("catalog:home"))
