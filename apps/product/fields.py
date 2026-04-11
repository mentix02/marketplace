from rest_framework.reverse import reverse
from rest_framework.relations import HyperlinkedIdentityField


class MultiLookupHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    Handles multiple lookup fields for a URL.
    """

    def __init__(self, *args, **kwargs):
        self.lookup_fields: dict[str, str] = kwargs.pop('lookup_fields', {})
        super().__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        # Map model attributes to URL kwargs
        kwargs = {}
        for model_attr, url_kwarg in self.lookup_fields.items():
            attr_parts = model_attr.split('__')
            value = obj
            for part in attr_parts:
                value = getattr(value, part)
            kwargs[url_kwarg] = value
        return reverse(view_name, kwargs=kwargs, request=request, format=format)
