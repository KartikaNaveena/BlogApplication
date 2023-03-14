from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'



class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile'

    # add this
    def ready(self):
        import blog.signals