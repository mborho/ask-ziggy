// Copyright 2009 Martin Borho <martin@borho.net>
// GPL - see License.txt for details
var oLangs = {
'dk':'Dansk','nl':'Nederlands','en':'English','fi':'Suomi','fr':'Français','de':'Deutsch',
'it':'Italiano','no':'Norsk','ro':'Română','ru':'Русский','es':'Español','tr':'Türkçe'}
var oGtlate = {'af':'Afrikaans','sq':'Albanian','ar':'Arabic','be':'Belarusian',
'bg':'Bulgarian','ca':'Catalan','zh-CN':'Chinese (Simplified)',
'zh-TW':'Chinese (Traditional)','hr':'Croatian','cs':'Czech','da':'Danish',
'nl':'Dutch','en':'English','et':'Estonian','tl':'Filipino','fi':'Finnish',
'fr':'French','gl':'Galician','de':'German','el':'Greek','ht':'Haitian Creole',
'iw':'Hebrew','hi':'Hindi','hu':'Hungarian','is':'Icelandic','id':'Indonesian',
'ga':'Irish','it':'Italian','ja':'Japanese','lv':'Latvian','lt':'Lithuanian',
'mk':'Macedonian','ko':'Korean','ms':'Malay','mt':'Maltese','no':'Norwegian',
'fa':'Persian','pl':'Polish','pt':'Portuguese','ro':'Romanian','ru':'Russian',
'sr':'Serbian','sk':'Slovak','sl':'Slovenian','es':'Spanish','sw':'Swahili',
'sv':'Swedish','th':'Thai','tr':'Turkish','uk':'Ukrainian','vi':'Vietnamese',
'cy':'Welsh','yi':'Yiddish'}
var oGlangs = {'lang_af':'Afrikaans',
'lang_ar':'Arabic','lang_be':'Belarusian','lang_bg':'Bulgarian','lang_ca':'Catalan',
'lang_zh-CN':'Chinese (Simplified)','lang_zh-TW':'Chinese (Traditional)','lang_hr':'Croatian',
'lang_cs':'Czech','lang_da':'Danish','lang_nl':'Dutch','lang_en':'English',
'lang_eo':'Esperanto','lang_et':'Estonian','lang_tl':'Filipino','lang_fi':'Finnish',
'lang_fr':'French','lang_de':'German','lang_el':'Greek','lang_iw':'Hebrew',
'lang_hu':'Hungarian','lang_is':'Icelandic','lang_id':'Indonesian','lang_it':'Italian',
'lang_ja':'Japanese','lang_ko':'Korean','lang_lv':'Latvian','lang_lt':'Lithuanian',
'lang_no':'Norwegian','lang_fa':'Persian','lang_pl':'Polish','lang_pt':'Portuguese',
'lang_ro':'Romanian','lang_ru':'Russian','lang_sr':'Serbian','lang_sk':'Slovak',
'lang_sl':'Slovenian','lang_es':'Spanish','lang_sw':'Swahili','lang_sv':'Swedish',
'lang_th':'Thai','lang_tr':'Turkish','lang_uk':'Ukrainian','lang_vi':'Vietnamese'}
var oGeditions = {'us':'U.S.','uk':'U.K.','au':'Australia','nl_be':'België',
'fr_be':'Belgique','ca':'Canada English','fr_ca':'Canada Français','cs_cz':'Česká republika',
'de':'Deutschland','es':'España','el_gr':'Ελλάδα','fr':'France','in':'India',
'en_ie':'Ireland','en_il':'Israel','it':'Italia','hu_hu':'Magyarország',
'nl_nl':'Nederland','nz':'New Zealand','no_no':'Norge','de_at':'Österreich',
'pl_pl':'Polska','pt-PT_pt':'Portugal','ru_ru':'Россия','de_ch':'Schweiz',
'fr_ch':'Suisse','en_za':'South Africa','sv_se':'Sverige','tr_tr':'Türkiye',
'ru_ua':'Украина','uk_ua':'Україна','ar_me':'العالم العربي', /*(Arab world)*/
'ar_ae':'الإمارات', /*(UAE)*/'ar_lb':'لبنان', /*(Lebanon)*/
'ar_sa':'السعودية',/* (KSA)*/'ar_eg':'مصر',/* (Egypt)*/'iw_il':'ישראל',/* (Israel)*/
'cn':'中国版','hk':'香港版','jp':'日本','kr':'한국','tw':'台灣版','hi_in':'भारत',
'en_my':'Malaysia','en_pk':'Pakistan','en_ph':'Philippines','en_sg':'Singapore',
'vi_vn':'Việt Nam','es_ar':'Argentina','pt-BR_br':'Brasil','es_cl':'Chile',
'es_co':'Colombia','es_cu':'Cuba','es_us':'Estados Unidos','es_mx':'México',
'es_pe':'Perú','es_ve':'Venezuela','en_bw':'Botswana','en_et':'Ethiopia',
'en_gh':'Ghana','en_ke':'Kenya','en_na':'Namibia','en_ng':'Nigeria',
'fr_sn':'Sénégal','en_tz':'Tanzania','en_ug':'Uganda','en_zw':'Zimbabwe'}
var oWpedia = {'ar':'العربية','ca':'Català',
'cs':'Česky','da':'Dansk','de':'Deutsch','en':'English','es':'Español',
'eo':'Esperanto','fr':'Français','ko':'한국어','id':'Bahasa Indonesia',
'it':'Italiano','he':'עברית','lt':'Lietuvių','hu':'Magyar','nl':'Nederlands',
'ja':'日本語','no':'Norsk (bokmål)','pl':'Polski','pt':'Português','ru':'Русский',
'ro':'Română','sk':'Slovenčina','sr':'Српски','fi':'Suomi','sv':'Svenska',
'tr':'Türkçe','uk':'Українська','vi':'Tiếng Việt','vo':'Volapük','zh':'中文'}
var oImdb = {'en':'English','de':'Deutsch','fr':'Français',
'es':'Español','it':'Italiano','pt':'Português'}
var oAmazon = {'com':'US','co.uk':'UK','ca':'Canada',
'cn':'China','fr':'France','de':'Germany','co.jp':'Japan'}
var oMusic = {'artist':'Artist','release':'Release','track':'Track'}
var oMaemo = {'talk':'Talk','packages':'Packages','wiki':'Wiki',}

var ServiceOptions = function() {

    return {
        imdb:oImdb,
        wikipedia:oWpedia,
        amazon:oAmazon,
        music:oMusic,
        maemo:oMaemo,
        web:oLangs,
        news:oLangs,
        weather:oLangs,
        gweb:oGlangs,
        gnews:oGeditions,
        tlate_from:oGtlate,
        tlate_to:oGtlate,

        get : function(service, index, short) {
            var lang_list = ServiceOptions[service]
            if( index > -1) {
                return lang_list[index]
            } else if (short != '') {
                for(var shorty in lang_list) {
                    if (short == shorty) {
                        return {shorty:lang_list[short]}
                    }
                }
            } else {
                return lang_list;
            }
        }
    }

} ();
