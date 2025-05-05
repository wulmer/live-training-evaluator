import { BACKEND } from '$env/static/private';

export function load() {
  return {
    backendUrl: BACKEND,
  }
}
