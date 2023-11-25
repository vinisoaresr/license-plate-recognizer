import { Recognizer } from "./src/Recognizer.js";

const rec = new Recognizer();

const plate = await rec.getTextFromImagemPath("./assets/placa.png");

console.log(plate);
