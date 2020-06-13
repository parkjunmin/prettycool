import { Command } from "commander";
//@ts-ignore
import { version } from "../package.json";
import { CensysIpv4Service } from "./services/censys.service";
import { CrtShService } from "./services/crtsh.service";
import { HunterService } from "./services/hunter.service";
import Target from "./services/target";
import cheerio from "cheerio";
import Hermes from "hermes-http";
const prettyCool = new Command();

prettyCool
    .version(version)
    .option("-c, --company <company>", "Define company name")
    .option("-d, --domain <domain>", "Define domain of company")
    .allowUnknownOption(false);

prettyCool.parse(process.argv);

if (!prettyCool.domain || !prettyCool.company) {
    prettyCool.help();
    process.exit(1);
}

// const target = new Target(prettyCool.domain, prettyCool.company);

// target.save().then(async () => {
//     const hunter = new HunterService(target);
//     const dataHunter = await hunter.query();
//     hunter.save(dataHunter);
//     const censysIp = new CensysIpv4Service(target);
//     const censysData = await censysIp.query();
//     await censysIp.save(censysData);
//     const crt = new CrtShService(target);
//     const data = await crt.query();
//     console.log(JSON.stringify(data, null, 4));
// });
