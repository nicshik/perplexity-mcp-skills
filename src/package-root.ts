import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function packageRoot() {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const candidates = [
    path.resolve(here, ".."),
    path.resolve(here, "..", ".."),
    process.cwd(),
  ];

  for (const candidate of candidates) {
    const packageJson = path.join(candidate, "package.json");
    if (!fs.existsSync(packageJson)) continue;
    try {
      const parsed = JSON.parse(fs.readFileSync(packageJson, "utf8")) as { name?: string };
      if (parsed.name === "perplexity-mcp-skills") return candidate;
    } catch {
      continue;
    }
  }

  return path.resolve(here, "..");
}

export function fromRoot(...parts: string[]) {
  return path.join(packageRoot(), ...parts);
}
