# S3 Uploader Downloader
An embeddable xblock to allow students/staff to upload and download from/to S3

Installation
------------

Make sure that `ALLOW_ALL_ADVANCED_COMPONENTS` feature flag is set to `True` in `cms.env.json`.

Change user and activate env:

```bash
sudo -H -u edxapp bash
source /edx/app/edxapp/edxapp_env
```

Get the source to the /edx/app/edxapp/ folder:

```bash
cd /edx/app/edxapp/
git clone https://github.com/jswope00/s3-uploader-downloader.git

```

For Installation:
```bash
pip install s3-uploader-downloader/
```

To upgrade an existing installation of this XBlock, fetch the latest code and then update:

```bash
cd s3-uploader-downloader/
git pull origin master
pip install -U --no-deps s3-uploader-downloader/
```

Configuration
-------------

Configure S3 keys in `lms.auth.json` and `cms.auth.json`:

```
"AWS_ACCESS_KEY_ID":"YOUR_AWS_ACCESS_KEY_ID",
"AWS_SECRET_ACCESS_KEY":"YOUR_AWS_SECRET_ACCESS_KEY"
```

Add `s3uploader_downloader` in `INSTALLED_APPS` of `lms/envs/common.py` & `cms/envs/common.py`:

```bash
cd /edx/app/edxapp/edx-platform
nano lms/envs/common.py
nano cms/envs/common.py
```

Run migration:

```bash
python manage.py lms makemigrations s3uploader_downloader --settings=aws
python manage.py lms migrate s3uploader_downloader --settings=aws
```

Compile Assets:

```bash
paver update_assets cms --settings=aws
paver update_assets lms --settings=aws
```

Restart Edxapp:

```bash
exit
sudo /edx/bin/supervisorctl restart edxapp:
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
