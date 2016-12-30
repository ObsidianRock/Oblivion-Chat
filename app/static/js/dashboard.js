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

             $('#roomTable').append(data);
             $('#room_name').val('');
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

             $('#saverRoomTable').append(data);
             $('#room_id').val('');
            });
        });