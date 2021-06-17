import { Request } from 'express';
import { AxiosRequestConfig } from "axios";

export function getToken(req: Request): string {
  if (typeof req.headers.token === "string") {
    return req.headers.token;
  }
  return "";
}

export function getRequestConfig(token: string): AxiosRequestConfig {
  return {
    headers: {
      token: token
    }
  }
}
