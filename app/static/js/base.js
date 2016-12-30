   $(".button-collapse").sideNav();

           var clipboard = new Clipboard('#copy-button');

           clipboard.on('success', function(e) {
            Materialize.toast('Link Copied', 1000)
            e.clearSelection();
        });

        clipboard.on('error', function(e) {
            Materialize.toast('Copy error', 1500)
        });
