$(document).ready(function(){
    init();
});

function init(){
    init_hide_btn();
    init_reply_btn();
    init_topic_btn();
    init_root_del_btn();
}

function get_data_id(self, p){
    return $(self).parents(p).attr('data-id');
}

function init_hide_btn(){
    let hide_btns = $('.hide-btn');
    for(let i=0; i<hide_btns.length; i++){
        $(hide_btns[i]).click(function(){
            let root = $(this).parents('div.card-wrap');
            let node = '<div class="hide" style="display: none;">显示此条</div>'
            root.parent().append(node);

            root.slideUp('fast', function(){
                $('.hide').fadeIn('slow');
                $('.hide').click(function(){
                    root.slideDown('fast');
                    $(this).remove();
                });
            });
        });
    }
}

function init_reply_btn(){
    let reply_btns = $('.reply-btn');

    for(let i=0; i<reply_btns.length; i++){
        $(reply_btns[i]).click(function(){
            let root = $(this).parents('div.card-wrap');
            let relpy_box_wrap = root.find('div.reply-box-wrap');
            let text_wrap = root.find('div.textarea-wrap');

            if (relpy_box_wrap.css('display') == 'none'){
                relpy_box_wrap.slideDown();
                relpy_box_wrap.css('display', 'block');
            }else{
                relpy_box_wrap.slideUp();
            }
                
            text_wrap.find('.sbt-btn').unbind('click').click(function(){
                let data_id = get_data_id(this, 'div.card');
                let text_node = $(this).prev();
                let text = text_node.val();
                let self = this;
                if(text.length > 0 && text.length <= 255){
                    $.post('reply', {text: text, data_id: data_id}).done(function(){
                        
                        let node = '<div class="reply"><div class="time">刚刚</div>'+
                        '<span class="text">' + text + '</span></div>'
                        let reply_box = $(self).parents('div.card').find('div.reply-box');

                        if(reply_box.css('display') == 'none'){
                            reply_box.css('display', 'block');
                        }

                        reply_box.append(node);
                        text_node.val("");
                        reply_box.scrollTop(100000); // 这里用了一个比较敷衍的办法
                    });

                    $(this).parent().parent().hide('fast');
                }
            });
        });
    }
}

function init_topic_btn(){
    let topic_btns = $('.topic_btn');
    if(topic_btns){
        for(let i=0; i<topic_btns.length; i++){
            $(topic_btns[i]).unbind('click').click(function(){
                let data_id = get_data_id(this, 'div.card');
                $.post('topic', {data_id: data_id}).done(function(){
                    window.location.reload();
                    window.location.reload();
                });
            });
        }
    }
}

function init_root_del_btn(){
    let delete_btns = $('.delete-btn');

    if(delete_btns){
        for(let i=0; i<delete_btns.length; i++){
            $(delete_btns[i]).unbind('click').click(function(){
                if($(this).parent().attr('class') == 'operation'){
                    let data_id = get_data_id(this, 'div.card');
                    let root = $(this).parents('div.card');
                    if(confirm('确定要删除留言吗？')){
                        $.post('delete', {data_id: data_id}).done(function(){
                            root.hide('fast');
                        });
                    }
                }else{
                    let data_id = get_data_id(this, 'div.reply')
                    let root = $(this).parents('div.reply')
                    if(confirm('确定要删除回复吗？')){
                        $.post('delete_reply', {data_id: data_id}).done(function(){
                            root.hide('fast');
                        });
                    }
                }
            });
        }
    }
}
