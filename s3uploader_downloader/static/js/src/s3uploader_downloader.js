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
        var course_level = '{{course_level}}';
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
                        return course_level+'/'+s3_mid_folder+'/'+"{{unit_id}}"+'/'+fileUUID+'/'+filename;
                    }else{
                        return course_level+'/'+"{{unit_id}}"+'/'+fileUUID+'/'+filename;
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
                                file_name: foldername+'/'+fileNameExt,
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
        qq(document.getElementById("trigger-add-url")).attach("click", function () {
            $('.url-detail-modal').modal('show');
        });

    });
    
    $(".delete_row").click(function(e) {
        e.preventDefault();
        if ($(this).parents('tr')["0"].childNodes[1].childNodes[0].target.length>0) {
            var delete_url_row_url = runtime.handlerUrl(element, 'delete_url_row');
            $.ajax({
                url: delete_url_row_url,
                type: "POST",
                data: JSON.stringify({ 
                    row_id: this.id,
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

        }else{
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
        }
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

    $(".name_edit").click(function(e) {
        e.preventDefault();
        var title = $(this).parents('tr')["0"].childNodes[1].innerText;
        var description = $(this).parents('tr')["0"].childNodes[3].innerText;
        //To Check if its file or URL
        if ($(this).parents('tr')["0"].childNodes[1].childNodes[0].target.length>0) {
            var url = $(this).parents('tr')["0"].childNodes[1].childNodes[0].href;
            $('#addUrl').val(url);
            $('#addUrlName').val(title);
            $('#addUrlDescription').val(description);
            $('#editUrlID').val(this.id);
            $('.url-detail-modal').modal('show');
        }else{
            
            $('#s3filename').val(title);
            $('#s3description').val(description);
            $('#editFileID').val(this.id);
            $('.file-detail-modal').modal('show');
        }
    });

    $("#s3editSave").click(function() {
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
                    location.reload();                
                },
                error: function (error) {
                    console.log("Error : ");
                    console.log(error);
                }
            });
        }
    });

    $("#urlEditSave").click(function(e) {
        if($('#addUrl').val().length>0 & $('#addUrlName').val().length>0){
            //for Updating URL
            if($('#editUrlID').val().length>0){
                var edit_url_details_url = runtime.handlerUrl(element, 'edit_url_details');
                $.ajax({
                    url: edit_url_details_url,
                    type: "POST",
                    data: JSON.stringify({ 
                        url_id: $('#editUrlID').val(),
                        url_src: $('#addUrl').val(),
                        url_title: $('#addUrlName').val(),
                        url_description: $('#addUrlDescription').val()
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
            //for Adding Url
            else{
                var add_url_details_url = runtime.handlerUrl(element, 'add_url_details');
                $.ajax({
                    url: add_url_details_url,
                    type: "POST",
                    data: JSON.stringify({
                            addUrl: $('#addUrl').val(),
                            addUrlName: $('#addUrlName').val(),
                            addUrlDescription: $('#addUrlDescription').val(),
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
        }else{
            $('#required_error').show();
            return false;
        }
    });
}
