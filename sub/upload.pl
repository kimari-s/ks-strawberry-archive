#!/usr/bin/perl

sub upload
{


	# このスクリプトのURL(HTTP)
# 解説：このままの設定で動作しない場合は正確なURL(URI)を入力してください。
$url = "http://$ENV{SERVER_NAME}$ENV{SCRIPT_NAME}";
$url =~ s/index.cgi//;

# アップロードデータの格納先ディレクトリ
# 推奨パーミッション：700->777
# 解説：FTPモードの場合も作業用に使うので必ず設定してください。
$storedir = './up/s/';

# アップロードデータの格納先ディレクトリURL
# 解説：URLリスト作成・画像閲覧モードで使います。
# FTPモード使用の場合は正しく設定しておかないと
# 訪問者がファイルをダウンロードできなくなります。
$storeurl = "$url".'up/s/';

# ログファイル
# 推奨パーミッション：600->666
$log_file = './up/sourcelog.txt';

# 投稿処理時の排他制御用lockファイル
# 解説：空のファイルを用意してください。
# 推奨パーミッション：600->604  (要するにCGIから読めるだけでOKです。)
$up_lockfile = './up/upload.lock';


# ########################################
# もう少し細かい設定
# ########################################


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

# ログの最大件数
$max = 20000;

# ファイルサイズ制限(キロバイト単位)
$limitk = 50 * 1024;

# URLリスト出力フォーム
# 1:表示する 0:表示しない
$listform_enable = 0;

# ロックファイル
# 1:使用する 0:使用しない
$lock = 0;

# ロックファイルのディレクトリ+ファイル名
# 解説：ロック用ディレクトリ 推奨パーミッション700->777
$lockfile = './up/lock/lock-file.lock';

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

# crcチェックサム算出
# 1:使用する 0:使用しない
# 解説：大炸裂氏作のdcrc、またはcrc.plを利用してファイルのチェックサムを記録します。
# dcrcはhttp://daisakuretsu.hypermart.net/dcrc.htmlから入手できます。
# ソースファイルを入手後、telnetクライアントやtelnet.cgiを使ってコンパイルしてください。
# crc.plはhttp://zurubon.strange-x.com/uploader/crc_pl.txtから入手できます。
#
$dcrc_enable = 0;

# dcrcの場所
$dcrc_path = './up/dcrc';

# Perlでcrcチェックサム算出
# 解説：拙作のcrc.plを使ってCRCチェックサムを算出します。
# ※dcrcで計算した場合に比べて処理スピードがかなり落ちます。
#
# crc.plを使ってCRC計算をする場合はcrc.plへのパスを設定してください。
$crc_pl = './up/crc.pl';

# md5チェックサム算出
# 1:使用する 0:使用しない
# 解説：サーバー側のmd5コマンドまたはmd5.plを利用してファイルのチェックサムを記録します。
# md5.plはhttp://zurubon.strange-x.com/uploader/md5_pl.txtから入手できます。
# ※アップロード時に記録
$md5_enable = 0;

# md5コマンドのサーバーパス
$md5_path = '/upload/sbin/md5';

# md5.plへのサーバーパス
# なるべくサーバー側のmd5コマンドが使えない場合の代替処置としてmd5.plを使うようにしてください。
# ※md5コマンドで計算した場合に比べてかなり処理速度が落ちます。
#
# md5.plを使ってMD5計算をする場合はmd5.plへのパスを設定してください。
$md5_pl = './up/md5.pl';

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

# 連続投稿間隔の制限
# 1:制限する 0:制限しない
$continue_limit = 0;

# 連続投稿制限用データファイル
# 推奨パーミッション：600->666
$continue_file = './up/continue.cgi';

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
$denylist = './up/deny.cgi';

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




	# アクセス制限
	my $host = $ENV{REMOTE_ADDR};
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
#		if($continue_limit){
#			$cont_val = &continue_check('check');
#			&error('連続投稿制限中','時間を置いてやり直してください') if(!$cont_val);
#		}
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


		$comment = $FORM{'v'};
		# 引用部分の消去
		$comment =~ s|(&gt; .*?\r)||g;
		# 空行の消去
		$comment =~ s|^\r$||g;
		# 参考の消去
		$comment =~ s|<a href="\S+">参考：(\S+)</a>||gi;

		($comment."\r") =~ /(.+?)\r/;
		$comment = $1;

		$comment = "<a href=\"$url?m=f&s=$newpostid\">&gt; $comment</a>";

		&write if($comment);
		close (UPLOCK); # 排他処理の終わり
		&readlog;

		#後ろに挿入
#		if($FORM{'v'} =~ /\r\r<a href="\S+">参考：\S+<\/a>$/){
#			$FORM{'v'} =~ s|(\r\r<a href="\S+">参考：(\S+)</a>)$|\r$storeurl$prefix$id.$type$1|gi;
#		}else{
#			$FORM{'v'} .= "\r$storeurl$prefix$id.$type";
#		}

		#引用のあと、本文の前に挿入
		if ( $FORM{'v'} =~ /&gt; .*/ ) {
			$FORM{'v'} =~ s|((&gt; .*?\r)*\r?)(.*)|$1$storeurl$prefix$id.$type\r$3|s;
		} else {
			$FORM{'v'} = "$storeurl$prefix$id.$type\r$FORM{'v'}";
		}
	}

	# ロックファイル削除
	unlink($lockfile) if($lock);



}



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
	my $size;

	return if($ENV{CONTENT_LENGTH} > $limitk*1024);
	return unless($ENV{HTTP_REFERER} =~/$url/);


	use CGI;
	$query = new CGI;

	$ctype = $query->uploadInfo($FORM{'filedata'})->{'Content-Type'};

	while($bytesread = read($filename, $buffer, 2048)) {
		$file .= $buffer;
	}

	# ファイル名の取得
	$filename = $query->param('filedata');

	# MIMEタイプの取得
	$ctype = $query->uploadInfo($filename)->{'Content-Type'};

	# ファイルの受け取り
	while($bytesread = read($filename, $buffer, 2048)) {
		$file .= $buffer;
	}

	# ファイルの保存
	open(OUT, ">$storedir$uniq_name") or die("ファイルの保存に失敗しました。");
	binmode(OUT);
	print(OUT $file);
	close(OUT);




#	binmode(STDIN);
#	while(<STDIN>){
#		last if(/^\r\n/);
#		$bound = $_ if(/^--/);
#		$rext = $1 if(/^Content-Disposition:.*filename="(.*)"/i);
#		$ctype = $1 if(/^Content-Type:(.*)/i);
#	}
#
#	$rext =~ s/.*\.//go;
#	$ctype =~ s/(^\s|\s$)//go;
#	$bound=~s/\r\n//;
#

	foreach $mext (@MEXT)
	{
		if($ctype =~ /$MIME{$mext}/)
		{
			next if (defined($EMIM{$mext}) && $ctype =~ /$EMIM{$mext}/);
			$type = $mext;
		}
	}

#	if($rext ne "")
#	{
#		$rextl = "\L$rext\E";
#		foreach $ext (@sup)
#		{
#			if("\L$ext\E" eq $rextl)
#			 {
#				$type = $ext;
#				last;
#			}
#		}
#	}
#
#	$type = 'xxx' if($type eq '');
#	$ctype = "www/none" unless $ctype;
#	$ctype = &htmlenc($ctype);
#
#	open(DB,">$storedir$uniq_name");
#	binmode(DB);
#	$dbuf = "";
#		while(<STDIN>){
#			last if($_=~/^$bound/);
#			print DB $dbuf;
#			$dbuf = $_;
#		}
#	$dbuf =~ s/\r\n$//;
#	print DB $dbuf;
#	close (DB);

	$size = -s "$storedir$uniq_name";
	ruturn if(!$size); #sizeが0ならリロード

#	#$ext = &post_decode;
#	$ext = "ext";
#
#	if($ext ne 'ext'){
#		if(!grep($ext eq $_, @sup)){
#			unlink("$storedir$uniq_name");
#			&error('投稿データエラー', '許可されていない拡張子です。');
#		}
#		$type = $ext;
#	}
#
#	if($dcrc_enable){ # CRC計算
#		if(-f $crc_pl){
#			require $crc_pl;
#			$dcrc = &crc::crc16("$storedir$uniq_name");
#		}
#		else{
#			$dcrc = &dcrc("$storedir$uniq_name");
#		}
#	}
#	if($md5_enable){ # MD5計算
#		if(-f $md5_pl){
#			require $md5_pl;
#			$md5 = &md5::from_file("$storedir$uniq_name");
#		}
#		else{
#			$md5 = &md5("$storedir$uniq_name");
#		}
#	}



	#&error('投稿エラー','コメントが長すぎます') if(length($comment) > $comment_max);
	#$comment =~ s/(https?|ftp|news)(:.*)([a-z]|[A-Z]|[0-9]|\/)/<a href="$1$2$3">$1$2$3<\/a>/g if($autolink);

#	if($del_enable){
#		$input_pass = &post_decode;
#		$pass = crypt($input_pass, $del_seed);
#		$pass = '*' if($input_pass eq '');
#		&error('投稿エラー','パスワードが長すぎます') if(length($input_pass) > 10);
#		if($postpass_enable){
#			&error('投稿用パスワードが違います','投稿用パスワードを管理者から入手してください。') if(!&postpass);
#		}
#	}
#	elsif($postpass_enable){
#		&error('投稿用パスワードが違います','投稿用パスワードを管理者から入手してください。') if(!&postpass);
#	}

#	&continue_check('add') if($continue_limit);
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

# エラー出力
sub error{
	print <<"ERROR";
Content-type: text/html

<html>
<head>
<title>Notice!</title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Pragma" content="no-cache">
</head>
<body>
<hr>
<center>
<strong>$_[0]</strong><br>
<p>$_[1]</p>
<a href="$url">Return</a>
</center>
</body>
</html>
ERROR
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

1;