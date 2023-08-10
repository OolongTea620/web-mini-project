function insert_video(){
    let video_url = $("#video-url").val()
    let mode = $("input[name='mode']:checked").val()
    let type = $("input[name='type']:checked").val() //radio로 가정
    let tags = $("#tags").val()
    
    console.log(video_url)
    console.log(mode,type,tags)

    let formdata = new FormData()
    formdata.append("video_url", video_url)
    formdata.append("mode", mode) 
    formdata.append("type",type) 
    formdata.append("tags", tags) 
    
    fetch('/video/insert', { method: "POST", body: formdata, })
    .then((response) => response.json())
    .then((data) => {
        alert(data["result"]);
        // list 화면으로 가도록 추가
        window.location.href=""; 
    });
}