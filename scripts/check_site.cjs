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
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
      assert.equal(await page.locator('.paper-card').count(), 24);
      await page.screenshot({ path: path.join(screenshots, `${lang}-desktop.png`) });

      await page.locator('#search').fill('ParamISP 2024');
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      assert.match(await page.locator('#languageLink').getAttribute('href'), /q=ParamISP/);
      await page.locator('#languageLink').click();
      assert.equal(await page.locator('.paper-card').count(), 1);
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.goto(url);

      await page.locator('#spotlightButton').click();
      assert.equal(await page.locator('.paper-card').count(), 5);
      assert.ok((await page.locator('.paper-card').allTextContents()).some(text => text.includes('CtrlISP')));
      await page.locator('#status').selectOption('WR');
      assert.equal(await page.locator('.paper-card').count(), 3);
      await page.locator('#host').selectOption('gdrive');
      assert.equal(await page.locator('.paper-card').count(), 2);
      await page.locator('#year').selectOption('2024');
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.reload();
      assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      await page.locator('#reset').click();

      await page.locator('#search').fill('no-such-paper-<img onerror=alert(1)>');
      assert.equal(await page.locator('.paper-card').count(), 0);
      assert.equal(await page.locator('#results img').count(), 0);
      await page.locator('[data-reset]').click();
      assert.equal(await page.locator('.paper-card').count(), 24);
      await page.locator('#showMore').click();
      assert.equal(await page.locator('.paper-card').count(), 48);
      await page.locator('#search').fill('Modular Neural ISP');
      await page.locator('.paper-details summary').click();
      assert.equal(await page.locator('.downloads a').count(), 2);
      assert.ok(await page.locator('.downloads a').first().isVisible());

      await page.locator('#reset').click();
      await page.locator('#sort').selectOption('ready');
      assert.equal(await page.locator('.paper-card .status:not(.status-W):not(.status-R)').count(), 0);
      await page.locator('#sort').selectOption('az');
      const names = await page.locator('.paper-card').evaluateAll(items => items.map(item => item.dataset.paper));
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
        await page.locator('#search').fill('Learned Forward and Inverse ISPs');
        assert.equal(await page.locator('.paper-card').getAttribute('data-paper'), 'ParamISP');
      }
      await page.goto(url);
      for (const width of [1440, 1024, 768, 390, 320]) {
        await page.setViewportSize({ width, height: 900 });
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Overflow at ${width}px / ${lang}`);
      }
      await page.setViewportSize({ width: 390, height: 844 });
      await page.screenshot({ path: path.join(screenshots, `${lang}-mobile.png`), fullPage: false });
      await page.locator('#menuButton').click();
      assert.equal(await page.locator('#menuButton').getAttribute('aria-expanded'), 'true');
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#menuButton').getAttribute('aria-expanded'), 'false');
      await page.locator('#menuButton').click();
      await page.locator('[data-topic=controllable]').click();
      assert.equal(await page.locator('.paper-card').count(), 5);
      assert.equal(await page.locator('#menuButton').getAttribute('aria-expanded'), 'false');
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({ path: path.join(screenshots, `${lang}-mobile-library.png`) });
      assert.deepEqual(errors, []);
      assert.deepEqual(remoteRequests, []);
      await page.close();
      console.log(`PASS ${lang}: navigation, filtering, search, downloads, language state, resources, mobile and offline rendering`);
    }
    console.log(`Screenshots: ${screenshots}`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
