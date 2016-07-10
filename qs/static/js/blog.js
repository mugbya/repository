/**
 * Created by mugbya on 2016/7/3.
 */


// 获取 csrftoken
jQuery(document).ajaxSend(function(event, xhr, settings) {
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


$('.blog_vote').click(function() {
    //url = "{% url 'blog:vote' %}";
     url = '/blog/vote/';
    is_click = $('.is_vote')[0].innerHTML;
    $.ajax({
        url: url,
        method: 'POST', // or another (GET), whatever you need
        dataType:'json',
        data: {
            'id': window.location.href,
            'is_click': is_click,
            //'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function (data) {
            if(data['fail']){
                window.location.href = '/user/login/?next=/blog/'+data['id']+'/';
            }else {
                $('#blog_vote_num')[0].innerHTML = data['voted'];
                $('.is_vote')[0].innerHTML = data['is_vote'];
                if(data['is_vote']) {
                    $('#blog_voted').show();
                    $('#blog_vote').hide();
                }else {
                    $('#blog_voted').hide();
                    $('#blog_vote').show();
                }
            }
        }
    });
});


// 博客收藏功能
$('.blog_favorite').click(function () {
    //url = "{% url 'blog:favorite' %}";
    url = '/blog/favorite/';
    is_favorite = $('.is_favorite')[0].innerHTML;
    $.ajax({
        url: url,
        method: 'POST', // or another (GET), whatever you need
        dataType: 'json',
        data: {
            'id': window.location.href,
            'is_favorite': is_favorite
            //'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function (data) {
            if(data['fail']){
                window.location.href = '/user/login/?next=/blog/'+data['id']+'/';
            }else {
                $('#blog_favorite_num')[0].innerHTML = data['favorite'];
                $('.is_favorite')[0].innerHTML = data['is_favorite'];
                if(data['is_favorite']) {
                    $('#blog_favorited').show();
                    $('#blog_favorite').hide();
                }else {
                    $('#blog_favorited').hide();
                    $('#blog_favorite').show();
                }
            }
        }
    });
});