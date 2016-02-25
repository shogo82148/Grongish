(function() {
    var original = document.getElementById('original');
    var translated = document.getElementById('translated');
    var retranslated = document.getElementById('retranslated');
    var translate = document.getElementById('translate');

    translate.addEventListener('click', function() {
        var xhr = new XMLHttpRequest();
        var data = new FormData();
        data.append('text', original.value);
        data.append('retranslation', 'true');
        xhr.open('POST', 'http://www5170up.sakura.ne.jp/api/grongish/translate', true);
        xhr.responseType = 'json';
        xhr.addEventListener('load', function() {
            translated.value = xhr.response.translated[0];
            retranslated.value = xhr.response.retranslated[0];
        });
        xhr.addEventListener('error', function(e) {
            console.log(e);
        });
        xhr.send(data);
    });
})();
