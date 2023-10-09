
$(document).ready(function () {
    $('#login').click(function(event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        var profile = $('#profile').val(); // Получаем значение поля профайла
        var email = $('#email').val(); // Получаем значение поля электронной почты
        // Выполняем GET-запрос с помощью jQuery
        $.get("http://localhost:8080/api/v1/authorize?profile="+encodeURIComponent(profile)+"&email="+encodeURIComponent(email), function (token) {
            // Сохраняем токен в сессии
            saveTokenToSession(token);
            window.location.replace('/');
        });
    });

    $('#register').click(function(event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        var profile = $('#profile-reg').val(); // Получаем значение поля профайла
        var email = $('#email-reg').val(); // Получаем значение поля электронной почты

        $.ajax({
            url: 'http://localhost:8080/api/v1/registration',
            type: 'POST',
            contentType: "application/json",
            headers: {'token': JWT},
            data: JSON.stringify({
                profile: profile,
                email: email
            }),
            success: function (data) {
                $('#profile-reg').val('');
                $('#email-reg').val('');
            }
        });
    });


});

// Сохранение токена в cookie
function saveTokenToSession(token) {
    // Устанавливаем срок действия cookie (например, 2 часа)
    var expires = new Date();
    expires.setTime(expires.getTime() + (2 * 60 * 60 * 1000));

    // Записываем токен в cookie
    document.cookie = "session_token=" + token + ";expires=" + expires.toUTCString() + ";path=/";
}

// Получение токена из cookie
function getTokenFromSession() {
    // Разбиваем cookie на отдельные значения
    var cookies = document.cookie.split(";");

    // Ищем нужное значение в cookie
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith("session_token=")) {
            return cookie.substring("session_token=".length, cookie.length);
        }
    }

    return null; // Если токен не найден
}

var JWT = getTokenFromSession();
let isLoad = JWT !== '{"message":"Access Denied"}' && JWT !== '' && JWT !== null;

if(isLoad){
    $('.auth-card').hide();

    $.ajax({
        url: 'http://localhost:8080/api/v1/callback?jwt=' + JWT,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if(data.isAdmin === false){
                $('.statistics-card').hide();
                $('.available-cars-card').hide();

            }
        }
    });

} else {
    //$('.information-leases-card').hide();
    //$('.book-car-card').hide();
    //$('.information-specific-card').hide();
    //$('.cancellation-rental-card').hide();
    //$('.completion-rental-card').hide();
}
