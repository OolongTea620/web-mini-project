$(document).ready(function () {
    request_videoList();
});

function request_videoList() {
    fetch('/home').then((res) => res.json()).then((data) => {
        let videoList = data['res_videoList']

        videoList.forEach((video) => {
            let image = video['thumbnail_url']
            let title = video['title']

            let video_card = `<div class="card">
                                <img src="${image}" class="img-fluid card_image" alt="...">
                                <div class="card_title">${title}</div>
                              </div>`

            $('#card_list').append(video_card);
        })
    })
}

document.getElementById("addVideo_btn").onclick = function () {
    let url = "https://www.youtube.com/watch?v=XSKxJ7BpTyo";
    let mode = 'work';

    let formData = new FormData();
    formData.append('req_url', url)
    formData.append('req_mode', mode)

    fetch('/home', { method: "POST", body: formData }).then((res) => res.json()).then((data) => {
        alert(data['msg']);
    })
}