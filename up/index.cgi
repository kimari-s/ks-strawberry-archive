#!/usr/bin/perl
#
# 1997.9.14製作
# すくりぷと　ばい　ゆいちゃっと　
# 　　　　　　　　　Since  1996

# ■改造版■
$copyright = 'ずるぼん+擬古描+しばカウンタ 2001年10月27日版';
# 連絡先：zurubon@lycos.ne.jp

# さらに改造したらここに"+ hogehoge"等と書くと良いかもしれない
$modified = '<a href="REDACTED">REDACTED</a>';

# 2001年10月27日版変更点
# ・記事の開始番号を必ず001からではなく、任意の数字から開始できるようにした
# ・記事の連番を3桁表示から4桁表示に変更(ex. 001.jpg -> 0001.jpg)
# ・画像閲覧モードの外観を変更
# ・サーバディスク使用量の概算を表示(FTPモードには非対応)
# ・アクセス集中によるアップロードミス防止処理を若干改良
# ・その他細かいところ・ソースコードのダイエット等

# ずるぼんあぷろだサポートページ
# 過去の改造版ソース等もここに置いておきます。
# http://zurubon.strange-x.com/uploader/


# ＊無保証
# 　このスクリプトを使用することによって生じたいかなる
# 　損害・事件について、私ずるぼんは引責・補償できません。

# ＊2次配布条件
# 　ゆいちゃっとさんの配布条件に準ずるものとします。

# ＊「FTPモード」使用に関する注意事項
# 　2000年3月17日改修版から保存先にFTPホストを指定できるようになっています。
# 　このFTPモードは十分にテストされているわけではありません。
# 　したがって安定・高速な動作を希望される場合には使用しないようにしてください。
# 　また、セキュリティーの面でも問題がありますので保存先のFTPホストに
# 　クラックされて困るようなサーバーを指定しないでください。

# ＊バグレポートは歓迎します
# 　ロクにテストもせずに公開していますのでおそらくバグがあると思います。
# 　もしお気づきの点がありましたら、私に直接メールを送るか、
# 　＠プログラマのアンチダウソコーダー掲示板にでも書き込んでください。
# 　ただし、私のスキル、余暇にも限界がありますので必ず対処できるとは限らないことをご承知置き下さい。

# ＊注意
# 　＠プログラマ、及びアンチダウソコーダー掲示板はあやしいわーるどの一部です。
# 　書き込みの際は、あやしいわーるどに相応しい書き込みをお願いします。
# 　※特に２ちゃんねるネタやそれに類似する書き込みはご遠慮ください。

# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
# ＊＊＊以上のことを了承される方のみご利用ください＊＊＊
# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊

# ＊謝辞
# みらいあぷろだ管理人様 2000/09/07
# HTMLタグの間違い等、鋭い指摘に感謝
#
# 改竄 by 擬古描 - Sat, Apr 15, 2000 - gkJVMgleaMcTQ
#
# 　　　 ∧ ∧
# ～′￣(´ー`)＜コメントにタグが複数入ってると上手く&lt;等に変換されないのを修正
# 　UU￣ U　U　　MIME typeからの拡張子判定の強化
# 　　　　　　　 MIME typeの記録/表示
# 　　　　　　　 アプされたファイルの末尾にゴミがついてウゼェのを解消
#
# 改竄 by 擬古描 - Thu, May 11, 2000 - gkwWZ40tgKf5I
#
# 拡張子の自動判定の強化
# 誤認識の多かったlzh等の対応を強化
#
# 改竄 by 擬古描 - Fri, Jun 30, 2000 - gkHcafwBNEY86
#
# MIME typeが送信されない場合への対応の修正
# MIME typesを少し修正

# ################################
# 初期設定	※必ず設定/変更
# ################################

# このスクリプトのURL(HTTP)
# 解説：このままの設定で動作しない場合は正確なURL(URI)を入力してください。
$url = "http://$ENV{SERVER_NAME}$ENV{SCRIPT_NAME}";
$url =~ s/index.cgi//;

# アップロードデータの格納先ディレクトリ
# 推奨パーミッション：700->777
# 解説：FTPモードの場合も作業用に使うので必ず設定してください。
$storedir = './s/';

# アップロードデータの格納先ディレクトリURL
# 解説：URLリスト作成・画像閲覧モードで使います。
# FTPモード使用の場合は正しく設定しておかないと
# 訪問者がファイルをダウンロードできなくなります。
$storeurl = './s/';

# ログファイル
# 推奨パーミッション：600->666
$log_file = './sourcelog.txt';

# 投稿処理時の排他制御用lockファイル
# 解説：空のファイルを用意してください。
# 推奨パーミッション：600->604  (要するにCGIから読めるだけでOKです。)
$up_lockfile = './upload.lock';

# 表示するタイトル
$title = 'REDACTED';

# タイトルの下に表示するお知らせ
$info = <<EOF;
<pre style="font-size:2.5em;margin:0.5em;">


  無　　三(>
  ﾉ職へ　　|
 　 ￣　  ￣
</pre>
EOF

# ########################################
# もう少し細かい設定
# ########################################

# HTMLのBODY設定
$body = '<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">';

# HTMLのスタイルシート設定
$css = '
A	{text-decoration: none;}
A:link	{text-decoration: none;}
A:hover	{text-decoration: none; background-color: #508080; color: #FFFFFF;}

';

# HTMLの広告バナー設定
# 解説：設置するサーバーに応じて書き換えてください。
$ban = '<!--#echo banner=""-->';

# リンクバー
# 各自の都合・環境に合わせて適宜修正してください。
$links = '
| <a href="REDACTED">掲示板</a> |

';

# タイトルの入るオビの色
$obi = '#007f7f';

# 保存ファイル名の接頭辞
# 解説：'up0001.jpg'のようなファイル名で保存されます。なにも書かなくてもOKです。
$prefix = 'up';

# 記事の開始番号
# 解説：記事の開始番号を任意の数字に変更できます。
$start_num = '0001';

# コメントのオートリンク
# 1:する 0:しない
$autolink = 1;

# コメントの長さ制限
# 解説：単位はバイトです。
$comment_max = 256;

# デフォルトでの1ページにおける表示件数
$lmaxdef = 20;

# ログの最大件数
$max = 20000;

# ファイルサイズ制限(キロバイト単位)
$limitk = 50 * 1024;

# URLリスト出力フォーム
# 1:表示する 0:表示しない
$listform_enable = 0;

# しばカウンター
#
# カウンタプラス値文字列(記述例："+1000")
$shiba::countplus = "";

# カウンタ開始日
$shiba::countdate = 'REDACTED';

# カウンター作業用ディレクトリ・ファイルの指定
# 解説：カウンター機能を使う場合はカウンター作業用ディレクトリを作成してください。
# 以下の設定でのカウンター作業用ディレクトリはcountになります。
# ※./count/以下の"count"ファイルは作成する必要はありません。
# 推奨パーミッション：700->707
$shiba::countfile = './count/count';

# カウンター作業用ファイルの拡張子
# 解説：運用上特に問題無い場合は変更する必要はありません。
$shiba::countfiledat = '.txt';

# カウンタ強度(0より大きい整数値・0のときは使用しない)
# 解説：カウンター機能を使う場合は1以上の整数値を設定してください。
# (頻繁にアクセスがあるようなサイトでも3～4くらいで十分です。)
$shiba::countlevel = 3;

# 過去ログ検索用jcode.pl
# 解説：過去ログ検索にjcode.plを使いたい場合は、jcode.plへのサーバーパスを書いてください。
# 以下はあぷろだ本体と同じディレクトリに置く場合の設定です。
# ※必ず設置する必要はありません。設置しなくてもエラーにはなりません。
$jcode = './jcode.pl';

# ロックファイル
# 1:使用する 0:使用しない
$lock = 0;

# ロックファイルのディレクトリ+ファイル名
# 解説：ロック用ディレクトリ 推奨パーミッション700->777
$lockfile = './lock/lock-file.lock';

# 対応ファイル形式
# 解説：半角カンマで区切って特別に対応させたいファイル形式を入力
$support = '';

# ########################################
# ちょっとむずかしい設定
# ########################################

# 投稿ファイル削除
# 1:使用する 0:使用しない
# 解説：投稿者がパスワードを設定して自分の投稿データを削除できるようになります。
# このオプションを有効にしてもパスワードが何も設定されなかった場合は
# 管理者以外削除できなくなります。
$del_enable = 1;

# 投稿ファイル削除パス生成時の'種'
# 解説：設定文字列を'種'として削除パスワードを生成します。
$del_seed = 'z8';

# 投稿ファイルの管理者削除
# 1:使用する 0:使用しない
# 解説：全ての投稿ファイルを削除できる管理者パスワードを設定します。
# 上記の"投稿ファイル削除"を有効にする必要があります。
$admindel_enable = 1;

# 管理者パスワードの'種'
# 解説：上記の投稿制限用パスワードを生成するときに用いた種です。
$adminseed = 'REDACTED';

# 管理者パスワード
# 解説：平文のパスワードではなく暗号化されたものが必要です。
#
# まずhttp://zurubon.strange-x.com/crypt.txtを自分の利用するサーバーに設置して、
# 平文のパスワードと管理者パスワードの種を入力、生成された暗号化パスワード
# をここに設定してください。
$adminpass = 'REDACTED';

# gzip圧縮転送を許可する
# 解説：HTMLページをgzipで圧縮転送できるようになります。
# サーバーにかかる負担が多少上昇します。
# 1:許可する 0:許可しない
$gzipenc_enable = 0;

# gzip圧縮転送を許可した場合、
# 解説：gzip圧縮転送をデフォルトとするか
# 1:デフォルトとする 0:デフォルトとしない
$gzipenc_def = 0;

# crcチェックサム算出
# 1:使用する 0:使用しない
# 解説：大炸裂氏作のdcrc、またはcrc.plを利用してファイルのチェックサムを記録します。
# dcrcはhttp://daisakuretsu.hypermart.net/dcrc.htmlから入手できます。
# ソースファイルを入手後、telnetクライアントやtelnet.cgiを使ってコンパイルしてください。
# crc.plはhttp://zurubon.strange-x.com/uploader/crc_pl.txtから入手できます。
#
$dcrc_enable = 0;

# dcrcの場所
$dcrc_path = './dcrc';

# Perlでcrcチェックサム算出
# 解説：拙作のcrc.plを使ってCRCチェックサムを算出します。
# ※dcrcで計算した場合に比べて処理スピードがかなり落ちます。
#
# crc.plを使ってCRC計算をする場合はcrc.plへのパスを設定してください。
$crc_pl = './crc.pl';

# md5チェックサム算出
# 1:使用する 0:使用しない
# 解説：サーバー側のmd5コマンドまたはmd5.plを利用してファイルのチェックサムを記録します。
# md5.plはhttp://zurubon.strange-x.com/uploader/md5_pl.txtから入手できます。
# ※アップロード時に記録
$md5_enable = 0;

# md5コマンドのサーバーパス
$md5_path = '/sbin/md5';

# md5.plへのサーバーパス
# なるべくサーバー側のmd5コマンドが使えない場合の代替処置としてmd5.plを使うようにしてください。
# ※md5コマンドで計算した場合に比べてかなり処理速度が落ちます。
#
# md5.plを使ってMD5計算をする場合はmd5.plへのパスを設定してください。
$md5_pl = './md5.pl';

# FTPモード
# 1:使用する 0:使用しない
$ftp_enable = 0;

# upftp.plへのサーバーパス
# 解説：upftp.plはhttp://zurubon.strange-x.com/uploader/upftp_pl.txtから入手できます。
# FTPモードを使用しない場合はupftp.plを設置する必要はありません。
$upftp_pl = './upftp.pl';

# FTP転送先ホスト
$ftp_host = 'REDACTED';

# FTPユーザー名
$ftp_user = 'REDACTED';

# FTPパスワード
$ftp_pass = 'REDACTED';

# FTP保存先ディレクトリ
# 解説：FTP転送先ホストにログイン後指定されたディレクトリに
# 移動してそこにデータをアップロードします。
$ftp_dir = '.';

# 「環境設定」で発行されるcookieの有効期限日数
# 解説：デフォルトは90日間(およそ3ヶ月)
# ※あまりに日数を多くしてもブラウザー側で処理不能となりますのでほどほどに。
$cookie_limit_day = 90;

# ########################################
# セキュリティーに関する設定
# ########################################

# HTMLファイルは拡張子を*.txtに変更する(※イタズラ防止)
# 1:変更する 0:変更しない
$htmlext = 0;

# 投稿者IPのログファイルへの記録
# 1:記録する 0:記録しない
$getip = 1;

# 投稿制限用パスワード
# 解説：投稿者は全て管理者が設定したパスワードを入力しないと
# 投稿できなくなります。
$postpass_enable = 0;

# 投稿制限用パスワードの'種'
# 解説：上記の投稿制限用パスワードを生成するときに用いた種です。
$postseed = 'REDACTED';

# 投稿制限用パスワード
# 解説：平文のパスワードではなく暗号化されたものが必要です。
#
# まずhttp://zurubon.strange-x.com/crypt.txtを自分の利用するサーバーに設置して、
# 平文のパスワードと投稿制限用パスワードの種を入力、生成されたパスワード
# をここに設定してください。
$postpass = 'REDACTED';

# 連続投稿間隔の制限
# 1:制限する 0:制限しない
$continue_limit = 0;

# 連続投稿制限用データファイル
# 推奨パーミッション：600->666
$continue_file = './continue.cgi';

# 連続投稿を許可する間隔
# 解説：デフォルトは30分。
# 「以前の"同じIP"の投稿から30分経ったら再度投稿してもOK」ということです。
# ◆記述例◆
# 2時間「200」
# 1時間半「130」
# 30分「030」
# 1分「001」
$contine_time = '030';

# アクセス制限
# 1:使用する 0:使用しない
$access_ctl = 0;

# アクセス制限用データファイル
# 解説：このファイルにはアクセスを禁止したいホストを
# 「1行1ホスト名・FQDN(またはIPアドレス)」で記述します。
# ※正規表現も使えます。
$denylist = './deny.cgi';

# MIME types
%MIME =
(
# テキスト
	c   => "text/c",
	css => "text/css",
	csv => "text/comma-separated-values",
	htm => "text/html",
	js  => "text/(js|javascript)",
	rtf => "text/rtf|application/rtf",
	smi => "text/smil-basic|application/smil",
	txt => "text/plain",
	vbs => "text/vbscript",
	xml => "text/xml|application/xml",
# イメージ
	bmp => "image/(bmp|x-bmp|x-MS-bmp)",
	gif => "image/gif",
	ico => "image/x-icon",
	jpg => "image/.*jpeg",
	png => "image/(png|x-png)",
	psd => "image/x-photoshop",
	tif => "image/(tiff|x-tiff)",
	xbm => "image/(x-xbm|x-xbitmap)",
# ビデオ
	asf => "video/(x-ms-asf|x-ms-asf-plugin)|application/x-mplayer2",
	avi => "video/(avi|msvideo|x-msvideo)",
	mov => "video/quicktime",
	mpg => "video/(mpg|mpeg|x-mpeg)",
# オーディオ
	aif => "audio/(aiff|x-aiff|x-pn-aiff)",
	au  => "audio/(basic|x-pn-au)",
	m3u => "audio/(mpegurl|x-scpls|x-mpegurl)",
	mid => "audio/(mid|midi|x-mid|x-midi)|application/x-midi|music/crescendo|x-music/x-midi",
	mod => "audio/x-mod",
	mp3 => "audio/(mp3|mpg|mpeg|x-mp3|x-mpg)",
	ra  => "audio/(x-realaudio|vnd\\.rn-realaudio)",
	ram => "audio/x-pn-realaudio",
	rm  => "application/vnd\\.rn-realmedia",
	rpm => "audio/x-pn-realaudio-plugin",
	vqe => "audio/x-twinvq-plugin",
	vqf => "audio/x-twinvq|application/x-twinvq",
	wav => "audio/(wav|x-wav|x-pn-wav|x-pn-windows-acm|x-pn-windows-pcm)",
	wma => "audio/x-ms-wma",
# 他
	arj => "application/arj",
	bin => "application/(octet-stream|x-macbinary)",
	dcr => "application/x-director",
	exe => "application/(x-exe|x-msdownload)",
	gz  => "gzip",
	hlp => "application/(winhlp|x-winhelp)",
	jar => "application/java-archive",
	js  => "application/x-javascript",
	lzh => "lha|lzh|LhasaArchive|LHMelt",
	pac => "application/x-ns-proxy-autoconfig",
	pdf => "application/pdf",
	rar => "application/x-rar-compressed",
	sit => "application/x-stuffit",
	swf => "application/x-shockwave-flash",
	tar => "application/x-tar",
	uue => "application/x-uuencode",
	wmf => "application/x-msmetafile",
	wri => "application/application/x-mswrite",
	yz1 => "application/x-yz1",
	Z   => "application/x-compress",
	zip => "zip",
	wrl => "model/vrml|x-world/x-vrml",
);
%EMIM =
(
	"zip" => "gzip",
);

# ############################################################################
# 以下はスクリプトのエンジン部分。無闇にいじくると動かなくなるかも(ﾜﾗ
# ############################################################################

# アクセス制限
$host = $ENV{REMOTE_ADDR};
if($access_ctl){
	open(DB,"$denylist") || die &error('アクセス制限ファイルがオープンできません','');
	@lines = <DB>;
	close(DB);
	foreach $line (@lines) {
		next if(length($line)<4);
		chop $line;
		if( $host=~/$line/ ){&error('アクセス制限','あなたにはアクセス権限がありません。');}
	}
	$lines = 0;
}

@sup = split(/,/, $support);
@MEXT = sort keys(%MIME);
%sup = ();
grep($sup{$_} = 1, @sup, @MEXT);
if($htmlext != 0)
{
	delete $sup{"htm"} if exists $sup{"htm"};
	delete $sup{"html"} if exists $sup{"html"};
	delete $MIME{"htm"} if exists $MIME{"htm"};
	delete $MIME{"html"} if exists $MIME{"html"};
}
@sup = sort keys(%sup);

if($lock){
	$retry = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0){unlink($lockfile); exit;}
		sleep(1);
	}
}

# ログ読み込み
&readlog;

# アップロード処理とログへの追加書込み
if ($ENV{REQUEST_METHOD} eq "POST") {
# $dateに現在時刻を入れる
	$ENV{TZ} = 'JST-9';
	$times = time;
	($sec,$min,$hour,$mday,$month,$year,$wday,undef,undef) = localtime($times);
	$month++;
	$youbi = ('日','月','火','水','木','金','土') [$wday];
	$year = 1900 + $year;
	$date = sprintf("%d年%02d/%02d(%s)%02d:%02d", $year, $month, $mday, $youbi, $hour, $min);
# 連続投稿制限
	if($continue_limit){
		$cont_val = &continue_check('check');
		&error('連続投稿制限中','時間を置いてやり直してください') if(!$cont_val);
	}
	srand(time^$$);
	$uniq_name = time . int(rand(time)) . '.temp'; # temporaryにuniqueな名前を付ける
	unlink <$storedir*.temp>; # ディレクトリにゴミが残っている場合には掃除する
	&decode;
	open (UPLOCK, "$up_lockfile");
	flock (UPLOCK, 2); # 排他処理の始まり
	&readlog; # uploadが終わってからログを読む
	# 正式な$idを決める
	if((-s "$log_file")==0){
		$id = $start_num;
	}else{
		($id) = split(/\t/, $lines[0]);
		$id = sprintf("%04d",++$id);
	}
	rename ("$storedir$uniq_name", "$storedir$prefix$id.$type"); # temporaryな名前から正式な名前へrename
	chmod 0604, "$storedir$prefix$id.$type";
	if($ftp_enable){
		if(-f $upftp_pl){
			require $upftp_pl;
			use Cwd; my $olddir = cwd;
			chdir $storedir || die error('エラー', "$storedirが開けません");
			&upftp::login($ftp_host, 21, $ftp_user, $ftp_pass);
			&upftp::cd($ftp_dir);
			&upftp::upload("$prefix$id.$type");
			&upftp::logout;
			chdir $olddir;
		}
		else{
			&error('エラー','upftp.plが見つかりません。<br>設定を見直してください。');
		}
		unlink("$storedir$prefix$id.$type");
	}
	&write if($comment);
	close (UPLOCK); # 排他処理の終わり
	&readlog;
}

# フォームデータのデコード(GET)
$buffer = $ENV{QUERY_STRING};
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$FORM{$name} = $value;
}

# 環境設定モード
if($ENV{QUERY_STRING} eq 'env'){
	&env_form;
}
# 過去ログ検索
elsif($FORM{search} ne "" || $ENV{QUERY_STRING} eq "search"){
	if($FORM{search}){
		@search_ary = &search_log($FORM{search});
		$search_hit = @search_ary;
	}
	&search_result;
}
# 画像閲覧モード
elsif($ENV{QUERY_STRING} eq "image" || $FORM{image} ne ""){
	&image_view($FORM{image});
}
# URLリスト作成
elsif($FORM{lstart} ne "" && $FORM{lend} ne ""){
	&list;
}
# 投稿データ削除フォーム
elsif($FORM{del} ne "" && $del_enable){
	&del_form($FORM{del});
}
# 投稿データの削除
elsif($FORM{delid} && $FORM{delpass} ne ""){
	&del($FORM{delid},$FORM{delpass});
	&readlog;
	&html;
}
# md5表示
elsif($md5_enable && $FORM{md5} ne ""){
	&md5_disp($FORM{md5});
}
# dcrc
elsif($dcrc_enable && $FORM{dcrc} ne ""){
	&dcrc_disp($FORM{dcrc});
}
# ヘルプ
elsif($FORM{help} ne ""){
	&help($FORM{help});
}
# トップページ表示
else{
	&html;
}
# ロックファイル削除
unlink($lockfile) if($lock);

# 終了
exit;

# ############################################################################
# 以下関数定義&実装
# ############################################################################

# ログ読み込み
sub readlog{
	if(!open(DB,"$log_file")){&error('ログファイルがオープンできません','スクリプトの設定を見直してください。');}
	seek(DB,0,0);
	@lines = <DB>;
	$end_num = (split(/\t/,$lines[0]))[0];
	close(DB);
}

# ログ書き込み
sub write{
	$size = $ENV{CONTENT_LENGTH}/1024;
	$size = 1 if($ENV{CONTENT_LENGTH} < 1024);
	$size = sprintf("%d", $size);
	$host = 'anonymous' if(!$getip);
	$pass = '*' if(!$del_enable);
	$value = &tjoin($id, $type, $comment, $host, $ENV{HTTP_USER_AGENT}, $date, $size, $ctype, $pass, $md5, $dcrc);
	$value .= "\n";

	#$valueを@linesに加えたのち、書き込む
	if(@lines > $max-1){#最大を超えたら削除します。
		$del= pop(@lines);
		($id, $type) = split(/\t/, $del);
		if($ftp_enable){
			if(-f $upftp_pl){
				require $upftp_pl;
				&upftp::login($ftp_host, 21, $ftp_user, $ftp_pass);
				&upftp::cd($ftp_dir);
				&upftp::del("$prefix$id.$type");
				&upftp::logout;
			}
			else{
				&error('エラー','upftp.plが見つかりません。<br>設定を見直してください。');
			}
		}
		else{unlink("$storedir$prefix$id.$type");}
	}
	unshift(@lines,$value);
	open(DB,">$log_file");
	eval { flock(DB,2); };
	seek(DB,0,0);
	print DB @lines;
	eval { flock(DB,8); };
	close(DB);
}

# POSTされたデータのMIMEタイプ決定、CRC・MD5算出、
# コメント長計算・パスワード照合処理
sub decode{
	my $size, $expfile;

	return if($ENV{CONTENT_LENGTH} > $limitk*1024);
	return unless($ENV{HTTP_REFERER} =~/$url/);

	binmode(STDIN);
	while(<STDIN>){
		last if(/^\r\n/);
		$bound = $_ if(/^--/);
		$rext = $1 if(/^Content-Disposition:.*filename="(.*)"/i);
		$ctype = $1 if(/^Content-Type:(.*)/i);
	}

	$rext =~ s/.*\.//go;
	$ctype =~ s/(^\s|\s$)//go;
	$bound=~s/\r\n//;

	foreach $mext (@MEXT)
	{
		if($ctype =~ /$MIME{$mext}/)
		{
			next if (defined($EMIM{$mext}) && $ctype =~ /$EMIM{$mext}/);
			$type = $mext;
		}
	}

	if($rext ne "")
	{
		$rextl = "\L$rext\E";
		foreach $ext (@sup)
		{
			if("\L$ext\E" eq $rextl)
			 {
				$type = $ext;
				last;
			}
		}
	}

	$type = 'xxx' if($type eq '');
	$ctype = "www/none" unless $ctype;
	$ctype = &htmlenc($ctype);

	open(DB,">$storedir$uniq_name");
	binmode(DB);
	$dbuf = "";
		while(<STDIN>){
			last if($_=~/^$bound/);
			print DB $dbuf;
			$dbuf = $_;
		}
	$dbuf =~ s/\r\n$//;
	print DB $dbuf;
	close (DB);

	$size = -s "$storedir$uniq_name";
	&reload if(!$size); #sizeが0ならリロード

	$ext = &post_decode;

	if($ext ne 'ext'){
		if(!grep($ext eq $_, @sup)){
			unlink("$storedir$uniq_name");
			&error('投稿データエラー', '許可されていない拡張子です。');
		}
		$type = $ext;
	}
	if($dcrc_enable){ # CRC計算
		if(-f $crc_pl){
			require $crc_pl;
			$dcrc = &crc::crc16("$storedir$uniq_name");
		}
		else{
			$dcrc = &dcrc("$storedir$uniq_name");
		}
	}
	if($md5_enable){ # MD5計算
		if(-f $md5_pl){
			require $md5_pl;
			$md5 = &md5::from_file("$storedir$uniq_name");
		}
		else{
			$md5 = &md5("$storedir$uniq_name");
		}
	}

	$comment = &post_decode;
	&reload if(!$comment); # コメントが書かれていない場合はReload
	&error('投稿エラー','コメントが長すぎます') if(length($comment) > $comment_max);
	$comment = &htmlenc($comment);
	$comment =~ s/(https?|ftp|news)(:.*)([a-z]|[A-Z]|[0-9]|\/)/<a href="$1$2$3">$1$2$3<\/a>/g if($autolink);

	if($del_enable){
		$input_pass = &post_decode;
		$pass = crypt($input_pass, $del_seed);
		$pass = '*' if($input_pass eq '');
		&error('投稿エラー','パスワードが長すぎます') if(length($input_pass) > 10);
		if($postpass_enable){
			&error('投稿用パスワードが違います','投稿用パスワードを管理者から入手してください。') if(!&postpass);
		}
	}
	elsif($postpass_enable){
		&error('投稿用パスワードが違います','投稿用パスワードを管理者から入手してください。') if(!&postpass);
	}

	&continue_check('add') if($continue_limit);
}#decode END

# POSTデータを文字列に変換して返す
sub post_decode{
	my $post_str;
	while(<STDIN>){
		last if(/^$bound/);
		next if(/^\r\n/);
		next if(/^Content/);
		$post_str .=$_;  $post_str=~s/\r\n//;
	}
	return $post_str;
}

# トップページ表示
sub html{
	$page = $FORM{page};
	$page=0 unless($page);
	$lmax = $FORM{lm};
	$lmax=$lmaxdef unless($lmax);# 一ページにどれだけ表示するか？
	$page2 = $page*$lmax;

	my $limitm = $limitk / 1024;
	&print_header;
	print <<"_HTML_";
	<FORM METHOD="POST" ENCTYPE="multipart/form-data" ACTION="$url" >
	アプするファイル<strong>（$limitm MBまで）</strong><br>
	<INPUT TYPE=file  SIZE="40" NAME="filedata">
	<select name="ext">
	<option value="ext" selected>特殊拡張子選択</option>
_HTML_

	foreach (@sup){print "<option value=\"$_\">$_</option>\n";}
	print "</select>\n";
	print "<br>コメント<i><small>（※コメント無記入の場合リロードになります\n";
	print "/URLはオートリンクします" if($autolink);
	print "）</small></i><br>\n", "<INPUT TYPE=text SIZE=\"45\" NAME=\"comment\">\n",
	"<INPUT TYPE=submit VALUE=\"Up/Reload\" class=\"button\"><INPUT TYPE=reset VALUE=\"Cancel\" class=\"button\"><br>\n";
	print " <a href=\"$url?help=del\">del pass</a>: <INPUT TYPE=password SIZE=\"10\" NAME=\"delpass\" maxlength=\"10\">\n" if($del_enable);
	print " <a href=\"$url?help=post\">post pass</a>: <INPUT TYPE=password SIZE=\"10\" NAME=\"postpass\">\n" if($postpass_enable);
	print "</FORM><br>\n";
	print "<form method=\"GET\" action=\"$url\">\n" if($listform_enable);
	print "<small>\n";
	&shiba::html_out; # カウンター
	print ' D：投稿記事削除' if($del_enable);
	print ' C：CRC表示' if($dcrc_enable);
	print ' 5：md5表示' if($md5_enable);
	print "</small>\n",
		"<HR><small>| <a href=\"$url?search\">過去ログ検索</a>\n",
		" | <a href=\"$url?image\">画像閲覧</a> | <a href=\"$url?env\">環境設定</a> $links</small>\n",
		"<HR>ページ：[<A HREF=\"$url?page=0&lm=$max\">ALL</A>] \n";
	$total = @lines;
	$count = int(($total-1)/$lmax);
	for($i=0;$i<=$count;$i++){
	        if($i eq $page){$disp = $i + 1; print "[<b>$disp</b>] \n";}else{
			$disp = $i + 1;
	                print "[<A HREF=\"$url?page=$i&lm=$lmax\">$disp</A>] \n";
	        }
	} # for
	print "<HR>\n";
	if($listform_enable){
		print "Range\:<input type=\"text\" size=\"5\" name=\"lstart\" value=\"$start_num\"> -",
			"<input type=\"text\" size=\"5\" name=\"lend\" value=\"$end_num\">\n";
		print " <input type=\"checkbox\" name=\"md5list\" value=\"checked\">md5\n" if($md5_enable);
		print " <input type=\"checkbox\" name=\"dcrclist\" value=\"checked\">CRC\n" if($dcrc_enable);
		print " <select name=\"extlist\"><option value=\"\" selected>拡張子</option>\n";
		foreach (@sup){print "<option value=\"$_\">$_</option>\n";}
		print "</select>\n", " <input type=\"submit\" value=\"URL list\" class=\"button\"><HR>\n";
	}
	(@lines < $lmax) || (@lines = @lines[$page2 .. $page2+$lmax-1]);
	&print_postdata(@lines);

	print "<hr><small>対応ファイルフォーマット：\n<tt>\n";
	for($i = 0; $i < $#MEXT; $i++)
	{
	        print "<br>\n" if(($i % 12) == 0);
	        print "*.$MEXT[$i] ";
	}
	print "*.$MEXT[$i]",
	"</tt><br>\n";

	print "その他のファイルフォーマット：特に指定の無い限り*.xxxとして保存されます。<br>\n",
	"ログ保持限界は$maxで1ページにつき$lmaxdef件づつ\表\示します。<br>\n";
	if(!$ftp_enable){
		print "現在のサーバディスク使用量は約"; print(&calc_disk_usage); print "kbです。\n";
	}
	print "</form>\n" if($listform_enable);
	print "</small>\n";
	&print_footer;
}#html END

# HTMLのヘッダ部分
sub print_header{
	my $subtitle = shift;
	my $title_h;

	if(!$subtitle){$title_h = $title}
	else{$title_h = "$title -$subtitle-";}

	# 環境設定cookie取得
	&get_cookie;

	print "Content-type: text/html\n";
	if($FORM{mode} eq 'envset'){
		&send_cookie; # cookie送信
		# 新しく設定された環境設定を有効化する
		$crce=$FORM{crce}; $md5e=$FORM{md5e}; $acte=$FORM{acte}; $commente=$FORM{commente};
		$sizee=$FORM{sizee}; $mimee=$FORM{mimee}; $datee=$FORM{datee}; $anothere=$FORM{anothere};
		$gzipence=$FORM{gzipence};
	}
	if($gzipenc_enable && $gzipence){&gzip_encode;}
	else{print "\n";}

	print <<"HEADER";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
	<HTML LANG="ja">
	<HEAD>
	<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
	<link rel="shortcut icon" href="../res/favicon.ico">
	<TITLE>$title_h</TITLE>
	<STYLE><!--$css--></STYLE>
	</HEAD>
	$body
	<table width="100%"><tr><td bgcolor="$obi"><strong><font size="4">$title_h</font></strong></td></tr></table>
	<p>$info</p>
HEADER
}

# HTMLのフッタ部分
sub print_footer{
	print "<HR><H5 ALIGN=right><A HREF=\"REDACTED\">ゆいのーと</A> + \n",
	"<a href=\"REDACTED\">$copyright</a> $modified\n",
	"</H5>\n<p>$ban</p>\n</body></html>\n";
	close(STDOUT) if($gzipenc_enable && $gzipence);
}

# 投稿記事部分のHTML
sub print_postdata{
	my @matrix = @_;
	my $id, $type, $comment, $host, $brauza, $date, $size, $ctype, $pass, $md5, $dcrc;

	print "<table><tr>\n";
	print "<th>ACT</th>\n" if($acte);
	print "<th>NAME</th>\n";
	print "<th>COMMENT</th>\n" if($commente);
	print "<th>SIZE(KB)</th>\n" if($sizee);
	print "<th>MIME</th>\n" if($mimee);
	print "<th>DATE</th>\n" if($datee);
	print "<th>MD5</th>\n" if($md5e && $md5_enable);
	print "<th>CRC</th>\n" if($crce && $dcrc_enable);
	print "</tr>\n";
	foreach (@matrix){
		s/\n//g;
		($id, $type,$comment,$host,$brauza,$date,$size,$ctype,$pass,$md5,$dcrc) = split(/\t/);
		next unless($id);
		print "<tr>\n";

		if($acte){
			print "<td><small>\n";
			print "<a href=\"$url?del=$id\">D</a>\n" if($del_enable);
			print " <a href=\"$url?dcrc=$id\">C</a>\n" if($dcrc_enable && !$crce);
			print " <a href=\"$url?md5=$id\">5</a>\n" if($md5_enable && !$md5e);
			print "</small></td>\n";
		}

		print "<td>[<a href=\"";
		if($ftp_enable){ print "$storeurl"; }
		else{ print "$storedir"; }
		print "$prefix$id.$type\"";
		print " target=\"anotherwin\"" if($anothere);
		print ">$prefix$id.$type</a>]</td>\n";

		print "<td><font size=2>$comment</font></td>\n" if($commente);
		print "<td align=right><b><font size=2>$size</font></b></td>\n" if($sizee);
		print "<td><font size=2 color=\"#888888\">$ctype</font></td>\n" if($mimee);
		print "<td><font size=2>$date</font></td>\n" if($datee);
		print "<td><small>$md5</small></td>\n" if($md5e && $md5_enable);
		print "<td><small>$dcrc</small></td>\n" if($crce && $dcrc_enable);
		print "</tr>\n";
	}
	print "</table>\n";
}

#gzip圧縮転送
sub gzip_encode{
	if($ENV{HTTP_ACCEPT_ENCODING}=~/gzip/){
		if($ENV{HTTP_ACCEPT_ENCODING}=~/x-gzip/ ){
			print "Content-encoding: x-gzip\n\n";
		}else{
			print "Content-encoding: gzip\n\n";
		}
		open(STDOUT,"| gzip -1 -c");
		print "<!--gzip_enable-->\n";
	}
}

#URLリスト出力
sub list{
	my $id, $type, $comment, $host, $brauza, $date, $size, $ctype, $pass, $md5, $dcrc;
	my $start = $FORM{lstart};
	my $end = $FORM{lend};
	my $ext = $FORM{extlist} if($FORM{extlist});

	print "Content-type: text/plain\n\n";
	foreach(@lines){
		s/\n//g;
		($id,$type,$comment,$host,$brauza,$date,$size,$ctype,$pass,$md5,$dcrc) = split(/\t/);
		next if($ext && ($type ne $ext));

		if($id <= $end){
			print "$storeurl$prefix$id.$type";
			print "\t$md5" if($FORM{md5list} eq "checked");
			print "\t$dcrc" if($FORM{dcrclist} eq "checked");
			print "\n";
		}
		last if($id eq $start);
	}
}

# 投稿データ削除フォーム
sub del_form{
	my $target_id = shift;

	&print_header('投稿データ削除');
	print <<"DEL";
	<h3>ID：$target_idを削除します</h3>
	<form action=$url method="GET">
	<input type="hidden" name="delid" value="$target_id">
	パスワード入力：<input type="password" size="12" name="delpass"><br>
	<input type="submit" value="削除" class=\"button\">
	</form>
DEL
	&print_footer;
}

# 投稿ファイル削除処理
sub del{
	my ($target_id, $target_pass) = @_;
	my $id, $type, $pass, $target_type;

	foreach (@lines){
		chop;
		($id, $type, undef, undef, undef, undef, undef, undef, $pass, undef, undef) = split(/\t/);
		if($id eq $target_id){$target_type=$type; $org_pass=$pass; last;}
	}
	&error('削除エラー','該当ファイル無し') if(!$target_type);

	if(!$admindel_enable || ($admindel_enable && $adminpass ne (crypt($target_pass, $adminseed)))){
		&error('削除エラー','削除禁止ファイルです') if($org_pass eq '*');
		&error('削除エラー','パスワードが違います') if($org_pass ne (crypt($target_pass, $del_seed)));
	}
	if($ftp_enable){
		if(-f $upftp_pl){
			require $upftp_pl;
			&upftp::login($ftp_host, 21, $ftp_user, $ftp_pass);
			&upftp::cd($ftp_dir);
			&upftp::del("$prefix$id.$type");
			&upftp::logout;
		}
		else{
			&error('エラー','upftp.plが見つかりません。<br>設定を見直してください。');
		}
	}
	else{unlink("$storedir$prefix$target_id.$target_type");}

	open(DB,">$log_file");
	eval { flock DB, 2; };
	foreach (@lines){
		next if($target_id eq (split(/\t/))[0]);
		s/\n//g;
		print DB "$_\n";
	}
	eval { flock DB, 8; };
	close(DB);
}

# エラー出力
sub error{
	&print_header('Notice！');
	print <<"ERROR";
	<hr>
	<center>
	<strong>$_[0]</strong><br>
	<p>$_[1]</p>
	<a href="$url">Return</a>
	</center>
ERROR
	&print_footer;
	exit;
}

# 引数の配列を分解してタブで区切られた文字列を返す
sub tjoin
{
	my @data = @_;
	foreach (@data)
	{
		next if(!$_);
		s/\s/ /go;
	}
	return join("\t", @data);
}

# 文字列中のHTMLタグを無効にする
sub htmlenc
{
	my $str = shift;
	$str =~ s/\&/&amp;/go;
	$str =~ s/\</&lt;/go;
	$str =~ s/\>/&gt;/go;
	$str =~ s/\"/&quot;/go;
	$str =~ s/\t/ /go;
	return $str;
}

# md5コマンドからmd5 CRCを得る
sub md5{
	open MD5, "$md5_path $_[0] |";
	my $val = <MD5>;
	close MD5;
	$val =~ s/ //g;
	$val = (split(/\=/,$val))[1];
	return $val;
}

# md5表示
sub md5_disp{
	my $target_id = $_[0];
	my $ans, $id, $md5;

	foreach (@lines){
		chop;
		($id, undef, undef, undef, undef, undef, undef, undef, undef, $md5, undef) = split(/\t/);
		if($id eq $target_id){$ans = $md5; last;}
	}
	&error('エラー','該当ファイルが存在しないか、md5チェックサムが記録されていません。') if(!$ans);
	&error("$target_idのmd5チェックサム","$ans");
}

# ログファイルを検索して結果を収納した配列を返す
sub search_log{
	my $search_str = $_[0];
	my $count = 0;
	my $id, $type, $comment, $host, $brauza, $date, $size, $ctype;
	my $start, $end, $ext;
	my @ans;

	$start = $FORM{sstart};
	$end = $FORM{send};
	$ext = $FORM{extlist};
	$min = $FORM{size_min};
	$max = $FORM{size_max};

	if(-f $jcode){
		require $jcode;
#		&jcode'convert(*search_str,'sjis') if(!$FORM{nojcode});
		#perl5対応? epicの色分けが破綻するので lam 6/24
		jcode::convert(*search_str,'sjis') if(!$FORM{nojcode});
	}
	$search_str = quotemeta($search_str);
	foreach (@lines){
		s/\n//g;
		($id,$type,$comment,$host,$brauza,$date,$size,$ctype) = split(/\t/);
		if($id >= $start && $id <= $end){
			if($ext ne '' && $ext ne $type){next;}
			else{
				if($size >= $min){
					if($size <= $max || !$max){
						if(/$search_str/){$ans[$count] = $_; $count++;}
					}
				}
			}
		}
	}
	return @ans;
}

# 過去ログ検索のトップページ/結果 表示
sub search_result{
	if($FORM{sstart}){$sstart = $FORM{sstart};}else{$sstart = $start_num;}
	if($FORM{send}){$send = $FORM{send};}else{$send = $end_num;}
	if($FORM{size_min}){$size_min = $FORM{size_min};}else{$size_min = 1;}
	if($FORM{size_max}){$size_max = $FORM{size_max};}else{$size_max = '';}
	if($FORM{extlist}){$ext = $FORM{extlist}; $extv = $FORM{extlist};}
	else{$ext = '拡張子'; $extv = '';}

	&print_header('過去ログ検索');
	print <<"FORM";
	<form method=GET action="$url">
	検索文字列:<INPUT TYPE=text SIZE="25" NAME="search" value="">
	<INPUT TYPE=submit VALUE="Search/Return" class="button">
	<INPUT TYPE=reset VALUE="Cancel" class="button"><br>
	範囲:<input type="text" size="5" name="sstart" value="$sstart"> -
	<input type="text" size="5" name="send" value="$send">
	<select name="extlist"><option value="$extv" selected>$ext</option>
FORM

	foreach (@sup){print "<option value=\"$_\">$_</option>\n";}

	print <<"FORM";
	</select><br>
	サイズ:<input type="text" size="10" name="size_min" value="$size_min">K～<input type="text" size="10" name="size_max" value="$size_max">Kの間で
FORM

	print "<INPUT TYPE=checkbox NAME=nojcode value=checked checked>jcode.plを使わない\n" if(-f $jcode);
	print "</FORM><small>\n";
	print ' D：投稿記事削除' if($del_enable);
	print ' C：CRC表示' if($dcrc_enable);
	print ' 5：md5表示' if($md5_enable);
	print "</small>\n";
	print '<hr>';
	if($search_hit){&print_postdata(@search_ary);}
	if($search_str){
		print "<h4>\"$search_str\"は$search_hit件見つかりました。</h4>" if($search_hit);
		print "<h4>\"$search_str\"は見つかりませんでした。</h4>" if(!$search_hit);
	}
	&print_footer;
}

# dcrcからターゲットファイルのCRCを得る
sub dcrc{
	my $target = shift;
	open DCRC, "$dcrc_path $target |";
	my $val = <DCRC>;
	close DCRC;
	$val = (split(/ /,$val))[1];
	return $val;
}

# CRC表示
sub dcrc_disp{
	my $target_id, $ans, $id, $dcrc;

	$target_id = $_[0];
	foreach (@lines){
		chop;
		($id, undef, undef, undef, undef, undef, undef, undef, undef, undef, $dcrc) = split(/\t/);
		if($id eq $target_id){$ans = $dcrc; last;}
	}
	&error('エラー','該当ファイルが存在しないか、CRCチェックサムが記録されていません。') if(!$ans);
	&error("$target_idのCRCチェックサム","$ans");
}

# 投稿制限用パスチェック
sub postpass{
	my $input_postpass = &post_decode;

	if($postpass ne crypt($input_postpass, $postseed)){
		unlink "$storedir$uniq_name";
		return 0;
	}
	return 1;
}

# 画像閲覧モード
sub image_view{
	my $page = $_[0];
	my $total, $page_max, $id, $type, $comment, $date, $size, $i;
	my @images;

	foreach (@lines){
		if((split(/\t/))[1] =~ /(jpg|png|gif)/){
			$images[$count] = $_; $count++;
		}
	}
	$total = @images;
	$page_max = int($total/10);
	$page_max++ if((split(/\./, $total/10))[1]);
	$page = 1 if(!$page || $page > $page_max);

	&print_header('画像閲覧');
	print "<HR><small>| <a href=\"$url?search\">過去ログ検索</a>\n",
	" | <a href=\"$url?image\">画像閲覧</a> | <a href=\"$url?env\">環境設定</a> $links</small>\n";
	print "<hr>\n", "ページ: ";
	for($i=1; $i<=$page_max; $i++){
		if($i==$page){ print "<strong>[$i]</strong>\n"; }
		else { print "<a href=\"$url?image=$i\">[$i]</a>\n"; }
	}

	print "<hr>\n<center>\n";
	if($page == 1){ print "<s>[Prev]</s>&nbsp;&nbsp;&nbsp;\n"; }
	else { print sprintf("<a href=\"$url?image=%d\">[Prev]</a>&nbsp;&nbsp;&nbsp;\n", ($page-1)); }
	print "<a href=\"$url\">[戻る]</a>\n";
	if($page == $page_max){ print "&nbsp;&nbsp;&nbsp;<s>[Next]</s>\n"; }
	else { print sprintf("&nbsp;&nbsp;&nbsp;<a href=\"$url?image=%d\">[Next]</a>\n", ($page+1)); }
	print "</center>\n";

	for($i=($page*10-10); $i<=($page*10-1); $i++){
		last if(($i+1) > $total);
		($id, $type, $comment, undef, undef, $date, $size, undef, undef, undef, undef) = split(/\t/, $images[$i]);
		print "<p><a href=\"$storeurl$prefix$id.$type\"";
		print " target=\"new_win\"" if($anothere);
		print "><img src=\"$storeurl$prefix$id.$type\" height=\"250\"></a><br>\n";
		print "<a href=\"$storeurl$prefix$id.$type\">$prefix$id.$type</a><br>\n",
		"$comment <small>$date</small></p>\n";
	}

	print "<center>\n";
	if($page == 1){ print "<s>[Prev]</s>&nbsp;&nbsp;&nbsp;\n"; }
	else { print sprintf("<a href=\"$url?image=%d\">[Prev]</a>&nbsp;&nbsp;&nbsp;\n", ($page-1)); }
	print "<a href=\"$url\">[戻る]</a>\n";
	if($page == $page_max){ print "&nbsp;&nbsp;&nbsp;<s>[Next]</s>\n"; }
	else { print sprintf("&nbsp;&nbsp;&nbsp;<a href=\"$url?image=%d\">[Next]</a>\n", ($page+1)); }
	print "</center>\n";

	print "<hr>\n", "ページ: ";
	for($i=1; $i<=$page_max; $i++){
		if($i==$page){ print "<strong>[$i]</strong>\n"; }
		else { print "<a href=\"$url?image=$i\">[$i]</a>\n"; }
	}

	&print_footer;
}

# Reload
sub reload{
	unlink "$storedir$prefix$id.$type";
	&readlog;
	&html;
	exit;
}

# 連続投稿制限ファイルの読み書き、連続投稿チェック
sub continue_check{
	my $mode = shift;
	my $date_id, $post_ip, $line_c, $line_num, $ans, $ip, $id;

	$date_id = sprintf("%d%02d%02d%02d%02d", $year, $month, $mday, $hour, $min);
	$post_ip = $ENV{REMOTE_ADDR};
	if(!open(DB, "$continue_file")){&error('連続投稿制限ファイルがオープンできません');}
	@line_c = <DB>;
	close(DB);

	if($mode eq 'check'){ # 投稿者情報のチェック
		foreach (reverse(@line_c)){
			chop;
			($ip,$id) = split(/:/);
			if($post_ip eq $ip){
				$ans = $date_id - $id;
				return 0 if($ans < $contine_time);
			}
		}
	}
	if($mode eq 'add'){ # 連続投稿制限ファイルに投稿者情報を追加
		$line_num = @line_c;
		push(@line_c, "$post_ip:$date_id");
		pop(@line_c) if($line_num > $max-1);
		if(!open(DB,">$continue_file")){
		&error('連続投稿制限ファイルを書込みモードで開けません','ファイルのパーミッションを見直してください');}
		eval { flock DB, 2; };
		foreach (@line_c){print DB "$_\n";}
		eval { flock DB, 8; };
		close (DB);
	}
	return 1;
}

# 環境設定フォーム
sub env_form{
	&print_header('環境設定');
	print <<"ENV";
	<hr>
	<strong>環境設定</strong><br>
	<form method="GET" action="$url">
	<input type="hidden" name="mode" value="envset">
	<ul>
	<li><strong>\表\示設定</strong>
	<ul>
ENV
	if($md5_enable){
		print '<input type="checkbox" name="md5e" value="1"';
		print " checked" if($md5e); print ">MD5<br>\n";
	}
	if($dcrc_enable){
		print '<input type="checkbox" name="crce" value="1"';
		print " checked" if($crce); print ">CRC<br>\n";
	}
	print '<input type="checkbox" name="acte" value="1"';
	print " checked" if($acte); print ">ACT<br>\n";
	print '<input type="checkbox" name="commente" value="1"';
	print " checked" if($commente); print ">COMMENT<br>\n";
	print '<input type="checkbox" name="sizee" value="1"';
	print " checked" if($sizee); print ">SIZE<br>\n";
	print '<input type="checkbox" name="mimee" value="1"';
	print " checked" if($mimee); print ">MIME<br>\n";
	print '<input type="checkbox" name="datee" value="1"';
	print " checked" if($datee); print ">DATE<br>\n";
	print "</ul>\n<li><strong>動作設定</strong>\n<ul>\n";
	print '<input type="checkbox" name="anothere" value="1"';
	print " checked" if($anothere); print ">ファイルを開く時は別窓で開く<br>\n";
	if($gzipenc_enable){
		print '<input type="checkbox" name="gzipence" value="1"';
		print " checked" if($gzipence); print ">gzip圧縮転送<br>\n";
	}
print <<"ENV";
</ul>
<br>
cookieを利用しています。<br>
上記の設定で「$title」を訪問することができます。<br><br>
<input type="submit" value="登録" class=\"button\">
<input type="reset" value="元に戻す" class=\"button\">
</form>
<a href="$url">戻る</a>
ENV
	&print_footer;
}

# cookie送信
sub send_cookie{
	my $cookie = "crce:$FORM{crce}<>md5e:$FORM{md5e}<>acte:$FORM{acte}<>";
	$cookie .= "commente:$FORM{commente}<>sizee:$FORM{sizee}<>mimee:$FORM{mimee}<>";
	$cookie .= "datee:$FORM{datee}<>anothere:{anothere}<>gzipence:$FORM{gzipence}";

	# cookieの有効期限の計算
	my($sec, $min, $hour, $mday, $month, $year, $wday) = gmtime(time + $cookie_limit_day * 24 * 60 * 60);
	my $youbi = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') [$wday];
	my $tuki = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec') [$month];
	my $year = 1900 + $year;
	my $expire = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT", $youbi, $mday, $tuki, $year, $hour, $min, $sec);

	print "Set-Cookie: env=$cookie; expires=$expire\n";
}

# cookie取得
sub get_cookie{
	my $key, $value, $db, $db2, $env;

	foreach (split(/; /,$ENV{HTTP_COOKIE})){
		($key, $value) = split(/=/);
		$db{$key} = $value;
	}
	$env = $db{env};
	foreach (split(/<>/,$env)){
		($key, $value) = split(/:/);
		$db2{$key} = $value;
	}
	$crce = $db2{crce}; $md5e = $db2{md5e};
	$acte = $db2{acte}; $commente = $db2{commente};
	$sizee = $db2{sizee}; $mimee = $db2{mimee};
	$datee = $db2{datee}; $anothere = $db2{anothere};
	$gzipence = $db2{gzipence};

	if(!$env){ # cookieが取得できなかった場合
		$acte=1; $commente=1; $sizee=1;
		$datee=1; $gzipence=$gzipenc_def;
	}
}

# HELPページ表示
sub help{
	my $target = shift;

	&print_header('HELP');
	if($target eq 'del'){
		print <<"DEL";
		<h3>投稿記事削除パスについて</h3>
		<p>
		投稿者が後々自分の投稿記事を削除したい場合に入力します。<br>
		パスワードが入力されないまま投稿された記事は管理者にしか削除できなくなります。<br>
		パスワードには10文字未満の英数記号を指定できます。
		</p>
DEL
	}
	elsif($target eq 'post'){
		print <<"POST";
		<h3>投稿用パスワードについて</h3>
		<p>
		全ての投稿者は、管理者があらかじめ設定した投稿用パスワードを、"postpass"<br>
		フィールドに入力する必要があります。投稿用パスワードは、サイトの管理者から<br>
		入手してください。
		</p>
POST
	}
	else{
		print "その項目についてのヘルプはありません。";
	}
	print "<a href=\"$url\">戻る</a>\n";
	&print_footer;
	exit;
}

# サーバディスク使用量を計算
sub calc_disk_usage{
	my $sum = 0;
	opendir DIR, "$storedir";
	foreach (readdir DIR){
		next if(/^\.$|^\.\.$/);
		$sum += -s "$storedir/$_";
	}
	closedir DIR;
	return int($sum/1024);
}

# しばカウンターの移植 from minibbsしば改造版
package shiba;

sub html_out {
	if ( $countlevel > 0 ){
		print "$countdateから ";
		&counter;
		print "$countplus　\n";
	}
}

sub counter {
	my $i, $maxcount, $mincount;
	my @count, @filenumber, @sortedcount;

	for( $i=0 ; $i < $countlevel ; $i++){
		open(IN,"$countfile$i$countfiledat");
		$count[$i] = <IN>;
		$filenumber[$count[$i]] = $i;
		close(IN);
	}
	@sortedcount = sort { $a <=> $b; } @count;
	$maxcount = $sortedcount[$countlevel-1];
	$mincount = $sortedcount[0];
	$maxcount++;
	print $maxcount;
	open(OUT,">$countfile$filenumber[$mincount]$countfiledat");
	print OUT $maxcount;
	close(OUT);
}
1;
# end of package shiba

__END__
