$('#btn-token').click(function (e) {
    e.preventDefault();
    alert('kek');
    $('.cars-reservations').text('');

    //const baseUrl = 'http://localhost:8070/api/v1/cars';
    const baseUrl = 'http://localhost:8080/api/v1/cars';

    const page = 1; // Замените на необходимую страницу
    const size = 10; // Замените на необходимый размер страницы
    const showAll = true; // Замените на true, чтобы показать все автомобили, или на false, чтобы показать только доступные

    //const url = `${baseUrl}?page=${page}&size=${size}&showAll=${showAll}`;
    const url = 'api/v1/cars?page='+page+'&size='+size+'&showAll='+showAll;

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let i = 0;
            $('.cars-reservations').append('<hr class="hr-type-1">');

            data.forEach(function (car) {
                const availability = car.availability ? 'Доступно' : 'В резерве';

                const carInfo = `<dl><dt>${car.brand} ${car.model}</dt><dd>Регистрационный номер: ${car.registration_number}</dd><dd>Мощность: ${car.power}</dd><dd>Цена: ${car.price}</dd><dd>Тип: ${car.type}</dd><dd>Статус: ${availability}</dd></dl>`;

                $('.cars-reservations').append(`${carInfo}<hr class="hr-type-2">`);
                i++;
            });
        }
    });
});

$(document).on("click", ".btn-finish-rental", function (e) {
    e.preventDefault();
    let i = $(this).attr('value');
    let rentalUid = $(`input[id="rentalUid${i}"]`).val(); // Предположим, что у вас есть элементы с id, содержащими "rentalUid".
    const today = new Date();
    const formattedDate = today.toISOString().slice(0, 10);

    $.ajax({
        url: 'http://localhost:8080/api/v1/rental/'+rentalUid+'/finish',
        type: 'POST',
        contentType: "application/json",
        headers: {'token': JWT},
        data: JSON.stringify({
            condition: 'EXCELLENT',
            date: formattedDate
        }),
        success: function (data) {
            loadHeader();
            $('.btn-token').trigger('click');
        }
    });

});