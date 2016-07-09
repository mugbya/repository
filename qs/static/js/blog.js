/**
 * Created by mugbya on 2016/7/3.
 */


// 防止跨域，只能写在模板中暂时不能独立
$('#blog_sideLike').click(function() {
    //url = "{% url 'blog:vote' %}";
     url = '/blog/vote/';
    // is_click = $('#blog_sideLike').val();
    is_click = $('#blog_sideLike')[0].innerHTML;
    $.ajax({
        url: url,
        method: 'POST', // or another (GET), whatever you need
        dataType:'json',
        data: {
            'id': window.location.href,
            'content': is_click,
            //'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function (data) {
            $('#sideLiked')[0].innerHTML = data['voted'];
            $('#blog_sideLike')[0].innerHTML = data['status'];

        }
    });
});


// 博客收藏功能
$('.blog_favorite').click(function () {
    //url = "{% url 'blog:favorite' %}";
    url = '/blog/favorite/';
    is_favorite = $('.is_favorite')[0].innerHTML;
    //is_click = $('#blog_sideLike')[0].innerHTML;
    $.ajax({
        url: url,
        method: 'POST', // or another (GET), whatever you need
        dataType: 'json',
        data: {
            'id': window.location.href,
            'is_favorite': is_favorite,
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