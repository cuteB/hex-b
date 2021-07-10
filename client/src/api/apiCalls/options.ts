import { GetToken } from 'utility'

export function getDefaultPostOptions(endpoint: string, obj: any): any {
  let body: string = JSON.stringify(obj);

  return({
    url: '/api/' +  endpoint,
    type: 'POST',
    data: body,
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    headers: { "token" : GetToken() },
  });
}
