import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import type { CommonOptions, FileAction } from "./types.js";

export async function copyPath(source: string, destination: string, options: CommonOptions): Promise<FileAction> {
  if (!fs.existsSync(source)) {
    throw new Error(`Source not found: ${source}`);
  }

  if (path.resolve(source) === path.resolve(destination)) {
    return {
      type: "skip",
      source,
      destination,
      message: `${destination} is already the source path`,
    };
  }

  if (fs.existsSync(destination) && !options.force) {
    return {
      type: "skip",
      source,
      destination,
      message: `${destination} already exists; use --force to replace it`,
    };
  }

  if (!options.dryRun) {
    await fsp.mkdir(path.dirname(destination), { recursive: true });
    await fsp.cp(source, destination, { recursive: true, force: Boolean(options.force) });
  }

  return {
    type: "copy",
    source,
    destination,
    message: `${options.dryRun ? "Would copy" : "Copied"} ${source} -> ${destination}`,
  };
}

export async function writeText(destination: string, body: string, options: CommonOptions): Promise<FileAction> {
  if (!options.dryRun) {
    await fsp.mkdir(path.dirname(destination), { recursive: true });
    await fsp.writeFile(destination, body, "utf8");
  }

  return {
    type: "write",
    destination,
    message: `${options.dryRun ? "Would write" : "Wrote"} ${destination}`,
  };
}

export async function removePath(destination: string, options: CommonOptions): Promise<FileAction> {
  if (!fs.existsSync(destination)) {
    return {
      type: "skip",
      destination,
      message: `${destination} is not installed`,
    };
  }

  if (!options.dryRun) {
    await fsp.rm(destination, { recursive: true, force: true });
  }

  return {
    type: "remove",
    destination,
    message: `${options.dryRun ? "Would remove" : "Removed"} ${destination}`,
  };
}

export function printActions(actions: FileAction[]) {
  for (const action of actions) {
    console.log(`- ${action.message}`);
  }
}
