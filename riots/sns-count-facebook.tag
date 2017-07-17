<sns-count-facebook>

    <span>{ count }</span>

    <script>

        this.count = '( Loading... )'

        var self = this

        fetch( 'https://api.facebook.com/restserver.php?method=links.getStats&format=json&urls=' + opts.url )
        .then( function ( data ) {
            return data.json()
        } )
        .then( function ( json ) {
            self.count = json[ 0 ].total_count
            self.update()
        } )

    </script>

</sns-count-facebook>