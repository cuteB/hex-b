import { Api } from './api';
import { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';
import User from '@models/User';
import TokenInfo from '@models/TokenInfo';
import { apiConfig } from '@api/api.config';
import { getRequestConfig } from '@api/api.utility';
import { UserEndpoints } from '@api/api.endpoints'

/**
 *  Put all of the api calls for users in here.
 *
 * import { userApi } from '@api/UserApi';
 *
 * userApi.userLogin(IUser);
 *
 */

export class UserApi extends Api {
  constructor (config: AxiosRequestConfig) {
    super (config)

    // this middleware is been called right before the http request is made.
    this.api.interceptors.request.use((param: AxiosRequestConfig) => ({
      ...param,
    }));

    // this middleware is been called right before the response is get it by the method that triggers the request
    this.api.interceptors.response.use((param: AxiosResponse) => ({
      ...param
    }));
  }

  /**
   * Login user
   * @param  credentials UserCredentials, username + password
   * @return string token
   */
  userLogin = (credentials: User): Promise<User> => {
    let endpoint = UserEndpoints.getToken;
    let body: User = new User(credentials);

    return this.post<string, User, AxiosResponse<string>>(endpoint, body)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((error: AxiosError<Error>) => {
        return Promise.reject(error);
      });
  }
  /**
   * Get All Users
   * @return List users
   */
  getListUser = (token: string): Promise<User[]> => {
    let endpoint = UserEndpoints.getList;
    let body = {}
    let config: AxiosRequestConfig = getRequestConfig(token);

    return this.post<User[], any, AxiosResponse<User>>(endpoint, body, config)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((error: AxiosError<Error>) => {
        return Promise.reject(error);
      });
  }

  /**
   * Get User by ID
   * @param  credentials UserCredentials, username + password
   * @return string token
   */
  getUserByID = (user: User, token: string): Promise<User> => {
    let _userID = user.InternalID || 0;

    return this.getListUser(token).then((res: User[]) => {
      let returnUser = new User(0);
      res.forEach((userInList: User) => {
        if (Number(userInList.InternalID) === Number(_userID)) {
          returnUser = userInList
        }
      })
      return returnUser;
    })

  }

  /**
   * Update or create a user
   * Sending internalID === 0 will create a new user
   * @param  token user token
   * @return New Updated/Created user
   */
  updateUser = (user: User, token: string): Promise<User> => {
    let endpoint = UserEndpoints.update;
    let body = user;
    let config: AxiosRequestConfig = getRequestConfig(token);

    return this.post<User, User, AxiosResponse<User>>(endpoint, body, config)
      .then((response: AxiosResponse) => {
        return response.data;
      })
      .catch((error: AxiosError<Error>) => {
        return Promise.reject(error);
      });
  }

}

export const userApi = new UserApi(apiConfig);
