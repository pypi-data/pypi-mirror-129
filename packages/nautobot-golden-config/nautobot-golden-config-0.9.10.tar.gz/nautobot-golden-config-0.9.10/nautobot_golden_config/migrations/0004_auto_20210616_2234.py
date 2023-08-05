# Generated by Django 3.1.8 on 2021-06-16 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0004_populate_default_status_records"),
        ("nautobot_golden_config", "0003_auto_20210510_2356"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goldenconfigsetting",
            name="backup_repository",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"provided_contents__contains": "nautobot_golden_config.backupconfigs"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
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
                on_delete=django.db.models.deletion.SET_NULL,
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
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="jinja_template",
                to="extras.gitrepository",
            ),
        ),
    ]
