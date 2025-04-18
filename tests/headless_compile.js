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

  // 4) Go directly to the sign‑in page
  await page.goto('https://www.tradingview.com/accounts/signin/', { waitUntil: 'domcontentloaded' });

  // 5) Wait for and fill the email field (try multiple selectors)
  const emailLocator = await page.waitForSelector(
    'input[type="email"], input[name="username"], input[placeholder="Email"]',
    { timeout: 30000 }
  );
  await emailLocator.fill(user);

  // 6) Fill the password field
  const passLocator = await page.waitForSelector(
    'input[type="password"], input[name="password"], input[placeholder="Password"]',
    { timeout: 30000 }
  );
  await passLocator.fill(pass);

  // 7) Submit the form
  await page.click('button[type="submit"], button:has-text("Log in")');

  // 8) Wait until logged in
  await page.waitForSelector('.tv-logo__link', { timeout: 60000 });

  // 9) Open chart & Pine Editor
  await page.goto('https://www.tradingview.com/chart/', { waitUntil: 'domcontentloaded' });
  await page.click('button[title="Open Pine Editor"]');

  // 10) Paste and compile
  await page.fill('textarea.cm-content', code);
  await page.click('button:has-text("Add to Chart")');

  // 11) Check for compile errors
  const err = await page.$('.tv-error-message__content');
  if (err) {
    console.error(`Compile error in ${file}:`, await err.textContent());
    process.exit(1);
  }
  console.log(`✅ Compile successful for ${file}`);

  await browser.close();
})();
