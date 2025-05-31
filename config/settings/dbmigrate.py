from decouple import config

MYAPP = ["accounts", "committees"]

MIGRATION_MODULES = {app: f"{app}.migrations_generated" for app in MYAPP}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", cast=str),
        "NAME": config("DB_NAME", cast=str),
        "USER": config("DB_USER", cast=str),
        "PASSWORD": config("DB_PASSWORD", cast=str),
        "OPTIONS": {
            "autocommit": True,
        },
    }
}
