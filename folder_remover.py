import re
import shutil
import os
import datetime

class Folder_Remover(object):
    def __init__(self):
        self.root_folder = r'ENTER_PATH_TO_ROOT_FOLDER'
        self.folder_to_remove = []
        self.folder_to_keep = []
        self.extracted_folders = []
        self.log = open('log_deleted.txt', 'w')

    def print_folder_info(self, folder_prfix, folder_full_path, timestamp):
        print ""
        print "###################"
        print "folder name      :   {0}".format(os.path.basename(folder_full_path))
        print "folder prefix    :   {0}".format(folder_prfix)
        print "folder timestamp :   {0}".format(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        print "folder path      :   {0}".format(folder_full_path)
        print "###################"
        print ""

    def remove_old_folder(self, oldFolder, newFolder):
        print "##################      {0}                                 |                       {1}".format("Old Folder", "New Folder")
        print "folder name      :      {0}             |       {1}".format(os.path.basename(oldFolder[1]), os.path.basename(newFolder[1]))
        print "folder prefix    :      {0}                    |       {1}".format(oldFolder[2], newFolder[2])
        print "folder timestamp :      {0}                        |       {1}".format(oldFolder[0].strftime("%Y-%m-%d %H:%M:%S"), newFolder[0].strftime("%Y-%m-%d %H:%M:%S"))
        print "folder path      :      {0}         |       {1}".format(oldFolder[1], newFolder[1])
        print "###################"
        print ""

        self.folder_to_remove.append(oldFolder[1])
        self.folder_to_keep.append(newFolder[1])

    def find_dup_folders(self, path, regex):
        folder_dict = {}
        dirs = [os.path.join(path, folder) for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        if len(dirs) <= 1:
            return

        for folder in dirs:
            x = (re.search(regex, folder))

            if x == None:
                continue

            folder_prfix = x.group()
            #if x =
            timestamp = datetime.datetime.fromtimestamp(os.path.getctime(folder))

            self.print_folder_info(folder_prfix, folder, timestamp)

            # collision
            if folder_prfix in folder_dict:
                folder_dict_val = folder_dict[folder_prfix]
                timestamp_dict_val = folder_dict_val[0]

                if timestamp_dict_val < timestamp:

                    old_folder = (folder_dict_val[0], folder_dict_val[1], folder_prfix)
                    new_folder = (timestamp, folder, folder_prfix)
                    print '#### Newer folder found ###'
                    print '#### remove old folder ###'
                    self.remove_old_folder(old_folder, new_folder)
                    folder_dict[folder_prfix] = (timestamp, folder)

                # folder that found is not the latest
                else:
                    print '#### remove old folder ###'
                    new_folder = (folder_dict_val[0], folder_dict_val[1], folder_prfix)
                    old_folder = (timestamp, folder, folder_prfix)
                    self.remove_old_folder(old_folder, new_folder)

            # folder does not exist add to dict
            else:
                folder_dict[folder_prfix] = (timestamp, folder)

    def list_files(self, root_dir, regex):
        for root, dirs, files in os.walk(root_dir):

            folder_match = (re.search(regex, root))
            if folder_match:
                continue

            for dir in dirs:
                folder_match_dirs = (re.search(regex, dir))
                if folder_match_dirs:
                    print root
                    self.extracted_folders.append(root)
                    break
        print self.extracted_folders

    def writer(self, command):
        print command
        self.log.write(command)

    def run_delete_folder(self):
        # Locate root folders where sub folders contains the following format yyyy-mm-dd-HH-MM-SS_numL
        regex = r'(\d{4}[-]?\d{2}[-]?\d{2})-\d{2}-\d{2}-\d{2}_\d{1,2}L'

        # Create a list of dirs to go over
        self.list_files(self.root_folder, regex)

        # Iterate over the list of folders generated and check in each folder for duplicated folders
        # Build two lists self.folder_to_keep, self.folder_to_remove
        for folder in self.extracted_folders:
            self.find_dup_folders(folder, regex)

        print "folders to keep  :" + str(self.folder_to_keep)
        print "folders to remove:" + str(self.folder_to_remove)
        print ""
        print ""

        # remove duplicated folders
        for i in range(len(self.folder_to_remove)):
            self.writer("{0}:".format(str(i+1)))
            self.writer("     remove   :" + self.folder_to_remove[i])
            self.writer("     keep     :" + self.folder_to_keep[i])
            #shutil.rmtree(self.folder_to_remove[i]) # remove "#" to remove folders
        self.writer("Total removed: {0}".format(len(self.folder_to_remove)))

        self.log.close()
        return

if __name__ == '__main__':
    t = Folder_Remover()
    t.run_delete_folder()
