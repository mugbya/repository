/**
 * Created by mugbya on 16-11-11.
 */
// 获取 csrftoken
jQuery(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


$(function () {
    $('.username').blur(function () {
        var username = $('.username').val();
        if (username.length == 0 || username.length > 20) {
            $('.username-error').html('<strong>*</strong>  请输入不超过20个字符的用户名');
            $('.username-error').show();
        }
    });

    $('.email').blur(function () {
        var email = $('.email').val();
        if (email.length > 0) {
            if (!/^w+([-+.]w+)*@w+([-.]w+)*.w+([-.]w+)*$/.test(email)) {
                $('.username-error').html('<strong>*</strong>  请输入正确的邮箱格式');
                $('.username-error').show();
            }
        }

    });

});

// 注册
$(function () {
    $('.register-btn').on('click', function () {

        var username = $('.username').val();
        var email = $('.email').val();
        var password = $('.password').val();

        if (username.length == 0 || username.length > 20) {
            $('.username-error').html('<strong>*</strong>  请输入不超过20个字符的用户名');
            $('.username-error').show();
            return
        }

        if (email == undefined || email.length == 0) {
            $('.email-error').html('<strong>*</strong>  请输入邮箱');
            $('.email-error').show();
            return
        }

        if (password == undefined || password.length == 0) {
            $('.password-error').html('<strong>*</strong>  请输入密码');
            $('.password-error').show();
            return
        }

        $.post('/user/register/', {
            'username': username,
            'email': email,
            'password': password
        }, function (data, status) {
            if (data['result'] == 'success') {
                window.location.href = '/';
            } else {

            }

        });

    });
});