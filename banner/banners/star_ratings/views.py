from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View

from . import app_settings, get_star_ratings_rating_model
from .forms import CreateUserRatingForm
from .compat import is_authenticated
import json

from django.views.generic import DetailView, TemplateView
from .models import Foo


class FooView(DetailView):
    model = Foo

    def get_object(self, queryset=None):
        obj, created = Foo.objects.get_or_create(bar='foo bar baz')
        return obj


class SizesView(TemplateView):
    model = Foo
    template_name = 'sizes.html'

    def get_context_data(self, **kwargs):
        kwargs['sizes'] = {size: self.model.objects.get_or_create(bar=str(size))[0] for size in range(10, 40)}
        return super(SizesView, self).get_context_data(**kwargs)



class Rate(View):
    model = get_star_ratings_rating_model()

    def get_object(self):
        """
        Returns the model instance we're rating from the URL params.
        """
        content_type = ContentType.objects.get_for_id(self.kwargs.get('content_type_id'))
        return content_type.get_object_for_this_type(pk=self.kwargs.get('object_id'))

    def post(self, request, *args, **kwargs):
        def _post(request, *args, **kwargs):
            data = request.POST or json.loads(request.body.decode())

            return_url = data.pop('next', '/')
            if 'HTTP_X_REAL_IP' in self.request.META:
                data['ip'] = self.request.META['HTTP_X_REAL_IP']
            else:
                data['ip'] = self.request.META['REMOTE_ADDR']

            data['user'] = is_authenticated(request.user) and request.user.pk or None

            res_status = 200
            result = {}

            try:
                form = CreateUserRatingForm(data=data, obj=self.get_object())
                if form.is_valid():
                    rating = form.save()
                    if rating:
                        result = rating.to_dict()

                        user_rating = form.cleaned_data.get('score')
                        if hasattr(rating, '_user_rating_deleted'):
                            user_rating = None

                        if user_rating:
                            user_rating = int(user_rating)

                        result['user_rating'] = user_rating
                else:
                    result = {'errors': form.errors}
                    res_status = 400
            except ValidationError as err:
                result = {'errors': err.message}
                res_status = 400

            if request.is_ajax():
                return JsonResponse(data=result, status=res_status)
            else:
                return HttpResponseRedirect(return_url)

        if not app_settings.STAR_RATINGS_ANONYMOUS:
            return login_required(_post)(request, *args, **kwargs)

        return _post(request, *args, **kwargs)
