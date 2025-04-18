const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  // 1) Pick a .pine test
  const files = fs.readdirSync('tests').filter(f => f.endsWith('.pine'));
  if (files.length === 0) {
    console.error('No .pine files found in tests/');
    process.exit(1);
  }
  const file = files[0];
  const code = fs.readFileSync(`tests/${file}`, 'utf-8');

  // 2) Get credentials
  const user = process.env.TV_USER;
  const pass = process.env.TV_PASS;
  if (!user || !pass) {
    console.error('Error: TV_USER and TV_PASS must be set as Secrets');
    process.exit(1);
  }

  // 3) Launch browser
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // 4) Go to homepage and click Log in
  await page.goto('https://www.tradingview.com');
  await page.click('text=Log in', { timeout: 30000 });

  // 5) Wait for the email input in the modal
  await page.waitForSelector('input[type="email"]', { timeout: 30000 });
  await page.fill('input[type="email"]',    user);
  await page.fill('input[type="password"]', pass);
  await page.click('button:has-text("Log in")');

  // 6) Wait for the chart page to confirm login
  await page.waitForSelector('.tv-logo__link', { timeout: 30000 });

  // 7) Open Pine Editor
  await page.goto('https://www.tradingview.com/chart/');
  await page.click('button[title="Open Pine Editor"]');

  // 8) Paste and compile
  await page.fill('.pine-editor textarea', code);
  await page.click('button:has-text("Add to Chart")');

  // 9) Check for compile errors
  const err = await page.$('.tv-error-message__content');
  if (err) {
    console.error(`Compile error in ${file}:`, await err.textContent());
    process.exit(1);
  }
  console.log(`✅ Compile successful for ${file}`);

  await browser.close();
})();
