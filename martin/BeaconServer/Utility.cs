using System.Runtime.CompilerServices;

namespace NSBeaconServer
{
    public class CUtility
    {
        public static string TraceMessage(
            [CallerLineNumber] int lineNumber = 0,
            [CallerMemberName] string callerMethod = null,
            [CallerFilePath] string filePath = null)
        {
            string cm = null;

            if (callerMethod == null)
            {
                cm = ":-unknown-";
            }
            else
            {
                cm = ":" + callerMethod + "()";
            }

            string fp = null;

            if (filePath == null)
            {
                fp = "-unknown-";
            }
            else
            {
                var fps = filePath.Split('/');
                fp = fps[fps.Length - 1];
                fp += ":";
            }

            return fp + lineNumber.ToString() + cm;
        }
    }
}