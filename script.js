(function() {
    var original = document.getElementById('original');
    var translated = document.getElementById('translated');
    var retranslated = document.getElementById('retranslated');
    var translate = document.getElementById('translate');
    var auto_detect = document.getElementById('auto-detect');
    var lang_grongish = document.getElementById('lang-grongish');
    var lang_ja = document.getElementById('lang-ja');
    var translated_lang_grongish = document.getElementById('translated-lang-grongish');
    var translated_lang_ja = document.getElementById('translated-lang-ja');
    var share_button = document.getElementById('twitter-share-button');

    original.value = decodeURIComponent(location.hash.replace(/^#/, ""));

    translate.addEventListener('click', function() {
        translate.disabled = true;
        var xhr = new XMLHttpRequest();
        var data = new FormData();
        data.append('text', original.value);
        data.append('retranslation', 'true');
        if (auto_detect.checked) {
            data.append('from', 'auto');
        } else if (lang_grongish.checked) {
            data.append('from', 'grongish');
        } else if (lang_ja.checked) {
            data.append('from', 'ja');
        }

        xhr.open('POST', 'https://shogo82148.com/api/grongish/translate', true);
        xhr.responseType = 'json';
        xhr.addEventListener('load', function() {
            translated.value = xhr.response.translated[0];
            retranslated.value = xhr.response.retranslated[0];

            // create share button
            while (share_button.firstChild) {
                share_button.removeChild(share_button.firstChild);
            }
            var link = document.createElement('a');
            link.href = "https://twitter.com/share";
            link.className = "twitter-share-button";
            link.innerHTML = "Tweet";
            link.dataset.url = location.protocol + "//" + location.host + location.pathname + "#" + encodeURIComponent(xhr.response.translated[0]);
            link.dataset.text = xhr.response.translated[0];
            link.dataset.hashtags = "グロンギ語語翻訳機";
            share_button.appendChild(link);
            twttr.widgets.load();

            var lang = xhr.response.lang;
            if (lang == "grongish") {
                lang_grongish.checked = true;
                translated_lang_ja.checked = true;
            } else {
                lang_ja.checked = true;
                translated_lang_grongish.checked = true;
            }
            translate.disabled = false;
        });
        xhr.addEventListener('error', function(e) {
            console.log(e);
            translate.disabled = false;
        });
        xhr.send(data);
    });

    function sync_lang() {
        if (lang_grongish.checked) {
            translated_lang_ja.checked = true;
        } else {
            translated_lang_grongish.checked = true;
        }
    }

    lang_grongish.addEventListener('change', sync_lang);
    lang_ja.addEventListener('change', sync_lang);
})();
