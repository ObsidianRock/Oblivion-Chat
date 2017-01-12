 $('#newRoomForm').on('submit', function(e) {
            e.preventDefault();
            console.log('prevented')
            $.ajax({
                type:'POST',
                url: '/newRoom',
                data: {
                      room_name: $('#room_name').val()
                }
            }).done(function(data){

              if (data.error){
                Materialize.toast('Something went wrong', 1000);
              }
              else {
                $('#roomTable').append(data.response);
                $('#room_name').val('');
                }
            });
        });

        $('#saveRoomForm').on('submit', function(e) {
            e.preventDefault();
            console.log('prevented')
            $.ajax({
                type:'POST',
                url: '/saveRoom',
                data: {
                      room_id: $('#room_id').val()
                }
            }).done(function(data){

              if (data.error){
                Materialize.toast('Something went wrong', 1000);
              }
              else {
                 $('#saverRoomTable').append(data.response);
                 $('#room_id').val('');
                }
            });
        });