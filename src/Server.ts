import cookieParser from 'cookie-parser';
import morgan from 'morgan';
import path from 'path';
import helmet from 'helmet';

import express, { Request, Response, NextFunction } from 'express';
import { BAD_REQUEST } from 'http-status-codes';
import 'express-async-errors';
import db from './db';

import BaseRouter from './routes';

// Init express
const app = express();
//---------------------------------------------------------
//  Basic express Settings
//---------------------------------------------------------
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(cookieParser());

// Show routes called in console during development
if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}

// Security
if (process.env.NODE_ENV === 'production') {
  app.use(helmet());
}

//---------------------------------------------------------
//  Database
//---------------------------------------------------------
db.on('error', console.error.bind(console, 'MongoDB connection error:'))

//---------------------------------------------------------
//  Attach api Routes
//---------------------------------------------------------
app.use('/api', BaseRouter);

// Export express instance
export default app;
