# Generated by Django 2.2.9 on 2020-02-19 13:52

from django.db import migrations, models
import django.db.models.deletion
import style.models


class Migration(migrations.Migration):

    replaces = [
        ("style", "0001_squashed_0002_auto_20151226_1110"),
        ("style", "0002_auto_20190316_0241"),
        ("style", "0003_auto_20190803_0749"),
        ("style", "0004_auto_20190809_1655"),
        ("style", "0005_documentstyle_documentstylefile_exporttemplate"),
        ("style", "0006_auto_20190809_1757"),
        ("style", "0007_auto_20190811_1204"),
        ("style", "0008_auto_20190830_0627"),
    ]

    initial = True

    dependencies = [
        ("document", "0001_squashed_20200219"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentStyle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="Default",
                        help_text="The human readable title.",
                        max_length=128,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        default="default",
                        help_text="The base of the filenames the style occupies.",
                        max_length=20,
                    ),
                ),
                (
                    "contents",
                    models.TextField(
                        default="", help_text="The CSS style definiton."
                    ),
                ),
                (
                    "document_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="document.DocumentTemplate",
                    ),
                ),
            ],
            options={
                "unique_together": {("slug", "document_template")},
            },
        ),
        migrations.CreateModel(
            name="ExportTemplate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="Default",
                        help_text="The human readable title.",
                        max_length=128,
                    ),
                ),
                (
                    "file_type",
                    models.CharField(
                        choices=[("docx", "DOCX"), ("odt", "ODT")],
                        max_length=5,
                    ),
                ),
                (
                    "template_file",
                    models.FileField(upload_to=style.models.template_filename),
                ),
                (
                    "document_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="document.DocumentTemplate",
                    ),
                ),
            ],
            options={
                "unique_together": {("title", "document_template")},
            },
        ),
        migrations.CreateModel(
            name="DocumentStyleFile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="A file references in the style. The filename will be replaced with the final url of the file in the style.",
                        upload_to=style.models.documentstylefile_location,
                    ),
                ),
                (
                    "filename",
                    models.CharField(
                        help_text="The original filename.", max_length=255
                    ),
                ),
                (
                    "style",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="style.DocumentStyle",
                    ),
                ),
            ],
            options={
                "unique_together": {("filename", "style")},
            },
        ),
    ]
