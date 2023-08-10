$(document).ready(function () {
    let time = new Date().getHours();
    let mode;
    if (9 <= time && time <= 17) {
        mode = 'work'
    }
    else {
        mode = 'rest';
    }

    request_videoList();
});

function request_videoList(userMode) {
    let nextMode;
    if (userMode == 'work') {
        nextMode = 'rest';
    }
    else {
        nextMode = 'work';
    }

    $('#changeMode_btn').val(nextMode);

    $('#card_list').empty();

    let url = '/home?mode=' + userMode
    fetch(url).then((res) => res.json()).then((data) => {
        let videoList = data['res_videoList']

        videoList.forEach((video) => {
            let image = video['thumbnail_url']
            let title = video['title']
            let tagList = video['tag']

            let tags = "";
            for (let tag in tagList) {
                string = `<div class="card_tag">#${tagList[tag]}</div>\n`;
                tags += string;
            }

            let video_card = `<div class="card">
                                <img src="${image}" class="img-fluid card_image" alt="...">
                                <div class="card_title">${title}</div>
                                <div class="card_tags">
                                    ${tags}
                                </div>
                              </div>`

            $('#card_list').append(video_card);
        })
    })
}

document.getElementById("addVideo_btn").onclick = function () {
    let url = "https://www.youtube.com/watch?v=758K-5ztV74";
    let mode = 'work';
    let tag = '음악; 플레이리스트; 잔잔;';

    let formData = new FormData();
    formData.append('req_url', url)
    formData.append('req_mode', mode)
    formData.append('req_tag', tag)

    fetch('/home', { method: "POST", body: formData }).then((res) => res.json()).then((data) => {
        console.log(data);
        alert(data['msg']);
    })
}