#!/usr/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (管理ツール)
#

###############################################################################
#  メッセージ削除モードメイン画面表示
###############################################################################

sub msglist {

	my @msgline;

	&prthtmlhead ( 'くずはすくりぷと メッセージ削除モード' );
	print <<EOF;
<center>
<form method="post" action="$cgiurl">
<input type="hidden" name="$adminkey" value="$FORM{$adminkey}">
<input type="hidden" name="ad" value="kx">
<h3 align="center">くずはすくりぷと メッセージ削除モード</h3>
<table  border="1">
  <tr>
    <th nowrap>削除</th>
    <th nowrap>投稿日</th>
    <th nowrap>題名</th>
    <th nowrap>投稿者</th>
    <th nowrap>host</th>
    <th nowrap>bbq</th>
    <th nowrap>内容（一部）</th>
  </tr>
EOF

	&loadmessage;
	for ( $i = 0 ; $i < @logdata ; $i++ ) {
		&getmessage ( $logdata[$i] );
#		@msgline = split ( /\r/, $msg );
#		$msg = $msgline[0];
		# 引用部分の消去
		$msg =~ s|(&gt; .*?\r)||g;
		# 参考の消去
		$msg =~ s|<a href="\S+">参考：(\S+)</a>||gi;


		#BBQ
#		my $bbq;
#		my $IP = join(".", unpack("C4", gethostbyname($phost)));;
#
#		if(!$bbq{$IP}){
#			my @DNSBL_list = qw|niku.2ch.net http.dnsbl.sorbs.net bbx.2ch.net all.rbl.jp zen.spamhaus.org b.barracudacentral.org|;
#			for my $DNSBL_host (@DNSBL_list){
#			    my $host = join ".", reverse (split /\Q.\E/, $IP) , $DNSBL_host;
#		    	my $result = join ".", unpack 'C*', gethostbyname $host;
#			    if ($result =~ /^127\./){
#			        # スパム判定に引っかかった時の処理
#			        $bbq{$IP} .= "$DNSBL_host ";
#			    }
#			}
#			if(!$bbq{$IP}){
#				$bbq{$IP} = "no";
#			}
#		}


		print <<EOF;
  <tr>
    <td align="center" nowrap><input type="checkbox" name="id$postid" value="checked"></td>
    <td nowrap><a href="$cgiurl\?m=f&s=$postid" target="_blank">$wdate</a></td>
    <td nowrap>$title</td>
    <td nowrap>$user</td>
    <td nowrap>$phost</td>
    <td nowrap>$bbq{$IP}</td>
    <td nowrap>$msg</td>
  </tr>
EOF
	}

	print <<EOF;
</table>
<input type="submit" value="削除実行">
</form>
<form method="post" action="$cgiurl">
<input type="hidden" name="$adminkey" value="$FORM{$adminkey}">
<input type="hidden" name="ad" value="tp">
<input type="submit" value="終了">
</form>
</center>
</body>
</html>
EOF
}


###############################################################################
#  メッセージ削除
###############################################################################

sub msgdel {

	my ( @newlog, @newoldlog, $logitems, $oldlogitems );

	open ( FLOG, "+<$logfilename" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( FLOG, 2 )';
	seek ( FLOG, 0, 0 );
	@logdata = <FLOG>;

	for ( $i = 0 ; $i < $logsave ; $i++ ) {
		@logitems = split ( /\,/, $logdata[$i] );
		if ( $FORM{"id$logitems[1]"} eq 'checked' ) {

			if ( $oldlogfiledir && $oldlogfmt ) {
				&getnowdate ( $logitems[0] );
				if ( !$oldlogsavesw ) {
					$oldlogfilename = sprintf ( "%s/%d%02d%02d.dat",
					  $oldlogfiledir, $year, $mon, $mday );
				} else {
					$oldlogfilename = sprintf ( "%s%d%02d.dat",
					  $oldlogfiledir, $year, $mon );
				}
				open ( CLOG, "+<$oldlogfilename" ) || &prterror ( '過去ログ読み込みに失敗しました' );
				eval 'flock ( CLOG, 2 )';
				seek ( CLOG, 0, 0 );
				@oldlogdata = <CLOG>;

				undef @newoldlog;
				for ( $j = 0 ; $j < $logsave ; $j++ ) {
					@oldlogitems = split ( /\,/, $oldlogdata[$j] );
					if ( $logitems[1] ne $oldlogitems[1] ) {
						$newoldlog[$j] = $oldlogdata[$j];
					}
				}

				$oldstream = select ( CLOG );
				$| = 1;
				seek ( CLOG, 0, 0 );
				truncate ( CLOG, 0 );
				print CLOG @newoldlog;
				eval 'flock ( CLOG, 8 )';
				close ( CLOG );
				select ( $oldstream );
			}

		} else {
			$newlog[$i] = $logdata[$i];
		}
	}

	$oldstream = select ( FLOG );
	$| = 1;
	seek ( FLOG, 0, 0 );
	truncate ( FLOG, 0 );
	print FLOG @newlog;
	eval 'flock ( FLOG, 8 )';
	close ( FLOG );
	select ( $oldstream );
}


###############################################################################
#  パスワード設定画面表示
###############################################################################

sub setpass {

	&prthtmlhead ( 'くずはすくりぷと パスワード設定画面' );
	print <<EOF;
<form method="post" action="$cgiurl">
<input type="hidden" name="ad" value="ps">
<input type="hidden" name="$adminkey" value="1">
<h2 align="center">くずはすくりぷと パスワード設定画面</h2>
<hr>
<center>
<table >
  <tr>
    <td>
      <font size="+1">パスワード設定を行います。</font><br>
      これから掲示板の管理で使用する「管理用パスワード」を入力してください。
    </td>
  </tr>
</table>
<br>
<table  border="2" cellspacing="4">
  <tr>
    <td>管理用パスワード</td>
    <td><input size="30" type="text" name="ps" maxlength="127"></td>
  </tr>
  <tr>
    <td colspan="2"><font size="-1">
      ここで入力するパスワードは、管理人名での投稿、管理モードの認証の際に使用します。
      </font>
    </td>
  </tr>
</table>
<br>
<input type="submit" value="設定">　<input type="reset" value="リセット">
</center>
</form>
</body>
</html>
EOF
}


###############################################################################
#  暗号化テスト
###############################################################################

sub MD5test {

	my $tpass = 'ABCDE';
	my $tsalt = 'r7';
	my ( $cpass, $rpass, $slen );

	$MD5salt = '$1$';
	$cpass = crypt ( $tpass, "$MD5salt$tsalt" );
	if ( $cpass =~ /^\$1\$/ ) {
		$slen = 5;
	} else {
		$slen = 2;
	}
	$rpass = crypt ( $tpass, substr ( $cpass, 0, $slen ) );
	if ( ( $slen == 5 ) && ( $cpass eq $rpass ) && $cpass ) {
		return 2;
	} else {
		$cpass = crypt ( $tpass, "$tsalt" );
		$rpass = crypt ( $tpass, substr ( $cpass, 0, 2 ) );
		if ( ( $cpass eq $rpass ) && $cpass ) {
			return 1;
		} else {
			return 0;
		}
	}
}


###############################################################################
#  パスワード生成
###############################################################################

sub makepass {

	my $pass = $_[0];
	my ( $salt, $ctype, $cpass );
	my @saltlist = ( '0'..'9', 'A'..'Z', 'a'..'z' );

	if ( length ( $pass ) > 5 ) {
		$ctype = &MD5test;
		if ( $ctype > 0 ) {
			srand ( time ^ ( $$ + ( $$ << 15 ) ) );
			$salt = splice ( @saltlist, int ( rand ( @saltlist ) ), 1 ) .
			  splice ( @saltlist, int ( rand ( @saltlist ) ), 1 );

			if ( $ctype == 2 ) {
				$cpass = crypt ( $pass, "\$1\$$salt" );
			} else {
				$cpass = crypt ( $pass, "$salt" );
			}
		} else {
			$cpass = $pass;
		}
		return $cpass;
	} else {
		&prterror ( 'パスワードが短すぎます。６桁以上の文字列を入力してください。' );
	}
}


###############################################################################
#  パスワード表示
###############################################################################

sub prtpass {

	my $cpass = &makepass ( $FORM{'ps'} );
	&prthtmlhead ( 'パスワード' );
	print <<EOF;
<h2 align="center">くずはすくりぷと パスワード設定画面</h2>
<hr>
<form>
<center>
<table >
  <tr>
    <td>
      <font size="+1">暗号化パスワードを生成しました。</font><br>
      掲示板スクリプト本体の所定の位置に、下記の暗号化パスワード文字列をコピーしてください。
    </td>
  </tr>
</table>
<br>
<table  border="2" cellspacing="4">
  <tr>
    <td>管理用パスワード</td>
    <td><input size="50" type="text" name="dummy" value="$cpass" readonly></td>
  </tr>
</table>
</form>
</body>
</html>
EOF
}


###############################################################################
#  ログ表示
###############################################################################

sub logprint {

	&loadmessage;
	print "Content-Type: text/plain\n\n";

	print @logdata;
}


###############################################################################
#  管理メニュー画面表示
###############################################################################

sub adminmenu {

	&prthtmlhead ( 'くずはすくりぷと 管理メニュー' );
	print <<EOF;
<h2 align="center">くずはすくりぷと 管理メニュー</h2>
<hr>
<center>
<form method="post" action="$cgiurl">
<input type="hidden" name="ad" value="kl">
<input type="hidden" name="$adminkey" value="$FORM{$adminkey}">
<input type="submit" value="メッセージ削除">
</form>
<form method="post" action="$cgiurl">
<input type="hidden" name="ad" value="rp">
<input type="hidden" name="$adminkey" value="$FORM{$adminkey}">
<input type="submit" value="暗号化パスワード再生成">
</form>
<form method="post" action="$cgiurl">
<input type="hidden" name="ad" value="lv">
<input type="hidden" name="$adminkey" value="$FORM{$adminkey}">
<input type="submit" value="ログ閲覧">
</form>
<form method="post" action="$cgiurl">
<input type="submit" value="終了">
</form>
</center>
</body>
</html>
EOF
}


###############################################################################
#  管理モードメイン処理
###############################################################################

sub adminmain {

#	if ( !$FORM{'ad'} || $FORM{'ad'} eq 'tp' ) {
#		&adminmenu;
#	} elsif ( $FORM{'ad'} eq 'ps' ) {
#		if ( $FORM{'ps'} ) {
#			&prtpass;
#		} else {
#			&prterror ( 'パスワードが入力されていません。' );
#		}
#	} else {
#		if ( &chkpasswd ) {
#			if ( $FORM{'ad'} eq 'rp' ) {
#				&setpass;
#			} elsif ( $FORM{'ad'} eq 'kl' ) {
#				&msglist;
#			} elsif ( $FORM{'ad'} eq 'kx' ) {
#				&msgdel;
#				&msglist;
#			} elsif ( $FORM{'ad'} eq 'lv' ) {
#				&logprint;
#			}
#		} else {
#			&prterror ( '認証に失敗しました。' );
#		}
#	}

	if ( $FORM{'ad'} eq 'ps' ) {
		if ( $FORM{'ps'} ) {
			&prtpass;
		} else {
			&prterror ( 'パスワードが入力されていません。' );
		}
	} elsif ( &chkpasswd ) {
		if ( !$FORM{'ad'} || $FORM{'ad'} eq 'tp' ) {
			&adminmenu;
		} elsif ( $FORM{'ad'} eq 'rp' ) {
			&setpass;
		} elsif ( $FORM{'ad'} eq 'kl' ) {
			&msglist;
		} elsif ( $FORM{'ad'} eq 'kx' ) {
			&msgdel;
			&msglist;
		} elsif ( $FORM{'ad'} eq 'lv' ) {
			&logprint;
		}
	} else {
		&prthtmlhead ( '管理者ログイン画面' );
		print <<EOF;
<form method="post" action="$cgiurl">
<h2 align="center">管理者ログイン画面</h2>
<hr>
<center>
<table  border="2" cellspacing="4">
  <tr>
    <td>管理用パスワード</td>
    <td><input size="30"  type=password name="$adminkey" maxlength="127"></td>
  </tr>
</table>
<br>
<input type="submit" value="ログイン">
</center>
</form>
</body>
</html>
EOF
	}
}

1;
