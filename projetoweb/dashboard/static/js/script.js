var map = L.map('map').setView([-15.808110, -47.884321], 4);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 10,
    opacity: 1,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                }).addTo(map);


    var marker = L.marker([-15.808110, -47.884321]).addTo(map);
    var popup = L.popup();

    function onMapClick(e) {

    marker.remove();
    marker = L.marker(e.latlng).addTo(map);

    $('.loading-icon-principal').show();
    $('#endereco').hide();
        $('#coords').hide();
        $('#rua').hide();
        $('#cidade').hide();
        $('#estado').hide();
    
    var latlng = e.latlng;
    // Envia uma requisição AJAX para o servidor
    $.ajax({
        url: '/dados_fotovoltaicos/',
    data: {
    'latitude': latlng.lat,
    'longitude': latlng.lng
                        },
    success: function (data) {

        $.getJSON('https://nominatim.openstreetmap.org/reverse', {
            format: 'json',
            lat: latlng.lat,
            lon: latlng.lng
        }, function (result) {
            var address = result.address;
            var cidade = address.city || address.town || address.village || address.hamlet;
            var estado = address.state;
            var rua = address.road || address.street || address.pedestrian || address.footway || address.path;
            var endereco;

            $('.loading-icon-principal').hide();
            $('#endereco').show();
            $('#coords').show();
            $('#rua').show();
            $('#cidade').show();
            $('#estado').show();
            /* Verificação do Endereço */
            if (typeof cidade == 'undefined') {
                if (typeof estado == 'undefined') {
                    endereco = "Brasil";
                }
                else {
                    endereco = estado;
                }
            } else {
                endereco = cidade
            }

            document.getElementById("endereco").innerHTML = endereco;

            if (typeof rua == 'undefined') {
                rua = ''
            } else {
                rua = rua + ", "
            }

            document.getElementById("rua").innerHTML = rua;

            if (typeof cidade == 'undefined') {
                cidade = ''
            } else {
                cidade = cidade + ", "
            }

            document.getElementById("cidade").innerHTML = cidade;

            if (typeof estado == 'undefined') {
                estado = ''
            }

            document.getElementById("estado").innerHTML = estado;
            
            document.getElementById("coords").innerHTML = latlng.lat.toFixed(6) + "°, " + latlng.lng.toFixed(6) + "°";
            pvout = data['solar_data_pvout'].toFixed(1);
            document.getElementById("valor_pvout").innerHTML = pvout;
            ghi = data['solar_data_ghi'].toFixed(1);
            document.getElementById("valor_ghi").innerHTML = ghi;
            dni = data['solar_data_dni'].toFixed(1);
            document.getElementById("valor_dni").innerHTML = dni;
            gti = data['solar_data_gti'].toFixed(1);
            document.getElementById("valor_gti").innerHTML = gti;

            // Envia informações para forms do botão de favoritos 
            dadosEnergia = { producao_fotovoltaica: pvout, irradiacao_direta_normal: dni, irradiacao_global_horizontal: ghi, irradiacao_global_inclinada: gti };
            localizacao = { rua: rua, cidade: cidade, estado: estado, latitude: latlng.lat, longitude: latlng.lng };
            document.getElementById("nome").value = endereco;
            document.getElementById("dados_energia").value = JSON.stringify(dadosEnergia)
            document.getElementById("localizacao").value = JSON.stringify(localizacao)
        });
    }
    });

}
    map.on('click', onMapClick);
    layer = null;
    console.log("Layer antes do switch: ", layer);
    function Switch(nome) {

        var gif = '#loading-icon-' + nome
        var button = '#button-' + nome
        
        $(gif).show();
        $(button).hide();

    var arquivo = '/static/dados_energia/' + nome + '.tif';
    console.log(arquivo);
    fetch(arquivo)
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => {
        parseGeoraster(arrayBuffer).then(georaster => {

            if (layer != null) {
                console.log("Layer dentro do if", layer)
                map.removeLayer(layer);
                layer = null;
            }
            else {
                console.log("Primeiro mapa")
            }
            console.log("Layer depois do if: ", layer);

            layer = new GeoRasterLayer({
                georaster: georaster,
                opacity: 0.7,
                pixelValuesToColorFn: values => {
                    const value = values[0];
                    if (value < 1100) return '#8BED6B';
                    if (value < 1200) return '#ABF056';
                    if (value < 1300) return '#EEF743';
                    if (value < 1400) return '#FEF13C';
                    if (value < 1500) return '#FCD32D';
                    if (value < 1600) return '#FAAB19';
                    if (value < 1700) return '#F5820F';
                    if (value < 1800) return '#ED590E';
                    if (value < 1900) return '#D93523';
                    if (value < 2000) return '#B5163E';
                    return 'rgba(0, 0, 0, 0)';
                },
                resolution: 128
            });
            layer.addTo(map);
            $(gif).hide();
            $(button).show();
        });
                        });

}

    Switch('pvout');
