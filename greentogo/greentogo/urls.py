"""greentogo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework.documentation import include_docs_urls

import core.views.locations
import core.views.subscriptions
from core import views as core_views
from core.views.webhook import stripe_webhook

from .adminsite import admin_site

subscriptions_patterns = [
    url(r'^$', core.views.subscriptions.subscriptions_view, name='subscriptions'),
    url(
        r'^corporate/$',
        core.views.subscriptions.corporate_subscription,
        name='corporate_subscription'
    ),
    url(r'^new/$', core.views.subscriptions.add_subscription, name='add_subscription'),
    url(
        r'^new/(?P<code>[A-Z0-9]+)/$',
        core.views.subscriptions.add_subscription,
        name='add_corporate_subscription'
    ),
    url(
        r'^(?P<sub_id>[A-Za-z0-9]+)/plan/$',
        core.views.subscriptions.change_subscription_plan,
        name='subscription_plan'
    ),
    url(
        r'^(?P<sub_id>[A-Za-z0-9]+)/add_cc/$',
        core.views.subscriptions.add_credit_card,
        name='subscription_add_credit_card',
    ),
]

urlpatterns = [
    url(r'^webhook/$', stripe_webhook),
    url(r'^locations/$', core.views.locations.locations, name='locations'),
    url(
        r'^locations/(?P<location_code>[A-Za-z1-9]{6})/$',
        core.views.locations.location,
        name='location'
    ),
    url(r'^restaurants/$', core_views.restaurants, name='restaurants'),
    url(r'^subscriptions/', include(subscriptions_patterns)),
    url(r'^account/change_password/$', core_views.change_password, name='change_password'),
    url(
        r'^account/change_payment_method/$',
        core_views.change_payment_method,
        name='change_payment_method'
    ),
    url(r'^account/$', core_views.account_settings, name='account_settings'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', admin_site.urls),
    url(r'^api/docs/', include_docs_urls(title='GreenToGo API')),
    url(r'^api/v1/auth/', include('djoser.urls.authtoken')),
    url(r'^api/v1/', include('apiv1.urls')),
    url(r'^$', core_views.index),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
