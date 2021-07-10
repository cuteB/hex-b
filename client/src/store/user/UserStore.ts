import { Action, Reducer } from 'redux';
import { AppThunkAction } from '../';
import { IUser, defaultUser } from 'models';
import {
  GETAllUser,
  GETOneUser,
} from 'api';

//---------------------------------------------------------
//  State
//---------------------------------------------------------

export interface UserState {
  isAllUserLoading: boolean;
  isCurrentUserLoading: boolean;
  allUser: IUser[];
  currentUser: IUser;
}

const unloadedState: UserState = {
  isAllUserLoading: false,
  isCurrentUserLoading: false,
  allUser: [],
  currentUser: defaultUser,
}

//---------------------------------------------------------
//  Actions
//---------------------------------------------------------
interface RequestAllUserAction {
  type: 'REQUEST_ALL_USER_DATA';
}

interface ReceiveAllUserAction {
  type: 'RECEIVE_ALL_USER_DATA',
  allUser: IUser[],
}

interface RequestCurrentUserAction {
  type: 'REQUEST_CURRENT_USER_DATA';
}

interface ReceiveCurrentUserAction {
  type: 'RECEIVE_CURRENT_USER_DATA',
  currentUser: IUser,
}

type KnownAction =
  RequestAllUserAction | ReceiveAllUserAction |
  RequestCurrentUserAction | ReceiveCurrentUserAction;

//---------------------------------------------------------
//  Action Creators
//---------------------------------------------------------
export const actionCreators = {

  requestAllUser: () : AppThunkAction<KnownAction> => (dispatch, getState) => {
    const appState = getState();
    if (appState && appState.User
      && !appState.User.isAllUserLoading
      && appState.User.allUser && appState.User.allUser.length !== 0
    ) {
      GETAllUser().then((res: any) => {
        dispatch({ type: 'RECEIVE_ALL_USER_DATA', allUser: res, });
      });

      dispatch({ type: 'REQUEST_ALL_USER_DATA' });
    }
  },

  requestUserByID: (id: string) : AppThunkAction<KnownAction> => (dispatch, getState) => {
    const appState = getState();
    if (appState && appState.User
      && !appState.User.isCurrentUserLoading
      && id !== ""
    ) {
      GETOneUser(id).then((res: any) => {
        dispatch({ type: 'RECEIVE_ALL_USER_DATA', allUser: res, });
      });

      dispatch({ type: 'REQUEST_ALL_USER_DATA' });
    }
  },

}

//---------------------------------------------------------
//  Reducer
//---------------------------------------------------------
export const reducer: Reducer<UserState> = (state: UserState | undefined, incomingAction: Action): UserState => {
  if (state === undefined) {
    return unloadedState;
  }

  const action = incomingAction as KnownAction;
  switch (action.type) {

    case 'REQUEST_ALL_USER_DATA':
      return {
        ...state,
        isAllUserLoading: true,
      };

    case 'RECEIVE_ALL_USER_DATA':
      return {
        ...state,
        isAllUserLoading: false,
        allUser: action.allUser,
      };

    default:
      return state;
  }
}
