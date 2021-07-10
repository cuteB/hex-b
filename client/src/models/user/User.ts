export interface User {
  _id?: string;
  username: string;
  systemRights: string;
  password?: string;
}

export const defaultUser: User = {
  username: "",
  systemRights: "",
}
