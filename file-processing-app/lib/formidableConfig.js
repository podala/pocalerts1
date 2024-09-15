import formidable from 'formidable';
import path from 'path';

export const parseForm = (req) => {
  const form = new formidable.IncomingForm();
  form.uploadDir = path.join(process.cwd(), '/uploads');
  form.keepExtensions = true;  // Preserve file extensions

  return new Promise((resolve, reject) => {
    form.parse(req, (err, fields, files) => {
      if (err) reject(err);
      resolve({ fields, files });
    });
  });
};
