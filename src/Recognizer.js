import { existsSync, readFile } from "fs";
import { createWorker } from "tesseract.js";

export class Recognizer {
  constructor() {}

  async getTextFromImagemPath(path) {
    const promise = new Promise(async (resolve, reject) => {
      const worker = await createWorker("eng");

      if (!existsSync(path)) {
        reject("File not found");
      }

      readFile(path, async (err, data) => {
        if (err) reject(err);

        const ret = await worker.recognize(data);

        worker.terminate();

        resolve(this.normalize(ret.data.text));
      });
    });

    return promise;
  }

  normalize(text) {
    text = text.toUpperCase();
    text = text.replace(/['`-]/g, "");
    return text.replace(/[^A-Z0-9]/gi, "");
  }
}
