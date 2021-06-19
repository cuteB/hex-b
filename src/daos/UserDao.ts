import User, { IUser, DBUser } from '@models/User';

export interface IUserDao {
  getOne: (email: string) => Promise<IUser | null>;
  getAll: () => Promise<IUser[]>;
  create: (user: IUser) => Promise<IUser>;
  update: (user: IUser) => Promise<void>;
  delete: (id: number) => Promise<void>;
}

class UserDao implements IUserDao {

  /**
  * @param email
  */
  public async getOne(email: string): Promise<IUser | null> {

    // TODO
    return [] as any;
  }

  /**
  *
  */
  public async getAll(): Promise<IUser[]> {
    return DBUser.find({}, (err: any, users: typeof DBUser[]) => {
      if (err) {
        return [];
      }
      console.log(users)
      return users;

    }).catch((err: any[]) => {
      console.log(err)
      return [];
    })

  }

  /**
  *
  * @param user
  */
  public async create(value: IUser): Promise<IUser> {
    let dbo = new DBUser(value)

    return dbo.save()
      .then((res: any) => {
        let user: IUser = new User(res);
        user.Password = ""; // make sure that Password doesn't get returned

        return new User(user);
      })
      .catch((error: any) => {
        return {};
      })
  }

  /**
  *
  * @param user
  */
  public async update(user: IUser): Promise<void> {
    // TODO
    return {} as any;
  }

  /**
  *
  * @param id
  */
  public async delete(id: number): Promise<void> {
    // TODO
    return {} as any;
  }
}

export default UserDao;
