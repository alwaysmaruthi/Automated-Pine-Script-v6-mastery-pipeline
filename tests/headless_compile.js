const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  // load the first test file (you can expand this loop later)
  const files = fs.readdirSync('tests').filter(f => f.endsWith('.pine'));
  const code = fs.readFileSync(`tests/${files[0]}`, 'utf-8');

  // read credentials
  const user = process.env.TV_USER, pass = process.env.TV_PASS;
  if (!user || !pass) {
    console.error('TV_USER / TV_PASS must be set in Secrets');
    process.exit(1);
  }

  const browser = await chromium.launch();
  const ctx     = await browser.newContext();
  const page    = await ctx.newPage();

  // 1) Log in
  await page.goto('https://www.tradingview.com/#signin');
  await page.fill('input[name="username"]', user);
  await page.fill('input[name="password"]', pass);
  await page.click('button[type="submit"]');
  await page.waitForSelector('.tv-logo__link', { timeout: 30000 });

  // 2) Open chart & Pine Editor
  await page.goto('https://www.tradingview.com/chart/');
  await page.click('button[title="Open Pine Editor"]');

  // 3) Paste code & compile
  await page.fill('.pine-editor textarea', code);
  await page.click('button:has-text("Add to Chart")');

  // 4) Check for errors
  const err = await page.$('.tv-error-message__content');
  if (err) {
    console.error('Compile error:', await err.textContent());
    process.exit(1);
  } else {
    console.log('✅ Compile successful for', files[0]);
  }

  await browser.close();
})();
