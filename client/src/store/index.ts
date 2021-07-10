import * as UserStore from './user/UserStore';

export interface ApplicationState {
  User: UserStore.UserState | undefined;
}

export const reducers = {
  User: UserStore.reducer
}

export interface AppThunkAction<TAction> {
  (dispatch: (action: TAction) => void, getState: () => ApplicationState): void;
}

export type UserStoreProps =
  UserStore.UserState &
  typeof UserStore.actionCreators;
