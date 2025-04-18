// tests/lint_pinejs.js
const fs = require('fs');
const { PineParser } = require('pine-js');

(async () => {
  const files = fs.readdirSync('tests').filter(f => f.endsWith('.pine'));
  if (!files.length) {
    console.error('❌ No .pine files to lint');
    process.exit(1);
  }
  let hasError = false;
  for (const file of files) {
    const code = fs.readFileSync(`tests/${file}`, 'utf-8');
    try {
      PineParser.parse(code);
      console.log(`✅ ${file} parsed OK`);
    } catch (e) {
      console.error(`❌ Syntax error in ${file}: ${e.message}`);
      hasError = true;
    }
  }
  if (hasError) process.exit(1);
})();
