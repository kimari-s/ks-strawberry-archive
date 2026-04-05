#! /usr/local/bin/perl

#
# 	くずはスクリプト用のimode表示スクリプト ver0.9.4 (03/02/02)
#

###############################################################################
#  使用法
###############################################################################
=comment
このファイルをsubフォルダに置き、
bbs.cgiの1400行目付近を以下のようにします。

&getformdata;
&jconv;
&getenv;
&getcookie if ( $cookie );
$nowtime = time - $difftime * 60 * 60;

# imode表示
if ($FORM{'mode'} eq 'i') {
	require './sub/ks_imode.pl';
	imode_exec();
	exit;
}

if ( $FORM{'m'} eq 'c' ) {
	require './sub/bbscust.pl';
	&setcustom;
	exit;
}


bbs.cgi?mode=iでimode用の表示ができます。
=cut




###############################################################################
#  設定
###############################################################################

# 一画面に表示する記事の数
my $imode_disp = 11;

# 投稿文が$imode_maxmsgline行以上なら省略する
my $imode_maxmsgline = 7;





###############################################################################
#  メイン
###############################################################################

$SYS{header}		= "Content-type:text/html\n\n";
$SYS{formmethod}	= "post";
$SYS{action}		= "$cgiurl?mode=i";
$SYS{title}			= "REDACTED";

sub imode_exec
{

	# http://specters.net/cgipon/labo/c_dist.htmlより
	# User Agent によるキャリア判別
	# 2002.03.11更新

	my @user_agent = split(/\//,$ENV{'HTTP_USER_AGENT'});
	if ($user_agent[0] eq 'ASTEL') {
		# ドットi 用の処理
		# 未対応
	} elsif ($user_agent[0] eq 'UP.Browser') {
	  # EZweb 旧端末用の処理
		$SYS{device}	= 'oldEZweb';
		$SYS{title}		= "oE ayasii";
	} elsif ($user_agent[0] =~ /^KDDI/ or $user_agent[0] =~ /^OPWV-SDK*/ or $user_agent[0] =~ /UP\.Browser/) {
	  # EZweb WAP2.0 対応端末用の処理
		$SYS{device}	= 'EZweb';
		$SYS{title}		= "E ayasii";
	} elsif ($user_agent[0] eq 'PDXGW') {
		# H" 用の処理
		# 未対応
	} elsif ($user_agent[0] eq 'DoCoMo') {
	  # i-mode 用の処理
		$SYS{device}	= 'i-mode';
		$SYS{title}		= "i ayasii";
	} elsif ($user_agent[0] eq 'J-PHONE') {
	  # J-SKY 用の処理
		$SYS{device}		= 'J-SKY';
		$SYS{formmethod}	= "get";
		$SYS{action}		= "$cgiurl";
		$SYS{title}			= "J ayasii";
	} elsif ($user_agent[0] eq 'L-mode') {
		# L-mode 用の処理
		# 未対応
	} else {
	  # それ以外
		$SYS{device} = 'etc';
	}



	if ($FORM{cmdPost}) {
		# 投稿ページ
		print postpage();
	} elsif ($FORM{cmd} eq 'flw') {
		# フォロー投稿ページ
		print followpage();
	} elsif ($FORM{iSearch}) {
		# 省略された記事を展開して表示
		print expandMessagepage();
	} else {
		# 標準画面
		print imodepage();
	}
	exit;
}




# ============================ imodepage ============================= #
# 標準画面
sub imodepage
{
	# ----------------- init ----------------- #
	my ($prtmessage, $dispcount, @pkeystr, $msgmore, $msgnext, $cntnext, $page, $toppostid);

	# 投稿の処理
	if (exists $FORM{posted} and $FORM{v} ne '') {

		# EZweb用の苦肉の策
		if ($SYS{device} eq 'EZweb') {
			$FORM{v} =~ s/＞/&gt;/g;
		}

		&chkmessage;
		&putmessage;
	};

	&loadmessage;

	# imodepageに必要な変数の生成
	my %state = getstate_imodepage(
		form		 => \%FORM,
		validparams  => ['b', 'd', 'u', 'i', 'p', 'pnext', 'count', 'article',
						'msgmore', 'msgtop', 'toppostid', 'mbrcount', 'view_headID', 'view_tailID'],
	);
	# ----------------- /init  --------------- #

	# ----------------- output ----------------- #
	return (qq|$SYS{header}
		<html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><title>$SYS{title}</title></head>
		<body bgcolor="#004040" text="#ffffff" link="#eeffee">
		<form method="$SYS{formmethod}" action="$SYS{action}">
		<input type="hidden" name="mode" value="i">
		<input type="hidden" name="k" value="あ">
		<input type="hidden" name="p" value="$state{p}">
		<input type="hidden" name="u" value="$state{u}">
		<input type="hidden" name="i" value="$state{i}">
		<input type="hidden" name="count" value="$state{count}">
		<a name="top"><a href="#bottom" accesskey="8">▼:8</a></a>
		<input size="2" type="text" name="d" value="$state{d}">
		<input type="submit" name="midokureload" value="未:0" accesskey="0">
		<input type="submit" name="cmdReload" value="Ｒ:7" accesskey="7">
		<input type="submit" name="cmdPost" value="投:9" accesskey="9">
		$state{mbrcount}名
		<input type="hidden" name="b" value="$state{msgtop}">
		<hr>
		$state{article}
		$state{msgmore}
		<input type="submit" name="pnext" value="＞:5" accesskey="5">
		<a name="bottom"><a href="#top" accesskey="2">▲:2</a></a>
		</form>
		@{[ prms() ]}
		</html>
	| =~ m#\t*([^\n]*\n)#gs);
	# ----------------- /output ---------------- #
}


# imodepageに必要な変数の生成
sub getstate_imodepage
{
	my %params = @_;

	my %state = (
		b		=> 0,
		d		=> $imode_disp,
		p		=> '',
		count	=> 0,
		%{$params{form}},
	);

	if (defined $FORM{pnext}) {
#		$state{b} = $FORM{'b'};
	} else {
		$state{b} = 0;
	}

	my $preP;
	if (exists $FORM{posted} and defined $FORM{preP}) {
		$preP = $FORM{preP};
	} else {
		$preP = $FORM{p};
	}

	# 最新のPOSTIDを取得（０件リロード用）
	$logdata[0] =~ /^.*,(.*),.*,.*,.*,.*,.*,.*,.*,.*/;
	$state{p} = $1;


	# メッセージ表示件数設定
	# => ごちゃごちゃしてきた
	if ($state{d} == 0) {
		if (defined $FORM{pnext}) {
			$dispcount = $imode_disp;
		} elsif ($FORM{cmd} eq 'posted' and $FORM{preP}) {
			$dispcount = ($state{p} - $preP) > $imode_disp ? $imode_disp : ($state{p} - $preP);
		} else {
			$dispcount = $state{p} - $preP;
		}
	} elsif ($FORM{midokureload}) {
		$dispcount = ($state{p} - $preP) > $state{d} ? $state{d} : ($state{p} - $preP);
	} else {
		$dispcount = $state{d};
	}

	# 表示メッセージ作成
	$state{msgtop} = $state{b} + $dispcount;
	$state{msgtop} = @logdata if ( $state{msgtop} > @logdata );

	my $flag = 0;

	if (	$FORM{midokureload}
		and $msgtop > $FORM{'d'}
		and $FORM{'d'} != 0
	) {
		$msgtop = $FORM{'d'}
	}

	@output_logdata = @logdata[$state{b} .. $state{msgtop} - 1];

	for (@output_logdata) {
		&getmessage($_);
		$state{article} .= prtmessage_imode(%state);
		$flag = 1;
	}


	$state{b}++;
	$flag and $state{msgmore} = "$state{b}～$state{msgtop}件";

	# 参加人数
	my $tmp = mbrcount();
	$tmp =~ m|現在の参加者 : (\d+)名 |;
	$state{mbrcount} = $1;

	return map { $_ => $state{$_} } @{$params{validparams}};
}
# ============================ /imodepage ============================= #




# ============================ postpage ============================= #
# 投稿ページ
sub postpage
{
	# ----------------- init ----------------- #
	&loadmessage;
	$prtmessage = '';

	# postpageに必要な変数の生成
	my %state = getstate_postpage(
			form		=> \%FORM,
			validparams => ['c', 'd', 'u', 'i', 'pcode', 'toppostid'],
	);
	# ----------------- /init ---------------- #

	# ----------------- output ----------------- #
	return (qq|$SYS{header}
		<html><head><title>$SYS{title}</title></head>
		<body bgcolor="#004040" text="#ffffff" link="#eeffee">
		<a href="$cgiurl?mode=i">戻</a>
		<FORM method="$SYS{formmethod}" action="$SYS{action}">
		<input type="hidden" name="mode" value="i">
		<input type="hidden" name="k" value="あ">
		<input type="hidden" name="c" value="$state{c}">
		<input type="hidden" name="d" value="$state{d}">
		<input type="submit" name="posted" value="投:9" accesskey="9"><br>
		<textarea rows="4" cols="14" name="v"></textarea><br>
		名<input size="8" type="text" name="u" maxlength="30" value="$state{u}"><br>
		<input type="hidden" name="p" value="$state{toppostid}">
		<input type="hidden" name="preP" value="$FORM{p}">
		<input type="hidden" name="a" value="checked">
		$state{pcode}
		</form>
		@{[ prms() ]}
		</body></html>
	| =~ m#\t*([^\n]*\n)#gs);
	# ----------------- /output ---------------- #
}

# postpageに必要な変数の生成
sub getstate_postpage
{
	my %params = @_;

	my %state = (
		d		=> $imode_disp,
		c		=> 300,
		%{$params{form}},
		pcode	=> pcode(),
	);

	# 最新のPOSTID
	$logdata[0] =~ /^.*,(.*),.*,.*,.*,.*,.*,.*,.*,.*/;
	$state{toppostid} = $1;

	return map { $_ => $state{$_} } @{$params{validparams}};
}
# ============================ /postpage ============================= #




# ============================ followpage ============================= #
# フォロー投稿ページ
sub followpage
{
	# ----------------- init ----------------- #
	&loadmessage;
	$prtmessage = '';

	# followpageに必要な変数の生成
	my %state = getstate_followpage(
			form		=> \%FORM,
			validparams => ['c', 'd', 'u', 'i', 'pcode', 'toppostid', 'formmsg', 'fuser', 'ftwitid'],
	);
	# ----------------- /init ---------------- #

	#9/30
	#	<input type="hidden" name="h" value="$thread">
	#が欠落してた
	if ( !$thread ) {
		$thread = $postid;
	}

	# ----------------- output ----------------- #
	return (qq|$SYS{header}
		<html><head><title>$SYS{title}</title></head>
		<body bgcolor="#004040" text="#ffffff" link="#eeffee">
		<a href="$cgiurl?mode=i">戻</a>
		<FORM method="$SYS{formmethod}" action="$SYS{action}">
		<input type="hidden" name="mode" value="i">
		<input type="hidden" name="k" value="あ">
		<input type="hidden" name="c" value="$state{c}">
		<input type="hidden" name="d" value="$state{d}">
		<input type="hidden" name="f" value="$postid:$wdate">
		<input type="hidden" name="p" value="$state{toppostid}">
		<input type="hidden" name="preP" value="$FORM{p}">
		<input type="hidden" name="a" value="checked">
		<input type="hidden" name="h" value="$thread">
		<input type="hidden" name="fuser" value="$state{fuser}">
		<input type="hidden" name="ftwitid" value="$state{ftwitid}">
		<input type="submit" name="posted" value="投:9" accesskey="9"><br>
		<textarea rows="4" cols="14" name="v">$state{formmsg}\r</textarea><br>
		名<input size="8" type="text" name="u" maxlength="30" value="$state{u}"><br>
		$state{pcode}
		</form>
		@{[ prms() ]}
		</body></html>
	| =~ m#\t*([^\n]*\n)#gs);
	# ----------------- /output ---------------- #
}

#		<textarea rows="4" cols="14" name="v">$state{formmsg}\r</textarea><br>

# followpageに必要な変数の生成
sub getstate_followpage
{
	my %params = @_;

	my %state = (
		d		=> $imode_disp,
		c		=> 300,
		%{$params{form}},
		pcode	=> pcode(),
	);

	# 最新のPOSTID
	$logdata[0] =~ /^.*,(.*),.*,.*,.*,.*,.*,.*,.*,.*/;
	$state{toppostid} = $1;


	foreach ( 0 .. @logdata - 1 ) {
		&getmessage ( $logdata[$_] );
		if ( $postid eq $FORM{'s'} ) {
			last;
		}
	}

	# レス先の投稿者名
	$state{fuser} = $user;

	# レス先のTwitterID
	$state{ftwitid} = $twitid;


	# res文字列の作成
	$state{formmsg} = $msg;
	$state{formmsg} =~ s/&gt; &gt;.*?\r//g;
	$state{formmsg} =~ s/<A href=\"m=f\S+\">.*<\/A>//i;
	$state{formmsg} =~ s/<A href=\S+ target=\"link\">(\S+)<\/A>/$1/ig;


	# EZwebの場合&gt;を上手く処理してくれない
	# 苦肉の策で&gt;の代わりに＞を一時的に使用して
	# 受けるときに再び&gt;に戻してやる

	if ($SYS{device} eq 'EZweb') {
		$state{formmsg} =~ s/\r/\r＞ /g;
		$state{formmsg} = "＞ $state{formmsg}\r";
		$state{formmsg} =~ s/\r＞\s+\r/\r/g;
		$state{formmsg} =~ s/\r＞\s+\r$/\r/g;
	} else {
		$state{formmsg} =~ s/\r/\r&gt; /g;
		$state{formmsg} = "&gt; $state{formmsg}\r";
		$state{formmsg} =~ s/\r&gt;\s+\r/\r/g;
		$state{formmsg} =~ s/\r&gt;\s+\r$/\r/g;
	}

	return map { $_ => $state{$_} } @{$params{validparams}};
}
# ============================ /followpage ============================= #




# ============================ expandMessagepage  ============================= #
# 省略された記事を展開して表示
sub expandMessagepage
{
	# ----------------- init ----------------- #
	&loadmessage;
	$prtmessage = '';

	# $FORM{iSearch}と等しいpostidの記事のみ出力
	for (@logdata) {
		&getmessage($_);
		if ($postid == $FORM{iSearch}) {
			$state{article} .= prtmessage_imode();
		}
	}
	# ----------------- /init ---------------- #

	# ----------------- output ----------------- #
	return (qq|$imode_header
		<html><head><title>i ayasii</title></head>
		<body bgcolor="#004040" text="#ffffff" link="#eeffee">
		<a href="$cgiurl?mode=i">戻</a><br>
		$state{article}
		</body></html>
	| =~ m#\t*([^\n]*\n)#gs);
	# ----------------- /output ---------------- #
}
# ============================ expandMessagepage  ============================= #




# imode用のprtmessage関数
sub prtmessage_imode
{
	my %state = @_;
	my ($tmp, $res_article, $hour, $min, $sec, $tmpuser, $no_shortmode);

	# フォロー投稿ボタン
	$btnfollow =
		qq|<A href="$cgiurl?mode=i&cmd=flw&u=@{[ &url_encode ( $FORM{'u'} ) ]}&d=$state{d}&p=$state{p}&s=$postid&c=$state{c}">$txtfollow</A>|;

	(undef, $mon, $date, undef, $hour, $min, $sec) = ($wdate =~ m|(\d\d\d\d)/(\d\d)/(\d\d)\((.*)\)(\d\d)時(\d\d)分(\d\d)秒|);

	# メールアドレス
	if ($mail) {
		$user = qq|<A href="mailto:$mail">$user</A>|;
	}

	# user名
	if (not $user =~ m|\s*| or not $user eq '　') {
		$tmpuser = "<br>name：$user";
	}

	# メッセージ

	# 参考の消去
	$msg =~ s|<a href="\S+">参考：(\S+)</a>||gi;

	# 二つ前のレスを消去
	$msg =~ s|(&gt; &gt; .*?\r)||g;

	# 一つ前のレスを操作
	$msg =~ s|&gt;(.*?)\r|<font color="#aaaaaa">$1</font>\r|g;

	# 投稿文両端の連続する改行をトリミング
	$msg =~ s/^[\r]{2,}//g;
	$msg =~ s/[\r]{2,}$//g;


	# アンカータグを付加 10/1
	my $urlchar = "[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]";
	$msg =~ s#(^|[^"])((https?|ftp|gopher|telnet|whois|news)://$urlchar+)#$1<a href="$2" target="_blank">$2</a>#ig;


	## BEGIN: 行数省略処理
	@lines  = split("\r", $msg);
	$linecount = @lines;

	if ($FORM{iSearch}) { $no_shortmode = 1 }
	# 投稿文が$imode_maxmsgline行以上なら省略する
	# バイト数でカウントするのもOKだが判定が難しい
	if ($linecount > $imode_maxmsgline and $no_shortmode != 1) {
		$msg = qq($lines[0]<br>);
		$msg .=
		 	qq!<a href="$cgiurl?mode=i&iSearch=$postid"><font size="-1">[!
			. ($linecount-2)
			. "行省略]</font></a><br>";
		$msg .= $lines[$linecount-1];
	} else {
		$msg =~ s/\r/<br>\n/g;
	}

	return "<tt>$btnfollow$mon/$date $hour:$min:$sec$tmpuser<br>\n$msg<br></tt><hr>\n\n";
}

sub prms
{
	my %params = @_;
	map { "$_ => $params{$_}<br>\n" } keys %params;
}
1;