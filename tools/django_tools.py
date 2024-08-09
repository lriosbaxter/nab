from rest_framework.response import Response


class GeneralModel:
    @classmethod
    def filter_object_per_model(cls, model, pk):
        try:
            object_found = model.objects.filter(pk=pk).first()
        except model.DoesNotExist:
            return Response({"Error": "Object not found"})
        return object_found
