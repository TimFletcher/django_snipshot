###########
# Thanks to baumer1122 for his AdminImageWidget snippet: http://www.djangosnippets.org/snippets/934/
###########
   
from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
import os
  
try:
    from sorl.thumbnail.main import DjangoThumbnail
    def thumbnail(image_path):
        t = DjangoThumbnail(relative_source=image_path, requested_size=(150,150))
        return u'<img style="padding: 5px; border: 1px solid #DDDDDD;" src="%s" alt="%s" />' % (t.absolute_url, image_path)
except ImportError:
    def thumbnail(image_path):
        absolute_url = os.path.join(settings.MEDIA_ROOT, image_path)
        return u'<img style="padding: 5px; border: 1px solid #DDDDDD;" src="%s" alt="%s" />' % (absolute_url, image_path)
  
class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
     
    Example
    -------
    Below is an example on how to implement in your app using the provided code.
             
        from sugar.wigets.admin_image.forms import AdminImageForm
         
        class PhotoAdmin(admin.ModelAdmin):
            form = AdminImageForm
            prepopulated_fields = {'slug': ('title',)}
             
        admin.site.register(Photo, PhotoAdmin)
         
    """
     
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            
            # assert False, Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
            
            try: # File is an image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append("""<a style='float: left; margin-right: 10px;' target="_blank" title="%(title)s" href="%(url)s">%(thumbnail)s</a>""" % {
                    'title': _("Click to View Original"),
                    'url': file_path,
                    'thumbnail': thumbnail(file_name)
                })
            except IOError, e: # File is not an image
            
                # raise e
            
                if file_name != 'None':
                    output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
                        (_('Currently:'), file_path, file_name, _('Change:')))            
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
