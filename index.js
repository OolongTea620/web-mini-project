var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

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
        $('#card_list').empty();
        $('#modal_list').empty();

        videoList.forEach((video) => {
            let image = video['thumbnail_url']
            let title = video['title']
            let tagList = video['tag']

            let youtubeId = video['video_id'];
            let youtubePlayer= youtubeId+'player';

            let tags = "";
            for (let tag in tagList) {
                string = `<div class="card_tag">#${tagList[tag]}</div>\n`;
                tags += string;
            }

            let video_card = `<div class="card" onclick="modalPlay('${youtubeId}','${youtubePlayer}')" data-bs-toggle="modal" data-bs-target="#${youtubeId}">
                                <img src="${image}" class="img-fluid card_image" alt="...">
                                <div class="card_title">${title}</div>
                                <div class="card_tags">
                                    ${tags}
                                </div>
                              </div>`
            let modal_card = `
            <div class="modal fade" id="${youtubeId}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog custom-modal">
                    <div class="modal-content">
                        <div class="modal-header">

                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                             <div id="${youtubePlayer}"></div>
                         </div>
                         <div class="modal-footer">
                         </div>
                    </div>
                </div>
            </div>`;
            

            $('#card_list').append(video_card);
            $('#modal_list').append(modal_card);
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
        window.location.reload();
    })
}

//유튜브 id베이스로 모달창 재생하기, 닫기버튼 누를시 멈추도록 
function modalPlay(youtubeId, youtubePlayer){
    let player;

$(`#${youtubeId}`).on('shown.bs.modal', function () {

    player = new YT.Player(`${youtubePlayer}`, {
       height: '350',
        width: '567',
        videoId: youtubeId,
        playerVars: {
            modestbranding: '1',
            showinfo: '0',
            autoplay: '1',
            rel: '0'
        },

        events: {
            'onReady': function (event) { event.target.playVideo(); }
        }
    });
});

$(`#${youtubeId}`).on('hidden.bs.modal', function () {
    player.stopVideo();
    var parent = $(`#${youtubePlayer}`).parent();
    parent.html(`<div id="${youtubePlayer}"></div>`);
});

}