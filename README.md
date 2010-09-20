snipshot.com is a cool little web service that allows its users to manipulate images. django_snipshot integrates Snipshot into the django admin, allowing users to edit their images during the upload process.

## Setup

* Install app
* Add `django_snipshot` to `INSTALLED_APPS`
* Add an image to one of your models e.g. `images = models.ManyToManyField('django_snipshot.Image', related_name="entry_images")`
* run `django-admin.py syncdb`

That should be it. Hit me up if you have any queries.