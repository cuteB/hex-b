import { IUser, User, UserDoc } from '@models/User';

export interface IUserDao {
  getOne: (email: string) => Promise<IUser | null>;
  getAll: () => Promise<IUser[]>;
  create: (user: IUser) => Promise<IUser>;
  update: (user: IUser) => Promise<IUser>;
  delete: (id: number) => Promise<boolean>;
}

class UserDao implements IUserDao {

  /**
  * @param email
  */
  public async getOne(id: string): Promise<IUser | null> {
    return User.findOne({ _id: id }).then((res: IUser) => {
      if (res) {
        return res;
      } else {
        return null
      }
    }).catch((err: any) => {
      console.log(err);
      return null;
    })

  }

  /**
  *
  */
  public async getAll(): Promise<IUser[]> {
    return User.find({}, (err: any, users: IUser[]) => {
      if (err) {
        return [];
      }
      return users;

    }).catch((err: any[]) => {
      console.log(err) // Keep Console
      return [];
    })

  }

  /**
  *
  * @param user
  */
  public async create(value: IUser): Promise<UserDoc | null> {
    let dbo = new User(value)

    return dbo.save()
      .then((res: any) => {
        let user: IUser = new User(res);
        user.password = ""; // make sure that Password doesn't get returned

        return new User(user);
      })
      .catch((error: any) => {
        console.log(error);
        return null;
      })
  }

  /**
  *
  * @param user
  */
  public async update(user: IUser): Promise<UserDoc | null> {

    return User.findOneAndUpdate(
      { _id: user._id },
      user,
      { new: true }, // return new document
    ).then((res: IUser) => {
      if (res) {
        return res;
      } else {
        return null
      }
    }).catch((err: any) => {
      console.log(err);
      return null;
    })
  }

  /**
  *
  * @param id
  */
  public async delete(id: number): Promise<boolean> {

    return User.deleteOne({ _id: id }).then((res: any) => {
      if (res.deletedCount && res.deletedCount !== 0) {
        return true;
      } else {
        return false;
      }
    }).catch((err: any) => {
      console.log(err);
      return null;
    })

  }
}

export default UserDao;
