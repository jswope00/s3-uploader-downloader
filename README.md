# S3 Uploader Downloader
An embeddable xblock to allow students/staff to upload and download from/to S3

Installation
------------

Make sure that `ALLOW_ALL_ADVANCED_COMPONENTS` feature flag is set to `True` in `cms.env.json`.

Get the source to the /edx/app/edxapp/ folder and execute the following command:

```bash
sudo -u edxapp /edx/bin/pip.edxapp install s3-uploader-downloader/
```

To upgrade an existing installation of this XBlock, fetch the latest code and then type:

```bash
sudo -u edxapp /edx/bin/pip.edxapp install -U --no-deps s3-uploader-downloader/
```

Configuration
-------------

Configure S3 keys in `lms.auth.json` and `cms.auth.json`

```
"AWS_ACCESS_KEY_ID":"YOUR_AWS_ACCESS_KEY_ID",
"AWS_SECRET_ACCESS_KEY":"YOUR_AWS_SECRET_ACCESS_KEY"
```

Enabling in Studio
------------------

You can enable the s3-uploader-downloader XBlock in studio through the advanced
settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add
   `"s3uploader_downloader"` to the policy value list.
3. Click the "Save changes" button.
