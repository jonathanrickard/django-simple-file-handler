from django.db.models.signals import (
    pre_delete,
)


from ..models import (
    BaseMixin,
)


def class_set(input_set):
    unchecked_classes = input_set
    unchecked_subclasses = set()
    output_classes = set()
    while len(unchecked_classes) > 0:
        for unchecked_item in unchecked_classes:
            unchecked_subclasses.update(unchecked_item.__subclasses__())
            output_classes.add(unchecked_item)
        unchecked_classes = unchecked_subclasses
        unchecked_subclasses = set()
    return output_classes


def delete_files(sender, instance, *args, **kwargs):
    for field in instance.check_fields:
        getattr(instance, field).delete(False)


for class_item in class_set(set({BaseMixin})):
    pre_delete.connect(delete_files, class_item)
