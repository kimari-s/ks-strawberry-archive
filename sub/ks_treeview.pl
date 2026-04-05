#!/usr/bin/perl

=comment
くずはスクリプト用のtree表示スクリプト ver0.9 (03/05/12)


-- これは何ですか? --

くずはスクリプトの記事をツリー型に表示するためのモジュールです。



-- 使用法 --

このファイルをsubフォルダに置き、
bbs.cgiの1400行目付近を以下のようにします。

# tree表示
if ($FORM{'tree'}) {
	require './sub/ks_treeview.pl';
	$prtmessage = output_treeview($bmsg, $msgtop);
}

bbs.cgi?tree=on でtreeview用の表示ができます。


+ 変更(2003/09/21)
- 本家暫定むけ変更(2003/11/12)
=cut

###############################################################################
#  設定
###############################################################################

my %treeview = (
  # 枝の色
  'color_branch' => $FORM{color_branch} || 'ffffff',

  # 新規記事の色
  'color_newmsg' => $FORM{color_newmsg} || 'aaccff',

);



###############################################################################
#  ツリー型で出力するための関数
###############################################################################

sub treeview {

# @logdata, %logdata, %kids, はグローバル変数
	loadmessage();

	@logdata = grep {
		my $log = $_;
		my $threadnum = (split m/,/)[3];
		my $postid = (split m/,/)[1];
		$threadnum == $FORM{'s'} or $postid == $FORM{'s'};
	} @logdata;

	&prthtmlhead ( "$bbstitle 投稿検索" );

	print <<EOF;
<a name="top"><a href="#bottom">$txt_go_bottom</a></a>
 <a href="$cgiurl?d=$FORM{'d'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_reset">掲示板へ($accesskey_reset)</a>
 <a href="$cgiurl?m=g&d=$FORM{'d'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_getlog">過去ログへ($accesskey_getlog)</a>
<HR>
EOF
	print output_treeview(0, 1);

	print <<EOF;
<a name="bottom"><a href="#top">$txt_go_top</a></a>
 <a href="$cgiurl?d=$FORM{'d'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_reset">掲示板へ($accesskey_reset)</a>
 <a href="$cgiurl?m=g&d=$FORM{'d'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_getlog">過去ログへ($accesskey_getlog)</a>
 </body></html>
EOF
	exit;
}


###############################################################################
# $head件目から $tail件目のツリーを出力する
###############################################################################

sub output_treeview {

	my ($head, $tail) = @_;
	my $output;

	%logdata		= make_hash_logdata(@logdata);
	%kids			= make_kids(@logdata);
	my @threadID	= get_threadID(@logdata);

	@threadID = map {$_->[0]} sort {$b->[1] <=> $a->[1]} map { [ $_ => max_postID($_) ] } @threadID;

	$tail = $#threadID >= $tail ? $tail : $#threadID;
	@threadID = @threadID[$head .. $tail];

	for my $threadID (@threadID) {
		my $max_postID = max_postID($threadID);
		my $ndate = (split m|,|, $logdata{$max_postID})[0];
		if ( $FORM{'midokureload'} and defined $FORM{'p'} and $max_postID <= $FORM{'p'}) { last; }

		my @tmp = enum_postID($threadID);
		my $count = @tmp;

		#9/19 途中でやめた
		#my $treebtn = qq| <a href="cgiurl?s=$threadID">木</a>|;

		$output .= qq|<div class="${CSSclass}Treearticle"><tt><font size="+0"> $count [ 更新日：@{[ getnowdate($ndate) ]} ]</font>$treebtn</tt><br><br>|;
		@header = ('　');

		$output .= output_tree($threadID);
		$output .= "<hr></div>\n";
	}
	return $output;
}


###############################################################################
# 1つのツリーを出力する
###############################################################################

sub output_tree {

	my $node = shift;
	my $output = '';

	# 出力
	$output .= output_node($node);

	# 子があるなら
	if (q_article($node, 'has_child')) {
		for my $node (@{ $kids{$node} }) { $output .= output_tree($node) }
		pop @header;
	}
	return $output;
}


###############################################################################
# 1つのノードを出力する
###############################################################################

sub output_node {

	my $node = shift;
	my ( $msgcolor, $msg_headder, $temp, $mode, );

#	my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split(m|,|, $logdata{$node});
	my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = getmessage_treeview($logdata{$node});

	if ( $CUST{'followwin'} ) {
#		$newwin = " target=\"$followwinname\"";
		$newwin = " target=\"_blank\"";
	} else {
		$newwin = '';
	}

	#レスボタンポイントで投稿日時ポップアップ lam 8/2
	my $nowdate = &getnowdate($ndate);

#	my $res_button_url = qq($cgiurl?m=f&d=$FORM{'d'}&p=$toppostid&s=$postid&$ks_param->{get});
	my $res_button_url = qq($cgiurl?m=f&d=$FORM{'d'}&p=$toppostid&s=$postid);
	my $res_button;

	my $windowopen;
	#window.openで開かないとwindow.closeで閉じれない(FF)、または確認メッセージが出る(IE)から
	if ($CUST{'followwin'} && $CUST{'autoclose'}) {
		$windowopen = qq( onclick="window.open('$res_button_url');return false;");
	}

	if ($phost eq 'TL' || $phost eq '@') {
		$txtfollow2 = '●';
	} else {
		$txtfollow2 = $txtfollow;
	}
	$res_button = qq(<a href="$res_button_url"$newwin style="text-decoration: none;" title="$user $nowdate"$windowopen>$txtfollow2</a>);

####
$defaultuser = '　';
$defaulttitle = ' ';

	if ( $msg ne "== not_found ==" ) {
#		# メールアドレス
#		if ( $mail ) {
#			$user = "<a href=\"mailto\:$mail\">$user<\/a>";
#		}
#
#		if ( ( $user eq $defaultuser ) && ( $title ne $defaulttitle ) && ( $title !~ /^＞/ ) ) {
#			$msg_headder = qq(<FONT color="#$CC{'subj'}"> 題名: <B>$title</B></FONT>\n);
#		}
#
#		if ( ( $user ne $defaultuser ) && ( $title ne $defaulttitle ) && ( $title !~ /^＞/ ) ) {
#			$msg_headder = qq(投稿者: $user <FONT color="#$CC{'subj'}"> 題名: <B>$title</B></FONT>\n);
#		}
#		if ( ( $user ne $defaultuser ) && ( ( $title eq $defaulttitle ) || ( $title =~ /^＞/ ) ) ) {
#			$msg_headder = qq(投稿者: $user\n);
#		}
#		if ( $user ne $defaultuser ) {
#			$msg_headder = qq(投稿者: $user\n);
#		}
	}
	# 参考を消す
#	s|<a href=[^>]*?>参考：[^>]*?</a>||g;
	if ( $thread ) {
		my @lines  = split( "\r", $msg );
		undef $lines[$#lines];
		undef $lines[$#lines - 1];
		$msg = join ( "\r", @lines );
	}
####
	$_ = $msg;
####
	s/\r/\n/g;

	if ( $FORM{'m'} eq 'tree' ) {
		$mode = 1;
	} else {
		$mode = 0;
	}
	if ( $thread && $dispqmsgline[$mode] ne '2' ) { #ルートは返信(引用部分)を消さない
		# 2つ前の返信を消す
#		s|&gt; &gt;.*?\0\0?||g;
		s/^&gt; &gt;.*?\n\n?//mg;

		# 1つ前の返信を消す
		if ( $dispqmsgline[$mode] eq '1' ) {
#			if (s|(&gt;.*?)\0\0||g) { $pre_msg = $1; }
#			if (s|(&gt; .*?)\n\n?||g) { $pre_msg = $1; }
			if (s|^(&gt; .*?)\n\n?||mg) { $pre_msg = $1; }
		} else {
#			s|&gt;.*?\0\0?||g;
			s/^&gt; .*?\n\n?//mg;
		}
	}

	# 記事
	my $article = $_;
	$article =~ s/\0//g;
	$article =~ s/\s//g;

# 掲示板表示モードかつ、投稿文が$FORM{'collimit'}桁以上なら省略・非表示する
	if ( ( $FORM{'collimit'} ) && ( ( $FORM{'m'} eq 'p' ) || ( $FORM{'m'} eq '' ) || ( $FORM{'m'} eq 'o' ) || ( $FORM{'m'} eq 'op' ) || ( $FORM{'m'} eq 'on' ) || ( $FORM{'m'} eq 'n' ) ) ) {
		$temp = $_;
		my @lines  = split( "\n", $temp );
		foreach ( @lines ) {
			if ( ( length ( $_ ) > $FORM{'collimit'} ) ) {
				if ( ( $_ =~ m|(<a href=\"m=f\S+\">).*<\/a>|i ) || ( $_ =~ m|(<a href=".*" target="link">)[^<*]|i ) ) {
					if ( ( length ( $_ ) - length ( $1 ) - 4 ) > $FORM{'collimit'} ) {
						if ( !$colswitchu ) {
							$temp = '省略'."\n";
						} else {
							$temp = "";
						}
						last;
					}
				} else {
					if ( !$colswitchu ) {
						$temp = '省略'."\n";
					} else {
						$temp = "";
					}
					last;
				}
			}
		}
		$_ = $temp;
	}
# 掲示板表示モードかつ、投稿文が$FORM{'linelimit'}行以上なら省略・非表示する
	if ( ( $FORM{'linelimit'} ) && ( ( $FORM{'m'} eq 'p' ) || ( $FORM{'m'} eq '' ) || ( $FORM{'m'} eq 'o' ) || ( $FORM{'m'} eq 'op' ) || ( $FORM{'m'} eq 'on' ) || ( $FORM{'m'} eq 'n' ) ) ) {
		my @lines  = split( "\n", $_ );
		if ( ( @lines > $FORM{'linelimit'} ) && ( @lines > 3 ) ) {
			$msg_head = $lines[0];
			$msg_body = "\n[" . ( @lines - 2 ) . '行省略]' . "\n";
			$msg_tail = $lines[$#lines];
			undef ( @lines );
			@lines = ( $msg_head, $msg_body, $msg_tail, "\n" ) if ( !$lineswitchu );
			$_ = join ( "\n", @lines );
		}
	}

	s|\n|\0|g;

	# 投稿文末尾の連続する改行をトリミング
#	s|[\0]{2,}$|\0|g;
	s|\0+$||g;

#### ノード間を一行詰めて表示する場合
	if ( !$nodeclose[$mode] ) {
		$_ .= "\0";
	}

#	# 半角空白を&nbsp;に変換
#	s/ /&nbsp;/g;
#	# A、FONTタグ対応
#	s/<a&nbsp;href/<a href/ig;
#	s/&nbsp;target="/ target="/ig;
#	s/<font&nbsp;/<font /ig;
######

	#URLにアンカータグを付加 9/20
	s#((https?|ftp|gopher|telnet|whois|news)://$urlchar+)#<a href="$1" target="_blank">$1</a>#ig;

	#amazon tag付加 9/21
	if($CUST{'affitag'}){
		s#<a href="http://(?:www\.)?amazon\.co\.jp/$urlchar*(?:ASIN/|dp/|product/)(\w*)$urlchar*"#<a href="http://www.amazon.co.jp/dp/$1?tag=$amazontag"#ig;
		s#(<a href="http://(?:www\.)?amazon\.co\.jp)/?"(.*?\0)#$1/?tag=$amazontag&linkCode=ure&creative=6339"$2#ig;
	}


	#リンクサムネイル化 9/19
	my $thumbnail = $CUST{'thumbnail_0'} + $CUST{'thumbnail_1'} * 2;
	if($thumbnail){

		if($thumbnail == 1){
			$thumnailsize = "height=\"90\"";
			$youtubethum = "default";
			$amazonthum = ".09.TZZZZZZZ";
		}
		elsif($thumbnail == 2){
			$thumnailsize = "height=\"250\"";
			$youtubethum = "default";
			$amazonthum = ".09.MZZZZZZZ";
		}
		elsif($thumbnail == 3){
			$thumnailsize = "";
			$youtubethum = "0";
			$amazonthum = ".09.LZZZZZZZ";
		}

		#画像
		s#(https?://$urlchar+\.(?:gif|jpe?g|png))(.*?\0)#$1$2<a href="$1" target="_blank"><img src="$1" $thumnailsize></a>\0#ig;

		#youtube
		s#(https?://(?:www\.youtube\.com/watch\?.*?v=|youtu\.be\/)([\w-]+))(.*?\0)#$1$3<a href="$1" target="_blank"><img src="http://i.ytimg.com/vi/$2/$youtubethum.jpg"><img src="res/youtube.png" style="position:relative; left:-16px;"></a>\0#ig;

		#ニコ動
		s#(https?://(?:www\.nicovideo\.jp/watch|nico.ms)/[a-z][a-z](\d+)/?)(.*?\0)#sprintf("$1$3<a href=\"$1\" target=\"_blank\"><img src=\"http://tn-skr%d.smilevideo.jp/smile?i=$2\"><img src=\"res/nicovideo.png\" style=\"position:relative; left:-16px;\"></a>\0",($2 % 4)+1)#ige;

		#amazon
		s#(https?://(?:www\.)?amazon\.co\.jp/$urlchar*(?:ASIN/|dp/|product/)(\w*)$urlchar*)(.*?\0)#$1$3<a href="$1"><img src="http://images-jp.amazon.com/images/P/$2$amazonthum.jpg"><img src="res/amazon.png" style="position:relative; left:-16px;"></a>\0#ig;
	}

	# 半角空白を&nbsp;に変換
	s/ /&nbsp;/g;
	# タグ対応
	s/(<.*?>)/nbsp2sp($1)/ge;

#試験的投稿者非表示
#	if( $user ne $defaultuser ) {
#		$_ = "投稿者: $user\0$_";
#	}

	#Twitterリンク化
	$_ =~ s|\@([a-zA-Z0-9_]+)|<a href="https://twitter.com/#!/$1" target="_blank">\@$1</a>|g;

	#「タ」の置換ができない 対策
	use Encode;
	$msg_dec = decode( 'shift-jis', $_ );
	$user_dec = decode( 'shift-jis', $user );

	#NG
	if ($CUST{'nguse'} && $FORM{'ng'}) {
		$FORM{'ng'} =~ s/\r/|/g;
		$ngword_dec = decode( 'shift-jis', $FORM{'ng'} );
		if ( $msg_dec =~ /$ngword_dec/ || $user_dec =~ /$ngword_dec/ ) {
			$_ = qq(<font color="#$CC{'qmsgc'}">…</font>\0);
		}
	}
	#自動NG
	if ($CUST{'autong'}) {
		$autongword =~ s/\n/|/g;
		$autongword_dec = decode( 'shift-jis', $autongword );
		if ( $msg_dec =~ /$autongword_dec/ ||  $user_dec =~ /$autongword_dec/ ) {
			$_ = qq(<font color="#$CC{'qmsgc'}">…</font>\0);
		}
	}

	q_article($node, 'is_last')
		? push @header, qq(<font color="#$treeview{color_branch}">└$res_button</font>)
		: push @header, qq(<font color="#$treeview{color_branch}">├$res_button</font>);

	q_article($node, 'is_root')  and  $header[-1] = qq(<font color="#$treeview{color_branch}">&nbsp;&nbsp;$res_button</font>);

	my $head = join '', @header;
	pop @header;

	if (q_article($node, 'has_child') and q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">　│</font>);
	} elsif (q_article($node, 'has_child') and not q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">││</font>);
	} elsif (not q_article($node, 'has_child') and q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">　　</font>);
	} elsif (not q_article($node, 'has_child') and not q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">│　</font>);
	}

	my $body = join '', @header;

	s|\0|<br>\n$body|g;


	# 子があるなら自分の頭を'│'に変える
	q_article($node, 'has_child')  and  $header[-1] = qq(<font color="#$treeview{color_branch}">│</font>);

	# 末の子なら自分の頭を'　'に変える
	q_article($node, 'is_last')  and  $header[-1] = '　';

	# 子がいないならポップ
	not q_article($node, 'has_child')  and  pop @header;

	# 新着記事なら色を変える
#### m=treeの場合は新着記事の色変えをしない
	if ( $FORM{'m'} ne 'tree' ) {
		$msgcolor = (defined $FORM{p} and $postid > $FORM{p}) ? $treeview{color_newmsg} : $CC{'text'};
	} else {
		$msgcolor = $CC{'text'};
	}
####

	if ($article eq '') {
		$pre_msg .= "\0" if ( $msg_headder );
		$pre_msg =~ s|\0|<br>\n$body|g;
		if ( $msg_headder ) {
			$_ .= $pre_msg;
		} else {
			$head .= $pre_msg;
		}
	}
	return qq(\n<tt><font size="+0" color="#$msgcolor">\n$head$_<br>\n</font></tt>\n);
}

sub base_decode($num, $alphabet) {
    $decoded = 0;
    $multi = 1;

    while (strlen($num) > 0) {
        $digit = $num[strlen($num)-1];
        $decoded += $multi * strpos($alphabet, $digit);
        $multi = $multi * strlen($alphabet);
        $num = substr($num, 0, -1);
    }

    return $decoded;
}

###############################################################################
# 各種問い合わせ
###############################################################################

sub q_article {

	my ($ID, $query) = @_;

	# is_root
	# is_dummy
	# get_parentID
	# is_last
	# has_child

	if ($query eq 'is_root') {
		return ( split m|,|, $logdata{$ID} )[3] ? 0 : 1;
	} elsif ($query eq 'is_dummy') {
		return ( split m|,|, $logdata{$ID} )[0];
	} elsif ($query eq 'has_child') {
		return defined $kids{$ID}
	} elsif ($query eq 'is_last') {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|, $logdata{$ID};

		# ルートならreturn
		if (not $thread) { return 1 }

		my $parent = q_article($ID, 'get_parentID');
		if ($parent and $logdata{$parent}) {
			return ${ $kids{$parent} }[-1] == $ID ? 1 : 0;
		} else {
			my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|, $logdata{$ID};
			return ${ $kids{$thread} }[-1] == $ID ? 1 : 0;
		}
	} elsif ($query eq 'get_parentID') {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|, $logdata{$ID};
		$msg =~ m|<a href=".*?&s=(\d*)[^>]*?>参考|i ?  return $1 : return undef;
#		$msg =~ m|<a href="m=f&s=(\d*)[^>]*?>参考|i ?  return $1 : return undef;
	}

}


sub max_postID { ( sort {$b <=> $a} enum_postID($_[0]) )[0] }


###############################################################################
# postid => article
###############################################################################

sub make_hash_logdata {  map { my $log = $_; (split m|,|, $log)[1] => $log } @_  }


###############################################################################
# parent_postid =>[child_postid, child_postid, ... ]
###############################################################################

sub make_kids {

	my @logdata = @_;
	my %kids;

	for (reverse @logdata) {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|;
		my $parent_postid = q_article($postid, 'get_parentID');

		if (not exists $logdata{$thread}) {
		# ルートが存在しない場合
		#
		# ダミーのルートを作成し
		# その子として登録する
		#
			$logdata{$thread} = make_dummy_article($thread);
			push @{ $kids{$thread} }, $postid;
		} elsif (q_article($thread, 'is_dummy') == -1) {
		# ダミールートが存在する場合
		# 注意: -1はTRUE
			if ($logdata{$parent_postid}) {
				push @{ $kids{$parent_postid} }, $postid;
			} else {
				push @{ $kids{$thread} }, $postid;
			}
		} elsif ($logdata{$thread}) {
		# ルートが存在する場合
		#
			push @{ $kids{$parent_postid} }, $postid;
		}
	}
	return %kids;
}


###############################################################################
# 記事が見つからなかったときのダミー記事を提供する
###############################################################################

sub make_dummy_article {  "-1,$_[0],,,,,,,,== not_found ==\n"  }


###############################################################################
# thread => [postid, postid, .. ]
###############################################################################

sub get_threadID {

	my @logdata = @_;
	my @threadID;

	for (@logdata) {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|;
		$thread  ?  push @threadID, $thread
				 :  push @threadID, $postid;
	}

	# @threadIDから重複した要素を削除
	return keys %{ { map {$_ => 1} @threadID} };
}


sub enum_postID {

	my $ID = shift;
	my @postID = ($ID);

	if (q_article($ID, 'has_child')) {
		for my $kid (@{ $kids{$ID} }) {
			push @postID, enum_postID($kid);
		}
	}

	return @postID;
}


sub getmessage_treeview {

	my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split(m|,|, $_[0]);

	$msg =~ s/\n$//;
	$title =~ s/\0/\,/g;
	$mail =~ s/\0/\,/g;
	$user =~ s/\0/\,/g;
	$msg =~ s/\0/\,/g;

	return ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg);
}


sub nbsp2sp {
	my $_ = $_[0];
	s/&nbsp;/ /g;
	return $_;
}


1;


__END__
