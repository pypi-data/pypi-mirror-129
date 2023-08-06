`pip install vtb-django-commands`

**Add to installed apps to your django project:**

```python
# settings.py
INSTALLED_APPS = (
    ...
    'vtb_django_commands',
    ...
)
```

### Export/import схемы сервиса в авторайзер

Для генерации схемы

```
python manage.py export_authorizer_schema --file "cfg.json"
```

Для загрузки схемы в авторайзер

```
python manage.py import_authorizer_schema --file "cfg.json"