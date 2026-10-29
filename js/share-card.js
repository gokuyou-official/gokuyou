// 金言を1枚の画像にしてシェアする（黒と金のカード）
(function () {
  var SITE = 'gokuyou-official.github.io/gokuyou';

  function wrap(ctx, text, maxWidth) {
    var lines = [], line = '';
    for (var i = 0; i < text.length; i++) {
      var ch = text[i], test = line + ch;
      if (ctx.measureText(test).width > maxWidth && line) {
        // 句読点や閉じかっこは行頭に置かない
        if ('、。」』）!?！？ー…'.indexOf(ch) >= 0) { line = test; continue; }
        lines.push(line); line = ch;
      } else { line = test; }
    }
    if (line) lines.push(line);
    return lines;
  }

  function drawCard(quote, author) {
    var W = 1080, H = 1080;
    var c = document.createElement('canvas'); c.width = W; c.height = H;
    var x = c.getContext('2d');
    var g = x.createRadialGradient(W / 2, 0, 50, W / 2, 200, 1100);
    g.addColorStop(0, '#2a241b'); g.addColorStop(1, '#121110');
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = '#c9a35a'; x.lineWidth = 2; x.strokeRect(56, 56, W - 112, H - 112);
    var serif = '"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP","Noto Serif CJK JP",serif';
    var sans = '"Hiragino Kaku Gothic ProN","Noto Sans JP","Noto Sans CJK JP",sans-serif';
    x.fillStyle = '#c9a35a'; x.font = '600 30px ' + sans; x.textAlign = 'center';
    x.fillText('敗北者の金言', W / 2, 170);
    x.fillRect(W / 2 - 24, 200, 48, 2);
    var size = quote.length > 40 ? 50 : quote.length > 24 ? 60 : 70;
    x.font = '600 ' + size + 'px ' + serif; x.fillStyle = '#f3ead6';
    var lines = wrap(x, '「' + quote + '」', W - 240);
    var lh = size * 1.7, top = H / 2 - (lines.length - 1) * lh / 2 + size / 3;
    lines.forEach(function (l, i) { x.fillText(l, W / 2, top + i * lh); });
    if (author) { x.font = '400 30px ' + sans; x.fillStyle = '#b8ad98'; x.fillText(author, W / 2, H - 230); }
    x.font = '600 34px ' + sans; x.fillStyle = '#e2c27f'; x.fillText('御供養', W / 2, H - 150);
    x.font = '400 24px ' + sans; x.fillStyle = '#8f8574'; x.fillText(SITE, W / 2, H - 110);
    return c;
  }

  window.shareKingenImage = function (quote, author) {
    var c = drawCard(quote, author);
    c.toBlob(function (blob) {
      var file = new File([blob], 'gokuyou-kingen.png', { type: 'image/png' });
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file], text: '「' + quote + '」 #御供養' }).catch(function () {});
      } else {
        var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
        a.download = 'gokuyou-kingen.png'; document.body.appendChild(a); a.click(); a.remove();
      }
      if (typeof gtag === 'function') gtag('event', 'share', { method: 'image', item_id: 'kingen' });
    }, 'image/png');
  };

  // 既存の金言カードのシェア欄に「画像で保存」ボタンを足す
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.share-btns').forEach(function (box) {
      if (box.dataset.img) return; box.dataset.img = '1';
      var tw = box.querySelector('.share-tw'); if (!tw) return;
      var m = (tw.getAttribute('onclick') || '').match(/shareTwitter\('(.*)'\)/); if (!m) return;
      var quote = m[1];
      var card = box.parentElement;
      var nameEl = card && card.querySelector('.kingen-author-name, .kingen-author');
      var author = nameEl ? nameEl.textContent.trim() : '';
      var b = document.createElement('button');
      b.className = 'share-btn'; b.type = 'button'; b.textContent = '画像';
      b.style.cssText = 'background:#121110;color:#e2c27f;border:1px solid #c9a35a;';
      b.addEventListener('click', function () { window.shareKingenImage(quote, author); });
      box.appendChild(b);
    });
  });
})();
