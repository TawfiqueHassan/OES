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

    // create player
    var player2 = videojs('myAudio2', options, function () {
        // print version information at startup
        var msg = 'Using video.js ' + videojs.VERSION +
            ' with videojs-record ' + videojs.getPluginVersion('record') +
            ', videojs-wavesurfer ' + videojs.getPluginVersion('wavesurfer') +
            ', wavesurfer.js ' + WaveSurfer.VERSION + ' and recordrtc ' +
            RecordRTC.version;
        videojs.log(msg);
    });

    // error handling
    player2.on('deviceError', function () {
        console.log('device error:', player2.deviceErrorCode);
    });

    player2.on('error', function (element, error) {
        console.error(error);
    });

    // user clicked the record button and started recording
    player2.on('startRecord', function () {
        console.log('started recording!');
    });

    // user completed recording and stream is available
    player2.on('finishRecord', function () {
        // the blob object contains the recorded data that
        // can be downloaded by the user, stored on server etc.
        console.log('finished recording: ', player2.recordedData);

        $('#submit').prop('disabled', false);
        $('#submit').removeClass('disable-btn');
    });





    // AJAX function
    $('#submit').on('click', function () {
        var btn = $(this);
        btn.html('Saving...').prop('disabled', true).addClass('disable-btn');
        var audio_file_name = document.getElementById("myVar").value + '.webm';
        var audio_file_name2=document.getElementById("myVar2").value + '.webm';
        var myFile = new File([player.recordedData], audio_file_name);
        var myFile2 = new File([player2.recordedData], audio_file_name2);
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var url = "";
        var data = new FormData();
        data.append('recorded_audio', myFile);
        data.append('recorded_audio2', myFile2);
        data.append('csrfmiddlewaretoken', csrf);
        console.log(myFile)
        console.log(myFile2)
        $.ajax({
            url: url,
            method: 'post',
            data: data,
            success: function (data) {
                window.location = "http://127.0.0.1:8000/ExamCohort/";
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });

});