import { installTarget } from "./install.js";
import type { InstallOptions, InstallTarget } from "./types.js";

export async function syncTarget(target: InstallTarget, options: InstallOptions) {
  return installTarget(target, { ...options, force: true, noKey: true });
}
