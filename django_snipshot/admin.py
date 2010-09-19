from django.contrib import admin
from models import Image
from django.utils.translation import ugettext as _
from forms import ImageAdminForm
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape
import urllib, urllib2
import urlparse

class ImageAdmin(admin.ModelAdmin):
    
    form = ImageAdminForm

    def save_model(self, request, obj, form, change):
        url = form.cleaned_data['snipshot_file']
        if url:
            parts = urlparse.urlparse(url)
            filename = parts.path.split('/')[-1]
            encoded_url = urlparse.urlunparse(list(parts[:2]) + [urllib.quote(parts[2])] + list(parts[3:]))
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(encoded_url).read())
            img_temp.flush()
            file = File(img_temp)
            obj.image.save(filename, file, save=False)
        obj.save()

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage.
        """        
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)
        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = '../'
            else:
                post_url = '../../../'
            return HttpResponseRedirect(post_url)        


    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()        
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.REQUEST.has_key('_popup'):
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif request.POST.has_key("_popup"):
            """
            When the popup window was created, it was given a property, window.name,
            set to the id of the foreign key field for which the new object was
            being created. In order for the window to close correctly, we must pass
            that same id to opener.dismissAddAnotherPopup(). However, if we're 
            returning from snipshot, the page is reloaded and the value of
            window.name is lost. To fix this, we simply define it before calling
            dismissAddAnotherPopup() below.
            """
            return HttpResponse("""<script type="text/javascript">window.name='id_images'; opener.dismissAddAnotherPopup(window, "%s", "%s");</script>""" % \
                # escape() calls force_unicode.
                (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_saveasnew"):
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(opts.verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect("../%s/" % pk_value)
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect("../add/")
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect("../")

admin.site.register(Image, ImageAdmin)