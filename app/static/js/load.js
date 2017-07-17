/**
 * Created by TU on 2017/7/17.
 */
$(document).ready(function () {
    var current_page = 1;
    var category_index = 0;
    var $lb = $('#load-button');
    <!-- var category = ['all','douban','guoke','zhihu'] -->
    var category = ['douban', 'douban', 'guoke', 'zhihu']
    $('#nav-tab li').each(function () {
        $(this).click(function () {
            if (!$(this).hasClass('active')) {
                $(this).addClass('active').siblings().removeClass('active');
                category_index = $(this).index();
                current_page = 1;
                $('aside:first article').remove();
                $lb.trigger("click");

            }
        })
    })


    $(document).ajaxSend(function () {
        $lb.attr('disabled', 'disabled');
        $lb.html("<a>loading</a>");
    })
    $lb.on('click', function () {
        $.ajax(
            {
                url: window.location.protocol + "//" + window.location.host + '/api/' + category[category_index] + '/article?page=' + current_page,
                dataType: 'json',
                type: 'get',
                success: function (data) {
                    current_page++;
                    $.each(data['article_resource'], function (index, item) {
                        if (item['content'].substring(0, 4) !== 'http') {
                            var $h = ' <article> <div class="content col-md-10" > <div class="title"> <a  target="_blank" href=""></a> </div> <p> </p> </div> <div class="pic col-md-2" > <a  target="_blank" ></a> </div></article>'
                            if ($('aside:first article:last').length == 0) {
                                $('aside:first ').prepend($h);
                            }
                            else {
                                $('aside:first article:last').after($h);
                            }
                            $('aside:first article:last div:first div[class="title"] a').attr('href', item['message_url']).text(item['title']);
                            $('aside:first article:last div:first p ').text(item['content']);
                            $('aside:first article:last div:last a').attr('href', item['message_url']).css('background-image', 'url(' + item['image_url'] + ')');

                        } else {
                            var $h = '<article> <div class="full-pic"> <div class="title"> <a  target="_blank"></a> </div> <div class="first-pic"> <a  target="_blank" ><img></a> </div> <div class="other-pic"> <a target="_blank" >  </a> </div> </div> </article>'
                            $('aside:first article:last').after($h);
                            $('aside:first article:last div:first div[class="title"] a').attr('href', item['message_url']).text(item['title']);
                            $('aside:first article:last div:first div[class="first-pic"] a').attr('href', item['message_url']);
                            $('aside:first article:last div:first div[class="first-pic"] a img').attr('src', item['image_url']);
                            $('aside:first article:last div:first div[class="other-pic"] a').attr('href', item['message_url']);
                            var im = item['content'].split(",");
                            for (var i in im) {
                                var $s = '<span style="background-image:url(' + im[i] + ')"></span>';
                                $('aside:first article:last div:first div[class="other-pic"] a').append($s);
                            }


                        }
                        if (data['has_next']) {
                            $lb.removeAttr('disabled');
                            $lb.html("<a>加载更多</a>");

                        } else {
                            console.log(data['has_next']);
                            $lb.attr('disabled', 'disabled');
                            $lb.html("<a>暂无更多</a>");
                        }

                    })

                }
            }
        )
    })
    $lb.trigger("click");
})