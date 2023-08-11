function registerPage() {
    window.location.href = '/register';
}

function loginPage() {
    window.location.href = '/login';
}

function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!');
    window.location.href = '/';
}
console.log({ nickname })

function login() {
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: { id_give: $('#userid').val(), pw_give: $('#userpw').val() },
        success: function (response) {
            if (response['result'] === 'success') {
                $.cookie('mytoken', response['token']);

                alert('로그인 완료!')
                window.location.href = '/auth'
            } else {
                alert(response['msg'])
            }
        }
    })
}

function register() {
    let id = $('#userid').val();
    let pw = $('#userpw').val();
    let nickname = $('#usernick').val();

    if (id.trim() === '' || pw.trim() === '' || nickname.trim() === '') {
        alert('값을 입력해주세요.');
        return; 
    }

    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: id,
            pw_give: pw,
            nickname_give: nickname 
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert(response['msg'])
            }
        }
    })
}