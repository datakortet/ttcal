# -*- coding: utf-8 -*-
import django


def pytest_configure():
    from django.conf import settings

    settings.configure(
        TEMPLATE_DEBUG=False,
        INSTALLED_APPS=(
            'django',
            'ttcal',
        )
    )
    django.setup()
