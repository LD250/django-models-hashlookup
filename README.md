# django-models-hashlookup
Modify SQL queries to use different field for lookup.

Queries like:
```python
  Model.objects.filter(field_name__field='big_text')
```
will be translated to:
```python
  Model.objects.filter(field_name__field_hash='dsfsdfergt345rfjspofj')
```
so if you have index on field_hash, queries will become more faster


# Example
1 Model
  ```python
    from django.db import models
    from hashlookups.managers import ManagerHash
    
    class GoodsModel(models.Model):
      good_name = models.TextField(null=True)
      good_name_hash = models.CharField(max_length=100, unique=True)
  
      objects = ManagerHash()
  ```
2 Code
  ```python
    GoodsModel.objects.filter(good_name='my super special good')
  ```

3 Result sql
  ```sql
    SELECT * FROM goodsmodel WHERE good_name_hash = '5974e28ba61e8a9dfaba28236f0ad01bfa3bbe6ce552f0b0705492f94bbc1164'
  ```
