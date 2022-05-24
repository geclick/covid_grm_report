# Generated by Django 2.2.16 on 2021-03-17 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_rest", "0042_dataepidemiologiamodel_hora"),
    ]

    operations = [
        migrations.RunSQL(
            """CREATE OR REPLACE FUNCTION aft_delete()
  RETURNS trigger AS
$$
BEGIN
  DELETE FROM public.api_rest_dataepidemiologiamodel WHERE no_muestra = OLD.codigo;
RETURN OLD;
END;

$$
LANGUAGE 'plpgsql';""",
            "DROP FUNCTION IF EXISTS aft_delete();",
        ),
        migrations.RunSQL(
            """
 CREATE TRIGGER delete_resultado
  AFTER DELETE
  ON public.api_rest_datahigienemodel
  FOR EACH ROW
  EXECUTE PROCEDURE aft_delete();
  """,
            "DROP TRIGGER IF EXISTS delete_resultado ON api_rest_dataepidemiologiamodel;",
        ),
    ]
