from .settings import *

DEBUG = True

DATABASES = {
	'default': {
    		'NAME': 'bankco2',
    		'ENGINE': 'django.db.backends.postgresql',
    		'HOST': 'localhost',
    		'USER': 'postgres',
    		'PASSWORD': 'bankco2'
	}
}
