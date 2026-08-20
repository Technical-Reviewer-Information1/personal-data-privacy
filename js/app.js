(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const NS = 'http://www.w3.org/2000/svg';

  /* ===== STEP 2 ===== */
  const COMBO = [
    { t: '性別', n: 2 }, { t: '生年月日', n: 25000 }, { t: '郵便番号', n: 120000 },
    { t: '通っている高校', n: 4800 }, { t: '部活動', n: 20 }, { t: '好きな音楽グループ', n: 200 }
  ];
  let picked = {};
  function drawCombo() {
    $('comboBox').innerHTML = COMBO.map((c, i) =>
      '<label class="' + (picked[i] ? 'on' : '') + '"><input type="checkbox" data-i="' + i + '"' + (picked[i] ? ' checked' : '') + '>' + c.t + '</label>').join('');
    $('comboBox').querySelectorAll('input').forEach(x => x.addEventListener('change', () => { picked[+x.dataset.i] = x.checked; drawCombo(); }));
    const POP = 125000000;
    let div = 1;
    COMBO.forEach((c, i) => { if (picked[i]) div *= c.n; });
    const cand = Math.max(1, POP / div);
    const risk = Math.min(100, Math.max(0, (1 - Math.log10(cand) / Math.log10(POP)) * 100));
    $('riskBar').style.width = risk + '%';
    const n = $('comboNote');
    const cnt = Object.values(picked).filter(Boolean).length;
    n.className = 'note ' + (cand <= 1.5 ? 'ng' : cand < 100 ? 'warn' : 'info');
    n.innerHTML = cnt === 0
      ? '項目をチェックすると、日本の人口（約1億2500万人）のうち何人にしぼられるかを、おおよそで計算します。'
      : 'チェックした ' + cnt + ' 項目の組合せで、<strong>およそ ' +
        (cand < 2 ? '1人' : Math.round(cand).toLocaleString() + ' 人') + '</strong>にまでしぼりこめます。' +
        (cand <= 1.5
          ? '<br><strong>ここまで来ると事実上、個人が特定できます。</strong>単体では個人情報でなくても、組み合わせれば個人情報になるのはこのためです。'
          : '<br>もう少しチェックを増やしてみましょう。（この人数は考え方を示すためのおおよその計算です）');
  }

  /* ===== STEP 3 ===== */
  const HOTS = [
    { x: 6, y: 8, w: 22, h: 16, t: '背景の建物・看板', d: '学校名や店名が写っていると、行動範囲が分かります。' },
    { x: 68, y: 12, w: 26, h: 14, t: '電柱・住所表示', d: '住所表示板や電柱の番号から、場所が特定できます。' },
    { x: 40, y: 30, w: 14, h: 10, t: '瞳への映り込み', d: '瞳に映った景色から場所を特定された事例があります。' },
    { x: 30, y: 62, w: 24, h: 14, t: '制服・持ち物', d: '制服やバッグから学校が分かることがあります。' },
    { x: 70, y: 66, w: 24, h: 16, t: '写真の位置情報（Exif）', d: '撮影時にGPSの位置情報が埋め込まれていることがあります。投稿前に確認しましょう。' }
  ];
  let found = {};
  function drawPhoto() {
    const svg = '<svg viewBox="0 0 100 90" role="img" aria-label="投稿しようとしている写真のイメージ">' +
      '<rect x="0" y="0" width="100" height="90" fill="#dfe6ec"/>' +
      '<rect x="0" y="58" width="100" height="32" fill="#c9d4dd"/>' +
      '<rect x="4" y="6" width="26" height="22" fill="#a9b8c4"/><rect x="8" y="12" width="6" height="6" fill="#eef1f4"/><rect x="18" y="12" width="6" height="6" fill="#eef1f4"/>' +
      '<rect x="72" y="10" width="4" height="34" fill="#9aa7b2"/><rect x="70" y="14" width="9" height="6" fill="#f1f3f5"/>' +
      '<circle cx="47" cy="34" r="11" fill="#e8d5c0"/><rect x="38" y="46" width="18" height="26" rx="3" fill="#3a4a5c"/>' +
      '<circle cx="43" cy="33" r="2" fill="#2b3440"/><circle cx="51" cy="33" r="2" fill="#2b3440"/>' +
      '<rect x="74" y="70" width="20" height="12" rx="2" fill="#8e9aa6"/>' +
      '</svg>';
    $('photoBox').innerHTML = svg + HOTS.map((h, i) =>
      '<span class="hot' + (found[i] ? ' found' : '') + '" data-i="' + i + '" style="left:' + h.x + '%;top:' + h.y + '%;width:' + h.w + '%;height:' + h.h + '%"></span>').join('');
    $('photoBox').querySelectorAll('.hot').forEach(el => el.addEventListener('click', () => {
      const i = +el.dataset.i; found[i] = true; drawPhoto();
      const n = $('photoNote');
      const c = Object.keys(found).length;
      n.className = 'note ' + (c === HOTS.length ? 'ok' : 'warn');
      n.innerHTML = '<strong>' + HOTS[i].t + '</strong>　' + HOTS[i].d + '<br>' + c + ' / ' + HOTS.length + ' か所' +
        (c === HOTS.length ? '<br>1枚の写真から、これだけのことが分かってしまいます。<strong>モザイクをかけても、他の手がかりから特定される可能性があります。</strong>' : '');
    }));
    $('photoNote').className = 'note info';
    $('photoNote').textContent = '赤い枠が5か所あります。クリックして確かめましょう。';
  }

  function init() {
    drawCombo(); drawPhoto();
    Quiz.judge('jBox', 'jNote', [
      { k: '⓪', t: '氏名や生年月日、マイナンバーなど、生存する特定の個人を識別する情報や符号。', ok: true,
        why: '個人情報の典型例です。マイナンバーなどは「個人識別符号」として明確に個人情報とされています。' },
      { k: '①', t: '新聞やニュースなどで既に報道されている、有罪判決を受けた人物の犯罪歴や家族構成などの情報。', ok: true,
        why: '報道されていても個人情報です。犯罪歴は<strong>要配慮個人情報</strong>として、より慎重な扱いが求められます。' },
      { k: '②', t: '単体では個人を特定できないが、他の情報と組み合わせることで個人を識別可能な情報。', ok: true,
        why: 'STEP 2 で確かめたとおり、組み合わせて特定できるなら個人情報にあたります。' },
      { k: '③', t: '国や地方公共団体などが保有している年代別や男女別人口などといった統計情報。', ok: false,
        why: '統計情報は<strong>個人を識別できない</strong>ので個人情報ではありません。これが問1の答えです。' }
    ], '個人情報に<strong>あたらない</strong>のは③なので、【ア】の答えは <strong>③</strong> です。');
    Quiz.choice('q1Box', 'q1Note', [
      { k: 'ア', q: '個人情報保護法で定められた個人情報として<strong>適当でない</strong>ものは',
        ch: ['氏名や生年月日、マイナンバーなど、生存する特定の個人を識別する情報や符号', '新聞やニュースなどで既に報道されている、有罪判決を受けた人物の犯罪歴や家族構成などの情報', '単体では個人を特定できないが、他の情報と組み合わせることで個人を識別可能な情報', '国や地方公共団体などが保有している年代別や男女別人口などといった統計情報'],
        a: 3, why: '統計情報は個人を識別できないため、個人情報にはあたりません。' }
    ], '本文の答えは【ア】③ です。');
    Quiz.choice('q2Box', 'q2Note', [
      { k: 'イ', q: '個人情報とプライバシーに関係する記述のうち最も適当なものは',
        ch: ['プライバシーマークを有している企業や団体は、厳格な審査を受けているため、個人情報が漏えいすることは絶対にない', 'スマートフォンで撮影した写真の背景にモザイク処理を施していても、撮影場所が特定される可能性はある', '自身が撮ったアイドルの写真をTシャツにプリントして、ネット上で販売しても問題ない', 'SNSのアカウントを非公開設定にしている場合、投稿内容が他人に漏れることは絶対にない'],
        a: 1, why: 'STEP 3 で確かめたとおりです。⓪と③の「絶対にない」は言いすぎ。②は<strong>肖像権・パブリシティ権</strong>の侵害にあたります。' }
    ], '本文の答えは【イ】① です。');
    Quiz.choice('q3Box', 'q3Note', [
      { k: 'ウ', q: '個人情報とプライバシーに関係する記述のうち最も適当なものは',
        ch: ['個人情報保護法は、個人情報の有用性に注目し、第三者への情報提供を促進することを目的としている', 'ポイントカードの購買履歴や交通系ICカードの乗降履歴等を複数の事業者間で利活用することで新たなサービスが生まれる可能性がある', 'フリマアプリで購入者と出品者との間でトラブルが生じたとき、フリマアプリの運営会社は本人の許可なく、購入者の連絡先を出品者へ提供できる', '本人の許可を得ずに、自社の商品を宣伝するためのメールやDMを配信することは問題ない'],
        a: 1, why: '適切に扱えば新しいサービスにつながります。⓪は「提供の促進」が目的ではなく<strong>権利利益の保護</strong>が目的、②③は<strong>本人の同意なしの第三者提供・利用</strong>にあたり原則できません。' }
    ], '本文の答えは【ウ】① です。');
    window.Terms.glossary($('glossBox'), ['個人情報', '個人情報保護法', 'プライバシー', '肖像権', 'パブリシティ権', '要配慮個人情報', 'デジタルタトゥー']);
    window.Terms.attach();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
