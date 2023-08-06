# Django Minifier

Minify Django Template.

Install:

```shell
pip install django_minifier
```

Add template loader

```python
# settings.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "example" / "templates"
        ],
        # "APP_DIRS": True, 
        "OPTIONS": {
            "context_processors": [
                ...
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django_minifier.app_directories.Loader",
                        "django_minifier.filesystem.Loader",
                        "django_minifier.themes.Loader",
                    ],
                )
            ],
        },
    },
]

TEMPLATE_MINIFIER = not DEBUG
TEMPLATE_MINIFIER_EXCLUDED_DIRS = ("admin/", "wagtailadmin/")
TEMPLATE_MINIFIER_FILENAME_EXTENSIONS = (".html", ".htm")
TEMPLATE_MINIFIER_STRIP_FUNCTION = False

```
