const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const files = fs.readdirSync('tests').filter(f => f.endsWith('.pine'));
  if (files.length === 0) {
    console.error('No .pine files found in tests/');
    process.exit(1);
  }
  const file = files[0];
  const code = fs.readFileSync(`tests/${file}`, 'utf-8');

  const user = process.env.TV_USER;
  const pass = process.env.TV_PASS;
  if (!user || !pass) {
    console.error('Error: TV_USER and TV_PASS must be set as GitHub Secrets');
    process.exit(1);
  }

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // 1) Log in to TradingView
  await page.goto('https://www.tradingview.com/#signin');
  await page.fill('input[type="email"]',    user);
  await page.fill('input[type="password"]', pass);
  await page.click('button[type="submit"]');
  await page.waitForSelector('.tv-logo__link', { timeout: 30000 });

  // 2) Open chart & Pine Editor
  await page.goto('https://www.tradingview.com/chart/');
  await page.click('button[title="Open Pine Editor"]');

  // 3) Paste code & compile
  await page.fill('.pine-editor textarea', code);
  await page.click('button:has-text("Add to Chart")');

  // 4) Check for compile errors
  const err = await page.$('.tv-error-message__content');
  if (err) {
    console.error(`Compile error in ${file}:`, await err.textContent());
    process.exit(1);
  } else {
    console.log(`✅ Compile successful for ${file}`);
  }

  await browser.close();
})();
