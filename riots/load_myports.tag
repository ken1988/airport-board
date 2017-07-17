 <load_myports>
		<div class="panel panel-primary col-md-6 pull-left">
			<h2 class="sub-header">{ opts.country_name }空港リスト</h2>
			<table class="table table-hover" id="airport_panel">
				<thead>
					<tr>
						<th class="col-md-1">規模</th>
						<th class="col-md-3">空港コード</th>
						<th class="col-md-4">空港名</th>
						<th class="col-md-4">所在都市</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					<form method="post" action="/Airport" role="form" data-toggle="validator">
					<tr each={ list }>
					<td>{ portpoint }</td>
					<td>{ portcode }</td>
					<td>{ portname }</td>
					<td>{ location }</td>
					<td>
					<input type="hidden" name="origin_country" value="{ country_key }">
					<input type="hidden" name="mode" value="u">
					<input type="hidden" name="portid" id="portid" value="{ portkey }">
					<input type="button" value="空港デザイナ" id="{ portkey }" class="btn btn-primary apdez">
					</form>
					</td>
					</tr>
				</tbody>
			</table>
			<div class="form-inline form-group" id="new_airport_panel">
				<form method="post" action="/Airport" role="form" data-toggle="validator">
					<label>空港コード</label>
					<input type="text" name="portcode" class="form-control" placeholder="空港コード(3桁)">
					<label>空港名</label>
					<input type="text" name="portname" class="form-control" placeholder="空港名">
					<label>所在都市</label>
					<input type="text" name="location" class="form-control" placeholder="所在都市">
					<input type="hidden" name="origin_country" value="{ country_key }">
					<input type="hidden" name="mode" value="c">
					<input type="submit" class="btn btn-primary">
				</form>
			</div>
	</div>

  <script>
        fetch( '/port_list?country='+opts.country_name )
        .then( function ( data ) {
            return data.json()
        } )
        .then( function ( json ) {
        	this.list = json;
            this.update();
        }.bind(this));

  </script>
  <style>
    :scope { font-size: 2rem }
    h3 { color: #444 }
    ul { color: #999 }
  </style>
 </load_myports>