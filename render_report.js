const { execFileSync } = require("child_process");
const { mkdirSync, readFileSync } = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const projectRoot = __dirname;
const outputPath = path.join(projectRoot, "reports", "test.pdf");

function getReportData() {
  const python = path.join(projectRoot, "venv", "Scripts", "python.exe");
  const command = "import json; from report import getReportData; print(json.dumps(getReportData()))";
  return JSON.parse(execFileSync(python, ["-c", command], { cwd: projectRoot }));
}

async function renderReport() {
  const template = readFileSync(path.join(projectRoot, "report_template.html"), "utf8");
  const reportData = JSON.stringify(getReportData()).replace(/</g, "\\u003c");
  const html = template.replace("{{REPORT_DATA}}", reportData);

  mkdirSync(path.dirname(outputPath), { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: "load" });
    await page.pdf({ path: outputPath, format: "A4", printBackground: true });
  } finally {
    await browser.close();
  }
  console.log(`Saved PDF to ${outputPath}`);
}

renderReport().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});