import path from "node:path";
import { removePath } from "./file-ops.js";
import { removePerplexityMcpServer } from "./mcp-config.js";
import {
  claudeSkillsDir,
  codexSkillsDir,
  expandTargets,
  resolveProjectDir,
  windsurfMcpConfigPath,
  windsurfSkillsDir,
  windsurfWorkflowsDir,
} from "./targets.js";
import type { CommonOptions, FileAction, InstallTarget } from "./types.js";

const codexSkills = ["perplexity_search_only", "perplexity_deep_research", "perplexity-pro-search", "perplexity-fetch-url-content"];
const windsurfSkills = ["perplexity-search", "perplexity-research", "perplexity-pro", "perplexity-fetch-url"];
const windsurfWorkflows = ["perplexity-search.md", "perplexity-research.md", "perplexity-pro.md", "perplexity-fetch-url.md"];
const claudeSkills = ["perplexity-search-only", "perplexity-pro-search", "perplexity-deep-research", "perplexity-fetch-url"];

interface UninstallOptions extends CommonOptions {
  projectDir?: string;
}

export async function uninstallTarget(target: InstallTarget, options: UninstallOptions) {
  const actions: FileAction[] = [];
  const projectDir = resolveProjectDir(options.projectDir);
  for (const concreteTarget of expandTargets(target)) {
    if (concreteTarget === "codex") {
      for (const skill of codexSkills) actions.push(await removePath(path.join(codexSkillsDir(), skill), options));
    }
    if (concreteTarget === "windsurf") {
      for (const skill of windsurfSkills) actions.push(await removePath(path.join(windsurfSkillsDir(), skill), options));
      for (const workflow of windsurfWorkflows) actions.push(await removePath(path.join(windsurfWorkflowsDir(), workflow), options));
      actions.push(await removePerplexityMcpServer(windsurfMcpConfigPath(), options));
    }
    if (concreteTarget === "cursor") {
      actions.push(await removePath(path.join(projectDir, ".cursor", "rules", "perplexity.mdc"), options));
      actions.push(await removePath(path.join(projectDir, ".cursor", "mcp.json"), options));
    }
    if (concreteTarget === "claude") {
      for (const skill of claudeSkills) actions.push(await removePath(path.join(claudeSkillsDir(), skill), options));
      actions.push(await removePath(path.join(projectDir, ".mcp.json"), options));
    }
  }
  return actions;
}
