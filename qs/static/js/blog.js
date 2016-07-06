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
            $('#sideLiked')[0].innerHTML = data['voted'];
            $('#blog_sideLike')[0].innerHTML = data['status'];

        }
    });
});