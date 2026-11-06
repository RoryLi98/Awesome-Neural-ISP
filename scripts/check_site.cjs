/* Optional browser verification: npm install --no-save playwright, then node scripts/check_site.cjs.
 * Uses an installed Chrome browser; no web server or network access is needed.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const screenshots = path.join(os.tmpdir(), 'awesome-neural-isp-review');
  fs.mkdirSync(screenshots, { recursive: true });
  try {
    for (const [file, lang] of [['index.html', 'en'], ['zh-CN.html', 'zh-CN']]) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, reducedMotion: 'reduce' });
      const errors = [], remoteRequests = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('request', request => { if (/^https?:/.test(request.url())) remoteRequests.push(request.url()); });
      const url = pathToFileURL(path.resolve(__dirname, '..', 'docs', file)).href;
      await page.goto(url);
      const data = await page.locator('#library-data').evaluate(el => JSON.parse(el.textContent));
      assert.equal(data.papers.length, 417);
      assert.equal(new Set(data.papers.map(p => p.id)).size, 417);
      assert.ok((await page.locator('.paper-name').first().boundingBox()).y < 680, 'Desktop should expose a paper in the first viewport');
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
      assert.equal(await page.locator('.paper-card').count(), 24);
      assert.equal(await page.locator('.collection-shortcuts, #spotlightButton, #mobileButton').count(), 0);
      assert.equal(await page.locator('.paper-card details, .citation, [data-copy=citation], [data-copy=bibtex]').count(), 0);
      assert.equal(await page.locator('[data-copy], #copyStatus, .reading-notes, .paper-framework, .implementation-framework, .method-tags, .detail-tags').count(), 0);
      assert.ok(data.papers.every(p => !('bibtex' in p) && !('bibtexSource' in p)));
      assert.ok(data.papers.every(p => !('fw' in p) && p.impl.every(r => !('fw' in r))));
      assert.ok(data.papers.every(p => !/核验日期|\(checked \d{4}/.test(p.note)));
      assert.ok(data.papers.every(p => p.s.length > 20));
      const twoShots = data.papers.find(p => p.n === '2-Shots in the Dark');
      assert.match(twoShots.s, lang === 'en' ? /per ISO setting/ : /每个 ISO/);
      assert.match(twoShots.s, lang === 'en' ? /spatial patterns/ : /空间纹理/);
      assert.match(twoShots.s, lang === 'en' ? /Fourier-domain spectral sampling/ : /傅里叶频谱采样/);
      assert.match(twoShots.s, lang === 'en' ? /contribution.*data-acquisition/ : /贡献.*采集成本/);
      assert.deepEqual(await page.locator('#topicNav .nav-group h2').allTextContents(), data.navigation.map(g => g.label));
      assert.deepEqual(await page.locator('#topicNav [data-topic]').evaluateAll(items => items.map(x => x.dataset.topic)), ['all', ...data.navigation.flatMap(g => g.topics)]);
      assert.equal(await page.locator('.topic-kind, .nav-note').count(), 0);
      if (lang === 'zh-CN') assert.ok(!(await page.locator('body').innerText()).includes('专题'));
      await page.screenshot({ path: path.join(screenshots, `${lang}-desktop.png`) });

      // Venue selections are a union; year and task remain intersections, even across reload/language changes.
      const visiblePapers = async () => (await page.locator('.paper-card').evaluateAll(items => items.map(x => x.dataset.paper))).map(name => data.papers.find(p => p.n === name));
      const expectTotal = async count => assert.match(await page.locator('#resultCount').textContent(), new RegExp(`\\b${count}\\b`));
      await page.locator('#venueSummary').click();
      await page.locator('#venueOptions input[value=cvpr]').check();
      assert.ok((await visiblePapers()).every(p => p.v === 'CVPR'), 'CVPR excludes CVPRW and Findings');
      await expectTotal(data.papers.filter(p => p.v === 'CVPR').length);
      await page.locator('#venueOptions input[value=iccv]').check();
      await expectTotal(data.papers.filter(p => ['CVPR','ICCV'].includes(p.v)).length);
      assert.ok((await visiblePapers()).every(p => ['CVPR','ICCV'].includes(p.v)));
      await page.screenshot({ path: path.join(screenshots, `${lang}-venue-picker.png`) });
      await page.keyboard.press('Escape');
      assert.ok(!(await page.locator('#venueFilter').evaluate(el => el.open)));
      await page.locator('#advancedFilters > summary').click();
      await page.locator('#year').selectOption('2024');
      await page.locator('[data-topic=e2e]').click();
      const expectedPrimary = data.papers.filter(p => ['CVPR','ICCV'].includes(p.v) && p.y === 2024 && p.c === 'e2e');
      assert.ok(expectedPrimary.length > 0);
      await expectTotal(expectedPrimary.length);
      assert.ok((await visiblePapers()).every(p => expectedPrimary.includes(p)));
      await page.reload();
      assert.equal(await page.locator('#year').inputValue(), '2024');
      assert.ok(await page.locator('#venueOptions input[value=cvpr]').isChecked());
      assert.ok(await page.locator('#venueOptions input[value=iccv]').isChecked());
      await page.locator('#languageLink').click();
      assert.equal(await page.locator('#venueOptions input:checked').count(), 2);
      await expectTotal(expectedPrimary.length);
      await page.goto(url);
      await page.locator('#venueSummary').click();
      await page.locator('[data-venue-preset=vision]').click();
      assert.equal(await page.locator('#venueOptions input:checked').count(), 3);
      await page.locator('#venueOptions input[value=neurips]').check();
      await expectTotal(data.papers.filter(p => ['cvpr','iccv','eccv','neurips'].includes(p.vk)).length);
      await page.keyboard.press('Escape');
      await page.locator('[data-clear=venue][data-value=cvpr]').click();
      assert.ok(!(await page.locator('#venueOptions input[value=cvpr]').isChecked()));
      await expectTotal(data.papers.filter(p => ['iccv','eccv','neurips'].includes(p.vk)).length);
      await page.locator('#venueSummary').click();
      await page.locator('[data-venue-clear]').click();
      assert.equal(await page.locator('#venueOptions input:checked').count(), 0);
      await expectTotal(data.papers.length);
      await page.locator('#venueOptions input[value=cvprw]').check();
      assert.ok((await visiblePapers()).every(p => /^CVPRW(?: |$)/.test(p.v)));
      await expectTotal(data.papers.filter(p => /^CVPRW(?: |$)/.test(p.v)).length);
      await page.keyboard.press('Escape');
      await page.locator('#reset').click();
      assert.equal(await page.locator('#venueOptions input:checked').count(), 0);
      await page.goto(`${url}?venues=unknown,cvpr,cvpr&year=not-a-year`);
      assert.equal(await page.locator('#venueOptions input:checked').count(), 1);
      assert.equal(await page.locator('#year').inputValue(), 'all');
      assert.ok(!(await page.locator('#languageLink').getAttribute('href')).includes('unknown'));
      await page.goto(url);

      await page.locator('#search').fill('ParamISP 2024');
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      assert.equal(await page.locator('.paper-name a').textContent(), 'ParamISP: Learned Forward and Inverse ISPs using Camera Parameters ↗');
      assert.match(await page.locator('#languageLink').getAttribute('href'), /q=ParamISP/);
      await page.locator('#languageLink').click();
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.goto(url);

      await page.locator('[data-topic=controllable]').click();
      assert.equal(await page.locator('.paper-card').count(), 9);
      assert.ok((await page.locator('.paper-card').allTextContents()).some(text => text.includes('CtrlISP')));
      assert.ok((await page.locator('.paper-card').allTextContents()).some(text => text.includes('Deep-FlexISP')));
      await page.locator('#control').selectOption('camera-conditioned');
      assert.equal(await page.locator('.paper-card').count(), 4);
      assert.equal(await page.locator('[data-paper=CtrlISP]').count(), 0);
      await page.locator('#control').selectOption('user-parameters');
      assert.equal(await page.locator('.paper-card').count(), 4);
      assert.equal(await page.locator('[data-paper=ParamISP]').count(), 0);
      await page.locator('#activeFilters [data-clear=control]').click();
      await page.locator('#status').selectOption('WR');
      assert.equal(await page.locator('.paper-card').count(), 3);
      await page.locator('#advancedFilters > summary').click();
      await page.locator('#host').selectOption('gdrive');
      assert.equal(await page.locator('.paper-card').count(), 2);
      await page.locator('#year').selectOption('2024');
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.reload();
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.locator('#reset').click();

      await page.locator('#search').fill('Residual JDSR');
      await page.locator('#status').selectOption('WR');
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.equal(await page.locator('.paper-card .status-U').count(), 1);
      assert.equal(await page.locator('.downloads a').count(), 1);
      await page.locator('#reset').click();

      await page.locator('#architecture').selectOption('transformer');
      await page.locator('#search').fill('Rawformer');
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'Rawformer');
      assert.match(await page.locator('#languageLink').getAttribute('href'), /architecture=transformer/);
      await page.reload();
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'Rawformer');
      await page.locator('#reset').click();

      // Challenge solutions remain searchable and downloadable without duplicate publications.
      await page.locator('#search').fill('MWRCANet');
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'NTIRE 2020 Real Denoising');
      assert.equal(await page.locator('.downloads a').count(), 2);
      assert.ok((await page.locator('.implementations').textContent()).includes('MWRCANet'));
      await page.locator('#reset').click();

      await page.goto(`${url}?paper=paper-paramisp#paper-paramisp`);
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.match(await page.locator('.paper-summary').textContent(), /ParamNet/);
      assert.equal(await page.locator('.paper-name a').getAttribute('href'), data.papers.find(p => p.n === 'ParamISP').p);
      assert.equal(await page.locator('.paper-card a').evaluateAll(items => items.filter(a => a.href === document.querySelector('.paper-name a').href).length), 1, 'The linked title is the single paper entry point');
      assert.ok(await page.locator('.paper-meta .method-tag').count() > 0);
      assert.equal(await page.locator('.paper-info .method-tag').count(), 0);
      const codeLink = page.locator('.paper-release .code-link');
      assert.equal(await codeLink.getAttribute('href'), data.papers.find(p => p.n === 'ParamISP').g);
      assert.equal(await page.locator('.paper-resources a').evaluateAll(items => items.filter(a => a.href === document.querySelector('.code-link').href).length), 0, 'Code should follow release status without a duplicate resource-row link');
      const statusBox = await page.locator('.paper-release .status').boundingBox();
      const codeBox = await codeLink.boundingBox();
      assert.ok(Math.abs(statusBox.y - codeBox.y) < 5 && codeBox.x > statusBox.x, 'Code link should stay immediately after release status');
      const publicationBox = await page.locator('.paper-publication').boundingBox();
      const tagBox = await page.locator('.paper-meta .method-tag').first().boundingBox();
      assert.ok(Math.abs(publicationBox.y - tagBox.y) < 5, 'Tags share the metadata row when space is available');
      assert.ok(await page.locator('.downloads a').first().isVisible());
      await page.screenshot({ path: path.join(screenshots, `${lang}-reading-card.png`) });
      await page.locator('#languageLink').click();
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.goto(url);

      await page.locator('#search').fill('DNF');
      await page.locator('[data-dataset=SID]').click();
      assert.equal(await page.locator('[data-view=datasets]').getAttribute('aria-pressed'), 'true');
      assert.ok((await page.locator('.resource-card h3').allTextContents()).includes('SID'));
      await page.goto(url);

      await page.locator('#search').fill('no-such-paper-<img onerror=alert(1)>');
      assert.equal(await page.locator('.paper-card').count(), 0);
      assert.equal(await page.locator('#results img').count(), 0);
      await page.locator('[data-reset]').click();
      assert.equal(await page.locator('.paper-card').count(), 24);
      await page.locator('#showMore').click();
      assert.equal(await page.locator('.paper-card').count(), 48);
      await page.locator('#search').fill('Modular Neural ISP');
      assert.equal(await page.locator('.downloads a').count(), 2);
      assert.ok(await page.locator('.downloads a').first().isVisible());

      await page.locator('#reset').click();
      await page.locator('#sort').selectOption('ready');
      assert.equal(await page.locator('.paper-card .status:not(.status-W):not(.status-R)').count(), 0);
      await page.locator('#sort').selectOption('az');
      const names = await page.locator('.paper-name a').allTextContents();
      assert.deepEqual(names, [...names].sort((a, b) => a.localeCompare(b)));
      await page.locator('#library').scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(screenshots, `${lang}-library.png`) });

      await page.locator('[data-view=datasets]').click();
      assert.equal(await page.locator('.resource-card').count(), 29);
      assert.ok(await page.locator('#paperFilters').isHidden());
      await page.locator('#search').fill('SIDD');
      assert.ok(await page.locator('.resource-card').count() > 0);
      await page.locator('[data-view=tools]').click();
      assert.equal(await page.locator('.resource-card').count(), 13);
      await page.locator('[data-view=learn]').click();
      assert.ok(await page.locator('.learning-item').count() > 15);

      if (lang === 'zh-CN') {
        await page.locator('[data-view=papers]').click();
        await page.locator('#search').fill('可控');
        assert.ok(await page.locator('.paper-card').count() > 0);
        await page.locator('#search').fill('ParamISP Learned Forward and Inverse ISPs');
        assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      }
      await page.goto(url);
      for (const width of [1440, 1024, 768, 390, 320]) {
        await page.setViewportSize({ width, height: 900 });
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Overflow at ${width}px / ${lang}`);
        await page.locator('#venueSummary').click();
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Venue picker overflow at ${width}px / ${lang}`);
        const panel = await page.locator('.venue-panel').boundingBox();
        assert.ok(panel.x >= 0 && panel.x + panel.width <= width, `Venue picker stays within ${width}px / ${lang}`);
        await page.keyboard.press('Escape');
      }
      await page.setViewportSize({ width: 390, height: 844 });
      assert.ok((await page.locator('.paper-name').first().boundingBox()).y < 790, 'Mobile should expose a paper in the first viewport');
      await page.screenshot({ path: path.join(screenshots, `${lang}-mobile.png`), fullPage: false });
      await page.locator('#venueSummary').click();
      await page.locator('[data-venue-preset=vision]').click();
      await page.locator('#venueOptions input[value=neurips]').check();
      assert.equal(await page.locator('#venueOptions input:checked').count(), 4);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({ path: path.join(screenshots, `${lang}-mobile-venue-picker.png`) });
      await page.keyboard.press('Escape');
      await page.locator('#reset').click();
      await page.locator('#menuButton').click();
      assert.equal(await page.locator('#menuButton').getAttribute('aria-expanded'), 'true');
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#menuButton').getAttribute('aria-expanded'), 'false');
      await page.locator('#menuButton').click();
      await page.locator('[data-topic=controllable]').click();
      assert.equal(await page.locator('.paper-card').count(), 9);
      assert.ok((await page.locator('#categoryDescription').boundingBox()).height < 115, 'Category overview should remain compact');
      assert.equal(await page.locator('#menuButton').getAttribute('aria-expanded'), 'false');
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({ path: path.join(screenshots, `${lang}-mobile-library.png`) });
      await page.locator('#search').fill('CtrlISP');
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.match(await page.locator('.paper-summary').textContent(), /DenoiseNet/);
      await page.locator('.paper-card').scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(screenshots, `${lang}-mobile-card.png`) });
      assert.deepEqual(errors, []);
      assert.deepEqual(remoteRequests, []);
      await page.close();
      console.log(`PASS ${lang}: grouped navigation, multi-venue OR/AND filters, main/workshop boundaries, language/URL persistence, paper resources, responsive picker and offline rendering`);
    }
    console.log(`Screenshots: ${screenshots}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
