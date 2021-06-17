import User, { IUser } from '@models/User';
import UserDao from '@daos/UserDao';

class _UserController {

  authenticateUser = (user: IUser): IUser => {
    if (user.Username === "cuteB" && user.Password === "password") {
      return new User(2, "cuteB", "", "admin", "bran", "e@ma.l")
    } else {
      return null;
    }

  }
}

export const UserController = new _UserController;
