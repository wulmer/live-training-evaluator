import { writable } from "svelte/store";

export const backendUrlStore = writable(
  "http://ulw2si-lte-backend-container-24231.westeurope.azurecontainer.io:8000",
);

export const timeSpanMin = writable(60);