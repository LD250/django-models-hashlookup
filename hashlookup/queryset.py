import hashlib
from django.db import models


def gen_hash(str_val):
    return hashlib.sha256(str_val.encode('utf-8')).hexdigest()


class HashFilterQuerySet(models.query.QuerySet):
    """
        queries like Model.objects.filter(field_name__field='big_text')
        will be translated to
            Model.objects.filter(field_name__field_hash='dsfsdfergt345rfjspofj')
        so if you have index on field_hash, queries will become more faster
    """
    gen_hash_fun = property(lambda self: gen_hash)

    def _filter_or_exclude(self, negate, *args, **kwargs):
        new_kwargs = {}

        def modify_lookup_parts(model_class, lookup_list):
            first, rest = lookup_list[0], lookup_list[1:]
            fields = {f.name: f for f in model_class._meta.local_fields}
            f = fields.get(first)
            if f and rest != ['contains'] and rest != ['icontains']:
                if f.rel and rest:
                    try:
                        parent_model = f.related.parent_model
                    except AttributeError:
                        parent_model = f.related.model
                    return [first] + modify_lookup_parts(parent_model, rest)
                else:
                    if (first + '_hash') in fields:
                        first += '_hash'
                    return [first] + rest
            else:
                return lookup_list

        def __gen_hash(val):
            if isinstance(val, list) or isinstance(val, tuple) or isinstance(val, set):
                return [self.gen_hash_fun(v) for v in val]
            else:
                return self.gen_hash_fun(val)

        for lookup in kwargs:
            hash_lookup = '__'.join(modify_lookup_parts(self.model, lookup.split('__')))
            lookup_val = kwargs[lookup]
            new_kwargs[hash_lookup] = lookup_val if hash_lookup == lookup else __gen_hash(lookup_val)

        return super(HashFilterQuerySet, self)._filter_or_exclude(negate, *args, **new_kwargs)

