import fs from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fromRoot } from "./package-root.js";
import {
  claudeSkillsDir,
  codexSkillsDir,
  expandTargets,
  resolveProjectDir,
  windsurfMcpConfigPath,
  windsurfSkillsDir,
  windsurfWorkflowsDir,
} from "./targets.js";
import { hasExpectedPerplexityMcpServer } from "./mcp-config.js";
import type { DoctorCheck, DoctorOptions } from "./types.js";

function check(target: string, name: string, status: DoctorCheck["status"], message: string): DoctorCheck {
  return { target, name, status, message };
}

function exists(target: string, name: string, filePath: string): DoctorCheck {
  return fs.existsSync(filePath)
    ? check(target, name, "pass", filePath)
    : check(target, name, "fail", `Missing ${filePath}`);
}

function pythonAvailable() {
  const result = spawnSync("python3", ["--version"], { encoding: "utf8" });
  return result.status === 0 ? `${result.stdout || result.stderr}`.trim() : undefined;
}

function nodeMajor() {
  const major = Number(process.versions.node.split(".")[0]);
  return Number.isFinite(major) ? major : 0;
}

export async function doctor(options: DoctorOptions) {
  const checks: DoctorCheck[] = [];
  const projectDir = resolveProjectDir(options.projectDir);
  const py = options.offline ? "skipped in offline mode" : pythonAvailable();

  checks.push(check("system", "node", nodeMajor() >= 20 ? "pass" : "fail", `Node ${process.versions.node}; expected >=20`));
  checks.push(check("system", "python3", options.offline || py ? "pass" : "warn", py || "python3 was not found; direct scripts require Python"));
  checks.push(exists("system", "shell codex installer", fromRoot("scripts", "install_to_codex.sh")));
  checks.push(exists("system", "shell windsurf installer", fromRoot("scripts", "install_to_windsurf.sh")));

  for (const target of expandTargets(options.target)) {
    if (target === "codex") {
      const base = codexSkillsDir();
      for (const skill of ["perplexity_search_only", "perplexity_deep_research", "perplexity-pro-search", "perplexity-fetch-url-content"]) {
        checks.push(exists(target, skill, path.join(base, skill)));
      }
      for (const skill of ["perplexity_search_only", "perplexity-pro-search", "perplexity-fetch-url-content"]) {
        checks.push(exists(target, `${skill} common module`, path.join(base, skill, "perplexity_common.py")));
      }
    }

    if (target === "windsurf") {
      for (const skill of ["perplexity-search", "perplexity-research", "perplexity-pro", "perplexity-fetch-url"]) {
        checks.push(exists(target, skill, path.join(windsurfSkillsDir(), skill)));
      }
      for (const workflow of ["perplexity-search.md", "perplexity-research.md", "perplexity-pro.md", "perplexity-fetch-url.md"]) {
        checks.push(exists(target, workflow, path.join(windsurfWorkflowsDir(), workflow)));
      }
      checks.push(check(target, "mcp config", hasExpectedPerplexityMcpServer(windsurfMcpConfigPath()) ? "pass" : "warn", windsurfMcpConfigPath()));
    }

    if (target === "cursor") {
      checks.push(exists(target, "cursor mcp", path.join(projectDir, ".cursor", "mcp.json")));
      checks.push(exists(target, "cursor rule", path.join(projectDir, ".cursor", "rules", "perplexity.mdc")));
    }

    if (target === "claude") {
      for (const skill of ["perplexity-search-only", "perplexity-pro-search", "perplexity-deep-research", "perplexity-fetch-url"]) {
        checks.push(exists(target, skill, path.join(claudeSkillsDir(), skill)));
      }
      checks.push(exists(target, "project mcp", path.join(projectDir, ".mcp.json")));
    }
  }

  return checks;
}

export function printDoctorChecks(checks: DoctorCheck[]) {
  for (const item of checks) {
    const label = item.status.toUpperCase();
    console.log(`[${label}] ${item.target} ${item.name}: ${item.message}`);
  }
}
