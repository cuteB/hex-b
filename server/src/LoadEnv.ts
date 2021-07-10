import dotenv from 'dotenv';
import commandLineArgs from 'command-line-args';

// Setup command line options
const options = commandLineArgs([
  {
    name: 'env',
    alias: 'e',
    defaultValue: process.env.NODE_ENV,
    type: String,
  },
]);

const environment = process.env.NODE_ENV || "development";
// Set the env file
const result2 = dotenv.config({
  path: `./env/${environment}.env`,
});

if (result2.error) {
  throw result2.error;
}
