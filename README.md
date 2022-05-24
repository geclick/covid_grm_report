El proyecto consiste en generar una herramienta capaz de generar reportes a partir de la data de los resultados de la covid19 en Granma que se obtiene diariamente.

## Tests

```bash
$ docker-compose -f docker-compose-test.yml run --rm api python manage.py test api_rest.tests --settings=MERCES.settings.docker
```
