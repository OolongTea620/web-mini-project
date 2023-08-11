$(document).ready(function () {
    $('#btn').val('work');
});

function change_mode(mode) {
    $('#btn').val(mode);
}

function insert_video(value) {
    let video_url = $('#url').val();
    let mode = value;
    // let type = $("input[name='type']:checked").val() //radio로 가정
    let tags = $("#tag").val();

    let formdata = new FormData()
    formdata.append("req_url", video_url);
    formdata.append("req_mode", mode);
    // formdata.append("type", type)
    formdata.append("req_tag", tags);

    fetch('/home', { method: "POST", body: formdata })
        .then((response) => response.json())
        .then((data) => {
            alert(data['msg']);
            window.location.href = '/';
        });
}