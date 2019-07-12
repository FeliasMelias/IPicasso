
import time
import sys

# path and name of the log file
logfile = 'logfile.log'

# function to save log messages to specified log file
def log(msg):

  # open the specified log file
  file = open(logfile,"a")

  # write log message with timestamp to log file
  file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))

  # close log file
  file.close

# main function

def clearLogFile():
    with open(logfile, "w") as file:
        pass


def main():
  # create new log message
  log("Eine neue Nachricht für die Log-Datei")

  # quit python script
  sys.exit(0)

if __name__ == '__main__':
  main()
