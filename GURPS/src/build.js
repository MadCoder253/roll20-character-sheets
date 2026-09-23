#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const MANIFEST_PATH = path.join(__dirname, 'manifest.json');
const CHECK_MODE = process.argv.includes('--check');

function readFile(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function ensureOutputDirectory(filePath) {
  const outputDir = path.dirname(filePath);
  fs.mkdirSync(outputDir, { recursive: true });
}

function normalize(text) {
  return text.replace(/\r\n/g, '\n');
}

function resolveInputEntries(entries) {
  if (!Array.isArray(entries)) {
    return [];
  }

  return entries.flatMap((entry) => {
    const absoluteEntry = path.resolve(__dirname, entry);

    if (!fs.existsSync(absoluteEntry)) {
      return [];
    }

    const stat = fs.statSync(absoluteEntry);

    if (stat.isFile()) {
      return [absoluteEntry];
    }

    if (stat.isDirectory()) {
      return fs
        .readdirSync(absoluteEntry)
        .filter((file) => !file.startsWith('.'))
        .sort()
        .map((file) => path.join(absoluteEntry, file));
    }

    return [];
  });
}

function loadManifest() {
  if (!fs.existsSync(MANIFEST_PATH)) {
    return {
      outputs: {
        html: { input: ['../gurps.html'], output: '../gurps.html' },
        css: { input: ['../gurps.css'], output: '../gurps.css' },
      },
    };
  }

  return JSON.parse(readFile(MANIFEST_PATH));
}

function buildOutput(config) {
  const inputFiles = resolveInputEntries(config.input || []);

  if (inputFiles.length === 0) {
    return '';
  }

  return inputFiles.map((filePath) => readFile(filePath)).join('');
}

function main() {
  const manifest = loadManifest();
  const outputs = manifest.outputs || {};
  let hasDifferences = false;

  for (const [type, config] of Object.entries(outputs)) {
    const outputFilePath = path.resolve(__dirname, config.output || `../${type}`);
    const generatedContent = normalize(buildOutput(config));
    const existingContent = fs.existsSync(outputFilePath) ? normalize(readFile(outputFilePath)) : '';

    if (CHECK_MODE) {
      if (generatedContent !== existingContent) {
        hasDifferences = true;
        console.error(`Mismatch detected for ${type}: ${path.relative(ROOT_DIR, outputFilePath)}`);
      }
      continue;
    }

    ensureOutputDirectory(outputFilePath);
    fs.writeFileSync(outputFilePath, generatedContent, 'utf8');
    console.log(`Built ${type}: ${path.relative(ROOT_DIR, outputFilePath)}`);
  }

  if (CHECK_MODE) {
    if (hasDifferences) {
      console.error('Build check failed: generated output does not match committed files.');
      process.exitCode = 1;
      return;
    }

    console.log('Build check passed: generated output matches committed files.');
  }
}

main();
