import mongoose from 'mongoose';

export interface IUser {
  InternalID?: number;
  Username?: string;
  Password?: string,
  SystemRights?: string;
  UserFullName?: string;
  EmailAddress?: string;
 }

class User implements IUser {
  InternalID?: number;
  Username?: string;
  Password?: string;
  SystemRights?: string;
  UserFullName?: string;
  EmailAddress?: string;

  constructor(InternalIDOrUser: number | IUser,
    Username?: string,
    Password?: string,
    SystemRights?: string,
    UserFullName?: string,
    EmailAddress?: string,
  ) {
    if (typeof InternalIDOrUser === 'number') {
      this.InternalID = InternalIDOrUser;
      this.Username = Username || "",
      this.Password = Password || "",
      this.SystemRights = SystemRights || "";
      this.UserFullName = UserFullName || "";
      this.EmailAddress = EmailAddress || "";

    } else {
      this.InternalID = InternalIDOrUser.InternalID;
      this.Username = InternalIDOrUser.Username;
      this.Password = InternalIDOrUser.Password;
      this.SystemRights = InternalIDOrUser.SystemRights;
      this.UserFullName = InternalIDOrUser.UserFullName;
      this.EmailAddress = InternalIDOrUser.EmailAddress;
    }
  }
}

export default User;
