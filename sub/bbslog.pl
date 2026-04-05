#!/usr/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (過去ログビューアー)
#
#	※ログ商人さんの Getlog Ver0.3b4.0921 (通常版及び月単位保存ログ対応版)
#	  の改造版です
#


###############################################################################
#  ダウンロード機能使用可否チェック
###############################################################################

sub dlchk {

	my ( $ver, $uos, $isie, $iever, $ismac );

	$ENV{'HTTP_USER_AGENT'} =~ m#^Mozilla/(\S+)\s(.+)#;
	$ver = $1;
	$uos = $2;
	if ( $uos =~ /MSIE (\S)/ ) {
		$isie = 1;
		$iever = $1;
	} else {
		$isie = 0;
	}
	if ( $uos =~ /Mac/ ) {
		$ismac = 1;
	} else {
		$ismac = 0;
	}

	if ( ( $ver >= 4 && !$isie ) || ( $ver >= 4 && $isie && $iever >= 5 && !$ismac ) ) {
		return 1;
	} else {
		return 0;
	}
}


###############################################################################
#  過去ログリスト表示
###############################################################################

sub oldloglist {

	my ( @files, @check, $ftitle, $fsize, $ftime, @fgmtime, $dsptopic, $dspqmsg, $dspgzip, $dspdown );

	if ( $oldlogfmt && $oldlogbtn ) {
		$dspqmsg = <<EOF;
                <INPUT type="checkbox" name="btn" value="checked">引用機能\使用
EOF
	} else {
		$dspqmsg = '&nbsp;';
	}

	if ( $gzip ) {
		$dspgzip = <<EOF;
                <INPUT type="checkbox" name="g" value="checked" $checked[$CUST{'gzip'}]>gzip圧縮転送
EOF
	} else {
		$dspgzip = '&nbsp;';
	}

	if ( &dlchk ) {
		$dspdown = '1">ダウンロード';
	} else {
		$dspdown = '2">全件表示';
	}

	opendir ( DIR, $oldlogfiledir ) || &prterror ( 'ディレクトリが開けませんでした' );
	@files = readdir ( DIR );
	closedir ( DIR );
	@files = sort { $a <=> $b; } @files;

	&prthtmlhead ( "$bbstitle 過去ログ検索・ダウンロード" );
	print <<EOF;
<P align="center"><STRONG><FONT size="+1">$bbstitle 過去ログ一覧</FONT></STRONG></P>

<FORM method="GET" action="$cgiurl">
  <CENTER>
    <TABLE border="0">
      <TR>
        <TD>
          <HR size="2">
          <TABLE border="0" width="100%">
            <TR>
              <TD colspan="5">過去ログ一覧</TD>
            </TR>
EOF

	$check[@files - 1] = 'checked';
	for ( $i = 0 ; $i < @files ; $i++ ) {
		if ( $files[$i] ne '.' && $files[$i] ne '..' ) {
			( $j, $j, $j, $j, $j, $j, $j, $fsize, $j, $ftime, $j, $j, $j ) = stat ( "$oldlogfiledir$files[$i]" );
			@fgmtime = gmtime ( $ftime + 32400 + $difftime );
			@fgmtime[4]++;
			$ftime = sprintf ( "%02d/%02d %02d:%02d:%02d", $fgmtime[4], $fgmtime[3], $fgmtime[2], $fgmtime[1], $fgmtime[0] );
			if ( !$oldlogsavesw ) {
				$files[$i] =~ /(\d\d\d\d)(\d\d)(\d\d)\.(\w+)/;
				$ftitle = "$1/$2/$3";
			} else {
				$files[$i] =~ /(\d\d\d\d)(\d\d)\.(\w+)/;
				$ftitle = "$1/$2";
			}
			if ( $oldlogfmt ) {
				$dsptopic = <<EOF;
              <TD align="right"><FONT size="-1"><A href="$cgiurl?m=l&e=$files[$i]">トピック一覧</A></FONT></TD>
EOF
			} else {
				$dsptopic = '';
			}

			print <<EOF;
            <TR>
              <TD><INPUT type="checkbox" name="chk$files[$i]" value="checked" $check[$i]></TD>
              <TD><A href="$cgiurl?m=g&e=$files[$i]">$ftitle</A></TD>
              <TD align="right"><FONT size="-1">$ftime</FONT></TD>
              <TD align="right"><FONT size="-1">$fsize bytes</FONT></TD>
              $dsptopic
              <TD align="right"><FONT size="-1"><A href="$cgiurl?m=g&e=$files[$i]&dl=$dspdown</A></FONT></TD>
            </TR>
EOF
		}
	}
	print <<EOF;
          </TABLE>
        </TD>
      </TR>
      <TR>
        <TD>
          <HR size="2">

<script langage="JavaScript">
<!--
function allcheck(obj)
{
	for(var i=0; i < obj.elements.length;i++){
		if ( (obj.elements[i].type == "checkbox") && (obj.elements[i].name != 'alp') && (obj.elements[i].name != 'btn') && (obj.elements[i].name != 'j') && (obj.elements[i].name != 'undo') ) {
			obj.elements[i].checked = true;
			obj.elements.undo.checked = false;
		}
	}
}

function undocheck(obj)
{
	for(var i=0; i < obj.elements.length;i++){
		if ( (obj.elements[i].type == "checkbox") && (obj.elements[i].name != 'alp') && (obj.elements[i].name != 'btn') && (obj.elements[i].name != 'j') && (obj.elements[i].name != 'undo') ) {
			obj.elements[i].checked = false;
		}
	}
}

//-->
</script>

          <table><tr><td>
          <label><input onclick=allcheck(this.form) type=checkbox name="all"><font size="-1">すべてをチェック</font></label>
          　<label><input onclick=undocheck(this.form) type=checkbox name="undo"><font size="-1">チェックを外す</font></label>
          </td></tr></table>
          <br>

          <TABLE border="0">
            <TR>
              <TD colspan="3">
                キーワード指定
              </TD>
            </TR>
            <TR>
              <TD colspan="3">
                <INPUT type="text" name="kwd" size="40" maxlength="255">
                <INPUT type="submit" value="   検   索   ">
              </TD>
            </TR>
            <TR>
              <TD>
                <FONT size="-1">時刻指定</FONT>
              </TD>
              <TD>
                <FONT size="-1">論理式</FONT>
              </TD>
              <TD>
                <FONT size="-1">検索対象</FONT>
              </TD>
            </TR>
            <TR>
              <TD><FONT size="-1">
EOF
	if ( !$oldlogsavesw ) {
		print <<EOF;
                <SELECT name="s1" size="1">
                  <OPTION value="0">0</OPTION>
                  <OPTION value="1">1</OPTION>
                  <OPTION value="2">2</OPTION>
                  <OPTION value="3">3</OPTION>
                  <OPTION value="4">4</OPTION>
                  <OPTION value="5">5</OPTION>
                  <OPTION value="6">6</OPTION>
                  <OPTION value="7">7</OPTION>
                  <OPTION value="8">8</OPTION>
                  <OPTION value="9">9</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="11">11</OPTION>
                  <OPTION value="12">12</OPTION>
                  <OPTION value="13">13</OPTION>
                  <OPTION value="14">14</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="16">16</OPTION>
                  <OPTION value="17">17</OPTION>
                  <OPTION value="18">18</OPTION>
                  <OPTION value="19">19</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="21">21</OPTION>
                  <OPTION value="22">22</OPTION>
                  <OPTION value="23">23</OPTION>
                </SELECT> 時
                <SELECT name="e1" size="1">
                  <OPTION value="0">00</OPTION>
                  <OPTION value="5">05</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="25">25</OPTION>
                  <OPTION value="30">30</OPTION>
                  <OPTION value="35">35</OPTION>
                  <OPTION value="40">40</OPTION>
                  <OPTION value="45">45</OPTION>
                  <OPTION value="50">50</OPTION>
                  <OPTION value="55">55</OPTION>
                </SELECT> 分から
                <SELECT name="s2" size="1">
                  <OPTION value="24">24</OPTION>
                  <OPTION value="0">0</OPTION>
                  <OPTION value="1">1</OPTION>
                  <OPTION value="2">2</OPTION>
                  <OPTION value="3">3</OPTION>
                  <OPTION value="4">4</OPTION>
                  <OPTION value="5">5</OPTION>
                  <OPTION value="6">6</OPTION>
                  <OPTION value="7">7</OPTION>
                  <OPTION value="8">8</OPTION>
                  <OPTION value="9">9</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="11">11</OPTION>
                  <OPTION value="12">12</OPTION>
                  <OPTION value="13">13</OPTION>
                  <OPTION value="14">14</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="16">16</OPTION>
                  <OPTION value="17">17</OPTION>
                  <OPTION value="18">18</OPTION>
                  <OPTION value="19">19</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="21">21</OPTION>
                  <OPTION value="22">22</OPTION>
                  <OPTION value="23">23</OPTION>
                </SELECT> 時
                <SELECT name="e2" size="1">
                  <OPTION value="0">00</OPTION>
                  <OPTION value="5">05</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="25">25</OPTION>
                  <OPTION value="30">30</OPTION>
                  <OPTION value="35">35</OPTION>
                  <OPTION value="40">40</OPTION>
                  <OPTION value="45">45</OPTION>
                  <OPTION value="50">50</OPTION>
                  <OPTION value="55">55</OPTION>
                </SELECT> 分まで</FONT>
EOF
	} else {
		print <<EOF;
                <SELECT name="s1" size="1">
                  <OPTION value="1">1</OPTION>
                  <OPTION value="2">2</OPTION>
                  <OPTION value="3">3</OPTION>
                  <OPTION value="4">4</OPTION>
                  <OPTION value="5">5</OPTION>
                  <OPTION value="6">6</OPTION>
                  <OPTION value="7">7</OPTION>
                  <OPTION value="8">8</OPTION>
                  <OPTION value="9">9</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="11">11</OPTION>
                  <OPTION value="12">12</OPTION>
                  <OPTION value="13">13</OPTION>
                  <OPTION value="14">14</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="16">16</OPTION>
                  <OPTION value="17">17</OPTION>
                  <OPTION value="18">18</OPTION>
                  <OPTION value="19">19</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="21">21</OPTION>
                  <OPTION value="22">22</OPTION>
                  <OPTION value="23">23</OPTION>
                  <OPTION value="24">24</OPTION>
                  <OPTION value="25">25</OPTION>
                  <OPTION value="26">26</OPTION>
                  <OPTION value="27">27</OPTION>
                  <OPTION value="28">28</OPTION>
                  <OPTION value="29">29</OPTION>
                  <OPTION value="30">30</OPTION>
                  <OPTION value="31">31</OPTION>
                </SELECT> 日
                <SELECT name="e1" size="1">
                  <OPTION value="0">0</OPTION>
                  <OPTION value="1">1</OPTION>
                  <OPTION value="2">2</OPTION>
                  <OPTION value="3">3</OPTION>
                  <OPTION value="4">4</OPTION>
                  <OPTION value="5">5</OPTION>
                  <OPTION value="6">6</OPTION>
                  <OPTION value="7">7</OPTION>
                  <OPTION value="8">8</OPTION>
                  <OPTION value="9">9</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="11">11</OPTION>
                  <OPTION value="12">12</OPTION>
                  <OPTION value="13">13</OPTION>
                  <OPTION value="14">14</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="16">16</OPTION>
                  <OPTION value="17">17</OPTION>
                  <OPTION value="18">18</OPTION>
                  <OPTION value="19">19</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="21">21</OPTION>
                  <OPTION value="22">22</OPTION>
                  <OPTION value="23">23</OPTION>
                </SELECT> 時 から
                <SELECT name="s2" size="1">
                  <OPTION value="1">1</OPTION>
                  <OPTION value="2">2</OPTION>
                  <OPTION value="3">3</OPTION>
                  <OPTION value="4">4</OPTION>
                  <OPTION value="5">5</OPTION>
                  <OPTION value="6">6</OPTION>
                  <OPTION value="7">7</OPTION>
                  <OPTION value="8">8</OPTION>
                  <OPTION value="9">9</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="11">11</OPTION>
                  <OPTION value="12">12</OPTION>
                  <OPTION value="13">13</OPTION>
                  <OPTION value="14">14</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="16">16</OPTION>
                  <OPTION value="17">17</OPTION>
                  <OPTION value="18">18</OPTION>
                  <OPTION value="19">19</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="21">21</OPTION>
                  <OPTION value="22">22</OPTION>
                  <OPTION value="23">23</OPTION>
                  <OPTION value="24">24</OPTION>
                  <OPTION value="25">25</OPTION>
                  <OPTION value="26">26</OPTION>
                  <OPTION value="27">27</OPTION>
                  <OPTION value="28">28</OPTION>
                  <OPTION value="29">29</OPTION>
                  <OPTION value="30">30</OPTION>
                  <OPTION value="31" selected>31</OPTION>
                </SELECT> 日
                <SELECT name="e2" size="1">
                  <OPTION value="24">24</OPTION>
                  <OPTION value="0">0</OPTION>
                  <OPTION value="1">1</OPTION>
                  <OPTION value="2">2</OPTION>
                  <OPTION value="3">3</OPTION>
                  <OPTION value="4">4</OPTION>
                  <OPTION value="5">5</OPTION>
                  <OPTION value="6">6</OPTION>
                  <OPTION value="7">7</OPTION>
                  <OPTION value="8">8</OPTION>
                  <OPTION value="9">9</OPTION>
                  <OPTION value="10">10</OPTION>
                  <OPTION value="11">11</OPTION>
                  <OPTION value="12">12</OPTION>
                  <OPTION value="13">13</OPTION>
                  <OPTION value="14">14</OPTION>
                  <OPTION value="15">15</OPTION>
                  <OPTION value="16">16</OPTION>
                  <OPTION value="17">17</OPTION>
                  <OPTION value="18">18</OPTION>
                  <OPTION value="19">19</OPTION>
                  <OPTION value="20">20</OPTION>
                  <OPTION value="21">21</OPTION>
                  <OPTION value="22">22</OPTION>
                  <OPTION value="23">23</OPTION>
                </SELECT> 時 まで</FONT>
EOF
	}
	print <<EOF;
              </TD>
              <TD><FONT size="-1">
                <SELECT name="ao">
                  <OPTION value="a">AND検索</OPTION>
                  <OPTION value="o">OR検索</OPTION>
                </SELECT></FONT>
              </TD>
              <TD><FONT size="-1">
                <SELECT name="tt">
                  <OPTION value="a">全文</OPTION>
                  <OPTION value="u">投稿者名</OPTION>
                  <OPTION value="t">題名</OPTION>
                </SELECT></FONT>
              </TD>
            </TR>
          </TABLE>
        </TD>
      </TR>
      <TR>
        <TD>
          <TABLE border="0" width="100%">
            <TR>
              <TD width="50%"><FONT size="-1">
                <INPUT type="checkbox" name="alp" value="checked" checked>大文字小文字同一視<BR>
                $dspqmsg</FONT>
              </TD>
              <TD width="50%"><FONT size="-1">
                <INPUT type="checkbox" name="j" value="checked">jcode.pl使用<BR>
                $dspgzip</FONT>
              </TD>
            </TR>
          </TABLE>
        </TD>
      </TR>
      <TR>
        <TD>
          <HR size="2">
        </TD>
      </TR>
    </TABLE>
  </CENTER>
  <INPUT type="hidden" name="m" value="g">
  <INPUT type="hidden" name="k" value="あ">
  <INPUT type="hidden" name="sv" value="on">
</FORM>
<P align="center"><A href="$cgiurl">掲示板へ</A></P>
<H4 align="right">Getlog Ver0.3b4.0921<BR>
（くずはすくりぷと組み込みバージョン）</H4>
</BODY>
</HTML>
EOF
}


###############################################################################
#  過去ログ表示
###############################################################################

sub prtoldlog {

	my (
	  @oldlog,
	  @prtbuf,
	  @msgline,
	  %MPTR,
	  @keyword,
	  $wmon,
	  $wday,
	  $whor,
	  $wmin,
	  $top,
	  $btm,
	  $hit,
	  $hitcount
	  );

	open ( OLDLOG, "$oldlogfiledir$FORM{'e'}" ) || &prterror ( "$FORM{'e'}を開けませんでした" );
	eval 'flock ( OLDLOG, 1 )';
	seek ( OLDLOG, 0, 0 );
	@oldlog = <OLDLOG>;
	eval 'flock ( OLDLOG, 8 )';
	close ( OLDLOG );

	$hitcount = 0;
	@keyword = split ( /\ /, $FORM{'kwd'} );
	foreach ( @keyword ) {
		$_ = quotemeta $_;
	}

	$FORM{'e'} =~ /.*\.(.*)/;
	if ( $1 =~ /htm/ ) {

		# HTML形式の過去ログ
		if ( $FORM{'sv'} ) {
			print "<H1>$FORM{'e'}</H1><HR>";

			$tmpl_msg =~ s/(\$[A-Za-z0-9\'\{\}]+)/\(.*\)/g;
			$tmpl_msg =~ s/\+/\\\+/g;
			@msgline = split ( /\n/, $tmpl_msg );
			$MPTR{'title'}	= 1;
			$MPTR{'user'}	= 2;
			$MPTR{'wdate'}	= 3;
			$MPTR{'mstart'}	= 5;
			$MPTR{'mend'}	= @msgline - 5;
			$top = 0;
			$btm = 0;

			$k = '';
			for ( $i = 0 ; $i < @oldlog ; $i++ ) {

				if ( $oldlog[$i] =~ /^<!-- \d+ -->/ ) {
					# メッセージブロックの先頭
					$top = $i;
				} elsif ( $oldlog[$i] =~ /^<!-- -->/ ) {
					# メッセージブロックの末尾
					$btm = $i;
				}

				if ( $top > 0 ) {
					#
					#  0 : ターミネーター文字列
					#  1 : 題名
					#  2 : 投稿者名
					#  3 : 投稿時刻
					#  5 ～ @msgline - 5 : メッセージ
					# @msgline - 1 : ターミネーター文字列
					# メッセージブロック内の処理
					if ( $oldlog[$i] =~ /$msgline[$MPTR{'user'}]/ ) {
						# 投稿者
						if ( ( $FORM{'tt'} eq 'u' ) || ( $FORM{'tt'} eq 'a' ) ) {
							$k .= $1
						}
					} elsif ( $oldlog[$i] =~ /^$msgline[$MPTR{'title'}]$/ ) {
						# 題名
						if ( ( $FORM{'tt'} eq 't' ) || ( $FORM{'tt'} eq 'a' ) ) {
							$k .= $2
						}
					} elsif ( $oldlog[$i] =~ /^$msgline[$MPTR{'wdate'}]$/ ) {
						$1 =~ m#\d+/(\d+)/(\d+)\D+(\d+)\D+(\d+)\D+\d+\D+#;
						$wmon = $1;
						$wday = $2;
						$whor = $3;
						$wmin = $4;
						if ( ( $FORM{'s1'} < $whor || ( $FORM{'s1'} == $whor && $FORM{'e1'} <= $wmin ) ) &&
						  ( $FORM{'s2'} > $whor || ( $FORM{'s2'} == $whor && $FORM{'e2'} >= $wmin ) ) ) {
							$hit = 1;
						} else {
							$hit = 0;
						}
					} elsif ( $oldlog[$i] =~ /^$msgline[$MPTR{'mstart'}]$/ ) {
						$msg = $i;
					} elsif ( $oldlog[$i] =~ /^$msgline[$MPTR{'mend'}]$/ ) {
						$msg = 0;
					} elsif ( $msg > 0 ) {
						if ( $FORM{'tt'} eq 'a' ) {
							$k .= $oldlog[$i];
						}
					}

					push ( @prtbuf, $oldlog[$i] );

					if ( $btm > 0 ) {
						if ( $hit > 0 ) {
							$hit = 0;
							$j = 0;
							if ( $FORM{'ao'} eq 'o' ) {			# OR検索
								while ( $j < @keyword && !$hit ) {
									if ( ( $FORM{'alp'} && $k =~ /$keyword[$j]/i ) ||
									  ( $k =~ /$keyword[$j]/ ) ) {
										$hit++;
									} else {
										$j++;
									}
								}
							} else {
								while ( $j < @keyword ) {		# AND検索
									if ( ( $FORM{'alp'} && $k =~ /$keyword[$j]/i ) ||
									  ( $k =~ /$keyword[$j]/ ) ) {
										$hit++;
									}
									$j++;
								}
								if ( $hit != @keyword ) {
									$hit = 0;
								}
							}
							if ( !$FORM{'kwd'} || ( $hit > 0 ) ) {
								$hitcount++;
								print @prtbuf;
							}
						}
						undef @prtbuf;
						$k = '';
						$top = 0;
						$btm = 0;
					}
				}

			} # for

			if ( $FORM{'kwd'} ) {
				if ( $hitcount > 0 ) {
					print "<H3>$hitcount件見つかりました。</H3>";
				} else {
					print "<H3>指定されたキーワードに該当するメッセージは見つかりませんでした。</H3>";
				}
			}

		} else {

			# 全メッセージ表示
			foreach ( @oldlog ) {
				print;
			}
		}

	} else {

		# 新バージョンの過去ログ
		if ( $FORM{'btn'} ) {
			$FORM{'btn'} = 1;
		} else {
			$FORM{'btn'} = 2;
		}

		print "<H1>$FORM{'e'}</H1><HR>";
		$i = 0;
		if ( $FORM{'sv'} ) {
			while ( $i < @oldlog ) {
				&getmessage ( $oldlog[$i] );
				if (
				 ( !$oldlogsavesw &&
				 ( ( $FORM{'s1'} < $hour || ( $FORM{'s1'} == $hour && $FORM{'e1'} <= $min ) ) &&
				   ( $FORM{'s2'} > $hour || ( $FORM{'s2'} == $hour && $FORM{'e2'} >= $min ) ) ) ) ||
				 ( $oldlogsavesw &&
				 ( ( $FORM{'s1'} < $mday || ( $FORM{'s1'} == $mday && $FORM{'e1'} <= $hour ) ) &&
				   ( $FORM{'s2'} > $mday || ( $FORM{'s2'} == $mday && $FORM{'e2'} >= $hour ) ) ) ) ) {
					if ( !$FORM{'kwd'} ) {
						print &prtmessage ( $FORM{'btn'}, "$FORM{'e'}" );
					} else {
						$j = 0;
						$hit = 0;
						$k = '';
						if ( ( $FORM{'tt'} eq 'u' ) || ( $FORM{'tt'} eq 'a' ) ) {
							$k .= $user;
						}
						if ( ( $FORM{'tt'} eq 't' ) || ( $FORM{'tt'} eq 'a' ) ) {
							$k .= $title;
						}
						if ( $FORM{'tt'} eq 'a' ) {
							$k .= $msg;
						}
						if ( $FORM{'ao'} eq 'o' ) {
							while ( $j < @keyword && !$hit ) {
								if ( ( $FORM{'alp'} && $k =~ /$keyword[$j]/i ) ||
								  ( $k =~ /$keyword[$j]/ ) ) {
									$hit++;
								} else {
									$j++;
								}
							}
						} else {
							while ( $j < @keyword ) {
								if ( ( $FORM{'alp'} && $k =~ /$keyword[$j]/i ) ||
								  ( $k =~ /$keyword[$j]/ ) ) {
									$hit++;
								}
								$j++;
							}
							if ( $hit != @keyword ) {
								$hit = 0;
							}
						}
						if ( $hit > 0 ) {
							print &prtmessage ( $FORM{'btn'} );
							$hitcount++;
						}
					}
				}
				$i++;
			} # while

			if ( $FORM{'kwd'} ) {
				if ( $hitcount > 0 ) {
					print "<H3>$hitcount件見つかりました。</H3>";
				} else {
					print "<H3>指定されたキーワードに該当するメッセージは見つかりませんでした。</H3>";
				}
			}

		} else {
			# 全メッセージ表示
			while ( $i < @oldlog ) {
				&getmessage ( $oldlog[$i] );
				print &prtmessage ( $FORM{'btn'} );
				$i++;
			}
		}
		print "\n</BODY>\n</HTML>\n";
	}
}


###############################################################################
#  Getlog メイン処理
###############################################################################

sub getlog {

	my ( $sendfile, $fcount );

	$FORM{'e'} =~ /^([\w.]*)$/;
	$FORM{'e'} = $1;

	if ( $FORM{'e'} || $FORM{'sv'} ) {
		$FORM{'kwd'} =~ s/\0/\,/g;

		if ( !$FORM{'e'} ) {

			&prthtmlhead ( "$bbstitle 過去ログ" );
			$fcount = 0;
			foreach ( sort keys %FORM ) {
				if ( $_ =~ /^chk([\w.]+)$/ && $FORM{$_} eq 'checked' ) {
					$FORM{'e'} = $1;
					&prtoldlog;
					$fcount++;
				}
			}
			if ( !$fcount ) {
				&prterror ( '表示するファイルを指定してください。' );
			}

		} else {

			if ( $FORM{'dl'} eq '1' ) {
				$sendfile = $FORM{'e'};
				$sendfile =~ /(.+\.)(.+)/;
				if ( $2 =~ /dat/ ) {
					$sendfile =~ s/dat/html/;
				}
				print <<EOF;
Content-type: application/octet-stream
Content-Disposition: attachment; filename="$sendfile"

<HTML>
<HEAD>
<TITLE>$bbstitle 過去ログ</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</HEAD>

$body
EOF
			} else {
				&prthtmlhead ( "$bbstitle 過去ログ $FORM{'e'}" );
			}
			&prtoldlog;
		}

	} else {
		&oldloglist;
	}
}



1;


__END__
