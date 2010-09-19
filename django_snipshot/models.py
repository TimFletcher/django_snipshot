from django.db import models
from django.utils.translation import ugettext_lazy as _

class Image(models.Model):

    image = models.ImageField(verbose_name=_('Image'), upload_to=lambda self, filename: self.upload_path(filename))
    title  = models.CharField(max_length=200, blank=True)

    def upload_path(self, filename):
        import uuid, os
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('images', filename)

    def __unicode__(self):
        return self.title or u"Untitled Image"