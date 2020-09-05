import shutil, os, glob
def moveAndCreateDir(sourcePath, dstDir):
    # Check if dst path exists
    if os.path.isdir(dstDir) == False:
        # Create all the dierctories in the given path
        os.makedirs(dstDir); 
    # Move the file to path    
    shutil.move(sourcePath, dstDir);

def main():  
    # sourceDir = '/home/varun/Documents/Boost/boost_1_66'
    # destDir =  '/home/varun/Documents/Boost/boost_1_66_backup'
    
    # moveAllFilesinDir(sourceDir, destDir)
    
    
    # sourceFile = 'test/sample1.txt'
    # destDir =  'test/test22/test1'
    
    # moveAndCreateDir(sourceFile, destDir)
    
    origin_path='M:/audiotemp/'
    dest_path='M:/Audiobooks/'
    for candidate in os.listdir(origin_path):
        candidate_path = origin_path + candidate
        # print("==> " ,candidate_path)
        if os.path.isdir(candidate_path) == True:
            print ("Move this folder: ", candidate_path)
            try:
                shutil.move(candidate_path, dest_path)    
            except Exception as e:
                print ("COULD NOT MOVE ", candidate_path)                
                print("Exception message : %s" %e)

if __name__ == '__main__':
    main()