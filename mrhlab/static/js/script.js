$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    $(document).ajaxError(function (event, request) {
        var message = null;

        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        M.toast({html: message});
    });

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });

    // Bind a callback that executes when document.location.hash changes.
    $(window).bind('hashchange', function () {
        // Some browers return the hash symbol, and some don't.
        var hash = window.location.hash.replace('#', '');
        var url = null;
        if (hash === 'generate') {
            url = generate_page_url
        } else {
            url = intro_page_url
        }

        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
                activeM();
            }
        });
    });

    if (window.location.hash === '') {
        window.location.hash = '#intro'; // home page, show the default view
    } else {
        $(window).trigger('hashchange'); // user refreshed the browser, fire the appropriate function
    }

    function generate_ShortURL() {
        var content = $('#content-textarea').val();
        if (!content){
            M.toast({html: empty_body_error_message});
            return;
        }

        var data = {
            'content':content
        };

        $.ajax({
            type: 'POST',
            url: generate_page_url,
            data:JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
                activeM();
            }
        });
    }

    $(document).on('click', '#generate-ShortURL-btn', generate_ShortURL);



    function copy2clipboard() {
        var short_url = $('#short-url').text();

        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val(short_url).select();
        document.execCommand("copy");
        $temp.remove();

        M.toast({html: "Copied"});
    };

    $(document).on('click', '#copy-btn', copy2clipboard);

    function activeM() {
        $('.sidenav').sidenav();
        $('ul.tabs').tabs();
        $('.modal').modal();
        $('.tooltipped').tooltip();
        $('.dropdown-trigger').dropdown({
                constrainWidth: false,
                coverTrigger: false
            }
        );
    }




    activeM();  // initialize Materialize
});
