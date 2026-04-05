#!/usr/bin/perl

use Net::Twitter::Lite;

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (掲示板本体)
#
#	  mailto	kuzuha@kurumi.ne.jp
#	  webpage	http://kuzuha.tripod.co.jp/
#
#	TABSIZE=4
#

#   くずはすくりぷと + ＠くずは萌え ver1.1.1

#
#	2002/11/27
#	Remix＠スクリプト改良:2002/11/21(木)09時04分45秒にて指摘されたバグ潰し
#	getformdata関数の改良
#
#	2002/12/01
#	URLに,が入ると途切れてしまうバグ修正
#	読専画面の下のリロードボタンを使うと標準画面に戻るバグ修正
#
#	2002/12/06
#   POST のサイズ制限をgetformdata関数に追加
#
#	2003/01/01
#   次のページのバグ修正
#
#	2003/01/25
#   未読リロード改善


###############################################################################
#  設定
###############################################################################

# 掲示板CGIのURL
$cgiurl = "http://$ENV{SERVER_NAME}$ENV{SCRIPT_NAME}";
$cgiurl =~ s/index.cgi$//;

$sub = './sub/';

# jcode.plのパス
$jcode = './jcode.pl';

# gzipのパス
#  (gzip圧縮転送機能を使用しない場合は空のままにしておきます)
$gzip = '/usr/bin/gzip';

# CGIを設置するホストアドレス
$bbshost = "$ENV{SERVER_NAME}";

if( $bbshost =~ /localhost/ ) {
	$debug = 1;
}

# ログファイル名
$logfilename = './bbs.log';

# カウンターのスタート日付
$countdate = 'REDACTED';

# カウンターのファイル名の先頭部分
$countfile = './count/count';

# カウンターの壊れにくさレベル
$countlevel = 3;

# リアルタイム参加者カウント用ファイル名
#  (リアルタイム参加者カウント機能使用しない場合は空のままにしておきます)
$cntfilename = './bbs.cnt';

# リアルタイム参加者カウント間隔 (秒)
# （最終ページビューからこの時間を超えた参加者は集計から除外されます）
$cntlimit = 300;

# メッセージの保存数
$logsave = 666;

# １画面に表示するメッセージの表示数
#  (1～メッセージの保存数)
$msgdisp = 30;

# サーバー設置場所と日本との時差
#   日本             : 0
#   グリニッジ標準時 : -9
#   アメリカ         : -14 (ワシントン)
#                    : -20 (ミッドウェー諸島)
#   ニュージーランド : 3
$difftime = 0;
#9/16
$ENV{'TZ'} = "JST-9";

# 掲示板の名前
$bbstitle = 'REDACTED';

# 掲示板のバージョン lam 6/26
#$bbsver = 'ver0';
$bbstitle_at = $bbstitle;


# 背景色
$bgc    = '004040';

# テキスト色
$textc  = 'ffffff';

# リンク色
$linkc  = 'eeffee';
$vlinkc = 'dddddd';
$alinkc = 'ff0000';

# 題名の色
$subjc  = 'fffffe';

# 引用メッセージの色
# （色を変えない場合は空にしてください）
$qmsgc  = 'd1d1d1';

# フォロー投稿画面ボタンに表示する文字
$txtfollow = '■';

# 投稿者検索ボタンに表示する文字
$txtauthor = '★';

# スレッド表示ボタンに表示する文字
$txtthread = '◆';

# フォロー投稿時に相手の投稿者名に付加する文字
# （一般の掲示板では「さん」などを付けると良いでしょう）
$fsubj = '';

# 過去ログ保存用ディレクトリの名前
$oldlogfiledir = './log/';

# 過去ログの保存形式
#   0 : HTML形式 (トピック一覧、過去ログからの引用機能は使用できません)
#   1 : バイナリ形式
$oldlogfmt = 1;

# 過去ログからのフォロー投稿・投稿者検索
#   0 : 不可
#   1 : 可 (過去ログの保存形式がHTML形式の場合は設定できません)
$oldlogbtn = 1;

# 過去ログの保存方法
#   0 : 日毎
#   1 : 月毎
$oldlogsavesw = 0;

# 過去ログの保存日数
#  (過去ログの保存方法が日毎の場合にのみ有効)
$oldlogsaveday = 30;

# 過去ログの最大ファイルサイズ
$maxoldlogsize = 4 * 1024 * 1024;

# 二重書き込みチェック件数
$checkcount = 30;

# １メッセージの最大桁数
$maxmsgcol = 192;

# １メッセージの最大行数
$maxmsgline = 100;

# １メッセージの最大サイズ(byte)
$maxmsgsize = 8400;

# 連続投稿防止コード（必ず変更すること）
$protect_a = 12785634;	# 0以外の数字から始まる8桁の数字
$protect_b = 14;		# 0以外の数字から始まる2桁の数字


#アマゾンアソシエイトタグ
$amazontag = "REDACTED";

$my_twit_id = "REDACTED";
#Twitter
#@REDACTED
my %CONSUMER_TOKENS = (
    consumer_key    => 'REDACTED',
    consumer_secret => 'REDACTED',
    access_token => 'REDACTED',
    access_token_secret => 'REDACTED',

    #API1.1対応
    apiurl                => 'https://api.twitter.com/1.1',
    searchapiurl          => 'https://api.twitter.com/1.1/search',
    search_trends_api_url => 'https://api.twitter.com/1.1',
    lists_api_url         => 'https://api.twitter.com/1.1',
    ssl => 1,
);

# twit_repの結果を書き出すテキストファイル
$rapFile = 'twitrep.txt';

$defaultuser = '　';

$urlchar = "[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]";
#$urlchar = "(=[\x21-\xfc]+|[\x21-\x7e])";

#Twitter機能使用
$twitter = 1;
if ($debug) { $twitter = 0;}

#TLを板に投稿
$tl_to_bbs = 1;

####################################カスタム関連#################################### 9/22
##                                                                                ##

@custom = ('custom', 'gzip', 'followwin', 'dummy5', 'autoclose', 'urltrim', 'affitag', 'tree', 'autong', 'link_sw',
 'link_comu', 'link_news', 'link_shop', 'link_search', 'link_cust', 'link_topic', 'link_ust', 'nguse', 'wide_msg',
 'thumbnail_0', 'thumbnail_1', 'midoku_tl', 'link_twit', 'dummy1', 'dummy2', 'dummy3', 'dummy4' );

#カスタム項目初期値

%CUST = (

# ダミー項目 常に1
'custom' => 1,

# サムネイルサイズ
'thumbnail_0' => 0,
'thumbnail_1' => 1,

# フォロー投稿画面表示
#   1 : 新規ウィンドウをオープンして表示
#   0 : 同一画面に表示
'followwin' => 1,

# gzip圧縮
'gzip' => 1,

# 投稿後自動で閉じる 9/20
'autoclose' => 1,

# 特定URL自動短縮
'urltrim' => 1,

# アフィリエイトタグ付加
'affitag' => 0,

# ツリー表示
'tree' => 1,

# 自動NG
'nguse' => 0,
'autong' => 0,

# リンク行
'link_sw' => 1,
'link_comu' => 1,
'link_news' => 1,
'link_shop' => 1,
'link_search' => 0,
'link_cust' => 0,
'link_topic' => 1,
'link_ust' => 1,
'link_twit' => 1,

# 投稿欄を広げる
'wide_msg' => 0,

# 未読無し時TL表示
'midoku_tl' => 1,

);

##                                                                                ##
####################################################################################

# 自動NG
$autongword = <<EOF;
\@PlayTrueName
Σ\\||Σ:|ΣX
EOF
$autongword =~ s/\n$//g;

# 投稿者IPアドレスの記録
#   0 : 記録しない
#   1 : 匿名プロクシのみ記録
#   2 : 全て記録
$iprec = 2;

# User Agent(ブラウザ名)の記録
#   0 : 無効
#   1 : 有効
$uarec = 1;

# 投稿者IPアドレスの表示
# （投稿者IPアドレスの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$ipprint = 0;

# User Agent(ブラウザ名)の表示
# （User Agentの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$uaprint = 0;

# 同一IPアドレスからの投稿を拒否する時間 (秒)
# （投稿者IPアドレスの記録が有効になっている必要があります
#   0に設定すると一切制限しません）
$sptime = 5;

# Cookieによる投稿者／メールアドレス記憶機能の使用
#   0 : 無効
#   1 : 有効
$cookie = 1;

$cookiename = 'custom2';

# 管理人の名前
$adminname = 'admin';

# 管理人のメールアドレス
$adminmail = 'REDACTED@invalid';

# 管理用パスワード（最初は空のままにしておいてください）
$adminpost = ''; #REDACTED

# 管理モード移行用キーワード（必ず変更すること）
$adminkey = 'REDACTED';

# 広報室のURL
$infopage = './info.htm';

# データの受渡方法
$formmethod = 'post';


###############################################################################
#  システム用設定・変数（特に指示がない限り変更不可）
###############################################################################

$tmpl_msg = <<EOF;
<!-- \$postid -->
　投稿者：<b>\$user1</b>
　<font size="-1">投稿日：\$wdate\$btn</font>
<blockquote>
<pre>
\$msg
</pre>
\$envlist
</blockquote>
<hr>
<!-- -->
EOF

$S_pstime = 1;
$S_pltime = 3600;
$S_cexp = 7776000; #90day
$checked[0] = '';
$checked[1] = 'checked';


###############################################################################
#  時刻フォーマット変換
###############################################################################

sub getnowdate {

	( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdat )
		= localtime ( $_[0] );
	$year += 1900;
	$mon++;
	$nowdate = sprintf ( "%d/%02d/%02d(%s)%02d時%02d分%02d秒",
	  $year, $mon, $mday,
	  ( '日', '月', '火', '水', '木', '金', '土' )[$wday],
	  $hour, $min, $sec );
}


###############################################################################
#  フォームデータ取得
###############################################################################

sub getformdata {

#	my ( $formbuf, $name, $value );
#
#	if ( $ENV{'REQUEST_METHOD'} eq 'POST' ) {
#		read ( STDIN, $formbuf[0], $ENV{'CONTENT_LENGTH'} );
#	} else {
#		$formbuf[0] = $ENV{'QUERY_STRING'};
#	}
#
#	if ($ENV{CONTENT_LENGTH} > $maxmsgsize * 5) {
#	    &prterror ('投稿内容が大きすぎます。');
#	}
#
#	if ( $formbuf[0] ) {
#
#		&prterror ( '呼び出し元が不正です。' )
#		  if ( $ENV{'HTTP_HOST'} && ! ( $ENV{'HTTP_HOST'} =~ /$bbshost/i ) );
#
		$referer = $ENV{'HTTP_REFERER'};
		$referer =~ s/\+/ /g;
		$referer =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack ( "C", hex ( $1 ) )/eg; #URLに含まれる「%xx」の部分を、元の文字に戻す処理 lam
#
#		foreach ( split ( /&/, $formbuf[0] ) ) {
#			( $name, $value ) = split ( /=/ );
#
#			$value =~ tr/+/ / ;
#			$value =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
#			$value =~ s/~!/ ~!/g;
#
#			if($name ne 'ng' && $name ne 'customlink') {
#				$value =~ s/&/&amp;/g;
#				$value =~ s/"/&quot;/g;
#				$value =~ s/'/&#39;/g;
#				$value =~ s/</&lt;/g;
#				$value =~ s/>/&gt;/g;
#			}
#
#			$value =~ s/\015\012/\015/g;
#			$value =~ s/\012/\015/g;
#			$value =~ s/\015$//g;
#
#			$value =~ s/\,/\0/g;
#			$FORM{$name} = $value;
#		}
#	}

	if ( $ENV{'HTTP_HOST'} && ! ( $ENV{'HTTP_HOST'} =~ /$bbshost/i ) ){
		&prterror ( '呼び出し元が不正です。' );
	}

	use CGI;
	$query = CGI->new;
	my @params = $query->param();
	foreach my $param (@params) {
		my $value = $query->param($param);

		$value =~ s/~!/ ~!/g;

		if($param ne 'ng' && $param ne 'customlink') {
			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/'/&#39;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
		}

		$value =~ s/\015\012/\015/g;
		$value =~ s/\012/\015/g;
		$value =~ s/\015$//g;

		$value =~ s/\,/\0/g;

		$FORM{$param} = $value;
	}



#デバッグ
#	print "Content-type: text/html\n\n";
#	print "<pre>";
#
#	foreach my $name ( keys %FORM ){
#		print "\FORM{$name} = $FORM{$name}\n";
#	}
#
#	print "</pre>";
#	exit;




}

###############################################################################
#  日本語文字コード変換
###############################################################################

sub jconv {

	if ( ( $FORM{'k'} ne 'あ' && $FORM{'v'} ) || $FORM{'j'} ) { #$FORM{'k'} ne 'あ' はsjis以外で投稿されたときにtrue
		require "$jcode";
		foreach ( keys %FORM ) { #keys 関数は，ハッシュの全要素のキーがならんだリストを返します． lam
#			&jcode'convert ( \$FORM{$_}, 'sjis' );
			#perl5対応? epicの色分けが破綻するので lam 6/24
			jcode::convert ( \$FORM{$_}, 'sjis' );
		}
	}
}


###############################################################################
#  環境変数取得
###############################################################################

sub getenv {

	if ( $uarec ) {
		$agent = $ENV{'HTTP_USER_AGENT'};
		$agent =~ s/</&lt;/g;
		$agent =~ s/>/&gt;/g;
		$agent =~ s/,/./g;
	}

	if ( !$iprec ) { return; }

	$addr = $ENV{'REMOTE_ADDR'};
	$host = $ENV{'REMOTE_HOST'};
	if ( $addr eq $host || !$host ) {
		$host = gethostbyaddr ( pack ( 'C4', split ( /\./, $addr ) ), 2 ) || $addr; #IPアドレスからホスト名への変換はgethostbyaddrを利用して行います
	}

	$proxyflg = 0;

	if ( $ENV{'HTTP_CACHE_CONTROL'} )			{ $proxyflg = 1; }
	if ( $ENV{'HTTP_CACHE_INFO'} )				{ $proxyflg += 2; }
	if ( $ENV{'HTTP_CLIENT_IP'} )				{ $proxyflg += 4; }
	if ( $ENV{'HTTP_FORWARDED'} )				{ $proxyflg += 8; }
	if ( $ENV{'HTTP_FROM'} )					{ $proxyflg += 16; }
	if ( $ENV{'HTTP_PROXY_AUTHORIZATION'} )		{ $proxyflg += 32; }
	if ( $ENV{'HTTP_PROXY_CONNECTION'} )		{ $proxyflg += 64; }
	if ( $ENV{'HTTP_SP_HOST'} )					{ $proxyflg += 128; }
	if ( $ENV{'HTTP_VIA'} )						{ $proxyflg += 256; }
	if ( $ENV{'HTTP_X_FORWARDED_FOR'} )			{ $proxyflg += 512; }
	if ( $ENV{'HTTP_X_LOCKING'} )				{ $proxyflg += 1024; }
	if ( $agent =~ /cache|delegate|gateway|httpd|proxy|squid|www|via/i ) {
		$proxyflg += 2048;
	}
	if ( $host =~ /cache|^dns|dummy|^ns|firewall|gate|keep|mail|^news|pop|proxy|smtp|w3|^web|www/i ) {
		$proxyflg += 4096;
	}
	if ( $host eq $addr ) {
		$proxyflg += 8192;
	}

	$realaddr = '';
	$realhost = '';
	if ( $proxyflg > 0 ) {

		if ( $ENV{'HTTP_X_FORWARDED_FOR'} =~
		  s/^(\d+)\.(\d+)\.(\d+)\.(\d+).*/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_FORWARDED'} =~
		  s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_VIA'} =~
		  s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_CLIENT_IP'} =~
		  s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_SP_HOST'} =~
		  s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_FORWARDED'} =~ s/.*\sfor\s(.+)/$1/ ) {
			$realhost = "$1";
		} elsif ( $ENV{'HTTP_FROM'} =~ s/\-\@(.+)/$1/ ) {
			$realhost = "$1";
		}

		if ( !$realaddr && $realhost ) {
			$realpackaddr = gethostbyname ( $realhost );
			( $a, $b, $c, $d ) = unpack ( 'C4', $realpackaddr );
			$realaddr = "$a.$b.$c.$d";
		}

		if ( $realaddr && $iprec != 2 ) {
			$host = '(leak)';
		}
	} else {
		$host = '(none)' if ( $iprec != 2 );
	}
}


###############################################################################
#  文字列のエンコード
###############################################################################

#改行コードに対応してない
#sub escstring {
#
#	my ( $srcstr ) = $_[0];
#
#	$srcstr =~ s/([^a-zA-Z0-9\s])/sprintf ( "%%%lx", ( unpack ( "C", $1 ) ) )/eg;
#	$srcstr =~ s/ /\+/g;
#
#	return $srcstr;
#}

sub url_encode($) {
  my $str = shift;
  $str =~ s/([^\w ])/'%'.unpack('H2', $1)/eg;
  $str =~ tr/ /+/;
  return $str;
}

sub url_decode($) {
  my $str = shift;
  $str =~ tr/+/ /;
  $str =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
  return $str;
}


###############################################################################
#  メッセージ読み込み
###############################################################################

sub loadmessage {

	my $openlog;

	if ( !$FORM{'ff'} ) {
		$openlog = $logfilename;
	} else { #過去ログ
		$FORM{'ff'} =~ /^([\w.]*)$/;
		$openlog = "$oldlogfiledir/$1";
	}

	open ( READLOG, "$openlog" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( READLOG, 1 )';
	seek ( READLOG, 0, 0 );
	@logdata = <READLOG>;
	eval 'flock ( READLOG, 8 )';
	close ( READLOG );
}


###############################################################################
#  メッセージ１件取得
###############################################################################

sub getmessage {

	( $ndate, $postid, $protect, $thread, $phost, $agent, $user, $twitid, $title, $msg )
	  = split ( /\,/, $_[0] );
	$msg =~ s/\n$//;
	$title =~ s/\0/\,/g;
	$user =~ s/\0/\,/g;
	$msg =~ s/\0/\,/g;
	$wdate = &getnowdate ( $ndate );
}


###############################################################################
#  メッセージ１件出力
###############################################################################

sub prtmessage {

	my $mode = $_[0];	# 0 : 掲示板 1 : 過去ログ(ボタン表示あり) 2 : 過去ログ(ボタン表示なし) 3 : 検索窓
	my $tlog = $_[1];
	my ( $tag, $refdate, $prtmessage, $btn, $btnfollow, $btnauthor, $btnthread, $newwin,
	  $envlist, $envaddr, $envua, $envbr );

	# 「参考」
	if ( $mode == 0 || $mode == 3 ) {
		$msg =~ s/<a href=\"m=f\&s=(\d+)\&r=(\S+)\">(.*)<\/a>/<a href=\"$cgiurl\?m=f&s=$1\&r=$2\">$3<\/a>/i;
		$msg =~ s/<a href=\"mode=follow\&search=(\d+)\&ref=(\S+)\">(.*)<\/a>/<a href=\"$cgiurl\?m=f\&s=$1\&r=$2\">$3<\/a>/i;
	} else {
		$msg =~ s/<a href=\"m=f\&s=(\d+)\&r=(\S+)\">(.*)<\/a>/<a href=\"#$1\">$3<\/a>/i;
		$msg =~ s/<a href=\"mode=follow\&search=(\d+)\&ref=(\S+)\">(.*)<\/a>/<a href=\"#$1\">$3<\/a>/i;
	}

	if ( $mode == 0 || $mode == 3 || ( $mode == 1 && $oldlogbtn && $oldlogfmt ) ) {

		if ( $CUST{'followwin'} ) { $newwin = " target=\"_blank\""; }
		else { $newwin = '' };

		# フォロー投稿ボタン
		$btnfollow = "<a href=\"$cgiurl\?m=f\&u=".
		  &url_encode ( $FORM{'u'} ) .
		  "&d=$FORM{'d'}&p=$toppostid&s=$postid";
		if ( !$mode ) {
			$btnfollow .= "\"";
		} elsif ( $mode == 3 ) {
			$btnfollow .= "&ac=1\"";
		} else {
			$btnfollow .= "&ff=$tlog\"";
		}
		$btnfollow .= qq( title="$user");
		$btnfollow .= "$newwin>$txtfollow</a>　\n";

		# 投稿者検索ボタン
		$btnauthor = "<a href=\"$cgiurl\?m\=s\&s\=".
		  &url_encode ( $user ) .
		  "\" target=\"link\">$txtauthor</a>　\n";

		# スレッド表示ボタン
		if ( $thread ) {
			$btnthread = "<a href=\"$cgiurl\?m\=t".
			  "\&s\=$thread\" target=\"link\">$txtthread</a>\n";
		} else {
			$btnthread = '';
		}

		$btn = "　\n  $btnfollow  $btnauthor  $btnthread";
	} else {
		$btn = '';
	}

	# メールアドレス
	if ( $mail ) {
		$user = "<a href=\"mailto\:$mail\">$user<\/a>";
	}

	# 引用色変更
	if ( !$mode ) {
		$msg =~ s/(^|\r)(&gt;[^\r]*)/$1<font color=\"#$CC{'qmsgc'}\">$2<\/font>/g;
		$msg =~ s/<\/font>\r<font color=\"#$CC{'qmsgc'}\">/\r/g;
	} elsif ( $mode >= 1 && $qmsgc ) {
		$msg =~ s/(^|\r)(&gt;[^\r]*)/$1<font color=\"#$qmsgc\">$2<\/font>/g;
		$msg =~ s/<\/font>\r<font color=\"#$qmsgc\">/\r/g;
	}

	# 環境変数
	if ( $ipprint ) {
		$envaddr = $phost;
	} else {
		$envaddr = '';
	}
	if ( $uaprint ) {
		$envua = $agent;
	} else {
		$envua = '';
	}
	if ( $ipprint && $uaprint ) {
		$envbr = '<br>';
	}
	if ( $envaddr || $envua ) {
		$envlist = qq!<font size="-1"><i>$envaddr$envbr$envua</i></font>!;
	} else {
		$envlist = '';
	}

	# アンカータグを付加 9/30
	my $urlchar = "[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]";
	$msg =~ s#(^|[^"])((https?|ftp|gopher|telnet|whois|news)://$urlchar+)#$1<a href="$2" target="_blank">$2</a>#ig;

	if($CUST{'affitag'}){
		s#<a href="http://(?:www\.)?amazon\.co\.jp/$urlchar*(?:ASIN/|dp/|product/)(\w*)$urlchar*"#<a href="http://www.amazon.co.jp/dp/$1?tag=$amazontag"#ig;
		s#(<a href="http://(?:www\.)?amazon\.co\.jp)/?"(.*?\0)#$1/?tag=$amazontag&linkCode=ure&creative=6339"$2#ig;
	}


	#リンクサムネイル化 9/30
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
		$msg =~ s#(https?://$urlchar+\.(?:gif|jpe?g|png))(.*?)(?:\r|$)#$1$2\r<a href="$1" target="_blank"><img src="$1" $thumnailsize></a>\r#ig;

		#youtube
		$msg =~ s#(https?://(?:www\.youtube\.com/watch\?.*?v=|youtu\.be\/)([\w-]+))(.*?)(?:\r|$)#$1$3\r<a href="$1" target="_blank"><img src="http://i.ytimg.com/vi/$2/$youtubethum.jpg"><img src="res/youtube.png" style="position:relative; left:-16px;"></a>\r#ig;

		#ニコ動
		$msg =~ s#(https?://(?:www\.nicovideo\.jp/watch|nico.ms)/[a-z][a-z](\d+)/?)(.*?)(?:\r|$)#sprintf("$1$3\r<a href=\"$1\" target=\"_blank\"><img src=\"http://tn-skr%d.smilevideo.jp/smile?i=$2\"><img src=\"res/nicovideo.png\" style=\"position:relative; left:-16px;\"></a>\r",($2 % 4)+1)#ige;

		#amazon
		$msg =~ s#(https?://(?:www\.)?amazon\.co\.jp/$urlchar*(?:ASIN/|dp/|product/)(\w*)$urlchar*)(.*?)(?:\r|$)#$1$3\r<a href="$1"><img src="http://images-jp.amazon.com/images/P/$2$amazonthum.jpg"><img src="res/amazon.png" style="position:relative; left:-16px;"></a>\r#ig;
	}


	if($FORM{'m'} ne 'f') {
		#NG
		if ($FORM{'ng'}) {
			$FORM{'ng'} =~ s/\r/|/g;
			if ($msg =~ /$FORM{'ng'}/ || $user =~ /$FORM{'ng'}/) {
				$user = "　";
				$msg = qq(<font color="#$CC{'qmsgc'}">…</font>\r);
			}
		}
		#自動NG
		if ($CUST{'autong'}) {
			$autongword =~ s/\n/|/g;
			if ($msg =~ /$autongword/ || $user =~ /$autongword/) {
				$user = "　";
				$msg = qq(<font color="#$CC{'qmsgc'}">…</font>\r);
			}
		}
	}

	#Twitterリンク化
	$msg =~ s|\@([a-zA-Z0-9_]+)|<a href="https://twitter.com/#!/$1" target="_blank">\@$1</a>|g;
	$user1 = $user;
	$user1 =~ s|^\@([a-zA-Z0-9_]+)$|<a href="https://twitter.com/#!/$1" target="_blank">$user1</a>|;


	#フォロー画面以外では投稿者名を表示しない
	if ( $FORM{'m'} ne 'f' ) {
		$user1 = "　";
	}

	# メッセージ表示内容定義
	$prtmessage = qq(<a name="$postid"></a>\n$tmpl_msg);
	$prtmessage =~ s/(\$[A-Za-z0-9\'\{\}]+)/$1/eeg;

	return $prtmessage;
}


###############################################################################
#  こわれにくいカウンター処理
###############################################################################

sub counter {

	my ( @count, @filenumber, @sortedcount, $maxcount, $mincount );

	for ( $i = 0 ; $i < $countlevel ; $i++ ) {
		open ( IN, "$countfile$i.dat" );
		$count[$i] = <IN>;
		$filenumber{$count[$i]} = $i;
		close ( IN );
	}

	@sortedcount = sort { $a <=> $b; } @count;
	$maxcount = $sortedcount[$countlevel-1];
	$mincount = $sortedcount[0];

	$maxcount++;

	if ( open ( OUT, ">$countfile$filenumber{$mincount}.dat" ) ) {
		print OUT $maxcount;
		close ( OUT );
		return $maxcount;
	} else {
		return '<font color="red">カウンターファイルの出力エラーです</font>';
	}
}


###############################################################################
#  参加者カウント
###############################################################################

sub mbrcount {

	my ( @hostbin, @ukey, @cntdata, $mbrcount, $cuser, $ctime, $cadd );

	if ( $cntfilename ) {
		undef @cntdata;
		$mbrcount = 0;
		@hostbin = split ( /\./, $ENV{'REMOTE_ADDR'} );
		for ( $i = 0 ; $i < 4 ; $i++ ) {
			$hostbin[$i] = vec ( pack ( 'C4', $hostbin[$i] ), 0, 8 );
		}
		$ukey[0] = $hostbin[0] + $hostbin[1] + $hostbin[2] + $hostbin[3];
		$ukey[1] = $hostbin[0] ^ $hostbin[1] & $hostbin[2] ^ $hostbin[3];
		$ukey[2] = $ukey[0] * $ukey[1];

		if ( open ( UCNT, $cntfilename ) ) {
			eval 'flock ( UCNT, 1 )';
			seek ( UCNT, 0, 0 );
			@cntdata = <UCNT>;
			eval 'flock ( UCNT, 8 )';
			close ( UCNT );

			$cadd = 0;
			for ( $i = 0 ; $i < @cntdata ; $i++ ) {
				( $cuser, $ctime ) = split ( /\,/, $cntdata[$i] );
				chomp ( $ctime );
				if ( $cuser eq $ukey[2] ) {
					$cntdata[$i] = "$ukey[2],$nowtime\n";
					$cadd = 1;
					$mbrcount++;
				} elsif ( ( $ctime + $cntlimit ) < $nowtime ) {
					# 除外
					$cntdata[$i] = '';
				} else {
					$mbrcount++;
				}
			}
			if ( !$cadd ) {
				push ( @cntdata, "$ukey[2],$nowtime\n" );
				$mbrcount++;
			}
		} else {
			push ( @cntdata, "$ukey[2],$nowtime\n" );
			$mbrcount++;
		}

		open ( UCNT, ">>$cntfilename" ) || &prterror ( '参加者カウントファイルの書き込みに失敗しました。' );
		eval 'flock ( UCNT, 2 )';
		truncate ( UCNT, 0 );
		seek ( UCNT, 0, 0 );
		print UCNT @cntdata;
		close ( UCNT );

		#lam 6/26
#		$cntlimit /= 60;
#		return "　現在の参加者 : $mbrcount名 ($cntlimit分以内)";
		return "　現在の参加者 : $mbrcount名 ($cntlimit秒以内)";
	} else {
		return;
	}
}


###############################################################################
#  HTMLヘッダ部分表示
###############################################################################

sub prthtmlhead {

	my $headtitle = $_[0];

	# ヘッダ出力
	print "Content-type: text/html\n";
	if ( $gzip && $CUST{'gzip'} && ( $ENV{'HTTP_ACCEPT_ENCODING'} =~ /gzip/ ) ) {
		print "Content-encoding: gzip\n\n";
		open ( STDOUT, "| $gzip -1 -c" );
		print "<!-- gzip enable -->";
	} else {
		print "\n<!-- gzip disable -->";
	}

	print <<EOF;
<html>
<head>
<title>$headtitle</title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="shortcut icon" href="res/favicon.ico">

<style type="text/css">
<!--
  img { border: none; }
-->
</style>

<style type="text/css">
<!--
 .rss_box {
 	margin: 1em;
 }

 .rss_box ul{
 	padding-left: 1.5em;
 }

 .rss_title, rss_title a {
 }

 .rss_item {
  font-size: xx-small;
}


.rss_item a:link, .rss_item a:visited, .rss_item a:active {
  font-size: small;
}

.rss_item a:hover {

}

.rss_date {
  font-size: xx-small;
  color: #$CC{'qmsgc'};
}
-->
</style>




<script type="text/javascript">
<!--
function dofocus() {

	var elm = document.form.v;
	elm.focus();

	if (elm.createTextRange) {
		var range = elm.createTextRange();
		range.move('character', elm.value.length);
		range.select();
	} else if (elm.setSelectionRange) {
		elm.setSelectionRange(elm.value.length, elm.value.length);
	}

}
-->
</script>

</head>

$body
EOF
}


###############################################################################
#  エラーメッセージ表示
###############################################################################

sub prterror {

	my $error = $_[0];

	print <<EOF;
Content-type: text/html

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Pragma" content="no-cache">
<title>$bbstitle (エラー)</title>
</head>
$body
<h3>$error</h3>
</body>
</html>
EOF
	exit;
}


###############################################################################
#  フォロー画面表示
###############################################################################

sub prtfollow {

	my $retry = $_[0];
	my $success = 0;
	my $formmsg;

	&loadmessage;

	&prterror ( 'パラメータがありません。' ) if ( !$FORM{'s'} );

	&prthtmlhead ( "$bbstitle フォロー投稿" );

	print <<EOF;
<h3><a href="REDACTED" style="color: \#$textc; text-decoration: none;">$bbstitle</a></h3>
<hr>
EOF

	foreach ( 0 .. @logdata - 1 ) {
		&getmessage ( $logdata[$_] );
		if ( $postid eq $FORM{'s'} ) {
			$success = 1;
			last;
		}
		$i++;
	}

	if ( !$success ) {
		print "<h3>指定されたメッセージが見つかりません。</h3></body></html>";
		exit;
	}

	if ( !$retry ) {
		$formmsg = $msg;
		$formmsg =~ s/&gt; &gt;.*?\r//g;
		$formmsg =~ s/<a href=\"m=f\S+\">.*<\/a>//i;
		$formmsg =~ s/<a href=\S+ target=\"link\">(\S+)<\/a>/$1/ig;
		$formmsg =~ s/\r/\r&gt; /g;
		$formmsg = "&gt; $formmsg\r";
		$formmsg =~ s/\r&gt;\s+\r/\r/g;
		$formmsg =~ s/\r&gt;\s+\r$/\r/g;
		$formmsg .= "\r";
	} else {
		$formmsg = "$FORM{'v'}";
		$formmsg =~ s/\r\r<a href=\"m=f\S+\">.*<\/a>//i;
	}

	print &prtmessage ( 0, '' );

	if ( !$thread ) {
		$thread = $postid;
	}

#	if ( $user =~ /\<A\shref=\"mailto\:.*\"\>(.*)\<\/A\>/ ) {
#		$user = $1;
#	}
	print "フォロー記事投稿<br>\n";
	&prtform ( "＞$user$fsubj", "$formmsg", '' );
#	変更予定 lam
#	&prtform ( '', '', '' );

	print <<EOF;
  <br>
  <input type="hidden" name="d" value="$FORM{'d'}">
  <input type="hidden" name="g" value="$checked[$CUST{'gzip'}]">
  <input type="hidden" name="p" value="$FORM{'p'}">
  <input type="hidden" name="s" value="$FORM{'s'}">
  <input type="hidden" name="h" value="$thread">
  <input type="hidden" name="f" value="$postid:$wdate">
  <input type="hidden" name="ac" value="$FORM{'ac'}">
  <input type="hidden" name="fuser" value="$user">
  <input type="hidden" name="ftwitid" value="$twitid">
  <hr>
  <p align="right"><font size="-1"><a href="./info.htm#copyright">$bbstitle_at</font></a></p>
</form>
</body>
</html>
EOF

	exit;
}


###############################################################################
#  パスワードチェック
###############################################################################

sub chkpasswd {

	my $slen;

	if ( $adminpost =~ /^\$1\$/ ) {
		$slen = 5;
	} else {
		$slen = 2;
	}

	if ( crypt ( $FORM{$adminkey}, substr ( $adminpost, 0, $slen ) ) eq $adminpost ) {
		return 1;
	} else {
		return 0;
	}
}


###############################################################################
#  メッセージチェック
###############################################################################

sub chkmessage {

	my ( @hostbin, $admincheck, $adminfname );

	if ( $referer && ! ( $referer =~ /$cgiurl/i ) ) {
		&chkerror ( "投稿画面のＵＲＬが<br>$cgiurl<br>" .
		  '以外からの投稿はできません。',  3 );
	}

	if ($CUST{'urltrim'}) {
		my $urlchar = "[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]";
		$FORM{'v'} =~ s#http://(?:www\.)?amazon\.co\.jp/$urlchar*(?:ASIN/|dp/|product/)(\w*)$urlchar*#http://www.amazon.co.jp/dp/$1#ig;
	}

	$i = 0;
	foreach ( split ( /\r/, $FORM{'v'} ) ) {
		if ( length ( $_ ) > $maxmsgcol ) {
			$i++;
		}
	}
	if ( $i != 0 ) { &chkerror ( '投稿内容の桁数が大きすぎます。', 10 ); }

	if ( ( $FORM{'v'} =~ tr/\r/\r/ ) > ( $maxmsgline - 1 ) ) {
		&chkerror ( '投稿内容の行数が大きすぎます。', 11 );
	}

	if ( length ( $FORM{'v'} ) > $maxmsgsize ) {
		&chkerror ( '投稿内容が大きすぎます。', 12 );
	}

	if ( $FORM{'pc'} ) {
		@hostbin = split ( /\./, $ENV{'REMOTE_ADDR'} );
		for ( $i = 0 ; $i < 4 ; $i++ ) {
			$hostbin[$i] = vec ( pack ( 'C4', $hostbin[$i] ), 0, 8 );
		}
		$protect_c = $hostbin[0] ^ $hostbin[1] ^ $hostbin[2] ^ $hostbin[3];
		$pcheck = ( $FORM{'pc'} - $protect_c ) / $protect_b - $protect_a; #pcode生成の逆算で生成時の$nowtimeを求める
		&getnowdate ( $pcheck );
		if ( ( $sec  < 0 ) || ( $sec  > 60 ) ||
		  ( $min  < 0 ) || ( $min  > 60 ) ||
		  ( $hour < 0 ) || ( $hour > 24 ) ) {
			&chkerror ( '', 32 );
		}
		if ( ( $nowtime - $pcheck ) < $S_pstime ) {
			&chkerror ( 'もう一度やり直して下さい。', 30 );
		}
		if ( ( $nowtime - $pcheck ) > $S_pltime ) { # フォーム作成から投稿まで $S_pltime = 3600 秒以上経過していたらエラー
			&chkerror ( '', 31 );
			if ( $FORM{'f'} ) {
				&prtfollow ( 1 );
			} else {
				&prtmain ( $FORM{'t'}, $FORM{'v'}, $FORM{'l'} );
			}
			exit;
		}
	} else {
		&chkerror ( 'フォームデータの一部に欠落があります。もう一度やり直して下さい。', 33 );
	}

#	if ( $FORM{'i'} =~ / /i ) {
#		$FORM{'i'} = '';
#	}
#	if ( $FORM{'i'} ) {
#		if ( ! ( $FORM{'i'} =~ /.*\@.*\..*/ ) ) {
#			&chkerror ( 'メールアドレスが正しく入力されていません。', 20 );
#		} elsif ( $FORM{'i'} =~ /,/ ) {
#			&chkerror ( 'メールアドレスは複数指定できません。', 21 );
#		}
#	}

	if ( !$FORM{'t'} ) {
		$FORM{'t'} = ' ';
	}

	$postname = $FORM{'u'}; #入力された名前と記録される名前を分けるlam 6/29
	if ( !$FORM{'u'} ) {
		$postname = '　';
	} else {
#管理者ログイン方法変更 lam 6/30
#		if ( &chkpasswd ) {
#			if ( $FORM{'v'} =~ /^$adminkey/ ) {
#				require 'sub/bbsadmin.pl';
#				&adminmain;
#				exit;
#			} else {
#				$postname = $adminname;
#				$FORM{'i'} = $adminmail;
#			}
#		} elsif ( $FORM{'u'} eq $adminpost ) {
#			$postname = "$adminname（ハカー）";
#		} else {
#			$adminfname = quotemeta $adminname;
#			if ( $FORM{'u'} =~ /$adminfname/i ) {
#				$admincheck = $FORM{'u'};
#				$admincheck =~ s/ //g;
#				$admincheck =~ s/　//g;
#				$admincheck =~ s/_//g;
#				if ( $admincheck eq $adminname ) {
#					$postname =~ s/$adminfname/$adminname（騙り）/;
#				}
#			}
#		}

		#管理者投稿用 lam 6/30
		if ( $FORM{'u'} eq 'admin_x') {
			$postname = $adminname;
#			$FORM{'i'} = $adminmail;
		} else {
			$adminfname = quotemeta $adminname;
			if ( $FORM{'u'} =~ /$adminfname/i ) {
				$admincheck = $FORM{'u'};
				$admincheck =~ s/ //g;
				$admincheck =~ s/　//g;
				$admincheck =~ s/_//g;
				if ( $admincheck eq $adminname ) {
					$postname =~ s/$adminfname/$adminname（騙り）/;
				}
			}
		}

		#トリップ変換 lam 6/29
		$postname =~ s/\◆/\◇/g;
		if ( $FORM{'u'} =~ /#(.+)/ ) {
			my $trip;
			my $key = $1;
			my $salt = substr( $key.'H.', 1, 2 );
			$salt =~ s/[^\.-z]/\./g;
			$salt =~ tr/:;<=>?@[\\]^_`/ABCDEFGabcdef/;
			$trip = '<em>◆' . substr( crypt ( $key, $salt ), -10 ) .'</em>';
			$postname =~ s/^#.+/$trip/ if ( $trip );
			$postname =~ s/#.+/ $trip/ if ( $trip );
		}

		#生入 9/20
		$postname =~ s#生入#<em>$host</em>#;

		#Twitter騙り防止
		$postname =~ s#^\@+##;

	}

#	if ( $autolink ) {
#		$FORM{'v'} =~ s#((https?|ftp|gopher|telnet|whois|news)://(=[\x21-\xfc\0]+|[\x21-\x7e\0])+)#<a href="$1" target="link">$1</a>#ig;
#	}



#	if ( $FORM{'l'} =~ /\s+/ || !$FORM{'l'} ) {
#		$FORM{'l'} = '';
#	} else {
#		$FORM{'l'} =~ s/http:\/\/http:\/\//http:\/\//;
#		$FORM{'v'} .= "\r\r<a href=\"$FORM{'l'}\" target=\"link\">$FORM{'l'}</a>";
#	}
	if ( $FORM{'f'} && !$FORM{'newpost'} ) {
		( $i, $j ) = split ( /:/, $FORM{'f'} );
		$FORM{'v'} .= "\r\r<a href=\"m=f\&s=$i\&r=$j\">参考：$j</a>";
	}


	#管理用
	my $flg=10**9;
	my $flg2=0;
	if(!($host =~ /\.jp/) && !($host =~ /^softbank/)){
		$flg += 10**0;
		$flg2 += 5;
	}
	if($FORM{'u'}){
		$flg += 10**1;
		$flg2 += 2;
	}
#	if($FORM{'u'} =~ /^[\w\s]+$/){
#		$flg += 10**2;
#		$flg2 += 2;
#	}
	my $v_ = $FORM{'v'};
	# 引用部分の消去
	$v_ =~ s|(&gt; .*?\r)||g;
	# 参考の消去
	$v_ =~ s|<a href="\S+">参考：(\S+)</a>||gi;
	$v__ = $v_;
	require $jcode;
	jcode::convert(\$v_, 'euc');
	if(!($v_ =~ /[\xA1-\xFE][\xA1-\xFE]/ || $v_ =~ /\x8E/ || $v_ =~ /[\x8E\xA1-\xFE]/)){
		$flg += 10**3;
		$flg2 += 4;
	}
	if($FORM{'f'}){
		$flg += 10**4;
		$flg2 += 1;
	}
	if($FORM{'f'} =~ /[^0-9:\/\(\)時分秒月火水木金土日]/){
		$flg += 10**5;
		$flg2 += 1000;
	}

	#スパム対策
	if($host =~ /REDACTED/){
		$flg += 10**6;
		$flg2 += 4;
	}
	for ('REDACTED') {
		if ($v__ =~ /$_/) {
			$flg += 10**7;
			$flg2 += 2;
		}
	}
	for ('REDACTED') {
		if ($v__ =~ /$_/) {
			$flg += 10**8;
			$flg2 += 4;
		}
	}

	$FORM{'t'} = "flg=$flg flg2=$flg2";

	#デバッグ
	#prterror($FORM{'t'});

	#書き込み無効化
	if($flg2 >= 6 && !$debug){
		if ( $FORM{'ac'} || ( $FORM{'f'} && $CUST{'followwin'} ) || $FORM{'newpost'} ) {
			if($CUST{'autoclose'}){
				$body = qq(<body bgcolor="#$CC{'bg'}" text="#$CC{'text'}" link="#$CC{'link'}" vlink="#$CC{'vlink'}" alink="#$alinkc" onload='window.close();'>);
			}
			&prthtmlhead ( "$bbstitle 書き込み完了" );
			print <<EOF;
<h2>書き込み完了</h2>
</body>
</html>
EOF
			exit;
		}
		undef $FORM{'f'}

		&prtmain ( '', '', '' );
		exit;
	}



}


###############################################################################
#  メッセージチェックエラー処理
###############################################################################

sub chkerror {

	my $errstr = $_[0];
	$posterr = $_[1];

	&prterror ( $errstr ) if ( $errstr );
}


###############################################################################
#  メッセージ登録
###############################################################################

sub putmessage {

	my $oldlogext;

	open ( FLOG, "+<$logfilename" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( FLOG, 2 )';
	seek ( FLOG, 0, 0 );
	@logdata = <FLOG>;



	$i = 0;
	if( $FORM{'ftwitid'} && ( $twitreppost || $FORM{'newpost'} ) ) {
		while ( $logdata[$i] ) {
			my @items = split ( /\,/, $logdata[$i] );
			if( $items[7] == $FORM{'ftwitid'} ){
				if( $items[3] ) {
					$FORM{'h'} = $items[3];
				} else {
					$FORM{'h'} = $items[1];
				}
				my $date = &getnowdate( $items[0] );

				my $formmsg = $items[9];
				$formmsg =~ s/\n$//;
				$formmsg =~ s/&gt; &gt;.*?\r//g;
				$formmsg =~ s/<a href=\"m=f\S+\">.*<\/a>//i;
				$formmsg =~ s/\r/\r&gt; /g;
				$formmsg = "&gt; $formmsg\r";
				$formmsg =~ s/\r&gt;\s+\r/\r/g;
				$formmsg =~ s/\r&gt;\s+\r$/\r/g;
				$formmsg .= "\r";

				$FORM{'v'} = qq($formmsg$FORM{'v'});
				$FORM{'v'} .= qq(\r\r<a href="m=f&s=$items[1]&r=$date">参考：$date</a>);
				last;
			}
			$i++;
		}
	}

	$posterr = 0;
	while ( $logdata[$i] && !$posterr) {
		my @items = split ( /\,/, $logdata[$i] );
		$items[9] =~ s/\n$//;
		$posterr = 1 if ( $i < $checkcount && $FORM{'v'} eq $items[9] ); # $checkcount = 30 以内に同じ内容の投稿があったらエラー
		
		if( !$twitreppost ) {
			$posterr = 2 if ( $FORM{'pc'} eq $items[2] ); #同じフォームから2度投稿されたらエラー
			$posterr = 2 if ( $host && ( $host eq $items[4] ) && ( $nowtime < ( $items[0] + $sptime ) ) ); #同一IPからの連続投稿を拒否
		}
		$i++;
	}
	
	if ( !$posterr ) {

		my @items = split ( /\,/, $logdata[0] );
		$newpostid = $items[1] + 1;


		#添付ファイルアップロード
		if($FORM{'filedata'} ne ""){
			require "${sub}upload.pl";
			&upload;
		}

		#Twitter投稿
		if( !$twitreppost && $twitter) {
			use Jcode;
			&twit_init;
			my $twit_msg = $FORM{'v'};
#			if( $FORM{'f'} ) {
			if( $FORM{'f'} || $FORM{'ftwitid'} ) {
				# 引用部分の消去
				$twit_msg =~ s|(&gt; .*?\r)||g;
				# 参考の消去
				$twit_msg =~ s|<a href="\S+">参考：(\S+)</a>||gi;
				
#				if( $FORM{'fuser'} =~ /^\@[A-Za-z0-9_]+$/ ) {
#					$repname = $FORM{'fuser'};
#				} else {
#					$repname = "\@$my_twit_id"
#				}

				if( $FORM{'ftwitid'} ) {
					my $s;
					eval { $s = $twit->show_status( $FORM{'ftwitid'} ); };
					if ( $@ ) { err("$@\n"); }
					$repname = "\@$s->{user}->{screen_name}";
				} else {
					$repname = "\@$my_twit_id"
				}
				
				if( !$FORM{'retweet'} ) {
					$twit_msg = "$repname $twit_msg";
				}
				
			}

#			$twit_msg = "\@REDACTED $twit_msg";

			if( &zlength($twit_msg) > 140  ){
				$twit_msg = z_substr($twit_msg, 0, 140-1, 2);
				$twit_msg .= "…";
			}

			&Jcode::convert( \$twit_msg, "utf8", "sjis" );
			utf8::decode($twit_msg);

			#RTリツイート
			if( $FORM{'retweet'} ){
				eval { $status = $twit->retweet( $FORM{'ftwitid'} ); };
			}
			if ( $@ ) {
 			   err("retweet failed because: $@\n");
			}

			if( $FORM{'ftwitid'} ){
				eval { $status = $twit->update({ status => $twit_msg, in_reply_to_status_id => $FORM{'ftwitid'} }); };
			} else {
				eval { $status = $twit->update({ status => $twit_msg }); };
			}
			if ( $@ ) {
 			   err("update failed because: $@\n");
			}
			$twitid = $status->{'id'};
		}

		#板に未投稿のツイートに対するレスはレス元の引用を加える
		if ( $FORM{'newpost'} && !$FORM{'h'} && $FORM{'ftwitid'} ) {
			use Jcode;
			&twit_init;

			my $s;
			eval { $s = $twit->show_status( $FORM{'ftwitid'} ); };
			if ( $@ ) { err("$@\n"); }
		    my $name = $s->{user}->{screen_name};
		    my $text = $s->{text};
			&Jcode::convert( \$name, "sjis", "utf8" );
			&Jcode::convert( \$text, "sjis", "utf8" );
			$text =~ s/\n/\r/g;
			$text =~ s/\r/\r&gt; /g;
			$text = "&gt; " . $text;

			$FORM{'v'} = qq(&gt; \@$name\r$text\r\r$FORM{'v'});
		}


		$msgdata = "$nowtime,$newpostid,$FORM{'pc'},$FORM{'h'},$host,$agent,$postname,$twitid,$FORM{'t'},$FORM{'v'}\n";

		@logdata = @logdata[0 .. $logsave - 2] if ( @logdata >= $logsave );
		unshift ( @logdata, $msgdata );

		$oldstream = select ( FLOG );
		$| = 1;
		seek ( FLOG, 0, 0 );
		truncate ( FLOG, 0 );
		print FLOG @logdata;
		eval 'flock ( FLOG, 8 )';
		close ( FLOG );
		select ( $oldstream );

		&getnowdate ( $nowtime );

		# 過去ログ出力
		if ( $oldlogfiledir ) {

			if ( !$oldlogfmt ) {
				$oldlogext = 'html';
			} else {
				$oldlogext = 'dat';
			}

			if ( !$oldlogsavesw ) {
				$oldlogfilename = sprintf ( "%s/%d%02d%02d.$oldlogext",
				  $oldlogfiledir, $year, $mon, $mday );
			} else {
				$oldlogfilename = sprintf ( "%s%d%02d.$oldlogext",
				  $oldlogfiledir, $year, $mon );
			}

			open ( CLOG, ">>$oldlogfilename" ) || &prterror ( '過去ログ出力に失敗しました' );
			eval 'flock ( CLOG, 2 )';
			chmod(0600, $oldlogfilename); #9/17 ログファイル見れないように

			$oldstream = select ( CLOG );
			$| = 1;

			if ( !$oldlogfmt ) {
				if ( -z CLOG ) {
					print CLOG <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>$bbstitle</title>
</head>
<body bgcolor="#$bgc" text="#$textc" link="#$linkc" vlink="#$vlinkc" alink="#$alinkc">
<hr>
EOF
				}

				&getmessage ( $msgdata );

				print CLOG &prtmessage ( 1, '' );

			} else {
				print CLOG $msgdata;
			}

			eval 'flock ( CLOG, 8 )';
			close ( CLOG );

			select ( $oldstream );

			chmod 0400, $logfilename if ( ( -s $oldlogfilename ) > $maxoldlogsize );

			&getnowdate ( time - $difftime - $oldlogsaveday * 60 * 60 * 24 );
			$oldlogfilename = sprintf (  "%s/%d%02d%02d.$oldlogext",
			  $oldlogfiledir, $year, $mon, $mday );
			unlink $oldlogfilename;

#なんだこれ たまにクッキーリセットされる
#			&putcookie ( 0 ) if ( $cookie );
		}



	} else {
		eval 'flock ( FLOG, 8 )';
		close ( FLOG );

		if ( $posterr == 2 ) { # 2だったらもう一度投稿を促す 1だったら無かったことにする
			&chkerror ( '', $posterr );
			if ( $FORM{'f'} ) {
				&prtfollow ( 1 );
			} else {
				&prtmain ( $FORM{'t'}, $FORM{'v'}, $FORM{'l'} );
			}
			exit;
		}
	}
}


###############################################################################
#  Cookie取得
###############################################################################

sub getcookie {
	if ( $ENV{'HTTP_COOKIE'} && $ENV{'HTTP_COOKIE'} =~ /$cookiename=/) {
		$ENV{'HTTP_COOKIE'} =~ s/$cookiename=(.*?);.*/$1/;
		@cookie = split(/&/, $ENV{'HTTP_COOKIE'});
		foreach (@cookie) {
			($key, $val) = split(/=/);

			if ($key eq 'm') {next;} #古いcookie対応 あとで消す

			if (!($key eq 'u' && !($val && !$FORM{'u'} && $FORM{'m'} ne 'p'))  &&
			   !($key eq 'ng' && $FORM{'m'} eq 'c') &&
			   !($key eq 'customlink' && $FORM{'m'} eq 'c')
			) {
				$FORM{$key} = $val;
			}
		}
		$FORM{'u'} = url_decode($FORM{'u'});
		$FORM{'ng'} = url_decode($FORM{'ng'});
		$FORM{'customlink'} = url_decode($FORM{'customlink'});
	}
}


###############################################################################
#  Cookie送信
###############################################################################

sub putcookie {

	my ( $cuser, $cng, @ctime, $cmday, $cmon, $cdate, $clink );
	my $cexpdif = $_[0];

	$cuser = &url_encode ( $FORM{'u'} );
	$cng = &url_encode ( $FORM{'ng'} );
	$clink = &url_encode ( $FORM{'customlink'} );

	( @ctime ) = gmtime ( time + $S_cexp - $cexpdif );
	$cmday = ( 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' )[$ctime[6]];
	$cmon = ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' )[$ctime[4]];
	$cdate = sprintf ( "%s, %02d\-%s\-%04d %02d:%02d:%02d GMT",
	  $cmday, $ctime[3], $cmon, $ctime[5] + 1900, $ctime[2], $ctime[1], $ctime[0] );

	print "Set-Cookie: $cookiename=u=$cuser&c=$FORM{'c'}&ng=$cng&customlink=$clink; expires=$cdate; path=/\n";

	print "Set-Cookie: c=; expires=Thu, 01-Jan-1970 00:00:00 GMT; path=/\n"; #古いcookieを削除
	print "Set-Cookie: custom=; expires=Thu, 01-Jan-1970 00:00:00 GMT; path=/\n"; #古いcookieを削除

}


###############################################################################
#  プロテクトコード生成
###############################################################################

sub pcode {

	my ( @hostbin, @pkey, @pkeystr, @apkey );
	srand ( time | $$ );

	#$nowtime = time - $difftime * 60 * 60;
	@hostbin = split ( /\./, $ENV{'REMOTE_ADDR'} );
	for ( $i = 0 ; $i < 4 ; $i++ ) {
		$hostbin[$i] = vec ( pack ( 'C4', $hostbin[$i] ), 0, 8 ); #??
	}
	$protect_c = $hostbin[0] ^ $hostbin[1] ^ $hostbin[2] ^ $hostbin[3];
	$pkey[0] = ( $nowtime + $protect_a ) * $protect_b + $protect_c;
	$pkey[1] = $pkey[0] - int ( rand ( 64 ) );
	$pkey[2] = $pkey[1] + int ( rand ( 128 ) );

	$pkeystr[0] = "\n  <input type=\"hidden\" name=\"pc\" value=\"$pkey[0]\">\n";
	$pkeystr[1] = "  <!--\n  <input type=\"hidden\" name=\"pc\" value=\"$pkey[1]\">\n  -->";
	$pkeystr[2] = "  <!--\n  <input type=\"hidden\" name=\"pc\" value=\"$pkey[2]\">\n  -->";

	#@pkeystrの順番をランダムで入れ替える
	push ( @apkey, splice ( @pkeystr, rand ( @pkeystr ), 1 ) ) while @pkeystr;
	@pkeystr = @apkey;

	return "$pkeystr[0]$pkeystr[1]$pkeystr[2]";
}


###############################################################################
#  フォーム部分表示
###############################################################################

sub prtform {

	my $dtitle = $_[0];
	my $dmsg = $_[1];
	my $dlink = $_[2];
#	my ( $bbslink, $counter, $mbrcount );
	my ( $bbslink, $gzipchk, $counter, $mbrcount );

	# プロテクトコード生成
	my $ptext = &pcode;

	# カウンタ
	$counter = &counter;
	$mbrcount = &mbrcount;

#	my $friends = &twit_friends_count;

#	if ( $gzip ) {
#		$gzipchk = qq#  　<font size="-1">gzip圧縮転送 <input type="checkbox" name="g" value="checked" $checked[$CUST{'gzip'}]></font>#;
#	} else {
#		$gzipchk = '';
#	}

	if ( $FORM{'m'} eq 'o' || $FORM{'m'} eq 'op' || $FORM{'m'} eq 'on') {

		my $windowopen;
		if ($CUST{'followwin'}) {
			$windowopen = qq( target="_blank" onclick="window.open('$cgiurl?newpost=1');return false;");
		}

		# ログ読み専用フォーム
		$bbslink = qq#<a href="$cgiurl">標準画面</a>#;
		print <<EOF;
<form method="$formmethod" action="$cgiurl">
  <font size="-1">
  <input type="hidden" name="m" value="op">
  <input type="hidden" name="k" value="あ">
  <input type="hidden" name="c" value="$FORM{'c'}">
  <input type="hidden" name="d" value="$FORM{'d'}">
  <input type="hidden" name="g" value="$checked[$CUST{'gzip'}]">
  $countdate から $counter$mbrcount$friends
  <hr>
  | $bbslink
  | <a href="$cgiurl?newpost=1"$windowopen>新規投稿</a>
  |
  <hr>
  <input type="submit" name="reload" value="リロード" accesskey="r">
  <input type="submit" name="midokureload" value="未読リロード" accesskey="y">
  <a href="$cgiurl?m=o&d=$msgdisp">最新$msgdisp件</a>
  <a href="$cgiurl?m=o&d=$logsave">全記事</a>
  <a href="#bottom">▼</a>
  </font>
  <input type="hidden" name="p" value="$toppostid">
</form>
EOF

	} else {

		# 標準投稿フォーム
		$bbslink = qq#<a href="$cgiurl?m=o">ログ読み</a>#;
		print <<EOF;
<form method="$formmethod" action="$cgiurl" enctype="multipart/form-data" name="form">
  <font size="-1">
  <input type="hidden" name="m" value="p">
  <input type="submit" name="post" value="　　投　　稿　　" tabindex="4" accesskey="r">
  <input type="reset" value="消す"  tabindex="5" accesskey="k">
  投稿者 <input size="15" type="text" name="u" maxlength="30" value="$FORM{'u'}" tabindex="1" accesskey="1">
  ファイル <input type=file  size="15" name="filedata" tabindex="2"><br>
  <textarea rows="5" cols="70" name="v" tabindex="3" wrap="off" accesskey="4" $wide_msg>$dmsg</textarea><br>
  $ptext
  <input type="hidden" name="k" value="あ">
  <input type="hidden" name="c" value="$FORM{'c'}">
EOF

		if ( $FORM{'m'} ne 'f' && !$FORM{'f'} && !($FORM{'newpost'} && !$FORM{'v'}) ) {
			print <<EOF;
  <input type="hidden" name="g" value="$checked[$CUST{'gzip'}]">
  <p>$countdate から ${counter}$mbrcount$friends</p>
  <hr>
  | <a href="$infopage">広報室</a>
  | <a href="$cgiurl?m=setup">環境設定</a>
  | <a href="$cgiurl?m=g">過去ログ</a>
  | $bbslink
  | <a href="$cgiurl?mode=i">携帯用</a>
  | <a href="./up/" target="_blank">あぷろだ</a>
  | <a href="REDACTED?newpost=1" target="_blank">リプライ投稿</a>$newcaption
  |
  $link_sw
  $link_comu
  $link_news
  $link_shop
  $link_twit
  $link_ust
  $link_cust
  $link_search
  <hr>
  <input type="submit" name="post" value="投稿／リロード">
  <input type="submit" name="midokureload" value="未読リロード" accesskey="y">
  <input type="hidden" name="d" value="$FORM{'d'}">

  <a href="$cgiurl?d=$msgdisp">最新$msgdisp件</a>
  <a href="$cgiurl?d=$logsave">全記事</a>
  <a href="#bottom">▼</a>
  <input type="hidden" name="p" value="$toppostid">
  </font>
</form>
EOF
		}
	}
}


###############################################################################
#  画面表示
###############################################################################

sub prtmain {

	my ( $prtmessage, $dispcount, @pkeystr, $msgmore, $msgnext, $cntnext, $msg_diff );
	my $dtitle = $_[0];
	my $dmsg = $_[1];
	my $dlink = $_[2];

	&loadmessage;

	$prtmessage = '';

	# 最新のPOSTIDを取得（０件リロード用）
	$logdata[0] =~ /^.*,(.*),.*,.*,.*,.*,.*,.*,.*,.*/;
	$toppostid = $1;
	if ($FORM{m} =~ /n/) {		# 次のページが押された
		# 新着投稿があったら開始ポインタをずらす
		# 次のページを表示するまでの間に新規投稿があったらその分ずらす lam
		$bmsg += ($msg_diff = $toppostid - $FORM{p}) if ($toppostid > $FORM{p});
		# 未読ポインタは更新させない
		$toppostid = $FORM{p};
	}

	# メッセージ表示件数設定
	if ( $FORM{'d'} == 0 or $FORM{'midokureload'}) {
		$dispcount = $toppostid - $FORM{'p'};
		$cntnext = $msgdisp;
	} else {
		$dispcount = $FORM{'d'};
		$cntnext = $FORM{'d'};
	}

	# 表示メッセージ作成
	$msgtop = $bmsg + $dispcount;
	$msgtop = @logdata if ( $msgtop > @logdata );
#	$j = 0;

	# 挿入場所はここであってるのか? lam 6/19
	# tree表示
	if ( $CUST{'tree'} ) {
		require "${sub}ks_treeview.pl";
		$prtmessage = output_treeview($bmsg, $msgtop); #新着順$bmsg番目から$msgtop番目までの記事

	} else {
		if ( $FORM{'d'} == 0 && $reltype ) { #$reltype:投稿時刻昇順表示
			for ( $i = $msgtop - 1 ; $i >= $bmsg ; $i-- ) {
				&getmessage ( $logdata[$i] );
				$prtmessage .= &prtmessage ( 0, '' );
				$j++
			}
		} elsif ($FORM{'midokureload'}) {
			if ($msgtop > $FORM{'d'} and $FORM{'d'} != 0) { $msgtop = $FORM{'d'} }
			for ( $i = $bmsg ; $i < $msgtop ; $i++ ) {
				&getmessage ( $logdata[$i] );
				$prtmessage .= &prtmessage ( 0, '' );
				$j++
			}
		} else {
			for ( $i = $bmsg ; $i < $msgtop ; $i++ ) {
				&getmessage ( $logdata[$i] );
				$prtmessage .= &prtmessage ( 0, '' );
				$j++
			}
		}
	}

#	if ( $j > 0 ) {
	if ( $msgtop > 0 ) {
		$msgmore = "以上は、現在登録されている新着順".($bmsg+1)."番目から$msgtop番目までの記事です。";
	} else {
		$msgmore = '未読メッセージはありません。';
		
		#ボーナスポイント
		$bonuspoint = 5 + int(rand(5));
		my $fontsize = 1;
		
		while (rand(20) <= 1) {
			$bonuspoint += 10;
			$fontsize *= 1.33;
		}
		
		$bonuspoint =  <<EOF;
<p><small>　ボーナスポイント：　<b><span style="font-size: ${fontsize}em;">$bonuspoint</span></b></small></p>
EOF

		if ($twitter && $CUST{'midoku_tl'} && !$tl_to_bbs) {
			&twit_init;
			&twit_tl;
			&twit_tl_print(10);
			$timeline = <<EOF;
<hr>
<b>【タイムライン】</b>
<hr>
<small>$timeline</small>

EOF
		}

		#未読0時 feed表示
		if($CUST{'newsfeed'}){
			$newsfeed = <<EOF;
<!-- REDACTED: RSS news feed -->
EOF
			$newsfeed = '<hr><p><b>【トピック】</b></p>'.$newsfeed.'<hr>';
		}
	}
	if ( $logdata[$msgtop] ) {
		my ($n_mode, $mode);
		if ($FORM{'m'} eq 'o' or $FORM{'m'} eq 'op' or $FORM{'m'} eq 'on') {
			$n_mode = 'on';
			$mode = 'o';
		} else {
			$n_mode = 'n';
			$mode = '';
		}
		$msgtop -= $msg_diff if ($msg_diff);

		$msgnext = <<EOF;
<table>
  <tr>
    <td>
      <form method="$formmethod" action="$cgiurl">
        <input type="hidden" name="m" value="$n_mode">
        <input type="hidden" name="b" value="$msgtop">
        <input type="hidden" name="u" value="$FORM{'u'}">
        <input type="hidden" name="p" value="$toppostid">
        <input type="hidden" name="d" value="$cntnext">
        <input type="hidden" name="c" value="$FORM{'c'}">
        <font size="-1"><input type="submit" name="pnext" value="次のページ" accesskey="n"></font>
      </form>
    </td>
    <td>
      <form method="$formmethod" action="$cgiurl">
        <input type="hidden" name="u" value="$FORM{'u'}">
        <input type="hidden" name="p" value="$toppostid">
        <input type="hidden" name="d" value="$FORM{'d'}">
        <input type="hidden" name="c" value="$FORM{'c'}">
        <input type="hidden" name="m" value="$mode">
        <font size="-1"><input type="submit" name="reload" value="リロード"></font>
      </form>
    </td>
    <td>
      <form method="$formmethod" action="$cgiurl">
        <input type="hidden" name="u" value="$FORM{'u'}">
        <input type="hidden" name="p" value="$toppostid">
        <input type="hidden" name="d" value="$FORM{'d'}">
        <input type="hidden" name="c" value="$FORM{'c'}">
        <input type="hidden" name="m" value="$mode">
        <font size="-1"><input type="submit" name="midokureload" value="未読リロード">
        <a href="#top">▲</a></font>
      </form>
    </td>
  </tr>
</table>
EOF
	} else {
		$msgmore .= 'これ以下の記事はありません。';
		$msgnext = <<EOF;
<table>
  <tr>
    <td>
      <form method="$formmethod" action="$cgiurl">
        <input type="hidden" name="u" value="$FORM{'u'}">
        <input type="hidden" name="p" value="$toppostid">
        <input type="hidden" name="d" value="$FORM{'d'}">
        <input type="hidden" name="c" value="$FORM{'c'}">
        <input type="hidden" name="m" value="$mode">
        <font size="-1"><input type="submit" name="reload" value="リロード"></font>
      </form>
    </td>
    <td>
      <form method="$formmethod" action="$cgiurl">
        <input type="hidden" name="u" value="$FORM{'u'}">
        <input type="hidden" name="p" value="$toppostid">
        <input type="hidden" name="d" value="$FORM{'d'}">
        <input type="hidden" name="c" value="$FORM{'c'}">
        <input type="hidden" name="m" value="$mode">
        <font size="-1"><input type="submit" name="midokureload" value="未読リロード">
        <a href="#top">▲</a></font>
      </form>
    </td>
  </tr>
</table>
EOF
	}

	# メイン出力
	&prthtmlhead ( "$bbstitle" );

	print <<EOF;
<h3>
<a name="top" href="REDACTED" style="color: \#$textc; text-decoration: none;">$bbstitle</a>
$twitbtn
</h3>


EOF

	&prtform ( $dtitle, $dmsg, $dlink );

#処理時間測定 lam 7/11
my $time = sprintf "%dms", ((times)[0] - $time_start )*1000;

	print <<EOF;
<hr>

$prtmessage

<p><i><font size="-1">$msgmore</font></i></p>

$bonuspoint

$timeline

$msgnext
<hr>

<a name="bottom"></a>

<p align="right">
<font size="-1"><a href="./info.htm#copyright">$bbstitle_at</font></a><br>
<font size="-2">処理時間: $time</font><br>
</p>

</body>
</html>
EOF
}


###############################################################################
#  個人用設定反映
###############################################################################

sub refcustom { #reflection=反映

	my $c;

	if ( $FORM{'c'} ) {
		if ( length ( $FORM{'c'} ) > 30  ) {
			$FORM{'c'} =~ /^(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w\w\w\w\w\w)([0-9a-f]*)$/;
			$CC{'text'} = $1;
			$CC{'bg'} = $2;
			$CC{'link'} = $3;
			$CC{'vlink'} = $4;
			$CC{'qmsgc'} = $5;
			$CC{'subj'} = $CC{'text'};
			$c = hex ( $6 );
		} else {
			$FORM{'c'} =~ /^([0-9a-f]*)$/;
			$CC{'text'} = $textc;
			$CC{'bg'} = $bgc;
			$CC{'link'} = $linkc;
			$CC{'vlink'} = $vlinkc;
			$CC{'qmsgc'} = $qmsgc;
			$CC{'subj'} = $subjc;
			$c = hex ( $1 );
		}
		#$cをデコードして%CUSTに反映
		for ($i = 0; $i < $#custom+1; $i++) {
			$CUST{$custom[$i]} = ($c / 2**$i) % 2;
		}

	} else {
		$CC{'text'} = $textc;
		$CC{'bg'} = $bgc;
		$CC{'link'} = $linkc;
		$CC{'vlink'} = $vlinkc;
		$CC{'qmsgc'} = $qmsgc;
		$CC{'subj'} = $subjc;
#		$gzipu = $FORM{'g'} if ( $FORM{'m'} eq 'g' );
	}

	#9/16 ?g=no だったら強制的にgzipオフ
	if ( $FORM{'g'} eq 'no' ) {
		$CUST{'gzip'} = 0;
	}

	#%CUSTをエンコードして$cに
	$c = 0;
	for ($i = 0; $i < $#custom+1; $i++) {
		$c += $CUST{$custom[$i]} * 2**$i;
	}
	$c = sprintf("%x", $c);

	if (
	  ( $CC{'text'} eq $textc ) &&
	  ( $CC{'bg'} eq $bgc ) &&
	  ( $CC{'link'} eq $linkc ) &&
	  ( $CC{'vlink'} eq $vlinkc ) &&
	  ( $CC{'qmsgc'} eq $qmsgc ) &&
	  ( $CC{'subj'} eq $subjc ) ) {
		$FORM{'c'} = "$c";
	} else {
		$FORM{'c'} = "$CC{'text'}$CC{'bg'}$CC{'link'}$CC{'vlink'}$CC{'qmsgc'}$c";
	}

	#リンク行設定反映
	if($CUST{'link_sw'}) {
		$link_sw = <<EOF;
<!-- links to other BBS -->

EOF
	}
	if($CUST{'link_comu'}) {
		$link_comu = <<EOF;
<!-- community links -->

EOF
	}
	if($CUST{'link_news'}) {
		$link_news = <<EOF;
<!-- news/weather links -->

EOF
	}
	if($CUST{'link_shop'}) {
		$link_shop = <<EOF;
<!-- shopping links -->

EOF
	}
	if($CUST{'link_twit'}) {
		$link_twit = <<EOF;
<!-- twitter links -->

EOF
	}
	if($CUST{'link_ust'}) {
		require "${sub}ust.pl";
		$ust_cache = './ust/channel.cache';
		$ust_cachetime = 10*60;
		$link_ust = "<small><b>UST:</b></small> | <a href=\"./ust/\">\@UST</a> |" . &ust_makeline;
	}
	if($CUST{'link_cust'}) {
		my $link;
		$_ = $FORM{'customlink'}."\r";
		while ( /(.+?)\r(.+?)\r/g ) {
			$link .= qq( <a href="$2" target="_blank">$1</a> |);
		}
		$link_cust = "<small><b>ｶｽﾀﾑ:</b></small> | " . $link;
	}
	#formがネストして使えない
	if($CUST{'link_search'}) {
		$link_search = <<EOF;
<span id="search" style="white-space:nowrap;"></span>
<script language="JavaScript">
<!--
function search() {
  var engine = document.form.select1.value;
  var key = encodeURI(document.form.key.value);
  if (engine == "google")     url = "http://www.google.com/search?lr=lang_ja&q=" + key;
  else if(engine == "amazon") url = "http://www.amazon.co.jp/s/?field-keywords=" + key + "&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&id=$amazontag";
  else if(engine == "rakuten") url = "http://search.rakuten.co.jp/search/mall/" + key + "/";
  else if(engine == "youtube") url = "http://www.youtube.com/results?search_query=" + key;
  else if(engine == "goodict") url = "http://dictionary.goo.ne.jp/srch/all/" + key + "/m0u/";
  window.open(url, "_blank");
}
document.getElementById("search").innerHTML = '\\
<select name="select1">\\
  <option value="google">Google</option>\\
  <option value="amazon">Amazon</option>\\
  <option value="rakuten">楽天市場</option>\\
  <option value="youtube">YouTube</option>\\
  <option value="goodict">goo辞書</option>\\
</select> \\
<input type="text" name="key" size="16" value="" onKeyPress="if(event.keyCode==13){search();return false;}"> \\
<input type="button" name="searchbutton" value="検索" onClick="search();">\\
';
// -->
</script>
EOF
	}
	if($CUST{'link_topic'}) {
		;
	}

	if($CUST{'wide_msg'}) {
		$wide_msg = 'style="width:100%"';
	}

}

###############################################################################
#  Twitterリプライから投稿
###############################################################################

sub twit_rep{

	# 参考
	# a pot of tea, twitter botをつくってみる。(6) - リズムシさんのbotをつくったよ！
	# http://cuddlecore.blog.shinobi.jp/Entry/21/
	&twit_init;


#↓複数行コメントアウト
=pot
	# 自分へのリプライを取得
	my $rapParam;
	eval { $rapParam = $twit->mentions(); };
	
	
#	if ($@) { err ( $@ ); }
	if ($@) { return; }
=cut


	$twitreppost = 1;

	#TLから投稿(取って付け)
	if ($tl_to_bbs) {

		# ログファイルを共用読み取りでオープン
		open (my $fh, '+<', $rapFile)
		or die "Can't open file : $!";

		my @line = <$fh>;

		&twit_tl;
		for (my $i = $#tl; $i >= 0; $i--) {
			my $id = $tl[$i][0];
			my $name = $tl[$i][1];
			my $replay_id = $tl[$i][2];
			my $text = $tl[$i][3];


			if($name ne $my_twit_id){
				my $flag = 1;
				for ( @line ){
					# ファイルの中にidがあるかチェック
					if( /$id/ ){
						$flag = 0;
						last;
					}
				}
				if( $flag ){
					$name = "\@$name";
					my $msg = $text;
					&Jcode::convert( \$msg, "sjis", "utf8" );

					#先頭@...除去
					$msg =~ s|^(\@[a-zA-Z0-9_]+[ \r]+)+||;
					$msg =~ s|^\@[a-zA-Z0-9_]+([^a-zA-Z0-9_])|$1|;

					$msg =~ s/~!/ ~!/g;
					if($name ne 'ng' && $name ne 'customlink') {
						$msg =~ s/&/&amp;/g;
						$msg =~ s/"/&quot;/g;
						$msg =~ s/'/&#39;/g;
						$msg =~ s/</&lt;/g;
						$msg =~ s/>/&gt;/g;
					}
					$msg =~ s/\015\012/\015/g;
					$msg =~ s/\012/\015/g;
					$msg =~ s/\015$//g;
					$msg =~ s/\,/\0/g;

					$FORM{'pc'} = '';
					$FORM{'h'} = '';
					$host = 'TL';
					$agent = 'TL';
					$postname = $name;
					$twitid = $id;
					$FORM{'t'} = '';
					$FORM{'v'} = $msg;

					$FORM{'ftwitid'} = $replay_id;
					&putmessage;

					print $fh $id;
					print $fh "\n";
				}
			}
		}

		# ファイルクローズ
		close $fh;
	}

=pot

	# ログファイルを共用読み取りでオープン
	open (my $fh, '+<', $rapFile)
	or die "Can't open file : $!";

	my @line = <$fh>;

	foreach my $str (reverse(@$rapParam)){

		use Jcode;
		my $name = $str->{'user'}{'screen_name'};
		&Jcode::convert( \$name, "sjis", "utf8" );

		if($name ne $my_twit_id){
			my $flag = 1;
			for ( @line ){
				# ファイルの中にidがあるかチェック
				if( /$str->{'id'}/ ){
					$flag = 0;
					last;
				}
			}
			if( $flag ){
				$name = "\@$name";
				my $msg = $str->{'text'};
				&Jcode::convert( \$msg, "sjis", "utf8" );

				#先頭@...除去
				$msg =~ s|^(\@[a-zA-Z0-9_]+[ \r]+)+||;
				$msg =~ s|^\@[a-zA-Z0-9_]+([^a-zA-Z0-9_])|$1|;

				$msg =~ s/~!/ ~!/g;
				if($name ne 'ng' && $name ne 'customlink') {
					$msg =~ s/&/&amp;/g;
					$msg =~ s/"/&quot;/g;
					$msg =~ s/'/&#39;/g;
					$msg =~ s/</&lt;/g;
					$msg =~ s/>/&gt;/g;
				}
				$msg =~ s/\015\012/\015/g;
				$msg =~ s/\012/\015/g;
				$msg =~ s/\015$//g;
				$msg =~ s/\,/\0/g;

				$FORM{'pc'} = '';
				$FORM{'h'} = '';
				$host = '@';
				$agent = '@';
				$postname = $name;
				$twitid = $str->{'id'};
				$FORM{'t'} = '';
				$FORM{'v'} = $msg;

				$FORM{'ftwitid'} = $str->{'in_reply_to_status_id'};
				&putmessage;

				print $fh $str->{'id'};
				print $fh "\n";
			}
		}

	}


	# ファイルクローズ
	close $fh;

=cut

	$twitreppost = 0;

}


###############################################################################
#  全角文字対応substr(S-JIS専用) http://akebi.jp/support/cyclamen.cgi?log=perl&tree=r20
###############################################################################
sub z_substr {
	local($s,$p,$l,$o) = @_;
	$s =~ s/(.)/$1\0/g;
	$s =~ s/([\x81-\x9f\xe0-\xfc])\0(.)\0/$o==2?"$1$2":"$1$2\0\0"/eg;
	$s = $l eq '' ? substr($s,$p*2):substr($s,$p*2,$l*2);
	if ($o==1) { $s =~ s/^\0\0/ /; $s =~ s/.[^\0]$/ /;}
	$s =~ tr/\0//d;
	$s;
}

###############################################################################
#  全角文字を含んだ文字列を数える http://snyc.s28.xrea.com/contents/001.htm
###############################################################################
sub zlength {
	$_ = $_[0];

	# 全角文字数を数え、全角文字を消去する
	$lz = s/[\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc]//g;

	# 半角文字数を数える
	$lh = length($_);

	# 全角・半角の文字数を足して返す
	return $lz + $lh;
}

###############################################################################
#  デバッグ用
###############################################################################
sub err{
	if( !$_[0] ) { $_[0] = "error"; };
	prterror( $_[0] );
}


###############################################################################
#  ツイッター連携ページ
###############################################################################
sub twit_mode{

	use Jcode;

	my $name;

	&twit_init;


	#フォロー／リムーブする
	if( ($FORM{'follow'} || $FORM{'remove'}) && $FORM{'name'} ){
		$name = $FORM{'name'};
		my $flg = 0;
		my $friends;
		eval { $friends = $twit->friends() };
		if ($@) { err ( $@ ); }
		foreach my $desc ( @$friends ){
			if( $name eq $desc->{'screen_name'} ) {

				if ($FORM{'remove'} && $name ne "REDACTED") {
					eval { $twit->destroy_friend( $name ); };
					if ($@) { err ( $@ ); }
					$msg = qq(<a href="https://twitter.com/#!/$name">\@$name</a>さんをリムーブしました);
					$name = "";
				} else {
					$msg = qq(<a href="https://twitter.com/#!/$name">\@$name</a>さんは既にフォローしています);
				}
				$flg = 1;
				last;

			}
		}
		if ( !$flg ) {
			if ($FORM{'follow'}) {
				eval { $twit->create_friend( $name ); };
				if ($@) { err ( $@ ); }
				$msg = qq(<a href="https://twitter.com/#!/$name">\@$name</a>さんをフォローしました);
				$name = "";
			} else {
				$msg = qq(<a href="https://twitter.com/#!/$name">\@$name</a>さんはフォローしていません);
			}
		}
	}

	#フレンドリスト取得
	my $friends;
	eval { $friends = $twit->friends(); };
	if ( $@ ) { err("$@\n"); }
	my $f_n = $#$friends + 1;
	$friendlist = "フォロー中($f_n)：";
	for (@$friends){
		my $name = $_->{'screen_name'};
		$friendlist .= qq(<a href="https://twitter.com/#!/$name">\@$name</a> );
	}

	if (!$tl_to_bbs) {
		&twit_tl;
		&twit_tl_print(30);
		$timeline = <<EOF;
<small>
<input type="button" value="リロード" onclick="document.location='$cgiurl?m=twitter'">
| <a href="$cgiurl?newpost=1" target="_blank" onclick="window.open('$cgiurl?newpost=1');return false;">ツイートする</a>
| <a href="./">戻る</a>
|
</small>

<hr>

<small>$timeline</small>

<input type="button" value="リロード" onclick="document.location='$cgiurl?m=twitter'">
EOF
	}
	if ( $msg ) {
		$msg = "<h4>$msg</h4>";
	}

	&prthtmlhead ( "$bbstitle" );
	print <<EOF;
<h3><a href="REDACTED" style="color: \#$textc; text-decoration: none;">$bbstitle</a> タイムライン</h3>

$msg

<form method="$formmethod" action="$cgiurl">
<input type="hidden" name="m" value="twitter">

<small>
\@<input size="25" type="text" name="name" value="$name">を<input type="submit" name="follow" value="フォロー">／<input type="submit" name="remove" value="リムーブ"><br>
</small>

</form>

<p><font size="-2">$friendlist</font></p>

<hr>


</body>
</html>
EOF

}

###############################################################################
#  ツイッター前処理
###############################################################################

sub twit_init {

	$twit = Net::Twitter::Lite->new(%CONSUMER_TOKENS);
#	$twit->access_token($ACCESS_TOKEN);
#	$twit->access_token_secret($ACCESS_TOKEN_SECRET);

}

###############################################################################
#  TLとフレンドリストを取得
###############################################################################

sub twit_tl {

	my $cache = './tl.cache';
	my $cachetime = 90;
	my $i = 0;

	#タイムライン取得
	my @cache = stat($cache);
	my $now = time();
	$cachetime = $cache[9] + $cachetime;

	if($cachetime < $now){

		my $stats;
		eval { $stats = $twit->home_timeline({ count => 50 }); };
#		if ( $@ ) { err("$@\n"); }
		if ( $@ ) {
			$timeline = qq(<div style="margin:0 0 1em 1em;">$@</div>);
			return;
		}

		flock(FH, LOCK_EX);
		open(FH,">$cache");

		$i = 0;
		for my $s (@$stats) {
			if ( $s->{user}{protected} eq "false" ) {
			    $tl[$i][0] = $s->{id};
			    $tl[$i][1] = $s->{user}->{screen_name};
			    $tl[$i][2] = $s->{'in_reply_to_status_id'};
			    $tl[$i][3] = $s->{text};
			    $tl[$i][3] =~ s/[\n\r]/\r/g;
			    print FH "$tl[$i][0]\t$tl[$i][1]\t$tl[$i][2]\t$tl[$i][3]\n";
				$i++;
			}
		}

		close(FH);
		flock(FH, LOCK_NB);

	} else {
		open(FH, "$cache");
		$i = 0;
		while (<FH>) {
			while ($_ =~ /^(.*?)\t(.*?)\t(.*?)\t(.*)$/g) {
				for($j = 0; $j < 4; $j++) {
					$tl[$i][$j] = ${$j+1};
				}
			}
			$i++;
		}
		close(FH);
	}

}

sub twit_tl_print {

	#NG前処理
	use Encode;
	if ($CUST{'nguse'} && $FORM{'ng'}) {
		$FORM{'ng'} =~ s/\r/|/g;
		$ngword_dec = decode( 'shift-jis', $FORM{'ng'} );
	}
	if ($CUST{'autong'}) {
		$autongword =~ s/\n/|/g;
		$autongword_dec = decode( 'shift-jis', $autongword );
	}

	#表示
	$n = 0;
	for (my $i = 0; $i < $#tl+1; $i++) {
		my $tl_id = $tl[$i][0];
		my $tl_name = $tl[$i][1];
		my $tl_text = $tl[$i][3];

		my $flg = 1;
		#NG
		if ($CUST{'nguse'} && $FORM{'ng'}) {
			if ( $tl_text =~ /$ngword_dec/ || "\@$tl_name" =~ /$ngword_dec/ ) {
				$flg = 0;
			}
		}
		#自動NG
		if ($CUST{'autong'}) {
			if ( $tl_text =~ /$autongword_dec/ || "\@$tl_name" =~ /$autongword_dec/ ) {
				$flg = 0;
			}
		}
		#表示
		if ( $flg ) {
			$n++;
			&Jcode::convert( \$tl_name, "sjis", "utf8" );
			&Jcode::convert( \$tl_text, "sjis", "utf8" );
			&Jcode::convert( \$tl_id, "sjis", "utf8" );
			$res_url = qq($cgiurl?newpost=1&f=1&fuser=\@$tl_name&ftwitid=$tl_id);
		    $tl_name = qq(<a href="https://twitter.com/#!/$tl_name" style="text-decoration: none;">\@$tl_name</a>);
			$tl_text =~ s#((https?|ftp|gopher|telnet|whois|news)://$urlchar+)#<a href="$1" target="_blank">$1</a>#ig;
			$tl_text =~ s|\@([a-zA-Z0-9_]+)|<a href="https://twitter.com/#!/$1" target="_blank">\@$1</a>|g;
			$tl_text =~ s|\r|<br>|g;
		    $timeline .= <<EOF;
<div style="margin:0 0 1em 1em;">
<a href="$res_url" target="_blank" style="text-decoration: none;" onclick="window.open('$res_url');return false;">$txtfollow</a>
<b>$tl_name</b>
<div style="margin:0.2em 0 0 1.5em;">$tl_text</div>
</div>
<hr>
EOF
		}
		if ( $n >= $_[0] ) { last; }
	}


}


sub twit_friends_count {

&twit_init;

my $totals;
eval { $totals = $twit->account_totals(); };
if ( $@ ) { err("$@\n"); }

return "　フォロー数 : <a href=\"./?m=twitter\">".$totals->{friends}."名</a>　フォロワー数 : ".$totals->{followers}."名";

}

###############################################################################
#  メイン
###############################################################################

#処理時間測定 lam 7/11
$time_start = (times)[0];
$nowtime = time - $difftime * 60 * 60;

&getformdata;
&jconv;
&getenv;
&getcookie if ( $cookie );

#new!
use Time::Local;
#if (!($referer =~ /$cgiurl/i) && !($agent =~ /^DoCoMo|^J-PHONE|^Vodafone|^SoftBank|^UP.Browser|^KDDI/)) {
#if (!($referer =~ /$cgiurl/i) && timelocal(0,0,0,4,3-1,2012) + 7*24*60*60 > $nowtime ) {
if ( !($referer =~ /$cgiurl/i) ) {
	if ( $FORM{'m'} eq 'setup' || timelocal(0,0,0,16,1-1,2014) + 7*24*60*60 > $nowtime ) {
		$newcaption = ' <font color="#90d0ff">←new!</font>';
	}
	$twitbtn = <<EOF;
<a href="https://twitter.com/REDACTED" class="twitter-follow-button" data-show-count="false" data-lang="ja">\@REDACTEDをフォロー</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
EOF
}

# imode表示
if ($FORM{'mode'} eq 'i') {
	require "${sub}ks_imode.pl";
	imode_exec();
	exit;
}

if ( $FORM{'m'} eq 'c' ) {
	require "${sub}bbscust.pl";
	&setcustom;
	exit;
}

# 個人用設定反映
&refcustom;
$body = qq(<body bgcolor="#$CC{'bg'}" text="#$CC{'text'}" link="#$CC{'link'}" vlink="#$CC{'vlink'}" alink="#$alinkc" onload="dofocus();">);

# Getlog
if ( $FORM{'m'} eq 'g' ) {
	require "${sub}bbslog.pl";
	&getlog;
	exit;
}

# トピック一覧
if ( $FORM{'m'} eq 'l' ) {
	require "${sub}bbstopic.pl";
	&lsttopic;
	exit;
}

# 管理モード lam 6/30
if ( $FORM{$adminkey} ) {
	require "${sub}bbsadmin.pl";
	&adminmain;
	exit;
}
if ( !$adminpost ) {
	require "${sub}bbsadmin.pl";
	&setpass;
	exit;
}

# 個人用設定
if ( $FORM{'m'} eq 'setup' ) {
	require "./sub/bbscust.pl";
	&prtcustom;
	exit;
}

# 表示件数設定
if ( $FORM{'d'} ne '' ) {
	if ( $FORM{'d'} > $logsave ) {
		$FORM{'d'} = $logsave;
	}
} else {
	$FORM{'d'} = $msgdisp;
}

# imode表示
#if ($FORM{'mode'} eq 'i') {
#	require './sub/ks_imode.pl';
#	imode_exec();
#	exit;
#}
#
#if ( $FORM{'m'} eq 'c' ) {
#	require './sub/bbscust.pl';
#	&setcustom;
#	exit;
#}

if ( $FORM{'m'} eq 'p' && $FORM{'v'} && !$FORM{'reload'} ) {
	$postid = 0;
	$posterr = 0;
#	if ( $ENV{'CONTENT_TYPE'} eq 'application/x-www-form-urlencoded' ) {
	if ( 1 ) {
		&chkmessage;
		&putmessage;
	} else {
		$posterr = 255;
	}
	if ( $FORM{'ac'} || $CUST{'followwin'} && ( $FORM{'f'} || $FORM{'newpost'} ) ) {
		if($CUST{'autoclose'}){
			$body = qq(<body bgcolor="#$CC{'bg'}" text="#$CC{'text'}" link="#$CC{'link'}" vlink="#$CC{'vlink'}" alink="#$alinkc" onload='window.close();'>);
		}
		&prthtmlhead ( "$bbstitle 書き込み完了" );
		print <<EOF;
<h2>書き込み完了</h2>
</body>
</html>
EOF
		exit;
	}
	undef $FORM{'f'};
} elsif ( $FORM{'m'} eq 'f' ) {
	&prtfollow ( 0 );
} elsif ( $FORM{'m'} eq 's' || $FORM{'m'} eq 't' ) { #投稿者検索、スレッド表示
	require "${sub}bbssrc.pl";
	&srcmessage;
} elsif ( $FORM{'newpost'} ) {
	&prthtmlhead ( "$bbstitle 新規投稿" );
		print <<EOF;
<h3><a name="top" href="REDACTED" style="color: \#$textc; text-decoration: none;">$bbstitle</a></h3>
<hr>
新規投稿<br>
EOF
	&prtform ( '', '', '' );
	print <<EOF;
  リプライ先ツイートID<input size="15" type="text" name="ftwitid" value="$FORM{'ftwitid'}">
  <label><input type="checkbox" name="retweet" value="1">リツイートする</label>
  <input type="hidden" name="newpost" value="1">
  <input type="hidden" name="f" value="$FORM{'f'}">
  <input type="hidden" name="fuser" value="$FORM{'fuser'}">
  <hr>
  <p align="right"><font size="-1"><a href="./info.htm#copyright">$bbstitle_at</font></a></p>
</form>
</body>
</html>
EOF

exit;

} elsif ( $FORM{'m'} eq 'n' or $FORM{'m'} eq 'on' ) {
	$bmsg = $FORM{'b'};
} elsif ( $FORM{'m'} eq 'twitter' ){
	&twit_mode;
	exit;
} else {
	$bmsg = 0;
}



#デバッグ用 ログの指定行を削除
if ( 0 ) {
	open ( FLOG, "+<$logfilename" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( FLOG, 2 )';
	seek ( FLOG, 0, 0 );
	@logdata = <FLOG>;


	splice @logdata, 0, 1; #開始要素インデックス、削除要素数

	seek ( FLOG, 0, 0 );
	truncate ( FLOG, 0 );
	print FLOG @logdata;
	eval 'flock ( FLOG, 8 )';
	close ( FLOG );

	err("done");
}

&prtmain ( '', '', '' );


#if($twitter){
if(0){
	my $cachetime = 300;
	@rapFile = stat($rapFile);
	if(($rapFile[9] + $cachetime) < time()){
		&twit_rep;
	}
}

exit;


__END__