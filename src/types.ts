export type InstallTarget = "codex" | "windsurf" | "cursor" | "claude" | "all";

export type ConcreteTarget = Exclude<InstallTarget, "all">;

export interface CommonOptions {
  dryRun?: boolean;
  force?: boolean;
  yes?: boolean;
}

export interface InstallOptions extends CommonOptions {
  apiKey?: string;
  noKey?: boolean;
  projectDir?: string;
}

export interface DoctorOptions {
  target: InstallTarget;
  json?: boolean;
  offline?: boolean;
  projectDir?: string;
}

export interface DoctorCheck {
  target: string;
  name: string;
  status: "pass" | "warn" | "fail";
  message: string;
}

export interface FileAction {
  type: "copy" | "write" | "remove" | "skip";
  source?: string;
  destination: string;
  message: string;
}
