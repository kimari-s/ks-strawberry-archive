#!/usr/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (個人用環境設定画面用関数群)
#


###############################################################################
#  環境設定画面表示
###############################################################################

sub prtcustom {

	my ( @reload );
	$reload[$reltype] = 'checked';

	&prthtmlhead ( "$bbstitle 環境設定" );


	my @thumbnail = (0, 0, 0, 0);
	$thumbnail[$CUST{'thumbnail_0'} + $CUST{'thumbnail_1'}*2] = 1;

	print <<EOF;
<h3>$bbstitle 環境設定</h3>
<form method="post" action="$cgiurl">
  <input type="hidden" name="m" value="c">
  <input type="hidden" name="nm" value="$FORM{'m'}">
  <ul>
    <li><strong>表\示設定</strong><br> <br>
    <table border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td>文字色　　　</td>
        <td><input type="text" name="tc" size="7" value="$CC{'text'}"></td>
        <td>　背景色</td>
        <td><input type="text" name="bc" size="7" value="$CC{'bg'}"></td>
      </tr>
      <tr>
        <td>リンク色</td>
        <td><input type="text" name="lc" size="7" value="$CC{'link'}"></td>
        <td>　訪問済リンク色 </td>
        <td><input type="text" name="vc" size="7" value="$CC{'vlink'}"></td>
      </tr>
      <tr>
        <td>引用色</td>
        <td><input type="text" name="qc" size="7" value="$CC{'qmsgc'}"></td>
        <td>　</td>
        <td>　</td>
      </tr>
    </table>
  </ul>
  <ul>
    <li><strong>機能\設定</strong><br><br>
    <label><input type="checkbox" name="tree" value="1" $checked[$CUST{'tree'}]> ツリー表\示</label> <small><font color="#90d0ff">←おすすめ</font></small><br>
    <label><input type="checkbox" name="gzip" value="1" $checked[$CUST{'gzip'}]> gzip圧縮転送</label><br>
    <label><input type="checkbox" name="followwin" value="1" $checked[$CUST{'followwin'}]> フォロー画面を新規ウィンドウで開く</label><br>
    <label><input type="checkbox" name="autoclose" value="1" $checked[$CUST{'autoclose'}]> 書き込み完了画面を自動で閉じる</label><br>
    サムネイルのサイズ<br>
    　<label><input type="radio" name="thumbnail" value="0" $checked[$thumbnail[0]]>表\示しない</label>
    <label><input type="radio" name="thumbnail" value="1" $checked[$thumbnail[1]]>小</label>
    <label><input type="radio" name="thumbnail" value="2" $checked[$thumbnail[2]]>中</label>
    <label><input type="radio" name="thumbnail" value="3" $checked[$thumbnail[3]]>大</label><br>
    <label><input type="checkbox" name="urltrim" value="1" $checked[$CUST{'urltrim'}]> 投稿時に特定URLを自動整形(Amazonなど)</label><br>
    <label><input type="checkbox" name="wide_msg" value="1" $checked[$CUST{'wide_msg'}]> 投稿欄を横に広げる</label><br>
    <label><input type="checkbox" name="affitag" value="1" $checked[$CUST{'affitag'}]> Amazonのリンクにアソ\シエイトタグを付加</label><br>
    <label><input type="checkbox" name="midoku_tl" value="1" $checked[$CUST{'midoku_tl'}]> 未読メッセージがない時にTLを表\示</label><br>
  </ul>
  <ul>
    <li><strong>リンク行</strong><br><br>
    <label><input type="checkbox" name="link_sw" value="1" $checked[$CUST{'link_sw'}]> あやしい関連</label><br>
    <label><input type="checkbox" name="link_comu" value="1" $checked[$CUST{'link_comu'}]> その他コミュニティ関連</label><br>
    <label><input type="checkbox" name="link_news" value="1" $checked[$CUST{'link_news'}]> 情報・ニュース関連</label><br>
    <label><input type="checkbox" name="link_shop" value="1" $checked[$CUST{'link_shop'}]> ショッピング関連</label><br>
    <label><input type="checkbox" name="link_twit" value="1" $checked[$CUST{'link_twit'}]> Twitter関連</label><br>
    <label><input type="checkbox" name="link_ust" value="1" $checked[$CUST{'link_ust'}]> オンアエ中のUSTチャンネル</label><br>
    <label><input type="checkbox" name="link_cust" value="1" $checked[$CUST{'link_cust'}]> カスタムリンク</label><br>
    <div style="margin-left:2em;">
      <textarea rows="5" cols="50" name="customlink" wrap="off">$FORM{'customlink'}</textarea><br>
      (タイトルとURLを改行で区切って交互に)<br>
    </div><label><input type="checkbox" name="link_search" value="1" $checked[$CUST{'link_search'}]> 検索フォーム</label><br>
    <!--<label><input type="checkbox" name="link_topic" value="1" $checked[$CUST{'link_topic'}]> ニューストピック(予\定)</label><br>-->
    <input type="hidden" name="link_topic" value="1">
  </ul>
  <ul>
	<li><strong>NGワード</strong><br><br>
    <label><input type="checkbox" name="nguse" value="1" $checked[$CUST{'nguse'}]> 次のワードを含む投稿を非表\示</label><br>
	<div style="margin-left:2em;">
		<textarea rows="5" cols="50" name="ng" wrap="off">$FORM{'ng'}</textarea><br>
		(正規表\現、改行でOR)<br>
	</div>
    <label><input type="checkbox" name="autong" value="1" $checked[$CUST{'autong'}]> 登録率の高いNGワードを含む投稿を非表\示(予\定)</label><br>
  </ul>
  <ul>
    <br>
    <input type="submit" value="　登　録　">
    <input type="submit" name="cdc" value="Cookie消去">
    <a href="./">戻る</a>
  </ul>

<input type="hidden" name="dummy1" value="1">
<input type="hidden" name="dummy2" value="1">
<input type="hidden" name="dummy3" value="1">
<input type="hidden" name="dummy4" value="1">
<input type="hidden" name="dummy5" value="1">

</form>
</body>
</html>
EOF
}


#  <ul>
#    <li><strong>０件リロード時のメッセージの表\示方法</strong><br> <br>
#    <label><input type="radio" name="rt" value="0" $reload[0]>標準（投稿時刻降順表\示）</label><br>
#    <label><input type="radio" name="rt" value="1" $reload[1]>反転（投稿時刻昇順表\示）</label><br>
#  </ul>


###############################################################################
#  環境設定結果画面表示
###############################################################################

sub setcustom {


	my ( $c, $nm, %alchk, %gzchk );

	$FORM{'custom'} = 1; # 設定項目すべて0の場合に c=0(設定なし：デフォルト) とならないためのダミーの設定項目

	$FORM{'thumbnail_1'} = $FORM{'thumbnail'} / 2 % 2; #割り算の結果は小数になるので % 2 する
	$FORM{'thumbnail_0'} = $FORM{'thumbnail'} % 2;

	#エンコード
	$c = 0;
	for ($i = 0; $i < $#custom+1; $i++) {
		$c += $FORM{$custom[$i]} * 2**$i;
	}
	$c = sprintf("%x", $c);

	if ( $FORM{'nm'} eq 'op' ) {
		$nm = 'm=o&';
	} else {
		$nm = '';
	}

	if (
		( $FORM{'tc'} eq $textc ) &&
		( $FORM{'bc'} eq $bgc ) &&
		( $FORM{'lc'} eq $linkc ) &&
		( $FORM{'vc'} eq $vlinkc ) &&
		( $FORM{'qc'} eq $qmsgc )
	   ) {
			$FORM{'c'} = "$c";
	} else {
		$FORM{'c'} = "$FORM{'tc'}$FORM{'bc'}$FORM{'lc'}$FORM{'vc'}$FORM{'qc'}$c";
	}


	if ( $FORM{'cdc'} ) {
		&putcookie ( $S_cexp - 2 );
	} else {
		&putcookie ( 0 ) if ( $cookie );
	}
	if($nm){
		print "Location: $cgiurl?${nm}\n\n";
	} else {
		print "Location: $cgiurl\n\n";
	}
}


1;


__END__
