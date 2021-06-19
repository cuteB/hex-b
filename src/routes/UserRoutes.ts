import { AxiosError } from 'axios';
import { Request, Response, Router } from 'express';
import { BAD_REQUEST, CREATED, OK,
  NOT_FOUND,
} from 'http-status-codes';
import { ParamsDictionary } from 'express-serve-static-core';

import UserDao from '@daos/UserDao';
import { getToken } from '@api/api.utility';
import { userApi } from '@api/UserApi';
import User, { IUser } from '@models/User';
import { UserController } from '@controllers/UserController';

// Init shared
const router = Router();
const userDao = new UserDao();

//---------------------------------------------------------
//  Create - "POST /api/User/POSTCreate"
//---------------------------------------------------------
router.post('/POSTCreate', async (req: Request, res: Response) => {
  if (!req.body) {
    return res.status(BAD_REQUEST).json({
      success: false,
      error: 'Need to provide a valid user'
    });
  }

  const token = getToken(req);
  const user = new User(req.body);

  userDao.create(user).then((user: IUser) => {
    if (user) {
      return res.status(OK).json(user);
    } else {
      return res.status(BAD_REQUEST).json({
        success: false,
        error: 'fail'
      })
    }
  })

});

//---------------------------------------------------------
//  Get All Users - "POST /api/User/GETAll"
//---------------------------------------------------------
router.post('/GETAll', async (req: Request, res: Response) => {
  const token = getToken(req);

  userDao.getAll().then((users: IUser[]) => {
    console.log(users)
    if (users.length === 0) {
      return res.status(NOT_FOUND).json({
        success: false,
        error: 'Users not found',
      })
    }

    return res.status(OK).json(users);
  })

});

//---------------------------------------------------------
//  Update - "PUT /api/User/POSTUpdate"
//---------------------------------------------------------
// router.post('/POSTUpdate', async (req: Request, res: Response) => {
//   const token = getToken(req);
//   const user = new User(req.body);
//
//   userApi.updateUser(user, token).then((response: User) => {
//     return res.status(OK).json(response);
//   }).catch((error: AxiosError<Error>) => {
//     return res.status(BAD_REQUEST).json(error.response.data);
//   });
//
// });

//---------------------------------------------------------
//  Authenticate - "POST /api/User/POSTAuthenticate"
//---------------------------------------------------------
// router.post('/POSTAuthenticate', async (req: Request, res: Response) => {
//   let creds: User = new User(req.body)
//
//   let responseUser: User = UserController.authenticateUser(creds)
//
//   if (responseUser) {
//     return res.status(OK).json(responseUser)
//
//   } else {
//     return res.status(BAD_REQUEST).json({error: "bad login"});
//
//   }
//
// });



//---------------------------------------------------------
//
//---------------------------------------------------------
// router.post('/GETByID', async (req: Request, res: Response) => {
//   const token = getToken(req);
//   const user = new User(req.body);
//
//   userApi.getUserByID(user, token).then((response: User) => {
//     // TODO handle errors. possible to return an error
//     return res.status(OK).json(response);
//   }).catch((error: AxiosError<Error>) => {
//     // maybe change to BAD_REQUEST although not really bad just wrong user/pass
//     return res.status(OK).json([]);
//   });
// });



//---------------------------------------------------------
//  Delete - "DELETE /api/User/delete/:id"
//---------------------------------------------------------
// router.delete('/delete/:id', async (req: Request, res: Response) => {
//   const { id } = req.params as ParamsDictionary;
//   await userDao.delete(Number(id));
//   return res.status(OK).end();
// });

//---------------------------------------------------------
//  Check Token - "POST /api/User/POSTUpdate"
//---------------------------------------------------------
// router.post('/POSTCheckToken', async (req: Request, res: Response) => {
//   const token = getToken(req);
//
//   userApi.checkToken(token).then((response: User) => {
//     return res.status(OK).json(response);
//   }).catch((error: AxiosError<Error>) => {
//     return res.status(BAD_REQUEST).json(error.response.data);
//   });
// });

//---------------------------------------------------------
//  Export
//---------------------------------------------------------

export default router;
