#!/usr/bin/env node
import { createRequire } from "node:module";
import { Command, Option } from "commander";
import { printActions } from "./file-ops.js";
import { installTarget } from "./install.js";
import { syncTarget } from "./sync.js";
import { uninstallTarget } from "./uninstall.js";
import { doctor, printDoctorChecks } from "./doctor.js";
import type { InstallTarget } from "./types.js";

const require = createRequire(import.meta.url);
const { version } = require("../package.json") as { version: string };

const targetChoices = ["codex", "windsurf", "cursor", "claude", "all"];

function parseTarget(target: string): InstallTarget {
  if (!targetChoices.includes(target)) {
    throw new Error(`Unsupported target: ${target}`);
  }
  return target as InstallTarget;
}

async function main() {
  const program = new Command();
  program
    .name("perplexity-mcp-skills")
    .description("Install Perplexity MCP skills, workflows, and direct API fallbacks.")
    .version(version);

  program
    .command("install")
    .description("Install integrations for one target or all targets.")
    .argument("<target>", "codex | windsurf | cursor | claude | all")
    .addOption(new Option("--api-key <key>", "Perplexity API key for MCP config writes"))
    .option("--no-key", "install files without modifying secret-bearing MCP config")
    .option("--project-dir <dir>", "project directory for Cursor/Claude project-local files", ".")
    .option("--dry-run", "print planned changes without writing files")
    .option("--force", "replace existing files managed by this package")
    .option("--yes", "accept defaults for non-interactive use")
    .action(async (target: string, options: { apiKey?: string; key?: boolean; projectDir?: string; dryRun?: boolean; force?: boolean; yes?: boolean }) => {
      const actions = await installTarget(parseTarget(target), {
        apiKey: options.apiKey,
        noKey: options.key === false,
        projectDir: options.projectDir,
        dryRun: options.dryRun,
        force: options.force,
        yes: options.yes,
      });
      printActions(actions);
    });

  program
    .command("sync")
    .description("Refresh installed package-owned files without changing stored API keys.")
    .argument("<target>", "codex | windsurf | cursor | claude | all")
    .option("--project-dir <dir>", "project directory for Cursor/Claude project-local files", ".")
    .option("--dry-run", "print planned changes without writing files")
    .option("--yes", "accept defaults for non-interactive use")
    .action(async (target: string, options: { projectDir?: string; dryRun?: boolean; yes?: boolean }) => {
      const actions = await syncTarget(parseTarget(target), {
        projectDir: options.projectDir,
        dryRun: options.dryRun,
        yes: options.yes,
      });
      printActions(actions);
    });

  program
    .command("uninstall")
    .description("Remove known files installed by this package.")
    .argument("<target>", "codex | windsurf | cursor | claude | all")
    .option("--project-dir <dir>", "project directory for Cursor/Claude project-local files", ".")
    .option("--dry-run", "print planned changes without writing files")
    .option("--force", "remove non-standard Perplexity MCP entries too")
    .option("--yes", "accept defaults for non-interactive use")
    .action(async (target: string, options: { projectDir?: string; dryRun?: boolean; force?: boolean; yes?: boolean }) => {
      const actions = await uninstallTarget(parseTarget(target), {
        projectDir: options.projectDir,
        dryRun: options.dryRun,
        force: options.force,
        yes: options.yes,
      });
      printActions(actions);
    });

  program
    .command("doctor")
    .description("Check local Perplexity MCP skills installation state.")
    .addOption(new Option("--target <target>", "target to check").choices(targetChoices).default("all"))
    .option("--project-dir <dir>", "project directory for Cursor/Claude project-local files", ".")
    .option("--offline", "skip subprocess checks")
    .option("--json", "print JSON output")
    .action(async (options: { target: string; projectDir?: string; offline?: boolean; json?: boolean }) => {
      const checks = await doctor({
        target: parseTarget(options.target),
        projectDir: options.projectDir,
        offline: options.offline,
        json: options.json,
      });
      if (options.json) {
        console.log(JSON.stringify(checks, null, 2));
      } else {
        printDoctorChecks(checks);
      }
      if (checks.some((item) => item.status === "fail")) {
        process.exitCode = 1;
      }
    });

  await program.parseAsync(process.argv);
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`perplexity-mcp-skills: ${message}`);
  process.exit(1);
});
