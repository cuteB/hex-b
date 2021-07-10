import { defaultApiCall, UserEndpoints } from 'api';
import {
  IUser, defaultUser,
} from 'models';

// GET All
export async function GETAllUser(): Promise<IUser[]> {
  let body: any = {}
  return defaultApiCall<IUser, IUser[]>(UserEndpoints.getAll, body, []);
}

// GET One
export async function GETOneUser(id: string): Promise<IUser> {
  let body: any = { _id: id }
  return defaultApiCall<IUser, IUser>(UserEndpoints.getOne, body, defaultUser);
}

// POST Create
export async function POSTCreateUser(value: IUser): Promise<IUser> {
  let body: any = value;
  return defaultApiCall<IUser, IUser>(UserEndpoints.create, body, defaultUser);
}

// POST Update
export async function POSTUpdateUser(value: IUser): Promise<IUser> {
  let body: any = value;
  return defaultApiCall<IUser, IUser>(UserEndpoints.update, body, defaultUser);
}

// POST Delete
export async function POSTDeleteUser(value: IUser): Promise<IUser> {
  let body: any = value;
  return defaultApiCall<IUser, IUser>(UserEndpoints.delete, body, defaultUser);
}

// Authenticate
export async function POSTAuthenticateUser(value: IUser): Promise<string> {
  let body: any = value;
  return defaultApiCall<IUser, string>(UserEndpoints.authenticate, body, "");
}
