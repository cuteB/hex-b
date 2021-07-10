import { RouteComponentProps } from 'react-router';

export interface PathParamKeys {
  // ids in path
  userID?: string;
}

export interface AppPathParams {
  // systemRights
  // modal, header actions
}

export type PathProps =
  RouteComponentProps<PathParamKeys> &
  AppPathParams

export interface Path {
  path: string,
  id: string,
  component: any,
  exact?: boolean,
}
