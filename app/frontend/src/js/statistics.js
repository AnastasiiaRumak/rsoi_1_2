$('.open-statistics').click(function (e) {

    let isClosed = $(this).attr('value');
    if (isClosed === 'true') {
        $('.open-statistics').text('Открыть статистику');
        $(this).attr('value', 'false');
        $('.statistic-table').text('');
    } else {
        $('.open-statistics').text('Закрыть статистику');
        $(this).attr('value', 'true');

        $.ajax({
            url: 'http://localhost:8080/api/v1/statistic',
            type: 'GET',
            dataType: 'json',
            headers: {'token': JWT},
            success: function (res) {
                var data = JSON.parse(res.message);

                var table = $("<table style='border-width: 1px !important;'></table>");

                var thead = $("<thead></thead>");
                var tr = $("<tr></tr>");
                tr.append($("<th>ID</th>"));
                tr.append($("<th>Message</th>"));
                tr.append($("<th>Service</th>"));
                tr.append($("<th>Username</th>"));
                tr.append($("<th>Datetime</th>"));
                thead.append(tr);
                table.append(thead);

                var tbody = $("<tbody></tbody>");
                for (var i = 0; i < data.length; i++) {
                    var row = $("<tr></tr>");
                    row.append($("<td>" + data[i].id + "</td>"));
                    row.append($("<td>" + data[i].message + "</td>"));
                    row.append($("<td>" + data[i].service + "</td>"));
                    row.append($("<td>" + data[i].username + "</td>"));
                    row.append($("<td>" + data[i].datetime + "</td>"));
                    tbody.append(row);
                }
                table.append(tbody);


                $('.statistic-table').append(table);
            }
        });

    }

});


