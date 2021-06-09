/* Javascript for ZoomCloudRecordingEditBlock. */
function s3UploaderDownloaderEditBlock(runtime, element) {

  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    var data = {
      general_title: $(element).find('input[name=general_title]').val(),
      s3_mid_folder: $(element).find('input[name=s3_mid_folder]').val(),
      s3_bucket: $(element).find('input[name=s3_bucket]').val(),
      uploadable_by_students : $(element).find('input[id=uploadable_by_students]')[0].checked,
      size_limit : $(element).find('input[id=size_limit]').val(),
      paginate : $(element).find('input[id=paginate]').val()
    };

    runtime.notify('save', {state: 'start'});

    console.log("===========");
    console.log("data");
    console.log(data);
    console.log("===========");

    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      runtime.notify('save', {state: 'end'});
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}