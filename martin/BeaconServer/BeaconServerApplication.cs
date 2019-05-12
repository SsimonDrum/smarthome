using System;
using NLog;

namespace NSBeaconServer
{
    class CBeaconArgParser : CArgumentParser
    {
        public static bool processConfigFile(string[] sa)
        {
            return true;
        }

        public static bool printHelp(string[] sa)
        {
            return true;
        }
    };

    class BeaconServerApplication
    {
        public static Logger logger = NLog.LogManager.GetCurrentClassLogger();



        static int Main(string[] args)
        {
            Console.WriteLine(CUtility.TraceMessage()); // TODO: delete
            
            var argParser = new CBeaconArgParser();
            argParser.addArgument("-h", 0, "get help for program", CBeaconArgParser.printHelp, "--help");
            argParser.addArgument("-c", 1, "specify path to configuretaion file", CBeaconArgParser.processConfigFile, "--config-file");
            argParser.parseArguments(args);

            return 0;
        }
    }
}