import os from "node:os";
import path from "node:path";
import type { ConcreteTarget, InstallTarget } from "./types.js";

export const concreteTargets: ConcreteTarget[] = ["codex", "windsurf", "cursor", "claude"];

export function expandTargets(target: InstallTarget): ConcreteTarget[] {
  return target === "all" ? concreteTargets : [target];
}

export function codexSkillsDir() {
  return path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "skills");
}

export function windsurfConfigDir() {
  return path.join(os.homedir(), ".codeium", "windsurf");
}

export function windsurfSkillsDir() {
  return path.join(windsurfConfigDir(), "skills");
}

export function windsurfWorkflowsDir() {
  return path.join(windsurfConfigDir(), "global_workflows");
}

export function windsurfMcpConfigPath() {
  return path.join(windsurfConfigDir(), "mcp_config.json");
}

export function claudeSkillsDir() {
  return path.join(os.homedir(), ".claude", "skills");
}

export function resolveProjectDir(projectDir?: string) {
  return path.resolve(projectDir || process.cwd());
}
