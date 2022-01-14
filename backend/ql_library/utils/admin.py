from django.urls import reverse
from django.utils.html import format_html


def _linkify_obj(obj, label_attr=None):
    if obj:
        model_name = obj._meta.model_name
        app_label = obj._meta.app_label
        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[obj.id])
        if label_attr:
            label = str(getattr(obj, label_attr))
        else:
            label = str(obj)
        return format_html('<a href="{}">{}</a>', link_url, label)
    else:
        return "-"


def linkify(field_name, label=None, order_field=None, display_attr=None):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change

    :param field_name: name of ForeignKey field
    :param label: optional label for list display column
    :param order_field: field name or query lookup to allow ordering column, defaults
        to field_name
    :param display_attr: attribute of object used as link display text, if not provided
        defaults to string representation of object instance
    """

    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        return _linkify_obj(linked_obj, label_attr=display_attr)

    _linkify.short_description = label or field_name.replace("_", " ")
    _linkify.admin_order_field = order_field or field_name
    return _linkify


def linkify_set(relation_name, label=None, order_field=None, link_empty=True):
    """
    Converts a reverse relation on foreign key into clickable links.

    Link will be admin url for list of related objects.

    :param relation_name: name of relation
    :param label: optional label for list display column
    :param order_field: set to field or annotation name from ModelAdmin.get_queryset
        to allow ordering column by that value
    :param link_empty: if False and there are no related objects link will not be
        displayed
    """

    def _linkify(obj):
        linked_relation = getattr(obj, relation_name)
        model_name = linked_relation.model._meta.model_name
        app_label = linked_relation.model._meta.app_label
        fk_field = linked_relation.field
        view_name = f"admin:{app_label}_{model_name}_changelist"
        link_url = reverse(view_name) + f"?{fk_field.name}__id__exact={obj.pk}"
        count = linked_relation.count()
        if count == 0 and not link_empty:
            return "-"
        return format_html('<a href="{}">{}</a>', link_url, count)

    _linkify.short_description = label or relation_name.replace("_", " ")
    if order_field:
        _linkify.admin_order_field = order_field
    return _linkify
