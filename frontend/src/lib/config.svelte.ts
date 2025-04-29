import { writable } from "svelte/store";

export const backendUrlStore = writable(
  "",
);

export const timeSpanMin = writable(60);