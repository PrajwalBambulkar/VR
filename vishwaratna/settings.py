"""
Django settings for vishwaratna project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = Path.joinpath(BASE_DIR,'static')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$3d@=c#05ru)&99vlse*d!hxz4!f4ws!3zw(m2(r)+w*v8v#z_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',  #for facebook 
    'django.contrib.sites',
    'social_django', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
     'django.contrib.auth.backends.ModelBackend',
    
    
]

ROOT_URLCONF = 'vishwaratna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vishwaratna.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [STATIC_DIR]
MEDIA_URL='/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '302128944641-sd9c3p1t3ae7f6u1c46aad3rlr8ktiss.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/' 


TINYMCE_SPELLCHCKER =True
X_FRAME_OPTIONS='SAMEORIGIN'
CELERY_CACHE_BACKEND='default'



SITE_ID = 1
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id':'370369037729-66dn8c5465inil61c1o9dj75668823g9.apps.googleusercontent.com',
#             'secret': "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",
#             'key': ''
#         }
#     }
# }

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': '370369037729-66dn8c5465inil61c1o9dj75668823g9.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'zappkodesolutions@gmail.com' 
EMAIL_HOST_PASSWORD = 'jwfvyxtfpnapytpt'

EMAIL_USE_TLS = True


#for Facebook

SOCIAL_AUTH_FACEBOOK_KEY = '316569487566075'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'a60bb07927ddb231a3a038e2280fdd00' 



SOCIALACCOUNT_ADAPTER = 'customer.adapters.CustomSocialAccountAdapter'