# worked with Daniel DeCarlo & Yehun Kang
# admin username = admin  
# non-admin username = anything else

import os

# COLORS 
GREEN =  '\033[32m' # Green Text
RED = '\033[31m' # Red Text
CYAN  = "\033[1;36m" # Cyan Text
DEFAULT = '\033[m' # reset to default

# NESTED ARRAY OF FILES
all_files = []

# FILE CLASS
class File:
    def __init__(self,file_name, file_content):
        self.file_name = file_name 
        self.file_content = file_content
        # adds file to all files array
        all_files.append([self.file_name, self.file_content])

# NEW TEMPORARY FILES
tempFile1 = File("red.txt", "DE3C4B")
tempFile2 = File("orange.txt", "D81E5B")
tempFile3 = File("yellow.txt", "FDD235")
tempFile4 = File("green.txt", "335d2d")
tempFile5 = File("blue.txt", "87F5FB")
test_file = File("test.txt", "Hello World")
test_file2 = File("test2.txt", "Helllloooooooo")

# ARRAY OF FILE COMMANDS
file_commands = [["new file", "Create a new file"], ["all files", "Show all files"], ["open", "Open a specific file"], ["update", "Update a specific file"], ["delete", "Delete a specific file"], ["help", "Show list of commands"], ["logout", "Log out of file system"]]

# THE FILE SYSTEM
def runSystem():
  
  # WELCOME MESSAGE
  print(CYAN + "Welcome to the CIS321 Project Very Simple File System!\nType in your username and password", DEFAULT)

  # ACCOUNTS
  user = input("Enter Username: ") # gets username
  admin_access = False # non-admin gets access to read/write files
  
  # CHECKS IF USER = ADMIN
  if(user == 'admin'):
    admin_access = True # admin gets access  to read/write/modify files
  # elif(user != 'admin'):
  #   admin_access = False
    # pwd = "password"
    # guest_pwd = ""
    # pwd_input = input("Enter Password: ")
    # if((pwd_input == pwd) or (pwd_input == guest_pwd)):
      
  # WHILE FILE SYSTEM IS RUNNING      
  print(CYAN +"\nType 'help' to view a list of commands", DEFAULT)

  while (admin_access == True or admin_access == False):
      
      # Asks for user command
        cmd_all = input("Enter File Command: ")
        cmd = ""
        
        # If user command = new file, then ask them for file info
        if(cmd_all == "new file"): 
            file_name = input("Enter File Name (.txt): ") # gets file name
            # returns array [['blue.txt', '87F5FB']]
            search = [x for x in all_files if file_name in x]
            # if there is a 'search result' showing a file with that same name, ask for new file name
            if(len(search)) > 0:
              print("This file name is already taken!! Enter a new file name. ")
              file_name = input("Enter File Name (.txt): ") # gets file name
            file_content = input("Enter File Content: ") # gets file content 
            file1 = File(file_name, file_content) # creates new file
            print(GREEN, "\nAll Files: ", DEFAULT)
            print("------------------------------------------")
            print("File Info           |  File Content\n------------------------------------------")
            for x in range(len(all_files)): 
                # prints the 'index' and the file at that index
                print(f'{[x]} {all_files[x][0]:15} |  {all_files[x][1]:12}')
            print("------------------------------------------\n")   

        # If user command = 'all files', then show all files
        if(cmd_all == "all files"):
            print(GREEN + "\nAll Files: ", DEFAULT)
            print("------------------------------------------")
            print("File Info           |  File Content\n------------------------------------------")
            for x in range(len(all_files)): 
                print(f'{[x]} {all_files[x][0]:15} |  {all_files[x][1]:12}')
            print("------------------------------------------\n")
        
        # If user command = 'open', ask them for a file name to 'open'   
        if(cmd_all == "open"):
            cmd = input("Enter File Name: ") # 'blue.txt'
            print(GREEN + "\nResults: ", DEFAULT)
            print("------------------------------------------")
            print("File Info           |  File Content\n------------------------------------------")
            for x in range(len(all_files)):
            # if file_info in the inode array = the inputted file name
              if(all_files[x][0] == cmd.lower()):
                print(f'{[x]} {all_files[x][0]:15} |  {all_files[x][1]:12}')
            print("------------------------------------------\n")

        # If user command = 'update', ask them for a file to update
        if(cmd_all == "update" and admin_access == False):
          print("Sorry, you can't update files unless you're an admin.\n")
          cmd = input("Enter File Command: ") 
        elif(cmd_all == "update" and admin_access == True):
          cmd = input("Enter File Name: ")
          for x in range(len(all_files)):
          # if file name in the array = the inputted file name
            if(all_files[x][0] == cmd.lower()):
              cmd = input("Enter New File Content: ")
              # save previous file content as a variable
              old_content = all_files[x].pop(1)
              # adds new file content to all files in same place 
              all_files[x].insert(x, cmd)
              print("\nOld Content:", old_content)
              print("Updated Content:", cmd)
          print(CYAN + "\nUpdated Files: ", DEFAULT)
          print("------------------------------------------")
          print("File Info           |  File Content\n------------------------------------------")
          for x in range(0, len(all_files)):
            print(f'{[x]} {all_files[x][0]:15} |  {all_files[x][1]:12}')
          print("------------------------------------------\n")
        
        # If user command = 'delete' and user = admin, ask them for a file to delete
        if(cmd_all == "delete" and admin_access == False):
          print("Sorry, you can't delete files unless you're an admin.\n")
          cmd_all = input("Enter File Command: ")
        elif(cmd_all == "delete" and admin_access == True):
          # type file_name + file_type
          cmd = input("Enter File Name: ") # 'blue.txt'
          print("\nNumber of old files:", len(all_files))
          # for loop that goes through all of the files
          for x in range(len(all_files)-1):
          # if file name in the array = the inputted file name
            if(all_files[x][0] == cmd.lower()):
              # remove the file from all_files ('blue.txt', '87F5FB')
              all_files.pop(x)
          print("Number of current files:", len(all_files))
          print(RED, "\nAll Files:", DEFAULT)
          print("------------------------------------------")
          print("File Info           |  File Content\n------------------------------------------")
          # for loop that prints all the files to show that the file was deleted
          for x in range(len(all_files)):
            print(f'{[x]} {all_files[x][0]:15} |  {all_files[x][1]:12}')
          print("------------------------------------------\n")
      
        # If user command = 'help', show them all the file commands
        if(cmd_all == "help"):
          print(GREEN + "\nCommands:", DEFAULT)
          print("------------------------------------------")
          print("File Commands       |  File Content\n------------------------------------------")
          for x in range(len(file_commands)):
            print(f'{[x]} {file_commands[x][0]:15} |  {file_commands[x][1]:12}')
          print("------------------------------------------\n")
    
        # If user command = "logout", go to login page 
        if(cmd_all == "logout"):
          os.system('clear')
          runSystem()

runSystem()      
