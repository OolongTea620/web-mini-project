$(document).ready(function () {
    request_movie();
});

function request_movie() {
    fetch('/home').then((res) => res.json()).then((data) => {
        let movies = data['videos']

        movies.forEach((movie) => {
            let writer = movie['writer'];
            let thumbnail_url = movie['thumbnail_url'];
            let video_url = movie['video_url'];

            let movie_card = `<div class="card">
                                <img src="${thumbnail_url}" class="img-fluid card_image" alt="...">
                                <div class="card_title">${video_url}</div>
                                <button class="card_button">보러 가기 -></button>
                              </div>`

            $('#card_list').append(movie_card);
        })
    })
}