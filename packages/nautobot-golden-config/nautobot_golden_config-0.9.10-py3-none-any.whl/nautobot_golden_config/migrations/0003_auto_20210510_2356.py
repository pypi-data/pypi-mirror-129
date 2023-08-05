# Generated by Django 3.1.8 on 2021-05-10 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0004_populate_default_status_records"),
        ("nautobot_golden_config", "0002_custom_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goldenconfigsetting",
            name="backup_repository",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"provided_contents__contains": "nautobot_golden_config.backupconfigs"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="backup_repository",
                to="extras.gitrepository",
            ),
        ),
        migrations.AlterField(
            model_name="goldenconfigsetting",
            name="intended_repository",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"provided_contents__contains": "nautobot_golden_config.intendedconfigs"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="intended_repository",
                to="extras.gitrepository",
            ),
        ),
        migrations.AlterField(
            model_name="goldenconfigsetting",
            name="jinja_repository",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"provided_contents__contains": "nautobot_golden_config.jinjatemplate"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="jinja_template",
                to="extras.gitrepository",
            ),
        ),
    ]
