import path from "node:path";
import { copyPath } from "./file-ops.js";
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
import { upsertPerplexityMcpServer } from "./mcp-config.js";
import type { FileAction, InstallOptions, InstallTarget } from "./types.js";

const codexSkills = [
  "perplexity_search_only",
  "perplexity_deep_research",
  "perplexity-pro-search",
  "perplexity-fetch-url-content",
];

const directCodexSkills = [
  "perplexity_search_only",
  "perplexity-pro-search",
  "perplexity-fetch-url-content",
];

const windsurfSkills = ["perplexity-search", "perplexity-research", "perplexity-pro", "perplexity-fetch-url"];
const windsurfWorkflows = ["perplexity-search.md", "perplexity-research.md", "perplexity-pro.md", "perplexity-fetch-url.md"];

async function installCodex(options: InstallOptions) {
  const actions: FileAction[] = [];
  const targetDir = codexSkillsDir();
  for (const skill of codexSkills) {
    actions.push(await copyPath(fromRoot(skill), path.join(targetDir, skill), options));
  }
  for (const skill of directCodexSkills) {
    actions.push(await copyPath(fromRoot("perplexity_common.py"), path.join(targetDir, skill, "perplexity_common.py"), options));
  }
  return actions;
}

async function installWindsurf(options: InstallOptions) {
  const actions: FileAction[] = [];
  for (const skill of windsurfSkills) {
    actions.push(await copyPath(fromRoot(".windsurf", "skills", skill), path.join(windsurfSkillsDir(), skill), options));
  }

  actions.push(await copyPath(fromRoot("perplexity_search_only", "scripts", "search_only.py"), path.join(windsurfSkillsDir(), "perplexity-search", "search_only.py"), options));
  actions.push(await copyPath(fromRoot("perplexity-pro-search", "scripts", "pro_search.py"), path.join(windsurfSkillsDir(), "perplexity-pro", "pro_search.py"), options));
  actions.push(await copyPath(fromRoot("perplexity-fetch-url-content", "scripts", "fetch_url_content.py"), path.join(windsurfSkillsDir(), "perplexity-fetch-url", "fetch_url_content.py"), options));

  for (const skill of ["perplexity-search", "perplexity-pro", "perplexity-fetch-url"]) {
    actions.push(await copyPath(fromRoot("perplexity_common.py"), path.join(windsurfSkillsDir(), skill, "perplexity_common.py"), options));
    actions.push(await copyPath(fromRoot("requirements.txt"), path.join(windsurfSkillsDir(), skill, "requirements.txt"), options));
  }

  for (const workflow of windsurfWorkflows) {
    actions.push(await copyPath(fromRoot(".windsurf", "workflows", workflow), path.join(windsurfWorkflowsDir(), workflow), options));
  }

  if (!options.noKey) {
    actions.push(await upsertPerplexityMcpServer(windsurfMcpConfigPath(), options.apiKey || process.env.PERPLEXITY_API_KEY, options));
  }

  return actions;
}

async function installCursor(options: InstallOptions) {
  const actions: FileAction[] = [];
  const projectDir = resolveProjectDir(options.projectDir);
  actions.push(await copyPath(fromRoot(".cursor", "mcp.json"), path.join(projectDir, ".cursor", "mcp.json"), options));
  actions.push(await copyPath(fromRoot(".cursor", "rules", "perplexity.mdc"), path.join(projectDir, ".cursor", "rules", "perplexity.mdc"), options));
  return actions;
}

async function installClaude(options: InstallOptions) {
  const actions: FileAction[] = [];
  const projectDir = resolveProjectDir(options.projectDir);
  const skillNames = ["perplexity-search-only", "perplexity-pro-search", "perplexity-deep-research", "perplexity-fetch-url"];
  for (const skill of skillNames) {
    actions.push(await copyPath(fromRoot(".claude", "skills", skill), path.join(claudeSkillsDir(), skill), options));
  }
  actions.push(await copyPath(fromRoot(".mcp.json"), path.join(projectDir, ".mcp.json"), options));
  return actions;
}

export async function installTarget(target: InstallTarget, options: InstallOptions) {
  const actions: FileAction[] = [];
  for (const concreteTarget of expandTargets(target)) {
    if (concreteTarget === "codex") actions.push(...await installCodex(options));
    if (concreteTarget === "windsurf") actions.push(...await installWindsurf(options));
    if (concreteTarget === "cursor") actions.push(...await installCursor(options));
    if (concreteTarget === "claude") actions.push(...await installClaude(options));
  }
  return actions;
}
