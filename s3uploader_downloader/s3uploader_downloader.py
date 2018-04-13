"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment
from xblock.exceptions import JsonHandlerError
from datetime import datetime
import xmodule
from django.views.decorators.csrf import csrf_exempt
import base64
import hmac
import hashlib
import json
from django.http import HttpResponse
from xblockutils.resources import ResourceLoader
from xmodule.modulestore.django import modulestore
from django.conf import settings

from .models import FileAndUrl, FileUploadAndUrl
import boto
from boto.s3.connection import Key, S3Connection
from courseware.access import has_access
# Please start and end the path with a trailing slash
loader = ResourceLoader(__name__)

import logging
log = logging.getLogger(__name__)

class UploaderDownloaderXBlock(XBlock):
    """
    Upload and list uploaded files on S3
    """

    display_name = String(
        display_name="S3 Uploader Downloader",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="S3 Uploader Downloder"
    )

    general_title = String(default="", scope=Scope.content, help="General Title")
    s3_mid_folder = String(default="", scope=Scope.content)
    uploadable_by_students = Boolean(default=False, scope=Scope.settings)
    size_limit = Integer(default=10,scope=Scope.content,help="Number of recordings on one page")
    paginate = Integer(default=20,scope=Scope.content)
    s3_bucket = String(default='public-sgu', scope=Scope.settings)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        context['general_title'] = self.general_title or ''
        context['s3_mid_folder'] = self.s3_mid_folder or ''
        context["uploadable_by_students"] = self.uploadable_by_students
        context['size_limit'] = self.size_limit
        context['paginate'] = self.paginate

        if(context["uploadable_by_students"]==True):
            context["check_uploadable_by_students"] = "checked"
            context["check_uploadable_by_staff"] = ""
        else:
            context["check_uploadable_by_students"] = ""
            context["check_uploadable_by_staff"] = "checked"

        fragment = Fragment()

        fragment.add_content(loader.render_template("static/html/s3uploader_downloader_edit.html",context))

        fragment.add_javascript(self.resource_string("static/js/src/s3uploader_downloader_edit.js"))
        fragment.initialize_js('s3UploaderDownloaderEditBlock')
        return fragment

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.general_title = data.get('general_title')
        self.s3_mid_folder = data.get('s3_mid_folder')
        self.uploadable_by_students = data.get('uploadable_by_students')
        self.size_limit = data.get('size_limit')
        self.paginate = data.get('paginate')

        return {'result': 'success'}

    def get_course(self):

        return self.scope_ids.usage_id.course_key

    def get_course_level(self):
        course = self.scope_ids.usage_id.course_key
        course_level = course.course
        return course_level

    def student_view(self, context=None):
        """
        The primary view of the UploaderDownloaderXBlock, shown to students
        when viewing courses.
        """
        unit_location = modulestore().get_parent_location(self.location)
        unit_id = unit_location.name
        course_level = self.get_course_level()
        data = FileUploadAndUrl.objects.filter(unit_id=unit_id , course_level=course_level)
        context.update({
                        "self": self,
                        "data":data,
                        "paginate":self.paginate,
                        "aws_key":settings.AWS_ACCESS_KEY_ID,
                        "unit_id":unit_id,
                        "s3_mid_folder":self.s3_mid_folder,
			"course_level":course_level,
                        "general_title":self.general_title,
                        "size_limit":self.size_limit,
                        "bin_icon":self.runtime.local_resource_url(self, 'static/img/bin.png'),
                        "gear_icon":self.runtime.local_resource_url(self, 'static/img/gear.png')
                    })

        frag = Fragment()
        frag.add_content(loader.render_template("static/html/list_download.html",context))
        frag.add_css_url("https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css")
        frag.add_javascript_url("https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js")
        frag.add_css(self.resource_string("static/css/s3uploader.css"))

        display_to_students = self.runtime.user_is_staff or self.uploadable_by_students
        if "username" in context and display_to_students:
            frag.add_content(self.resource_string("static/html/s3uploader.html"))

            css_context = dict(
                continue_gif=self.runtime.local_resource_url(self, 'static/img/continue.gif'),
                edit=self.runtime.local_resource_url(self, 'static/img/edit.gif'),
                loading=self.runtime.local_resource_url(self, 'static/img/loading.gif'),
                pause=self.runtime.local_resource_url(self, 'static/img/pause.gif'),
                processing=self.runtime.local_resource_url(self, 'static/img/processing.gif'),
                retry=self.runtime.local_resource_url(self, 'static/img/retry.gif'),
                trash=self.runtime.local_resource_url(self, 'static/img/trash.gif'),
            )
            css = loader.render_template('static/css/fine-uploader-gallery.css', css_context)
            frag.add_css(css)

            frag.add_css(self.resource_string("static/css/fine-uploader.min.css"))
            frag.add_css(self.resource_string("static/css/bootstrap.min.css"))
            frag.add_css(self.resource_string("static/css/bootstrap-grid.min.css"))
            frag.add_css(self.resource_string("static/css/bootstrap-reboot.min.css"))

            frag.add_javascript_url("https://npmcdn.com/tether@1.2.4/dist/js/tether.min.js")
            frag.add_javascript_url("https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.1.3/js.cookie.min.js")

            frag.add_javascript(self.resource_string("static/js/src/bootstrap.min.js"))
            frag.add_javascript(self.resource_string("static/js/src/dnd.min.js"))
            frag.add_javascript(self.resource_string("static/js/src/s3.fine-uploader.core.min.js"))
            frag.add_javascript(self.resource_string("static/js/src/s3.fine-uploader.js"))
            frag.add_javascript(self.resource_string("static/js/src/s3.jquery.fine-uploader.min.js"))
        frag.add_javascript(loader.render_template("static/js/src/s3uploader_downloader.js",context))
        frag.initialize_js('UploaderDownloaderXBlock')
        return frag

    @XBlock.json_handler
    def sign_content(self, data, suffix=''):
        """ Handle S3 uploader POST requests here. For files <=5MiB this is a simple
        request to sign the policy document. For files >5MiB this is a request
        to sign the headers to start a multipart encoded request.
        """
        if data.get('success', None):
            return self.make_response(200)
        else:
            request_payload = data 
            headers = request_payload.get('headers', None)
            if headers:
                # The presence of the 'headers' property in the request payload 
                # means this is a request to sign a REST/multipart request 
                # and NOT a policy document
                response_data = self.sign_headers(headers)
            else:
                if not self.is_valid_policy(request_payload):
                    raise JsonHandlerError(400, 'Points must be an integer')
                response_data = self.sign_policy_document(request_payload)
            response_payload = json.dumps(response_data)
            response_payload = json.loads(response_payload)
            return response_payload


    @XBlock.json_handler
    def add_file_details(self, data, suffix=''):
        file_name = data.get('file_name', None)
        file_title = data.get('file_title', None)
        description = data.get('description', None)
        uploaded_by = data.get('uploaded_by', None)
        unit_id = data.get('unit_id', None)
        course_level = self.get_course_level()
        folder_name = self.s3_mid_folder
        is_url = False
        if folder_name is None:
            folder_name = course_level
        else:
	    folder_name = course_level + '/' + folder_name
        fileuploader = FileAndUrl()
        fileuploader.create_record(file_name, file_title, description, uploaded_by, unit_id, course_level, folder_name, is_url)
        return

    @XBlock.json_handler
    def edit_file_details(self, data, suffix=''):
        file_id = data.get('file_id', None)
        file_title = data.get('file_title', None)
        description = data.get('description', None)
        is_url = False
        fileuploader = FileAndUrl()
        fileuploader.update_record(file_id, None, file_title, description, is_url)
        return

    @XBlock.json_handler
    def delete_file(self, data, suffix=''):
        """ Handle file deletion requests. For this, we use the Amazon Python SDK,
        boto.
        """
        boto.set_stream_logger('boto')
        S3 = S3Connection(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)
        if boto:
            file_id = data.get('file_id', None)
            bucket_name = self.s3_bucket
            aws_bucket = S3.get_bucket(bucket_name, validate=False)

            fileuploader = FileAndUrl()
	    log.info(u"fileuploader.get_file_path(file_id)%s",fileuploader.get_file_path(file_id))
            #Delete for S3
            file_key = Key(aws_bucket, fileuploader.get_file_path(file_id))
            file_key.delete()
            #Delete from db
            fileuploader.delete_record(file_id)

            return
        else:
            return

    @XBlock.json_handler
    def download_file(self, data, suffix=''):
        """ Handle file deletion requests. For this, we use the Amazon Python SDK,
        boto.
        """
        S3 = S3Connection(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)
        file_id = data.get('file_id', None)
        fileuploader = FileAndUrl()
        url = S3.generate_url(
            60,
            'GET',
            self.s3_bucket,
            fileuploader.get_file_path(file_id),
            response_headers={
                'response-content-type': 'application/octet-stream'
            })
        return url

    @XBlock.json_handler
    def add_url_details(self, data, suffix=''):
        addUrl = data.get('addUrl', None)
        addUrlName = data.get('addUrlName', None)
        addUrlDescription = data.get('addUrlDescription', None)
        uploaded_by = data.get('uploaded_by', None)
        unit_id = data.get('unit_id', None)
        course = self.get_course()
        folder_name = None
        course_level = self.get_course_level()
        is_url = True

        urlClass = FileAndUrl()
        urlClass.create_record(addUrl, addUrlName, addUrlDescription, uploaded_by, unit_id, course_level, folder_name, is_url)
        return

    @XBlock.json_handler
    def edit_url_details(self, data, suffix=''):

        url_id = data.get('url_id', None)
        url_src = data.get('url_src', None)
        url_title = data.get('url_title', None)
        url_description = data.get('url_description', None)
        is_url = True

        fileAndUrl = FileAndUrl()
        fileAndUrl.update_record(url_id, url_src, url_title, url_description, is_url)
        return

    @XBlock.json_handler
    def delete_url_row(self, data, suffix=''):
        row_id = data.get('row_id', None)
        fileAndUrl = FileAndUrl()
        fileAndUrl.delete_record(row_id)
        return

    def make_response(self, status=200, content=None):
        """ Construct an HTTP response. Fine Uploader expects 'application/json'.
        """
        response = HttpResponse()
        response.status_code = status
        response['Content-Type'] = "application/json"
        response.content = content
        return response


    def sign_headers(self, headers):
        """ Sign and return the headers for a chunked upload. """
        return {
            'signature': base64.b64encode(hmac.new(settings.AWS_SECRET_ACCESS_KEY, headers, hashlib.sha1).digest())
        }

    def sign_policy_document(self, policy_document):
        """ Sign and return the policy doucument for a simple upload.
        http://aws.amazon.com/articles/1434/#signyours3postform
        """
        policy = base64.b64encode(json.dumps(policy_document))
        signature = base64.b64encode(hmac.new(str(settings.AWS_SECRET_ACCESS_KEY), policy, hashlib.sha1).digest())
        return {
            'policy': policy,
            'signature': signature
        }

    def is_valid_policy(self, policy_document):
        """ Verify the policy document has not been tampered with client-side
        before sending it off. 
        """
        bucket = ''
        parsed_max_size = 0

        for condition in policy_document['conditions']:
            if isinstance(condition, list) and condition[0] == 'content-length-range':
                parsed_max_size = condition[2]
            else:
                if condition.get('bucket', None):
                    bucket = condition['bucket']

        sys_values = bucket.lower() == str(self.s3_bucket).lower() and int(parsed_max_size) == int(1000000*self.size_limit)
        return sys_values
