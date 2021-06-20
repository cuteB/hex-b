import mongoose from 'mongoose';
import bcrypt from 'bcrypt-nodejs';
import uniqueValidator from 'mongoose-unique-validator';

// remove deprication warnings for unique
mongoose.set('useNewUrlParser', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useCreateIndex', true);

//---------------------------------------------------------
//  Interfaces
//---------------------------------------------------------
export interface IUser {
  _id?: string;
  username: string;
  systemRights: string;
  password: string;
}

export interface UserDoc extends mongoose.Document {
  username: string;
  systemRights: string;
  password: string;

  // methods and such
  generateHash: (password: string) => string;
  validPassword: (password: string) => string;
}

export interface IUserModel extends mongoose.Model<UserDoc> {
  build(attr: IUser): any;
  generateHash(password: string): string;
  validPassword(password: string): boolean;
}

//---------------------------------------------------------
//  DB Model
//---------------------------------------------------------
const userSchema = new mongoose.Schema(
  {
    username: {
      type: String,
      required: true,
      index: { unique: true, dropDups: true },
    },
    systemRights: {
      type: String,
      required: true
    },
    password: {
      type: String,
      required: true,
      select: false,
    },
  },
  { timestamps: true },
);

//---------------------------------------------------------
//  Functions
//---------------------------------------------------------
// constructor
userSchema.statics.build = (attr: IUser) => {
  return new User(attr);
}

// Hash password
userSchema.methods.generateHash = function(
  this: UserDoc,
  password: string,
) {
  return bcrypt.hashSync(password, bcrypt.genSaltSync(8));
}

// Check password is valid
userSchema.methods.validPassword = function(
  this: UserDoc,
  password: string,
) {
  return bcrypt.compareSync(password, this.password);
}

//---------------------------------------------------------
//  Middleware
//---------------------------------------------------------
// hash password before save
userSchema.pre("save", function(
  this: UserDoc,
  next: () => void,
) {
  if (this.isModified("password")) {
    this.password = this.generateHash(this.password);
  }

  next();
})

/* don't need these password functions but will keep these demos
// remove password
userSchema.post("find", function(doc: UserDoc[]) {
  if (doc) {
    doc.forEach((user: UserDoc) => {
      user.password = ""
    })
  }
})

// remove password
userSchema.post("findOne", function(doc: UserDoc) {
  if (doc) {
    doc.password = "";
  }
})
*/

userSchema.plugin(uniqueValidator);

export const User = mongoose.model<UserDoc, IUserModel>('User', userSchema);
