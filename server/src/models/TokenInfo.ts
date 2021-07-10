export interface ITokenInfo {
  InternalID?: number;
  StartDateTime?: string;
  ExpirationDateTime?: string;
  SystemAccess?: string;
}

class TokenInfo implements ITokenInfo {
  InternalID?: number;
  StartDateTime?: string;
  ExpirationDateTime?: string;
  SystemAccess?: string;

  constructor(InternalIDOrTokenInfo: number | ITokenInfo,
    StartDateTime?: string,
    ExpirationDateTime?: string,
    SystemAccess?: string,
  ) {
    if (typeof InternalIDOrTokenInfo === 'number') {
      this.InternalID = InternalIDOrTokenInfo;
      this.StartDateTime = StartDateTime;
      this.ExpirationDateTime = ExpirationDateTime;
      this.SystemAccess = SystemAccess;

    } else {
      this.InternalID = InternalIDOrTokenInfo.InternalID;
      this.StartDateTime = InternalIDOrTokenInfo.StartDateTime;
      this.ExpirationDateTime = InternalIDOrTokenInfo.ExpirationDateTime;
      this.SystemAccess = InternalIDOrTokenInfo.SystemAccess;
    }
  }
}

export default TokenInfo;
