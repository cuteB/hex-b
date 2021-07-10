import * as $ from 'jquery';

import {
  getDefaultPostOptions,
} from './options';

export async function defaultApiCall<T, R>(endPoint: string, obj: T, defaultObj: R): Promise<R> {
  try {
    let postForm = () => {
      return $.ajax( getDefaultPostOptions(endPoint, obj) ).done((data) => {
        return data;
      }).then((res) => {
        return res;
      }).fail((xhr, status, err) => {
        console.log(status); // keep console

        return null;
      });
    };
    let res: R = await postForm();

    if (res) {
      return res;
    } else {
      return defaultObj;
    }

  } catch (err) {
    return defaultObj;
  }
}
