/* Javascript for UploaderDownloaderXBlock. */
function UploaderDownloaderXBlock(runtime, element) {

    var fileNameExt = '';
    var extension = '';

    $(document).ready(function() {
        $('#uploads').DataTable({
            "lengthChange": false
        });
    });

    $(function ($) {
        var signature_url = runtime.handlerUrl(element, 'sign_content');
        var s3_success_url = runtime.handlerUrl(element, 's3_success_endpoint');
        var add_file_url = runtime.handlerUrl(element, 'add_file_details');
        var s3_mid_folder = '{{s3_mid_folder}}';
        var uploader = new qq.s3.FineUploader({
            element: document.getElementById("uploader"),
            request: {
                endpoint: "https://{{self.s3_bucket}}.s3.amazonaws.com",
                accessKey: "{{aws_key}}"
            },
            objectProperties: {
                key: function (fileId) {
                    var filename = uploader.getName(fileId);
                    var fileUUID = uploader.getUuid(fileId);
                    if (s3_mid_folder.length > 0){
                        return s3_mid_folder+'/{{unit_id}}/'+fileUUID+filename;    
                    }else{
                        return '{{unit_id}}/'+fileUUID+filename;
                    }
                },
            },
            signature: {
                endpoint: signature_url,
                version: 2,
                customHeaders: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            },
            cors: {
                expected: true
            },

            chunking: {
                enabled: false,
            },
            resume: {
                enabled: true
            },
            messages: {
                noFilesError: "No file has been selected to upload"
            },
            callbacks: { 
                onSubmitted: function (id, name, jsonResponse) {
                    fileNameExt = uploader.getName(id)
                    extension = fileNameExt.substr(fileNameExt.lastIndexOf('.') + 1)
                    fileName = fileNameExt.replace(/\.[^/.]+$/, "");

                    $('#s3filename').val(fileName)
                    $('.file-detail-modal').modal('show')
                },
                onUpload: function (id, name) {
                    uploader.setName(id, $('#s3filename').val() + '.' + extension)
                },
                onComplete: function (id, name, jsonResponse) {
                    if(jsonResponse.success){
                        var foldername = uploader.getUuid(id);
                        var fileNameExt = uploader.getName(id)
                        $.ajax({
                            url: add_file_url,
                            type: "POST",
                            data: JSON.stringify({
                                file_name: foldername+fileNameExt,
                                file_title: $('#s3filename').val(),
                                description: $('#s3description').val(),
                                uploaded_by: "{{username}}",
                                unit_id: "{{unit_id}}"
                            }),
                            success: function (data) {
                                console.log("Success : ");
                                console.log(data);
                                location.reload();
                            },
                            error: function (error) {
                                console.log("Error : ");
                                console.log(error);
                            }
                        });
                    }

                 },
                onCancel: function (id, name) {
                    var uuid = uploader.getUuid(id);
                    var foldername = uploader.getName(id) + '_' + uuid
                },
                onProgress: function (id, name, uploadedBytes, totalBytes) {
                    console.log(uploadedBytes);
                },

            },
            autoUpload: false,
            multiple: false,
            debug: false,
            validation: {
                sizeLimit: 1000000*{{size_limit}}
            }
        });

        qq(document.getElementById("trigger-upload")).attach("click", function () {
            uploader.uploadStoredFiles();
        });
    });
    
    $(".S3_delete").click(function() {
        var delete_file_url = runtime.handlerUrl(element, 'delete_file');
        $.ajax({
            url: delete_file_url,
            type: "POST",
            data: JSON.stringify({ 
                file_id: this.id,
            }),
            success: function (data) {
                console.log("Success : ");
                console.log(data);
                location.reload();
            },
            error: function (error) {
                console.log("Error : ");
                console.log(error);
            }
        });

    });
    $(".file_download").click(function(e) {
        e.preventDefault();
        var download_file_url = runtime.handlerUrl(element, 'download_file');
        $.ajax({
            url: download_file_url,
            type: "POST",
            data: JSON.stringify({ 
                file_id: this.id,
            }),
            success: function (data) {
                window.location.href = data;
            },
            error: function (error) {
                console.log("Error : ");
                console.log(error);
            }
        });

    });

    $(".name_edit").click(function() {
        var fileName = $(this).parents('tr')["0"].childNodes[1].innerText;
        var fileDesc = $(this).parents('tr')["0"].childNodes[3].innerText;
        $('#s3filename').val(fileName);
        $('#s3description').val(fileDesc);
        $('#editFileID').val(this.id);
        $('.file-detail-modal').modal('show');
    });

    $("#editSave").click(function() {
        if($('#editFileID').val().length>0)
        {
            var edit_file_url = runtime.handlerUrl(element, 'edit_file_details');
            $.ajax({
                url: edit_file_url,
                type: "POST",
                data: JSON.stringify({ 
                    file_id: $('#editFileID').val(),
                    file_title: $('#s3filename').val(),
                    description: $('#s3description').val()
                }),
                success: function (data) {
                    console.log("Success : ");
                    console.log(data);
                    location.reload();                },
                error: function (error) {
                    console.log("Error : ");
                    console.log(error);
                }
            });
        }
    });
    
}
