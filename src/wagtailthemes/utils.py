import hashlib
import os
import time
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

from django.core.files.base import File
from django.db import transaction

from wagtailthemes.storage import default_static_file_storage


def compute_file_checksum_from_text(text, algorithm="sha256"):
    checksum = hashlib.new(algorithm)
    checksum.update(text.encode("utf-8"))
    return checksum.hexdigest()


def compute_file_checksum_from_file(file, read_chunksize=65536, algorithm="sha256"):
    checksum = hashlib.new(algorithm)
    f = file.open(mode="rb")
    for chunk in iter(lambda: f.read(read_chunksize), b""):
        checksum.update(chunk)
        time.sleep(0)
    #: do not close file as django save requires an open file
    return checksum.hexdigest()


def write_static_file_to_dir(static_file, dir):
    sub_dirs = os.path.dirname(static_file.path)
    if not os.path.exists(dir + os.sep + sub_dirs):
        os.makedirs(dir + os.sep + sub_dirs)
    file_contents = default_static_file_storage.open(static_file.location).read()
    file = open(dir + os.sep + static_file.path, "w")
    file.write(file_contents.decode("utf-8"))
    file.close()


def write_static_files_to_dir(static_files, dir):
    for static_file in static_files:
        write_static_file_to_dir(static_file, dir)


def write_template_to_dir(template, dir):
    sub_dirs = os.path.dirname(template.path)
    if not os.path.exists(dir + os.sep + sub_dirs):
        os.makedirs(dir + os.sep + sub_dirs)
    file = open(dir + os.sep + template.path, "w")
    file.write(template.value)
    file.close()


def write_templates_to_dir(templates, dir):
    for template in templates:
        write_template_to_dir(template, dir)


def export_theme_as_zip_file(theme):
    from wagtailthemes.models import StaticFile, Template

    static_files = StaticFile.objects.filter(theme=theme)
    templates = Template.objects.filter(theme=theme)
    temp_dir = TemporaryDirectory()

    write_static_files_to_dir(static_files, temp_dir.name + os.sep + "static")
    write_templates_to_dir(templates, temp_dir.name + os.sep + "templates")

    zip_file = ZipFile(theme.pathname + ".zip", "w", ZIP_DEFLATED)
    for dirname, subdirs, files in os.walk(temp_dir.name):
        rel_dir = dirname.replace(temp_dir.name, "")
        if rel_dir.startswith("/"):
            rel_dir = rel_dir[1:]
        zip_file.write(dirname, rel_dir)
        for filename in files:
            zip_file.write(
                os.path.join(dirname, filename), os.path.join(rel_dir, filename)
            )
    zip_file.close()
    temp_dir.cleanup()
    return zip_file


def import_theme_from_zip_file(theme, file):
    from wagtailthemes.models import StaticFile, Template

    temp_dir = TemporaryDirectory()

    zip_file = ZipFile(file, "r", ZIP_DEFLATED)
    zip_file.extractall(temp_dir.name)
    zip_file.close()

    templates = []
    static_files = []

    with transaction.atomic():
        #: Templates
        Template.objects.filter(theme=theme).delete()

        templates_dir = temp_dir.name + os.sep + "templates"

        for subdir, dirs, files in os.walk(templates_dir):
            for filename in files:
                abs_path = subdir + os.sep + filename
                rel_path = abs_path.replace(templates_dir + os.sep, "")

                with open(abs_path, "rb") as template_file:
                    template_contents = template_file.read()
                    template = Template(
                        theme=theme,
                        path=rel_path,
                        value=template_contents.decode("utf-8"),
                    )
                    templates.append(template)

        Template.objects.bulk_create(templates)

        #: Static files
        StaticFile.objects.filter(theme=theme).delete()

        static_dir = temp_dir.name + os.sep + "static"

        for subdir, dirs, files in os.walk(static_dir):
            for filename in files:
                abs_path = subdir + os.sep + filename
                rel_path = abs_path.replace(static_dir + os.sep, "")

                with open(abs_path, "rb") as file:
                    static_file = StaticFile.objects.create(
                        theme=theme,
                        path=rel_path,
                        file=File(file, rel_path),
                    )
                    static_files.append(static_file)

    temp_dir.cleanup()
    return (templates, static_files)
