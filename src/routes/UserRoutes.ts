import { AxiosError } from 'axios';
import { Request, Response, Router } from 'express';
import { BAD_REQUEST, CREATED, OK,
  NOT_FOUND,
} from 'http-status-codes';
import { ParamsDictionary } from 'express-serve-static-core';

import UserDao from '@daos/UserDao';
import { getToken } from '@api/api.utility';
import { userApi } from '@api/UserApi';
import { User, IUser } from '@models/User';
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
  const body = req.body;

  userDao.create(body).then((user: IUser) => {
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
//  Get User by ID - "POST /api/User/GETOne"
//---------------------------------------------------------
router.post('/GetOne', async (req: Request, res: Response) => {
  const token = getToken(req);
  const body = req.body;

  userDao.getOne(req.body.id).then((user: IUser) => {
    if (user) {
      return res.status(OK).json(user);
    } else {
      return res.status(NOT_FOUND).json({
        success: false,
        error: 'User not found',
      })
    }
  })

});


//---------------------------------------------------------
//  Update - "PUT /api/User/POSTUpdate"
//---------------------------------------------------------
router.post('/POSTUpdate', async (req: Request, res: Response) => {
  const token = getToken(req);
  const user = new User(req.body);

  userDao.update(req.body).then((user: IUser) => {
    if (user) {
      return res.status(OK).json(user);
    } else {
      return res.status(NOT_FOUND).json({
        success: false,
        error: 'User not found',
      })
    }
  })

});

//---------------------------------------------------------
//  Delete - "POST /api/User/PostDelete"
//---------------------------------------------------------
router.post('/POSTDelete', async (req: Request, res: Response) => {
  const token = getToken(req);
  const body = req.body;

  userDao.delete(req.body.id).then((success: boolean) => {
    if (success) {
      return res.status(OK).json({
        success: true,
        error: 'User deleted',
      });
    } else {
      return res.status(NOT_FOUND).json({
        success: false,
        error: 'User not found',
      })
    }
  })

});

//---------------------------------------------------------
//  Authenticate - "POST /api/User/POSTAuthenticate"
//---------------------------------------------------------
router.post('/POSTAuthenticate', async (req: Request, res: Response) => {

});









export default router;
