$(document).ready(function () {

    var options = {
        controls: true,
        bigPlayButton: false,
        width: 600,
        height: 300,
        fluid: false,
        plugins: {
            wavesurfer: {
                backend: 'WebAudio',
                waveColor: 'white',
                progressColor: 'green',
                displayMilliseconds: true,
                debug: true,
                cursorWidth: 1,
                hideScrollbar: true,
                plugins: [
                    // enable microphone plugin
                    WaveSurfer.microphone.create({
                        bufferSize: 4096,
                        numberOfInputChannels: 1,
                        numberOfOutputChannels: 1,
                        constraints: {
                            video: false,
                            audio: true
                        }
                    })
                ]
            },
            record: {
                audio: true,
                video: false,
                maxLength: 60,
                displayMilliseconds: true,
                debug: true
            }
        }
    };

    // apply audio workarounds for certain browsers
    applyAudioWorkaround();

    // create player
    var player = videojs('myAudio', options, function () {
        // print version information at startup
        var msg = 'Using video.js ' + videojs.VERSION +
            ' with videojs-record ' + videojs.getPluginVersion('record') +
            ', videojs-wavesurfer ' + videojs.getPluginVersion('wavesurfer') +
            ', wavesurfer.js ' + WaveSurfer.VERSION + ' and recordrtc ' +
            RecordRTC.version;
        videojs.log(msg);
    });

    // error handling
    player.on('deviceError', function () {
        console.log('device error:', player.deviceErrorCode);
    });

    player.on('error', function (element, error) {
        console.error(error);
    });

    // user clicked the record button and started recording
    player.on('startRecord', function () {
        console.log('started recording!');
    });

    // user completed recording and stream is available
    player.on('finishRecord', function () {
        // the blob object contains the recorded data that
        // can be downloaded by the user, stored on server etc.
        console.log('finished recording: ', player.recordedData);

    });



    // AJAX function
    $('#submit').on('click', function () {
        var btn = $(this);
        btn.html('Saving...').prop('disabled', true).addClass('disable-btn');
        var audio_file_name = document.getElementById("myVar").value + '.webm';
        var As_id=document.getElementById("As_ID").value ;
        var q_id=document.getElementById("id").value ;
        var myFile = new File([player.recordedData], audio_file_name);
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var url = "";
        var data = new FormData();
        data.append('recorded_audio', myFile);
        data.append('csrfmiddlewaretoken', csrf);
        data.append('id',q_id);
        console.log(myFile)
        $.ajax({
            url: url,
            method: 'post',
            data: data,
            success: function (data) {
                window.location = "http://127.0.0.1:8000/Assessments/attempt/"+As_id+"";
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });

});