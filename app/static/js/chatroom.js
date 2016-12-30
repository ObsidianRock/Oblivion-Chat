$(document).ready(function(){

           var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

           function update_list(msg){
              $("#user_online").empty()
             for(var i = 0; i < msg.users.length; i++ ) {

                $("#user_online").append(msg.user_color[i]);

             };
           };

           function update_message_list(msg) {

              for(var i = 0; i < msg.length; i++) {

                 $("#messages").append(msg[i])
              };

           };

           socket.on('connect', function() {
                socket.send('i am connected');
           });

           socket.on('new connection', function(msg) {
               var n = msg.message.indexOf('not');

               if (n == -1) {
                   Materialize.toast(msg.message, 1200)
                }

                $("#stuff").text(msg.connections);
                update_list(msg);

            });

           socket.on('refresh', function(msg) {

              update_message_list(msg.message_list)

            });


            socket.on('user_left', function(msg) {
                Materialize.toast(msg.message, 1200);
                $("#stuff").text(msg.connections);
                update_list(msg);
            });

           socket.on('chat_response', function(msg){
                $("#messages").append(msg.string);
           });


           socket.on('typing_response',function(msg){
                                                    // need to come back to this again, maybe just hava solid block of color
                if (typing_check.num < 1) {
                    $("#type_span").text(msg.message );
                    $("#type_span").fadeIn(1200).fadeOut(1500)
                 }

           });

           $("#sendbutton").on('click', function(){
                socket.emit("chat_message", {"message":$("#mymessage").val(), "user":$("#current_user").text()});
                $("#mymessage").val('');
           });


        $('#mymessage').keypress(function(e) {
                var code = e.keyCode || e.which;
                if (code == 13) {
            socket.emit("chat_message", {"message":$("#mymessage").val(), "user":$("#current_user").text()});
                $("#mymessage").val('')
                }
            });

         $("#closebutton").on('click', function(){
                socket.emit("leave_room", {} );
                update_list(msg);
                socket.disconnect();
             });

        $("#logout").on('click', function(){
            socket.emit("leave_room", {} );
            update_list(msg);
            socket.disconnect();
         });

         $("#logout_2").on('click', function(){
                    socket.emit("leave_room", {} );
                    update_list(msg);
                    socket.disconnect();
            });

        $("#dashboard ").on('click', function(){
                socket.emit("leave_room", {} );
                update_list(msg);
                socket.disconnect();
            });

        });