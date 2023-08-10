$(document).ready(function () {
    request_videoList();
});

function request_videoList() {
    fetch('/home').then((res) => res.json()).then((data) => {
        let videoList = data['res_videoList']

        videoList.forEach((video) => {
            let image = video['thumbnail_url']
            let title = video['title']
            let tagList = video['tag']
            
            let tags = "";
            for (tag in tagList) {
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
    let url = "https://www.youtube.com/watch?v=XCDeyqIrfN8";
    let mode = 'rest';
    let tag = '메타코미디클럽; 메코클;'

    let formData = new FormData();
    formData.append('req_url', url)
    formData.append('req_mode', mode)
    formData.append('req_tag', tag)

    fetch('/home', { method: "POST", body: formData }).then((res) => res.json()).then((data) => {
        console.log(data);
        alert(data['msg']);
    })
}