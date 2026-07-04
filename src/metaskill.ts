import { readFile } from "node:fs/promises";

const HTTP_URL_PATTERN = /^https?:\/\//i;

export async function readMetaskill(source: string): Promise<string> {
  if (!HTTP_URL_PATTERN.test(source)) {
    return readFile(source, "utf8");
  }

  const response = await fetch(source);
  if (!response.ok) {
    throw new Error(
      `Failed to download metaskill from ${source}: ${String(response.status)} ${response.statusText}`,
    );
  }

  return response.text();
}
