from django.apps import AppConfig

class FacetOneConfig(AppConfig):
    name = 'facet_one'
    
    def ready(self):
        import facet_one.signals
        import facet_one.admin