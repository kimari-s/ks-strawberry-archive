#!/usr/bin/perl


sub ust_renewcache
{
	my $cache = $ust_cache;

	## cache Time/sec
	my $cachetime = $ust_cachetime;

	## CHANNEL NAME
	@channel = (
	['REDACTED','REDACTED','REDACTED'], # REDACTED
	);

	## USTREAM.tv API Key Register
	## http://developer.ustream.tv/user/register
	$apikey = 'REDACTED';

	# Twitter
	my %CONSUMER_TOKENS = (
	    consumer_key    => 'REDACTED',
	    consumer_secret => 'REDACTED',
    #API1.1暫定対応
    apiurl                => 'https://api.twitter.com/1.1',
    searchapiurl          => 'https://api.twitter.com/1.1/search',
    search_trends_api_url => 'https://api.twitter.com/1.1',
    lists_api_url         => 'https://api.twitter.com/1.1',
    ssl => 1,
	);
	my $ACCESS_TOKEN        = 'REDACTED';
	my $ACCESS_TOKEN_SECRET = 'REDACTED';


	open(FH, "$cache");
	$i = 0;
	while (<FH>) {
		while ($_ =~ /^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$/g) {
			for($j = 0; $j < 8+1; $j++) {
				$channelcache[$i][$j] = ${$j+1};
			}
		}
		$i++;
	}
	close(FH);


	@cache = stat($cache);
	$now = time();
	$cachetime = $cache[9] + $cachetime;

	if($cachetime < $now){

		flock(FH, LOCK_EX);
		open(FH,">$cache");

		for ($i = 0; $i < $#channel+1; $i++) {

			use LWP::Simple qw($ua get);

			#sjisからut8に変換しておかないと日本語のチャンネルが取得できない
			$channel = $channel[$i][1];
			use Jcode;
			&Jcode::convert( \$channel, "utf8", "sjis" );

			my $uri = 'http://api.ustream.tv/xml/channel/'.$channel.'/getinfo?key='.$apikey;
			$doc = get($uri);


			$doc  =~ /<title><!\[CDATA\[(.*?)\]\]><\/title>/;
			$title = $1;
			&Jcode::convert( \$title, "sjis", "utf8" );

			$doc  =~ /<status><!\[CDATA\[(.*?)\]\]><\/status>/;
			$status = $1;

			$doc  =~ /<id>(.*?)<\/id>/;
			$id = $1;

			if( $doc  =~ /<small><!\[CDATA\[(.*?)\]\]><\/small>/ ){
				$icon = $1;
			}else{
				$icon = 'http://static-cdn1.ustream.tv/static/images/defaults/user_90x90:1.png';
			}

			$doc  =~ /<lastStreamedAt><!\[CDATA\[(.*?)\]\]><\/lastStreamedAt>/;
			$lastStreamedAt = $1;

			$doc  =~ /<views>(.*?)<\/views>/;
			$views = $1;


			$channel[$i][3] = $status;
			$channel[$i][4] = $icon;
			$channel[$i][5] = $title;
			$channel[$i][6] = $lastStreamedAt;
			$channel[$i][7] = $views;
			$channel[$i][8] = $id;

			for($j = 0; $j < 8+1; $j++) {
				if($j){print FH "\t";}
				print FH "$channel[$i][$j]";
			}
			print FH "\n";

			#新たにLIVEになったチャンネルをチェック

			#Twitter投稿
			if($channel[$i][3] eq 'live' && $channelcache[$i][3] ne 'live' && $channel[$i][1] eq $channelcache[$i][1]){
				use Net::Twitter::Lite;
				my $twit = Net::Twitter::Lite->new(%CONSUMER_TOKENS);
				$twit->access_token($ACCESS_TOKEN);
				$twit->access_token_secret($ACCESS_TOKEN_SECRET);

				my $twit_msg = "$channel[$i][5]が配信中 http://www.ustream.tv/channel/$channel[$i][1]";
				&Jcode::convert( \$twit_msg, "utf8", "sjis" );
				utf8::decode($twit_msg);
				eval { $twit->update($twit_msg); };
				if ( $@ ) {
	 			   err("update failed because: $@\n");
				}
			}

		}

		close(FH);
		flock(FH, LOCK_NB);

	} else {

		@channel = @channelcache;

	}

}

sub ust_makeline
{
	&ust_renewcache;

	my $buf;
	for ($i = 0; $i < $#channel+1; $i++) {
#		if($channel[$i][3] eq 'live' && $channel[$i][0] eq 'lamutara'){
		if( $channel[$i][3] eq 'live' ){
			$buf .= qq( <a href="http://www.ustream.tv/channel/$channel[$i][1]" target="_blank">$channel[$i][5]</a><b><font style="font-size: xx-small" color="#FF6666"> LIVE </font></b>|);
		}
	}

	return $buf;
}

sub ust_maketable
{
	&ust_renewcache;

	$livechcount = 0;

	#@channelから表を生成
	$table = '<table border="1" class="list"><tr><th>status</th><th></th><th>cannnel</th><th>user</th><th>views</th><th>last streamed at</th><th>Twitter</th></tr>';
	for ($i = 0; $i < $#channel+1; $i++) {
		$table .= '<tr>';
		$ch_n++;


		if($channel[$i][3] eq 'live'){
			$table .= qq(<td align="center"><b><font size="-1" color="#FF6666">LIVE</font></b></td>);
			$livechcount++;
		} else {
			$table .= qq(<td align="center"><small><font color="#709090">$channel[$i][3]</font></small></td>);
		}

		$table .= qq(<td align="center"><a href="http://www.ustream.tv/channel/$channel[$i][1]"><img src="$channel[$i][4]" height="24"></a></td>);
		$table .= qq(<td><a href="http://www.ustream.tv/channel/$channel[$i][1]">$channel[$i][5]</a></td>);
		$table .= qq(<td><a href="http://www.ustream.tv/user/$channel[$i][0]">$channel[$i][0]</a></td>);
		$table .= qq(<td align="right"><small>$channel[$i][7]</small></td>);
		$table .= qq(<td><small>$channel[$i][6]</small></td>);
		if ( $channel[$i][2] ) {
			$table .= qq(<td><a href="https://twitter.com/#!/$channel[$i][2]">\@$channel[$i][2]</a></td>);
		}else{
			$table .= qq(<td>　</td>);
		}
#		$table .= qq(<td>$channel[$i][8]</td>);

		$totalviews += $channel[$i][7];

		$table .= "</tr>";
	}
	$table .= '</table>';

	$table = qq(<p><small>総視聴数 : </small>$totalviews　<small>現在の配信数 : </small><b><big>$livechcount</big></b>/$ch_n</p>\n$table);

	return $table;

}

1;