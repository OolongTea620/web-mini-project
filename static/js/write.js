function insert_video() {
    let video_url = $('#url').val();
    let mode = $("#mode").val();
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
            window.location.href = '/';
        });
}