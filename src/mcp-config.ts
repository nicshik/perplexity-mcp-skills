import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import type { CommonOptions, FileAction } from "./types.js";

interface JsonObject {
  [key: string]: unknown;
}

export function expectedPerplexityServer(apiKey?: string) {
  const env: Record<string, string> = {};
  if (apiKey) env.PERPLEXITY_API_KEY = apiKey;
  return {
    command: "npx",
    args: ["-y", "@perplexity-ai/mcp-server"],
    ...(apiKey ? { env } : {}),
  };
}

function readJsonIfExists(filePath: string): JsonObject {
  if (!fs.existsSync(filePath)) return {};
  return JSON.parse(fs.readFileSync(filePath, "utf8")) as JsonObject;
}

export async function upsertPerplexityMcpServer(
  filePath: string,
  apiKey: string | undefined,
  options: CommonOptions,
): Promise<FileAction> {
  const config = readJsonIfExists(filePath);
  const mcpServers = typeof config.mcpServers === "object" && config.mcpServers !== null ? config.mcpServers as JsonObject : {};
  const current = typeof mcpServers.perplexity === "object" && mcpServers.perplexity !== null ? mcpServers.perplexity as JsonObject : {};
  const next = {
    ...current,
    ...expectedPerplexityServer(apiKey),
  };
  if (!apiKey && typeof current.env === "object" && current.env !== null) {
    next.env = current.env as Record<string, string>;
  }
  config.mcpServers = {
    ...mcpServers,
    perplexity: next,
  };

  if (!options.dryRun) {
    await fsp.mkdir(path.dirname(filePath), { recursive: true });
    await fsp.writeFile(filePath, `${JSON.stringify(config, null, 2)}\n`, "utf8");
  }

  return {
    type: "write",
    destination: filePath,
    message: `${options.dryRun ? "Would update" : "Updated"} Perplexity MCP config at ${filePath}`,
  };
}

export async function removePerplexityMcpServer(filePath: string, options: CommonOptions): Promise<FileAction> {
  if (!fs.existsSync(filePath)) {
    return {
      type: "skip",
      destination: filePath,
      message: `${filePath} does not exist`,
    };
  }

  const config = readJsonIfExists(filePath);
  const mcpServers = typeof config.mcpServers === "object" && config.mcpServers !== null ? config.mcpServers as JsonObject : {};
  const current = typeof mcpServers.perplexity === "object" && mcpServers.perplexity !== null ? mcpServers.perplexity as JsonObject : undefined;
  const packageOwned = current?.command === "npx" && Array.isArray(current.args) && current.args.includes("@perplexity-ai/mcp-server");

  if (!packageOwned && !options.force) {
    return {
      type: "skip",
      destination: filePath,
      message: `${filePath} has a non-standard Perplexity MCP entry; use --force to remove it`,
    };
  }

  delete mcpServers.perplexity;
  config.mcpServers = mcpServers;

  if (!options.dryRun) {
    await fsp.writeFile(filePath, `${JSON.stringify(config, null, 2)}\n`, "utf8");
  }

  return {
    type: "write",
    destination: filePath,
    message: `${options.dryRun ? "Would remove" : "Removed"} Perplexity MCP config from ${filePath}`,
  };
}

export function hasExpectedPerplexityMcpServer(filePath: string) {
  if (!fs.existsSync(filePath)) return false;
  try {
    const config = readJsonIfExists(filePath);
    const servers = config.mcpServers as JsonObject | undefined;
    const perplexity = servers?.perplexity as JsonObject | undefined;
    return perplexity?.command === "npx" && Array.isArray(perplexity.args) && perplexity.args.includes("@perplexity-ai/mcp-server");
  } catch {
    return false;
  }
}

export function hasPerplexityApiKeyInConfig(filePath: string) {
  if (!fs.existsSync(filePath)) return false;
  try {
    const config = readJsonIfExists(filePath);
    const servers = config.mcpServers as JsonObject | undefined;
    const perplexity = servers?.perplexity as JsonObject | undefined;
    const env = perplexity?.env as Record<string, string> | undefined;
    return Boolean(env?.PERPLEXITY_API_KEY);
  } catch {
    return false;
  }
}
