var MAXWIDTH = 330;
var MAXHEIGHT = 230;
var JCROPRATIO = 1;
jQuery(function($){
    var jcrop_api, boundx, boundy;
    FileReader = window.FileReader;
    $("#mugshot").change(function(){
    var image = document.createElement('img');
        var width = MAXHEIGHT;
        var height = MAXHEIGHT;
        $('#avatar').css('max-width', MAXWIDTH);
        $('#avatar').css('max-height', MAXHEIGHT);
        $('#avatar').css('width', MAXWIDTH);
        $('#avatar').css('height', MAXHEIGHT);
        $('#avatar').css('overflow', 'hidden');
        if(jcrop_api != null){
        jcrop_api.destroy();
    }
        if(FileReader){
            //Firefox
        var reader = new FileReader();
            var file = this.files[0];
            reader.readAsDataURL(file);
            reader.onload = function(e){
        image.src = this.result;
                image.id = "image";
                $("#preview").attr("src", this.result);
                //设置长宽比,延迟0.4秒
                setTimeout(function(){
            width = image.width;
                    height = image.height;
                    var rat;
                    if(width > MAXWIDTH){
            rat = MAXWIDTH/width;
                        width = MAXWIDTH;
                        height = height*rat;
            }
                    if(height > MAXHEIGHT){
            rat = MAXHEIGHT/height;
                        height = MAXHEIGHT;
                        width = width*rat;
            }
                    image.width = width;
                    image.height = height;
                    $("#avatar").html(image);
                    $("#preview").css({
                width: width,
                        height: height
                });
                    $(image).Jcrop({
            aspectRatio: JCROPRATIO,
                        onChange: updatePreview,
                        onChange: updateCoords,
                        onSelect: updateCoords,
                        onSelect: updatePreview,
                        onRelease: clearCoords
            },function(){
                        jcrop_api = this;
                    });
        }, 500); //设定时间延迟结束
        };
    }else{
        //IE
            var path = $(this).val();
            image.src = path;
            image.id = "image";
            $("#preview").attr("src", path);
            $("#avatar").html(image);
            $(image).Jcrop({
        aspectRatio: JCROPRATIO,
                onChange: updatePreview,
                onChange: updateCoords,
                onSelect: updateCoords,
                onSelect: updatePreview,
                onRelease: clearCoords
        },function(){
                jcrop_api = this;
            });
            //设置长宽比
            width = image.width;
            height = image.height;
            while(width > MAXWIDTH || height > MAXHEIGHT){
        var rat;
                if(width > MAXWIDTH){
            rat = MAXWIDTH/width;
                    width = MAXWIDTH;
                    height = height*rat;
        }
                if(height > MAXHEIGHT){
                    rat = MAXHEIGHT/height;
                    height = MAXHEIGHT;
                    width = width*rat;
        }
        }
            $(image).css('width', width);
            $(image).css('height', height);
            $("#preview").css({
        width: width,
                height: height
        });
    }
    });

    function clearCoords(){
        $('#id_x1').val("");
        $('#id_y1').val("");
        $('#id_x2').val("");
        $('#id_y2').val("");
        $('#id_w').val("");
        $('#id_h').val("");
    };

    function updateCoords(c){
        $('#id_x1').val(Math.round(c.x));
        $('#id_y1').val(Math.round(c.y));
        $('#id_x2').val(Math.round(c.x2));
        $('#id_y2').val(Math.round(c.y2));
        $('#id_w').val(Math.round(c.w));
        $('#id_h').val(Math.round(c.h));
    };

    function updatePreview(c){
        if( parseInt(c.w)> 0){
        boundx = $("#image").width();
            boundy = $("#image").height();
            if (parseInt(c.w) > 0){
                var rx = 100 / c.w;
                var ry = 100 / c.h;
                $("#preview").css({
                    width: Math.round(rx * boundx) + 'px',
                    height: Math.round(ry * boundy) + 'px',
                    marginLeft: '-' + Math.round(rx * c.x) + 'px',
                    marginTop: '-' + Math.round(ry * c.y) + 'px'
                });
            }
        }
    };

});