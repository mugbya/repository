/**
 * Created by mugbya on 2016/7/3.
 */


$('#blog_sideLike').click(function() {
    //url = "{% url 'blog:voted' %}";
    url = '/blog/voted/';
    is_click = $('#blog_sideLike').val();
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
            $('#blog_sideLike').val(data['status']);
            $('#sideLiked')[0].innerHTML = data['voted'];
            if('click' == data['status']){
                $('#blog_sideLike')[0].innerHTML = '推荐';
            }else{
                $('#blog_sideLike')[0].innerHTML = '已推荐';
            }
        }
    });
});