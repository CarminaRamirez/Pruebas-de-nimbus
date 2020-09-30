function nombre(par, par2){
    return algo
}


function eliminar_elemento(pk, url, csrfmiddlewaretoken) {
    $.ajax({
        method: "POST",
        url: url,
        data: { pk: pk, csrfmiddlewaretoken: csrfmiddlewaretoken }
    })
    .done(function( datos ) {
        devuelve = datos
    })
    .fail(function( jqXHR, textStatus ) {
        devuelve = 'Oops!!', 'Encontramos un problema: ' + jqXHR + ' estado: ' + textStatus;
    });
    return devuelve
}

(function eliminar_popup($) {
    'use strict';
    $('.eliminar_banner').on('click', function() {
        var pk = $(this).data('pk');
        $.ajax({
            method: "POST",
            url: "/popup/eliminar/",
            data: { pk: pk, csrfmiddlewaretoken: '{{ csrf_token }}' }
        })
        .done(function( datos ) {
            alert(datos.mensaje);
            location.reload();
        })
        .fail(function( jqXHR, textStatus ) {
            alert('Oops!!', 'Encontramos un problema: ' + jqXHR + ' estado: ' + textStatus, 'danger');
        });
    });
})(jQuery);