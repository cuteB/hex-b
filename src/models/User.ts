import mongoose from 'mongoose';

export interface IUser {
  Username?: string;
  SystemRights?: string;
  Password?: string;
}

class User implements IUser {
  Username?: string;
  SystemRights?: string;
  Password?: string;

  constructor(UsernameOrUser: string | IUser,
    SystemRights?: string,
    Password?: string,
  ) {
    if (typeof UsernameOrUser === 'string') {
      this.Username = UsernameOrUser;
      this.SystemRights = SystemRights;
      this.Password = Password;
    } else {
      this.Username = UsernameOrUser.Username;
      this.SystemRights = UsernameOrUser.SystemRights;
      this.Password = UsernameOrUser.Password;
    }
  }
}

//---------------------------------------------------------
//  DB Model
//---------------------------------------------------------
const _DBUser = new mongoose.Schema(
  {
    Username: { type: String, required: true },
    SystemRights: { type: String, required: true },
    Password: { type: String, required: true },
  },
  { timestamps: true },
);

export const DBUser = mongoose.model('users', _DBUser);
export default User;
