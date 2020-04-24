var socket;
	$(document).ready(function() {
        window.a = 1;
	    function online() {
            var url = document.location.toString();
            var arrUrl = url.split("//");
            var start = arrUrl[1].indexOf("/");
            window.relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符
            if (relUrl.indexOf("?") != -1) {
                relUrl = relUrl.split("?")[0];
            };
            $.ajax({
                url: "/online",   //对应flask中的路由
                type: "POST", //请求方法
                data: {url: relUrl},   //传送的数据
                success: function (data) {  //成功得到返回数据后回调的函数
                    if(data.code == 1 ){
                        alert(data.msg);
                        window.location.href = "/room/" + hs
                    }
                    else{
        window.e = function(head, name, messages, f) {
                //head头像,name用户名,messages内容,f时间
                messages=rep(messages)
                var i = "<div class='message clearfix'><div class='user-logo'><img src='../" + head + "'/>" + "</div>" + "<div class='wrap-text'>" + "<h5 class='clearfix'>" + name + "</h5>" + "<div>" + messages + "</div>" + "</div>" + "<div class='wrap-ri'>" + "<div clsss='clearfix'><span>" + f + "</span></div>" + "</div>" + "<div style='clear:both;'></div>" + "</div>";
                $(".mes" + a).append(i);
                $(".chat01_content").scrollTop($(".mes" + a).height());
            };
        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function() {
                    var url = document.location.toString();
                    var arrUrl = url.split("//");
                    var start = arrUrl[1].indexOf("/");
                    window.relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符
                    if (relUrl.indexOf("?") != -1) {
                        relUrl = relUrl.split("?")[0];
                    };
                    socket.emit('joined', {msg: relUrl});
                });
        socket.on('head', function(data) {
                    if(data.code =="1"){
                        alert(data.msg);
                    }
                    else{
                        $(".room-logo").attr("src","../" + data.head);
                    }
                });
        socket.on('name', function(data) {
                    if(data.code =="1"){
                        alert(data.msg);
                    }
                    else{
                        $('.room_name').empty();
                        $(".room_name").append(data.name);
                        $('.keTitle').empty();
                        $(".keTitle").append(data.name);
                    }
                });
        socket.on('status', function(data) {
                    if(data.code =="1"){
                        alert(data.msg);
                    }
                    else{
                        //e(data.msg.head, data.msg.username, data.msg.msg, data.msg.time)
                        $(".msg b").remove();
                        $(".msg").append("<b>" + data.msg.username + data.msg.msg + "    " + data.msg.time + "</b>");
                    }
                    $.ajax({
                        url: "/users",   //对应flask中的路由
                        type: "POST", //请求方法
                        data: {url: relUrl},   //传送的数据
                        success: function (data) {  //成功得到返回数据后回调的函数
                            var arr = data.list;
                            $(".chat03_content ul li").remove();
                            for (j = 0, len = arr.length; j < len; j++) {
                                var i = "<li class=''><label class=" + arr[j].status + "></label><a href='javascript:;'><img src='../" + arr[j].head + "'></a><a href='javascript:;' class='chat03_name' onclick=$('.username').val(this.innerHTML);>" + arr[j].name + "</a></li>"
                                $(".chat03_content ul").append(i);
                                $(".chat03_title_t b").remove();
                                $(".chat03_title_t").append("<b>"+"在线人数:" + data.l_in + '/' + data.l_out+"</b>");

                            }
                            ;
                        }
                    })
                });
        socket.on('message', function(data) {
                    e(data.head, data.username, data.msg, data.time)
                });
        socket.on('delete', function(data) {
                    alert(data.msg)
                    window.location.href = "/";
                });
        $('#textarea').keypress(function(key) {
                    var code = key.keyCode || key.which;
                    if (code == 13) {
                        key.preventDefault();
                        text = $('#textarea').val();
                        if (text ==''){
                            alert('内容不能为空!!')
                        }
                        else {
                        $('#textarea').val('');
                        socket.emit('text', {msg: text, room: hs});
                        //e(b, username, mes(), time());
                        }

                    }
                });
        function init() {
            $.ajax({
                url: "/init",   //对应flask中的路由
                type: "POST", //请求方法
                data: {url: relUrl},   //传送的数据
                success: function (data) {  //成功得到返回数据后回调的函数
                    window.b = data.user.head;
                    window.username = data.user.name;
                    window.room = data.room;
                    window.hs = data.hs;
                    $(".room_name").append(room);
                    $(".room_hs").append(hs);
                    $(".keTitle").append(room);
                    $(".room-logo").attr("src","../" + data.head);
                    $(".web_index").append(document.location.toString());
                    //var arr = data.list;
                    //for (j = 0, len = arr.length; j < len; j++) {
                     //   var i = "<li class=''><label class=" + arr[j].status + "></label><a href='javascript:;'><img src='../" + arr[j].head + "'></a><a href='javascript:;' class='chat03_name'>" + arr[j].name + "</a></li>"
                    //    $(".chat03_content ul").append(i);
                    //}
                    //;
                    var comments = data.comments;
                    for (j = 0, len = comments.length; j < len; j++) {
                        e(comments[j].head, comments[j].name, comments[j].content, comments[j].time);
                    }
                    ;
                }
            })
        };
        init();

        function rep(messages) {
            //表情替代

            while(messages.indexOf("*#/emo_")!=-1) {
                messages = messages.replace("*#", "<img src='../static/files/").replace(".gif#*", ".gif'/>");
            };

            return messages;
        };
        //表情框
        $(".ctb01").mouseover(function () {
            $(".wl_faces_box").show()
        }).mouseout(function () {
            $(".wl_faces_box").hide()
        }),
            $(".wl_faces_box").mouseover(function () {
                $(".wl_faces_box").show()
            }).mouseout(function () {
                $(".wl_faces_box").hide()
            }),
            $(".wl_faces_main img").click(
                function () {
                    var a = $(this).attr("src");
                    $("#textarea").val($("#textarea").val() + "*#" + a.substr(a.indexOf("img/") + 16, 18) + "#*"),
                        $("#textarea").focusEnd(),
                        $(".wl_faces_box").hide()
                }),
            //发送按钮
            $(".chat02_bar img").click(function () {
                        text = $('#textarea').val();
                        if (text ==''){
                            alert('内容不能为空!!')
                        }
                        else {
                        $('#textarea').val('');
                        socket.emit('text', {msg: text, room: hs});
                        //e(b, username, mes(), time());
                        }

                    }),
            $.fn.setCursorPosition = function (a) {
                return 0 == this.lengh ? this : $(this).setSelection(a, a)
            },
            $.fn.setSelection = function (a, b) {
                if (0 == this.lengh)
                    return this;
                if (input = this[0], input.createTextRange) {
                    var c = input.createTextRange();
                    c.collapse(!0),
                        c.moveEnd("character", b),
                        c.moveStart("character", a),
                        c.select()
                } else
                    input.setSelectionRange && (input.focus(), input.setSelectionRange(a, b));
                return this
            },
            $.fn.focusEnd = function () {
                this.setCursorPosition(this.val().length)
            };



                    }
                }
            })
        }
        online();

                    $(".change_room_name_btn").click(function () {
                        text = $('.new_name').val();
                        if (text ==''){
                            alert('名称不能为空!!')
                        }
                        else {
                        $('.new_name').val('');
                        socket.emit('name', {msg: text, room: hs});
                        //e(b, username, mes(), time());
                        }

                    }),
                    $(".change_room_head_btn").click(function () {
                        alert('前端写不动了，头像就将就一下吧。。。');
                        //text = $('.new_name').val();
                        //if (text ==''){
                        //    alert('名称不能为空!!')
                        //}
                        //else {
                        //$('.new_name').val('');
                        //socket.emit('head', {msg: head, room: hs});
                        //e(b, username, mes(), time());
                        //}

                    }),
        $(".close_room_btn").click(function () {
            var url = document.location.toString();
            var arrUrl = url.split("//");
            var start = arrUrl[1].indexOf("/");
            window.relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符
            if (relUrl.indexOf("?") != -1) {
                relUrl = relUrl.split("?")[0];
            };
            function close_room() {
            socket.emit('delete', {msg: relUrl}, function() {
                alert('房间即将关闭')
                //alert('0')
                //socket.close();
                // go back to the login page
                //window.location.href = "{{ url_for('main.index') }}";
            });
        }
            close_room();
        });
        window.onbeforeunload=function() {
            var url = document.location.toString();
            var arrUrl = url.split("//");
            var start = arrUrl[1].indexOf("/");
            window.relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符
            if (relUrl.indexOf("?") != -1) {
                relUrl = relUrl.split("?")[0];
            };
            function leave_room() {
            socket.emit('left', {msg: relUrl}, function() {
                socket.disconnect();
                // go back to the login page
                window.location.href = "/room/" + hs;
            });
        }
            leave_room();
        };
    });
