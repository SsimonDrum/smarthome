using System;
using System.Collections.Generic;

namespace NSBeaconServer
{
    class CArgumentParser
    {
        public CArgumentParser()
        {
        }

        public void addArgument(string shortParam, uint numArguments, string help, Func<string[], bool> action, string longParam = null)
        {
            var val = Tuple.Create(numArguments, help, action);

            arguments.Add(shortParam, val);
            values.Add(shortParam, null);

            if (longParam != null)
            {
                arguments.Add(longParam, val);
                values.Add(longParam, null);
            }
        }

        public void parseArguments(string[] args)
        {
            foreach (var arg in args)
            {
                Console.WriteLine(arg);
            }
        }

        // map of "short" and "long" version of argument to touple (number of params per argument, help string, and processing callback)
        private Dictionary<string, Tuple<uint, string, Func<string[], bool>>> arguments = new Dictionary<string, Tuple<uint, string, Func<string[], bool>>>();

        // map of "short" and "long" version of argument to actual value
        private Dictionary<string, string[]> values = new Dictionary<string, string[]>();
    };
}